from dataclasses import dataclass, field
from typing import Union, Callable, Any
from copy import deepcopy

from ir.nodes import Body, FuncDecl, Call, Identifier
from codegen.objects import (
    Type, Object, Position, POS_ZERO, kwargs, Param, Arg, EnvItem, Free, FunctionInfo
)


FunctionType = Union['UserFunction', 'BuiltinFunction']
Overloads = dict['OverloadKey', 'OverloadValue']
Callables = list['Modification']

@dataclass(**kwargs)
class OverloadKey:
    return_type: Type
    params: tuple['Param', ...] = field(default_factory=tuple)

@dataclass(**kwargs)
class OverloadValue:
    callable: Callable | str | None = field(default=None)
    free: Free | None = field(default=None)
    callables: Callables = field(default_factory=Callables)

@dataclass(**kwargs)
class Modification:
    callable: Callable | str
    args: tuple['Arg', ...] = field(default_factory=tuple)

@dataclass(**kwargs)
class BuiltinFunction:
    callable: Callable
    return_type: Type | None
    params: list[Param] = field(default_factory=list)
    overloads: Overloads = field(default_factory=Overloads)
    callables: Callables = field(default_factory=Callables)
    generic_params: list[str] = field(default_factory=list)

    def call(
        self, codegen, call_position: Position, key: OverloadValue | None, args: tuple[Arg, ...],
        **kwargs
    ):
        name = self.callable if key is None else key.callable
        if name is None:
            name = self.callable
        
        if not callable(name):
            call_position.error_here(f'{name} is not callable')
        
        return name(codegen, call_position, *[arg.value for arg in args], **kwargs)

    def add_overload(
        self, codegen, name: Callable, returns: Type, param_types: tuple[Param, ...],
        free: Free | None = None
    ) -> None:
        self.overloads[OverloadKey(returns, tuple(param_types))] = OverloadValue(name, free)
        codegen.c_manager.reserve(name)

@dataclass(**kwargs)
class UserFunction:
    name: str
    return_type: Type
    params: list[Param] = field(default_factory=list)
    body: Body | None = field(default=None)
    overloads: Overloads = field(default_factory=Overloads)
    callables: Callables = field(default_factory=Callables)
    generic_params: list[str] = field(default_factory=list)
    
    def call(
        self, codegen, call_position: Position, callee: OverloadValue | None, args: tuple[Arg, ...],
        **_
    ):
        if (out := codegen.function_manager.handle_callables(
            codegen, call_position, args, self
        )) is not None:
            return out
        
        return_type = self.return_type
        if self.name != callee:
            for k, v in self.overloads.items():
                if v == callee:
                    return_type = k.return_type
        
        name: Callable | str | None = self.name if callee is None else callee.callable
        if name is None:
            name = self.name
        
        args_str = ', '.join(str(arg.value) for arg in args)
        return Object(
            f'{name}({args_str})', return_type, call_position,
            free=callee.free if callee is not None else None
        )
    
    def add_modification(
        self, codegen, name: str, pos: Position, func: Callable,
        args: tuple[Arg, ...]
    ) -> None:
        param_types = getattr(func, 'param_types', ())
        if not codegen.function_manager.validate_args(tuple(args), param_types):
            pos.error_here(f'No matching overload for modification \'{name}\'')
        
        self.callables.append(Modification(func, args))
    
    def add_overload(
        self, codegen, name: str, returns: Type, param_types: tuple[Param, ...],
        **kwargs
    ) -> None:
        self.overloads[OverloadKey(returns, tuple(param_types))] = OverloadValue(name, **kwargs)
        codegen.c_manager.reserve(name)
    
    def new_overload(
        self, codegen, returns: Type, param_types: tuple[Param, ...],
        **kwargs
    ) -> str:
        name = codegen.get_unique_name(self.name)
        self.add_overload(codegen, name, returns, param_types, **kwargs)
        return name

class FunctionManager:
    GREEDY = '*'
    
    def __init__(self, codegen) -> None:
        self.codegen = codegen
    
    def is_main_function(self, func_name: str) -> bool:
        return func_name == 'main'
    
    # def make_function_type(
    #     self, return_type: Type, param_types: tuple[Type, ...], pos: Position
    # ) -> Type:
    #     temp_func_name: TempVar = self.codegen.create_temp_var(Type('function'), pos)
    #     return Type(
    #         f'({", ".join(str(param) for param in param_types)}) -> {return_type}',
    #         f'{return_type} (*{temp_func_name})({", ".join(str(param) for param in param_types)})',
    #         ('function',),
    #         (tuple(param_types), return_type, str(temp_func_name))
    #     )
    
    def main_body_code(self, body: Object | str | None) -> str:
        if body is None:
            body = ''
        
        basic_code = f"""{self.codegen.main_init_code}
{body}
"""
        if len(self.codegen.preprocessor.tests) == 0:
            return basic_code
        
        return f"""#ifndef TEST
{self.codegen.main_init_code}
{body}
#else
{'\n'.join(f"{test.name}_test();" for test in self.codegen.preprocessor.tests)};
return 0;
#endif
"""
    
    def get_definition_signature(
        self, name: str, return_type: Type, params: list[Param], body: Object | str | None
    ) -> str:
        is_main_function = self.is_main_function(name)
        params_str = self.params_str(tuple(params))
        
        if body is None:
            return f'{return_type.c_type} {name}({params_str});'
        
        if is_main_function:
            return f"""{return_type.c_type} {name}({params_str}) {{
{self.main_body_code(body)}
}}
"""
        
        return f"""{return_type.c_type} {name}({params_str}) {{
{body}
}}
"""

    @staticmethod
    def verify_params_length(args: tuple['Arg', ...], expected_length: int):
        if len(args) > expected_length:
            return False, f'Too many arguments. Expected {expected_length}, got {len(args)}'
        elif len(args) < expected_length:
            return False, f'Too few arguments. Expected {expected_length}, got {len(args)}'
        
        return True, ''
    
    @staticmethod
    def params_str(params: tuple['Param', ...]):
        if len(params) == 0:
            return 'void'
        
        return ', '.join(str(param) for param in params)
    
    @staticmethod
    def check_duplicate_params(params: tuple['Param', ...], pos: Position):
        used_param_names = []
        for p in params:
            if p.name in used_param_names:
                pos.error_here('Function parameter names duplicated')
            else:
                used_param_names.append(p)
    
    def handle_modifications(
        self, modifications: list[Call]
    ):
        callables = []
        for mod in modifications:
            if isinstance(mod.callee, Identifier):
                callee = mod.callee.name
            else:
                mod.callee.pos.error_here('Invalid function modification')
            
            modification = self.codegen.c_manager.get_object(callee)
            if modification is not None:
                callables.append((mod, modification))
            elif modification is None:
                mod.pos.error_here(f'Unknown function modification \'{callee}\'')
        
        return callables
    
    def handle_function_overload(
        self, name: str, return_type: Type, pos: Position, params: list[Param],
        modifications: list[Call], body: Body, generic_params: list[str]
    ):
        callables = self.handle_modifications(modifications)
        
        original_name = name
        overload_args: list | None = None
        if (fn := self.codegen.scope.env.get(name)) is not None:
            if len(callables) > 0:
                pos.error_here('Function modification overloads are not supported')
            
            name = self.codegen.get_unique_name(name)
            if fn.func is None:
                pos.error_here(f'Name \'{name}\' is used as a variable and not a function')
            
            overload_args = [self.codegen, name, return_type, tuple(params), {'callables': callables}]
            func = None
        else:
            if self.codegen.name_occupied(name):
                name = self.codegen.fix_name(name)
            
            func = UserFunction(name, return_type, params, body, generic_params=generic_params)
            for mod, modification in callables:
                func.add_modification(
                    self.codegen, mod.callee.name, mod.pos, modification,
                    tuple(self.codegen.visit_ArgNode(arg) for arg in mod.args)
                )
            
            # self.codegen.scope.env[original_name] = EnvItem(name, Type('function'), pos, func)
        
        return overload_args, name, original_name, func,\
            lambda key: self.codegen.scope.env.update({
            key: EnvItem(original_name, Type('function'), pos, func)
        })
    
    def define_function(self, node: FuncDecl) -> Object:
        if node.generic_params:
            self.codegen.type_checker.add_type(node.generic_params)
            
            # FIXME: This is a hack to allow generic parameters within array and dictionary contexts
            # e.g. array[T] but this should be changed in the future
            for param in node.generic_params:
                self.codegen.add_toplevel_code(f'typedef void* {param};')
        
        name = node.name
        return_type = self.codegen.visit_TypeNode(node.return_type)\
            if node.return_type is not None else Type('nil')
        
        params = [self.codegen.visit_ParamNode(param) for param in node.params]
        self.check_duplicate_params(tuple(params), node.pos)
        
        kwargs: dict[str, Any] = {'params': params}
        if self.is_main_function(name):
            if self.codegen.scope.env.get(name) is not None:
                node.pos.error_here('Main function already defined')
            
            if len(params) > 0:
                node.pos.warn_here('Overriding main function parameters')
            
            params = [Param('argc', Type('int')), Param('argv', Type('string*'))]
            if self.codegen.optimizer.uses_args:
                kwargs['ending_code'] = f'{self.codegen.main_end_code};'
                code, args_name = self.codegen.c_manager.array_from_c_array(
                    self.codegen, POS_ZERO, Type('string'), 'argv', 'argc'
                )
                
                self.codegen.main_init_code += f"""{code}
args = {args_name};
"""
        
        overload_args, name, original_name, func, add_to_env = self.handle_function_overload(
            name, return_type, node.pos, params, node.modifications, node.body, node.generic_params
        )
        
        if func is not None:
            add_to_env(original_name)
        
        if not node.generic_params:
            if node.extend_type is not None:
                from codegen.c_manager import c_dec
                extend_type = self.codegen.visit_TypeNode(node.extend_type)
                name = f'{extend_type.c_type}_{original_name}'
                self.codegen.scope.env.pop(original_name)
                add_to_env(name)
                original_name = name
                func.name = name
                
                @c_dec(
                    param_types=tuple(params), is_method=True,
                    add_to_class=self.codegen.c_manager, func_name_override=name
                )
                def _(_, call_position: Position, *_args):
                    # this function should not be called because the user function is called instead
                    call_position.error_here('An internal error occurred')
            
            if overload_args is not None:
                overload_kwargs = overload_args.pop()
                self.codegen.scope.env[original_name].func.add_overload(
                    *overload_args, **overload_kwargs
                )
            
            body = self.codegen.visit_Body(node.body, **kwargs)
            self.codegen.scope.env[original_name].free = body.free
            
            # return types of the `Body` are not reliable enough yet
            # if body.type != return_type:
            #     node.pos.error_here(f'Expected return type \'{return_type}\', got \'{body.type}\'')
            
            return Object(
                self.get_definition_signature(name, return_type, params, str(body)),
                Type('nil'), node.pos
            )
        
        if node.extend_type is not None:
            node.pos.error_here('Generics and type extensions are not supported')
        
        # don't generate code yet for generic functions, they are added when the function is called
        return Object('', Type('nil'), node.pos)
    
    def has_greedy(self, params: tuple['Param', ...]) -> bool:
        return any(p.type.c_type == self.GREEDY for p in params)

    def handle_args(self, codegen, args: tuple['Arg', ...], params: tuple['Param', ...], pos: Position):
        variadic_args: list[Arg] = []
        list_params: list = list(params)
        new_args: list[Arg | None] = [None] * len(list_params)
        variadic_param = None
        if list_params and list_params[-1].name == '*' and list_params[-1].type.c_type == '*':
            variadic_param = list_params.pop()
        
        arg: Arg | None
        for i, arg in enumerate(args):
            if i < len(list_params):
                if arg.name is None:
                    new_args[i] = arg
                else:
                    param_index = next(
                        (i for i, p in enumerate(list_params) if p.name == arg.name), None
                    )
                    if param_index is None:
                        return f'Unknown keyword argument \'{arg.name}\'', arg.value.position
                    
                    new_args[param_index] = arg
            else:
                if variadic_param is None:
                    return 'Too many arguments provided', pos
                
                variadic_args = list(args[len(list_params):])
        
        for i, (param, arg) in enumerate(zip(list_params, new_args)):
            if arg is not None:
                continue
            
            if param.default is None:
                return f'Missing required argument \'{param.name}\'', pos
            
            obj = param.default
            if obj.position == POS_ZERO:
                obj.position = pos
            
            new_args[i] = Arg(param.default, param.name)
        
        passing_args: list[Arg] = [
            arg for arg in new_args
            if arg is not None
        ] + (variadic_args if variadic_param is not None else [])
        
        for param, arg in zip(list_params, passing_args):
            if not param.ref:
                continue
            
            if not codegen.is_identifier(arg.value):
                return 'Cannot modify non-variable', pos
            
            arg.value.code = f'&({arg.value})'
        
        return passing_args, None

    def handle_overloads(self, f: FunctionType, codegen, args: tuple['Arg', ...], pos: Position):
        for k, v in f.overloads.items():
            new_args_or_error, _ = self.handle_args(codegen, args, k.params, pos)
            if isinstance(new_args_or_error, str):
                continue
            
            success, _, _ = self.validate_args(tuple(new_args_or_error), k.params)
            if success:
                return v, k.return_type, new_args_or_error
        
        return None, None, args

    def handle_callables(self, codegen, pos: Position, args: tuple['Arg', ...], f: FunctionType):
        for mod in f.callables:
            if isinstance(mod.callable, str):
                continue
            
            params = getattr(mod.callable, 'params')
            err, position = self.handle_args(codegen, mod.args, params, pos)
            if isinstance(position, Position):
                position.error_here(err)
            else:
                mod_args = err
            
            mod_res = mod.callable(codegen, f, pos, args, *[marg.value for marg in mod_args])
            if mod_res is not None and isinstance(mod_res, Object):
                return mod_res

    def get_generic_type(
        self, args: tuple[Type, ...], generic_params: list[str], generic: Type
    ) -> Type | None:
        if generic.c_type not in generic_params and generic not in generic_params:
            return None
        
        for arg, param in zip(args, generic_params):
            if param == generic.c_type:
                return arg
            elif generic.c_type in param:
                for gtype in generic_params:
                    if gtype in param:
                        type = generic.type.replace(gtype, arg.type)
                        c_type = generic.c_type.replace(gtype, arg.c_type)
                        return Type(type, c_type)
        
        return None
    
    def replace_generic_types(self, s: str, args: tuple[Type, ...], params: tuple[str, ...]):
        return s.format(**{
            param: str(arg)
            for param, arg in zip(params, args)
        })
    
    def infer_generic_args(
        self, args: tuple['Arg', ...], params: list[Param], generic_params: list[str]
    ):
        generic_args: dict[str, Type] = {}
        for i, arg in enumerate(args):
            if arg.name is not None:
                arg.value.position.error_here('Cannot infer generic type from named argument')
            
            param = params[i]
            generic_type = param.type.c_type
            if generic_type in generic_params:
                if generic_type not in generic_args:
                    generic_args[generic_type] = arg.value.type
                    continue
                
                if generic_args[generic_type] != arg.value.type:
                    arg.value.position.error_here(
                        f'Type mismatch for generic type \'{generic_type}\', expected '\
                            f'\'{generic_args[generic_type]}\', got \'{arg.value.type}\''
                    )
        
        return tuple(generic_args.values())

    def make_generics(
        self, codegen, args: tuple['Arg', ...], generic_args: tuple['Type', ...], f: FunctionType,
        pos: Position
    ):
        if f.return_type is None:
            pos.error_here(f'Cannot generate code for generic function without return type \'{f}\'')
        
        params = f.generic_params
        if len(generic_args) == 0:
            generic_args = self.infer_generic_args(args, f.params, params)
        
        if len(generic_args) != len(params):
            pos.error_here(f'Expected {len(params)} generic arguments, got {len(generic_args)}')
        
        new_params: list[Param] = []
        for param in deepcopy(f.params):
            p = param
            if any(generic_type in param.type.c_type for generic_type in params):
                generic_type = self.get_generic_type(generic_args, f.generic_params, param.type)
                if generic_type is None:
                    pos.error_here(f'Could not find generic argument for \'{param.type.c_type}\'')
                
                p.type = generic_type
            
            new_params.append(p)
        
        success, err, position = self.validate_args(tuple(args), tuple(new_params))
        if not success:
            (position or pos).error_here(err)
        
        return_type = f.return_type
        return_type.type = self.replace_generic_types(return_type.type, generic_args, tuple(params))
        return_type.c_type = self.replace_generic_types(return_type.c_type, generic_args, tuple(params))
        if return_type.c_type in params:
            t = self.get_generic_type(generic_args, f.generic_params, return_type)
            if t is None:
                pos.error_here(f'Could not find generic argument for \'{f.return_type}\'')
            
            return_type = t
        
        if isinstance(f, UserFunction):
            body: Object = codegen.visit_Body(f.body, params=new_params)
            name = f.new_overload(codegen, return_type, tuple(new_params), free=body.free)
            codegen.add_toplevel_code(
                self.get_definition_signature(name, return_type, new_params, body)
            )
        elif isinstance(f, BuiltinFunction):
            f.add_overload(codegen, f.callable, return_type, tuple(new_params))
        
        return {p: t for p, t in zip(params, generic_args)}

    def validate_args(self, args: tuple['Arg', ...], params: tuple['Param', ...]):
        if not self.has_greedy(params):
            success, err = self.verify_params_length(args, len(params))
            if not success:
                return success, err, None
        
        for arg, param in zip(args, params):
            param_type = param.type
            if param_type.c_type == 'any':
                continue # if the parameter type can be anything, don't bother to check it
            elif param.name == self.GREEDY or param_type.c_type == self.GREEDY:
                return True, '', None # no need to continue if there is a variadic 

            arg_type, arg_pos = arg.value.type, arg.value.position
            if arg_type != param_type:
                return False, f'Expected type \'{param_type}\', got \'{arg_type}\'', arg_pos

        return True, '', None

    def call_func(
        self, codegen, args: tuple['Arg', ...], f: FunctionType, call_position: Position,
        generic_args: tuple['Type', ...] | None = None
    ):
        if generic_args is None:
            generic_args = ()
        
        generic_dict = {}
        if f.generic_params:
            generic_dict = self.make_generics(codegen, args, generic_args, f, call_position)
        
        overload, params, args = self.handle_overloads(f, codegen, args, call_position)
        if overload is None and params is None:
            # if none of the overloads match, check the normal function params
            args, position = self.handle_args(codegen, args, tuple(f.params), call_position)
            
            # if nothing works, then the function call is invalid
            if isinstance(args, str) and isinstance(position, Position):
                position.error_here(args)
            
            # if the normal params worked, the correct arguments are the non-overloaded function params
            params = f.params
            
            # the parameters don't need to be checked since they are guaranteed to be correct
            # but the parameters are still not guaranteed to be correct
            success, err, position = self.validate_args(args, tuple(params))
            if not success:
                (position or call_position).error_here(err)
        
        return f.call(codegen, call_position, overload, args, **generic_dict)
    
    def call_type(
        self, codegen, args: tuple['Arg', ...], func_info: FunctionInfo, func_name: str,
        call_position: Position
    ) -> Object | None:
        params = [Param(f'param{i}', type_) for i, type_ in enumerate(func_info.param_types)]
        args, pos = self.handle_args(codegen, args, tuple(params), call_position)
        if pos is not None:
            pos.error_here(args)
        
        success, err, pos = self.validate_args(args, tuple(params))
        if not success:
            (pos or call_position).error_here(err)
        
        f = UserFunction(func_name, func_info.return_type, params)
        return f.call(codegen, call_position, None, args)
