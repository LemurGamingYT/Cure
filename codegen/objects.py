from dataclasses import dataclass, field
from re import compile as re_compile
from typing import Union, Callable

from ir.nodes import Position, Body


ID_REGEX = re_compile(r'[a-zA-Z_][a-zA-Z_0-9]*')
POS_ZERO = Position(0, 0, '')
FunctionType = Union['Function', 'BuiltinFunction']
OverloadKey = tuple[tuple['Param', ...], 'Type']
Overloads = dict[OverloadKey, Callable | str | None]
Callables = list[tuple[Callable | str, tuple['Arg', ...]]]
kwargs = {'slots': True, 'unsafe_hash': True}

def has_greedy(params: tuple['Param', ...]) -> bool:
    return any(p.type.c_type == GREEDY for p in params)

def handle_args(codegen, args: tuple['Arg', ...], params: tuple['Param', ...], pos: Position):
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
                param_index = next((i for i, p in enumerate(list_params) if p.name == arg.name), None)
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

def handle_overloads(f: FunctionType, codegen, args: tuple['Arg', ...], pos: Position):
    for k, v in f.overloads.items():
        new_args_or_error, _ = handle_args(codegen, args, k[0], pos)
        if isinstance(new_args_or_error, str):
            continue
        
        success, _, _ = validate_args(args, k[0])
        if success:
            return v, k[1], new_args_or_error
    
    return None, None, args

def handle_callables(codegen, pos: Position, args: tuple['Arg', ...], f: FunctionType):
    for modification_callable, modification_args in f.callables:
        if isinstance(modification_callable, str):
            continue
        
        params = getattr(modification_callable, 'params')
        err, position = handle_args(codegen, modification_args, params, pos)
        if isinstance(position, Position):
            position.error_here(err)
        else:
            modification_args = err
        
        mod_res = modification_callable(
            codegen, f, pos, args, *[marg.value for marg in modification_args]
        )
        if mod_res is not None and isinstance(mod_res, Object):
            return mod_res

def verify_params_length(args: tuple['Arg', ...], expected_length: int):
    if len(args) > expected_length:
        return False, f'Too many arguments. Expected {expected_length}, got {len(args)}'
    elif len(args) < expected_length:
        return False, f'Too few arguments. Expected {expected_length}, got {len(args)}'
    
    return True, ''

def call_func(codegen, args: tuple['Arg', ...], f: FunctionType, call_position: Position):
    # check the arguments
    callee, params, args = handle_overloads(f, codegen, args, call_position)
    if callee is None and params is None:
        # if none of the overloads match, check the normal function params
        args, position = handle_args(codegen, args, tuple(f.params), call_position)
        
        # if nothing works, then the function call is invalid
        if isinstance(args, str) and isinstance(position, Position):
            position.error_here(args)
        
        params = f.params # if the normal params worked, the correct arguments are the function params
        
        # the overloads don't need to be checked since they are guaranteed to be correct
        # but the parameters are still not guaranteed to be correct
        success, err, position = validate_args(args, tuple(params))
        if not success:
            (position or call_position).error_here(err)
    
    if isinstance(f, BuiltinFunction):
        if isinstance(callee, str):
            call_position.error_here(callee)
        
        return (callee or f.callable)(codegen, call_position, *[arg.value for arg in args])
    else:
        if (out := handle_callables(codegen, call_position, args, f)) is not None:
            return out
        
        return_type = f.return_type
        if f.name != callee:
            for k, v in f.overloads.items():
                if v == callee:
                    return_type = k[1]
        
        args_str = ', '.join(str(arg.value) for arg in args)
        return Object(f'{(callee or f.name)}({args_str})', return_type, call_position)

GREEDY = '*'

def validate_args(args: tuple['Arg', ...], params: tuple['Param', ...]):
    if not has_greedy(params):
        success, err = verify_params_length(args, len(params))
        if not success:
            return success, err, None
    
    for arg, param in zip(args, params):
        param_type = param.type
        if param_type.c_type == 'any':
            continue # if the parameter type can be anything, don't bother to check it
        elif param.name == GREEDY or param_type.c_type == GREEDY:
            return True, '', None # no need to continue if there is a variadic 

        arg_type, arg_pos = arg.value.type, arg.value.position
        if arg_type != param_type:
            return False, f'Expected type \'{param_type}\', got \'{arg_type}\'', arg_pos

    return True, '', None

@dataclass(**kwargs)
class Type:
    type: str
    c_type: str = field(default='')
    
    def __post_init__(self) -> None:
        if self.c_type == '':
            self.c_type = self.type
    
    def __repr__(self) -> str:
        return self.type
    
    def __str__(self) -> str:
        return self.__repr__()

@dataclass(**kwargs)
class Scope:
    parent: Union['Scope', None] = field(default=None)
    prepended_code: str = field(default='')
    ending_code: str = field(default='')
    appended_code: str = field(default='')
    free_vars: set['Free'] = field(default_factory=set)
    local_free_vars: set['Free'] = field(default_factory=set)
    env: dict[str, 'EnvItem'] = field(default_factory=dict)
    is_in_loop: bool = field(default=False)
    is_in_class: bool = field(default=False)
    assigning_to_variable: str | None = field(default=None)
    
    @property
    def toplevel(self) -> 'Scope':
        top = self
        while top.parent is not None:
            top = top.parent
        
        return top
    
    @property
    def is_toplevel(self) -> bool:
        return self.parent is None
    
    def add_free(self, free: 'Free') -> None:
        self.free_vars.add(free)
        self.local_free_vars.add(free)
    
    def remove_free(self, free: 'Free') -> None:
        for i, f in enumerate(self.local_free_vars):
            if f == free:
                local_free_vars = list(self.local_free_vars)
                local_free_vars.pop(i)
                self.local_free_vars = set(local_free_vars)

        for i, f in enumerate(self.free_vars):
            if f == free:
                free_vars = list(self.free_vars)
                free_vars.pop(i)
                self.free_vars = set(free_vars)
    
    def has_free(self, free: 'Free') -> bool:
        for f in self.local_free_vars:
            if f == free:
                return True
        
        for f in self.free_vars:
            if f == free:
                return True

        return False

@dataclass(**kwargs)
class Free:
    object_name: str = field(default='')
    free_name: str = field(default='free')
    basic_name: str = field(default='')
    
    @property
    def code(self) -> str:
        return f'{self.free_name}({self.object_name});'
    
    def replace(self, with_free: 'Free') -> 'Free':
        return Free(
            with_free.object_name.replace(with_free.basic_name, self.basic_name),
            free_name=with_free.free_name, basic_name=self.basic_name
        )
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Free):
            return self.object_name == other.object_name and self.free_name == other.free_name
        
        return False

@dataclass(**kwargs)
class Object:
    code: str
    type: Type
    position: Position = field(default=POS_ZERO)
    free: Free | None = field(default=None)
    
    @staticmethod
    def NULL(position: Position) -> 'Object':
        return Object('NULL', Type('nil'), position)
    
    @staticmethod
    def STRINGBUF(buf_free: Free, pos: Position) -> 'Object':
        return Object(buf_free.object_name, Type('string'), pos, free=buf_free)
    
    def __str__(self) -> str:
        return self.code

@dataclass(**kwargs)
class EnvItem:
    name: str
    type: Type
    defined_at: Position
    func: Union['Function', None] = field(default=None)
    reserved: bool = field(default=False)
    free: Free | None = field(default=None)
    is_const: bool = field(default=False)

@dataclass(**kwargs)
class TempVar:
    name: str
    type: Type
    created_at: Position
    free: Free | None = field(default=None)
    
    def __str__(self) -> str:
        return self.name
    
    def OBJECT(self) -> Object:
        return Object(self.name, self.type, self.created_at, free=self.free)

@dataclass(**kwargs)
class Arg:
    value: Object
    name: str | None = field(default=None)

@dataclass(**kwargs)
class Param:
    name: str
    type: Type
    ref: bool = field(default=False)
    default: Object | None = field(default=None)
    
    def __str__(self) -> str:
        return f'{self.get_type()} {self.name}'
    
    def get_type(self) -> str:
        return f'{self.type.c_type}{"*" if self.ref else ""}'
    
    def USE(self) -> str:
        return f'*({self.name})' if self.ref else self.name

@dataclass(**kwargs)
class BuiltinFunction:
    callable: Callable
    params: list[Param] = field(default_factory=list)
    overloads: Overloads = field(default_factory=Overloads)
    callables: Callables = field(default_factory=Callables)

@dataclass(**kwargs)
class Function:
    name: str
    return_type: Type
    params: list[Param] = field(default_factory=list)
    body: Body | None = field(default=None)
    overloads: Overloads = field(default_factory=Overloads)
    callables: Callables = field(default_factory=Callables)
    
    def add_modification(self, name: str, pos: Position, func: Callable, args: tuple[Arg, ...]) -> None:
        param_types = getattr(func, 'param_types', ())
        if not validate_args(tuple(args), param_types):
            pos.error_here(f'No matching overload for modification \'{name}\'')
        
        self.callables.append((func, args))
    
    def add_overload(self, name: str, returns: Type, param_types: tuple[Param, ...]) -> None:
        self.overloads[(tuple(param_types), returns)] = name
