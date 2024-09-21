from typing import Any, Iterable
from pathlib import Path

from codegen.objects import (
    Scope, Object, Type, Param, EnvItem, Function, Free, Arg, TempVar, ID_REGEX, POS_ZERO, call_func
)
from codegen.c_manager import CManager, STD_PATH, c_dec
from codegen.class_manager import ClassManager
from codegen.array_manager import ArrayManager
from codegen.dict_manager import DictManager
from ir.base_visitor import IRVisitor
from codegen.target import get_target
from ir import (
    Program, Body, TypeNode, ParamNode, ArgNode, Call, Return, Foreach, While,
    If, Use, VarDecl, Value, Identifier, Array, Dict, Brackets, BinOp, UOp, Attribute, New,
    Ternary, Position, Node, Break, Continue, FuncDecl, Nil, Index, DollarString, IRBuilder,
    Cast, Enum, Class, AttrAssign
)


op_map = {
    '+': 'add', '-': 'sub', '*': 'mul', '/': 'div', '%': 'mod', '==': 'eq', '!=': 'neq',
    '<': 'lt', '>': 'gt', '<=': 'lte', '>=': 'gte', '&&': 'and', '||': 'or', '!': 'not'
}


def str_to_c(cure: str, scope: Scope | None = None,
             filename: Path | None = None) -> tuple['CodeGen', str]:
    builder = IRBuilder()
    program = builder.build(cure)
    program.file = filename
    
    codegen = CodeGen(scope)
    return codegen, codegen.generate(program)

def cure_to_c(cure: Path, output: Path | None = None) -> tuple['CodeGen', str]:
    codegen, code = str_to_c(cure.read_text('utf-8'), filename=cure)
    if output is not None:
        output.write_text(code, 'utf-8')
    
    return codegen, code


class CodeGen(IRVisitor):
    def __init__(self, scope: Scope | None = None) -> None:
        super().__init__()
        
        self.main_end_code, self.main_init_code, self.top_level_code, self.top_code = '', '', '', ''
        self.scope = scope or Scope()
        
        self.valid_types = [
            'int', 'float', 'bool', 'string', 'nil', 'Math', 'System', 'Time', 'Cure', 'Fraction',
            'Vector2', 'hex', 'StringBuilder'
        ]
        
        self.library_classes: list[object] = []
        self.extra_compile_args: list[str] = []
        self.target = get_target()
        
        self.c_manager = CManager(self)
        self.dict_manager = DictManager(self)
        self.array_manager = ArrayManager(self)
        self.class_manager = ClassManager(self)
        
        self.add_toplevel_code('#ifndef _CURE_INITIALISED\n')
        
        str_array = self.array_manager.define_array(Type('string'))
        
        code, name = self.c_manager.array_from_c_array(
            self, POS_ZERO, Type('string'), '__argv', '__argc'
        )
        
        self.scope.env['init'] = EnvItem('init', Type('function'), POS_ZERO)
        self.scope.env['deinit'] = EnvItem('deinit', Type('function'), POS_ZERO)
        self.scope.env['args'] = EnvItem('args', str_array, POS_ZERO)
        self.add_toplevel_code(f'{str_array.c_type} args;')
        self.add_toplevel_code(f"""void init() {{
{code}
args = {name};
srand(time(NULL));
}}

void deinit() {{
    free(args.elements);
}}
""")

        self.add_toplevel_code('#define _CURE_INITIALISED\n#endif')
    
    def is_string_literal(self, value: Object | str) -> bool:
        """Checks whether a value is a string literal, i.e. starts and ends with double quotes.

        Args:
            value (Object | str): The value to check.

        Returns:
            bool: Whether the value is a string literal.
        """
        
        if isinstance(value, Object):
            return self.is_string_literal(str(value)) and value.type == Type('string')
        
        return value.startswith('"') and value.endswith('"')
    
    def is_identifier(self, value: Object | str) -> bool:
        """Checks against a regex pattern if a string is an identifier (a name).

        Args:
            value (Object | str): The value.

        Returns:
            bool: Whether the value is an identifier.
        """
        
        if isinstance(value, Object):
            return self.is_identifier(str(value))

        return ID_REGEX.fullmatch(value) is not None
    
    def generate(self, program: Program) -> str:
        """Generate C code from IR. Also prepends the `CodeGen.top_level_code` to the output.

        Args:
            program (Program): The IR program.

        Returns:
            str: The output C code.
        """
        
        self.FILENAME = program.file
        return self.visit(program)
    
    def add_c_lib(self, include: Path, libs: Path, *extra_args: str) -> None:
        """Compile the C code with a given library.

        Args:
            include (Path): The path to the includes folder with all of the .h files.
            libs (Path): The path to the libraries folder with all of the lib (usually .lib) files.
            *extra_args (str): Extra arguments to pass to the compiler such as other libraries
            e.g. -lgdi32.
        """
        
        self.extra_compile_args.extend((
            f'-I{include.absolute().as_posix()}',
            f'-L{libs.absolute().as_posix()}',
            *extra_args
        ))
    
    def enter_scope(self, params: list[Param] | None = None, **kwargs) -> None:
        """Enter a new scope with a new name environment.

        Args:
            params (list[Param] | None, optional): The parameters of a function. This will add
            them to the resulting scope. Defaults to None.
        """
        
        kwargs.pop('env', None)
        kwargs.pop('ending_code', None)
        
        self.scope = Scope(self.scope, env=self.scope.env.copy(), **kwargs)
        
        if params is not None:
            for param in params:
                self.scope.env[param.name] = EnvItem(param.USE(), param.type, Position(0, 0, ''))
    
    def exit_scope(self) -> None:
        """Exit out of a scope and restore the previous scope."""
        
        if self.scope.parent is None:
            return
        
        self.scope = self.scope.parent
    
    def name_occupied(self, name: str) -> bool:
        """Check if a name is already occupied by the `CManager`, `env` or `RESERVED_NAMES`.

        Args:
            name (str): The name to check.

        Returns:
            bool: True if the name is occupied and False if the name isn't occupied.
        """
        
        
        return name in self.scope.env or self.c_manager.get_object(name) is not None or\
            name in self.c_manager.RESERVED_NAMES
    
    def fix_name(self, name: str) -> str:
        """Make a name unique by appending numbers to it.

        Args:
            name (str): The name to fix.

        Returns:
            str: The fixed name that is not occupied.
        """
        
        return self.get_unique_name(name)
    
    def get_unique_name(self, base_name: str = '__temp') -> str:
        """Get a unique name that is not occupied, checked using `name_occupied()`.

        Args:
            base_name (str, optional): The base name to append numbers to. Defaults to '__temp'.

        Returns:
            str: The output name.
        """
        
        i = 0
        name = base_name + str(i)
        while self.name_occupied(name):
            i += 1
            name = base_name + str(i)
        
        return name
    
    def create_temp_var(
        self,
        type_: Type, pos: Position,
        name: str | None = None,
        free: Free | None = None
    ) -> TempVar:
        """Create a temporary variable. Handles adding freeing, creating a unique name (if one
        if not given) and adding the variable to the scope.

        Args:
            type_ (Type): The type of the variable.
            pos (Position): The position.
            name (str | None, optional): The name of the variable. Defaults to None where it will
            generate a unique name.
            free (Free | None, optional): The `Free` structure of the variable. Defaults to None.

        Returns:
            TempVar: The temporary variable.
        """
        
        given_name = name is not None
        if name is None:
            name = self.get_unique_name()
        
        if free is not None and free.object_name == '':
            free.object_name = name
            free.basic_name = name
        
        self.scope.env[name] = EnvItem(name, type_, pos, reserved=given_name, free=free)
        if free is not None:
            self.scope.add_free(free)
        
        return TempVar(name, type_, pos, free=free)
    
    def add_toplevel_code(self, code: str, very_top: bool = False) -> None:
        if very_top:
            self.top_code += code + '\n'
        else:
            self.top_level_code += code + '\n'
    
    def add_toplevel_constant(self, name: str, type: Type, value: str | None = None,
                              add_code: bool = True) -> None:
        pos = Position(0, 0, '')
        original_name = name
        if self.name_occupied(name):
            name = self.fix_name(name)
        
        if add_code:
            if value is None:
                pos.warn_here(f'Constant \'{original_name}\' has no value, skipping adding it.')
                return
            
            self.add_toplevel_code(f'const {type.c_type} {name} = {value};')
        
        self.scope.env[original_name] = EnvItem(name, type, pos)
    
    def prepend_code(self, code: str) -> None:
        self.scope.prepended_code += code
    
    def append_code(self, code: str) -> None:
        self.scope.appended_code += code
    
    def add_end_code(self, code: str) -> None:
        self.scope.ending_code += code
    
    def get_end_code(self) -> str:
        free_vars = self.scope.parent.free_vars if self.scope.parent is not None else set()
        return '\n'.join(
            v.code
            for v in self.scope.free_vars
            if v not in free_vars
        ) + '\n' + self.scope.ending_code
    
    def handle_free(self, free: Free | None, obj: Object, pos: Position) -> Object:
        """Handles freeing a variable.

        Args:
            free (Free): The free structure.
            out (Object): The object to free.
            pos (Position): The position.

        Returns:
            Object: The output code.
        """
        
        if free is None:
            return Object(str(obj), obj.type, pos)
        # elif item.free.object_name != '':
        #     call_position.warn_here(
        #         f'Overriding free variable \'{item.free.object_name}\', may cause memory issues'
        #     )
        
        temp_var = self.create_temp_var(obj.type, pos)
        temp_free = Free(object_name=str(temp_var), basic_name=str(temp_var)).replace(free)
        self.scope.add_free(temp_free)
        self.prepend_code(f'{obj.type.c_type} {temp_var} = {obj};')
        
        obj = temp_var.OBJECT()
        obj.free = temp_free
        return obj
    
    def call(self, name: str, args: list[Arg], call_position: Position,
             by_user: bool = False) -> Object:
        """Call a function. Supports C std Python functions and user defined functions. Handles
        `Free` variables and checking the parameter types.

        Args:
            name (str): The name of the callee.
            args (list[Object]): Arguments to pass to the callee.
            call_position (Position): The position.
            by_user (bool, optional): Whether or not the function was called by the user. Defaults
            to False.

        Returns:
            Object: The output of the function as an `Object`.
        """
        
        if (item := self.scope.env.get(name)) is not None and (func := item.func) is not None:
            obj = call_func(self, tuple(args), func, call_position)
            if obj is None:
                call_position.error_here(f'Function \'{name}\' returned absolutely nothing')
            
            return self.handle_free(item.free, obj, call_position)
        elif (c_func := self.c_manager.get_object(name)) is not None:
            if not getattr(c_func, 'can_user_call', False) and by_user:
                call_position.error_here(f'Name \'{name}\' is not defined')
            
            return call_func(self, tuple(args), c_func.object, call_position)
        
        if item is None:
            call_position.error_here(f'Name \'{name}\' is not defined')
        
        call_position.error_here(f'Name \'{name}\' is not a function')
    
    def call_callee(self, callee: str, args: list[Arg], err_msg: str, pos: Position) -> Object:
        """Utility function to call a function and if it doesn't exist, print an error.

        Args:
            callee (str): The callee name.
            args (list[Arg]): The call arguments.
            err_msg (str): The error message if the object does not exist.
            pos (Position): The call position.

        Returns:
            Object: The output of the function as an `Object`.
        """
        
        if self.c_manager.get_object(callee) is None:
            pos.error_here(err_msg)
        
        return self.call(callee, args, pos)
    
    def condition(self, expr: Node) -> Object:
        """Converts an expression into an `Object`, used in `if` statements.

        Args:
            expr (Node): The expression to convert.

        Returns:
            Object: The resulting `Object`, which is a boolean.
        """
        
        cond = self.visit(expr)
        return self.call(f'{cond.type}_to_bool', [Arg(cond)], cond.position)
    
    def use(self, lib_name: str, pos: Position) -> None:
        """Use a Cure library.

        Args:
            lib_name (str): The name of the library.
            pos (Position): The position.
        """
        
        for lib in STD_PATH.iterdir():
            if lib.stem == lib_name:
                rel_path = lib.relative_to(STD_PATH)
                lib_path = rel_path.as_posix().replace('/', '.')
                if lib_path.endswith('.py'):
                    lib_path = lib_path.removesuffix('.py')
                
                exec(f"""from .std.{lib_path} import {lib_name}
if {lib_name} not in [type(cls) for cls in libraries]:
    lib = {lib_name}(self)
    if not getattr(lib, 'CAN_USE', True):
        pos.error_here(f'Library \\'{lib_name}\\' cannot be used')
    
    libraries.append(lib)
    objects = CManager.get_all_objects(lib)
    for k, v in objects.items():
        setattr(c_manager, k, v)
""", globals(), {
    'c_manager': self.c_manager, 'self': self, 'libraries': self.library_classes,
    'pos': pos
})
                break
        else:
            full_lib_name = lib_name
            lib = Path(lib_name)
            if not lib.is_absolute() or not lib.exists():
                if self.FILENAME is None:
                    pos.error_here('Cannot perform relative imports without a proper filename')
                
                lib = self.FILENAME.parent.joinpath(lib)
            
            if lib == self.FILENAME:
                pos.error_here('Cannot use current file')
            
            if lib.exists() and lib.is_file():
                header = lib.with_suffix('.h')
                sub_codegen, code = cure_to_c(lib)
                self.scope.env |= sub_codegen.scope.env
                
                header.write_text(f"""#pragma once
#ifdef __cplusplus
extern "C" {{
#endif
{code}
#ifdef __cplusplus
}}
#endif
""")
                self.c_manager.include(f'"{header.absolute().as_posix()}"', self)
            else:
                pos.error_here(f'Library \'{full_lib_name}\' not found')
    
    def c_enum(self, name: str, fields: Iterable[str], pos: Position) -> Type:
        """Create a C enum

        Args:
            name (str): The name of the enum
            fields (Iterable[str]): The names that the enum should have
            pos (Position): The position when the enum is/should be created
        
        Returns:
            Type: The `Type` object of the enum
        """

        enum_type = Type(name)
        self.valid_types.append(name)
        self.add_toplevel_code(f'typedef int {name};')
        self.scope.env[name] = EnvItem(name, enum_type, pos)
        
        @c_dec(
            add_to_class=self.c_manager, func_name_override=f'{enum_type.c_type}_type',
            is_method=True, is_static=True
        )
        def _(_, call_position: Position) -> Object:
            return Object(f'"{name}"', Type('string'), call_position)
        
        @c_dec(
            param_types=(Param('enum', enum_type),), is_method=True,
            add_to_class=self.c_manager, func_name_override=f'{enum_type.c_type}_to_string'
        )
        def _(_, call_position: Position, _enum: Object) -> Object:
            return Object(f'"Enum \'{name}\'"', Type('string'), call_position)
        
        for value, member in enumerate(fields):
            callee = f'{enum_type.c_type}_{member}'
            if self.c_manager.get_object(callee) is not None:
                pos.error_here(f'Enum member \'{member}\' is already defined')
            
            @c_dec(
                add_to_class=self.c_manager, func_name_override=callee,
                is_property=True, is_static=True
            )
            def _(_, call_position: Position, value=value) -> Object:
                return Object(f'(({name})({value}))', enum_type, call_position)
            
        @c_dec(
            param_types=(Param('enum', enum_type),), is_method=True,
            add_to_class=self.c_manager, func_name_override=f'{enum_type.c_type}_to_int'
        )
        def _(_, call_position: Position, enum: Object) -> Object:
            return Object(f'((int)({enum}))', Type('int'), call_position)
        
        @c_dec(
            param_types=(Param('a', enum_type), Param('b', enum_type)), is_method=True,
            add_to_class=self.c_manager, func_name_override=f'{enum_type.c_type}_eq_{enum_type.c_type}'
        )
        def _(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) == ({b}))', Type('bool'), call_position)
        
        @c_dec(
            param_types=(Param('a', enum_type), Param('b', enum_type)),  is_method=True,
            add_to_class=self.c_manager, func_name_override=f'{enum_type.c_type}_neq_{enum_type.c_type}'
        )
        def _(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) != ({b}))', Type('bool'), call_position)
        
        return enum_type
    
    
    def visit_Program(self, node: Program) -> str:
        code = '\n'.join(line + ';' for line in [self.visit(stmt).code for stmt in node.nodes])
        return self.top_level_code + '\n' + code
    
    def visit_TypeNode(self, node: TypeNode) -> Type:
        # for class_ in self.library_classes:
        #     if (get_type := getattr(class_, 'get_type', None)) is not None:
        #         if (res := get_type(node)) is not None:
        #             return res
        
        if node.name not in self.valid_types and node.name not in {'array', 'dict'}:
            node.pos.error_here(f'Invalid type \'{node.name}\'')
        
        if node.array_type is not None:
            return self.array_manager.define_array(self.visit_TypeNode(node.array_type))
        elif node.dict_types is not None:
            return self.dict_manager.define_dict(
                self.visit_TypeNode(node.dict_types[0]),
                self.visit_TypeNode(node.dict_types[1])
            )
        else:
            return Type(node.name)
    
    def visit_Use(self, node: Use) -> Object:
        self.use(node.path, node.pos)
        return Object(f'// using {node.path}', Type('nil'), node.pos)
    
    def visit_If(self, node: If) -> Object:
        return Object(
            f"""if ({self.condition(node.expr)}) {{
{self.visit_Body(node.body)}
}}{''.join(f''' else if ({self.condition(expr)}) {{
{self.visit_Body(body)}
}}''' for expr, body in node.elseifs)}{f''' else {{
{self.visit_Body(node.else_body)}
}}''' if node.else_body is not None else ''}
""",
            Type('nil'), node.pos
        )
    
    def visit_While(self, node: While) -> Object:
        return Object(
            f"""while ({self.condition(node.expr)}) {{
{self.visit_Body(node.body)}
}}
""",
            Type('nil'), node.pos
        )
    
    def visit_Foreach(self, node: Foreach) -> Object:
        if self.name_occupied(node.loop_name):
            node.pos.error_here(f'Name \'{node.loop_name}\' is already in use')
        
        iterable: Object = self.visit(node.expr)
        
        iter_method_callee = f'iter_{iterable.type.c_type}'
        iter_method = self.c_manager.get_object(iter_method_callee)
        if iter_method is None:
            iterable.position.error_here(f'Cannot iterate over type \'{iterable.type}\'')
        
        len_callee_str = f'{iterable.type.c_type}_length'
        len_callee = self.c_manager.get_object(len_callee_str)
        if len_callee is None:
            iterable.position.error_here(f'Cannot iterate over type \'{iterable.type}\'')
        
        len_expr = self.call(len_callee_str, [Arg(iterable)], node.pos)
        
        i = self.create_temp_var(Type('int'), node.pos)
        idx_obj = Arg(i.OBJECT())
        
        self.enter_scope(is_in_loop=True)
        
        iter_var = self.create_temp_var(iter_method.return_type, node.pos, node.loop_name)
        iter_call = self.call(iter_method_callee, [Arg(iterable), idx_obj], node.pos)
        
        out = Object(f"""for (int {i} = 0; {i} < {len_expr}; {i}++) {{
{self.scope.prepended_code}
{iter_method.return_type.c_type} {iter_var} = {iter_call};
{self.visit_Body(node.body)}
{self.scope.appended_code}
}}
""", Type('nil'), node.pos)
        
        self.exit_scope()
        return out
    
    def visit_Return(self, node: Return) -> Object:
        expr = self.visit(node.expr)
        if expr.free is not None:
            self.scope.remove_free(expr.free)
        
        self.prepend_code(self.get_end_code())
        return Object(f'return {expr}', expr.type, node.pos, free=expr.free)
    
    def visit_Break(self, node: Break) -> Object:
        self.prepend_code(self.get_end_code())
        return Object('break', Type('nil'), node.pos)
    
    def visit_Continue(self, node: Continue) -> Object:
        self.prepend_code(self.get_end_code())
        return Object('continue', Type('nil'), node.pos)
    
    def visit_Body(self, node: Body, **kwargs) -> Object:
        self.enter_scope(**kwargs)
        
        if (ending_code := kwargs.pop('ending_code', None)) is not None:
            self.add_end_code(ending_code)
        
        code, free, code_type = [], None, Type('nil')
        for stmt in node.nodes:
            stmt_node = self.visit(stmt)
            if isinstance(stmt, (Return, If, While, Foreach)):
                code_type = stmt_node.type
                free = stmt_node.free
            
            if self.scope.prepended_code != '':
                code.append(self.scope.prepended_code + '\n')
                self.scope.prepended_code = ''
            
            code.append(stmt_node.code + ';')
            
            if self.scope.appended_code != '':
                code.append(self.scope.appended_code + '\n')
                self.scope.appended_code = ''
        
        if code_type == Type('nil'):
            code.extend(v.code for v in self.scope.local_free_vars)
        
        self.exit_scope()
        return Object('\n'.join(code), code_type, node.pos, free=free)
    
    def visit_FuncDecl(self, node: FuncDecl) -> Object:
        name = node.name
        return_type = self.visit_TypeNode(node.return_type)\
            if node.return_type is not None else Type('nil')
        params = [self.visit_ParamNode(param) for param in node.params]
        used_param_names = []
        for p in params:
            if p.name in used_param_names:
                node.pos.error_here('Function parameter names duplicated')
            else:
                used_param_names.append(p)
        
        kwargs: dict[str, Any] = {'params': params}
        is_main_function = name == 'main'
        if is_main_function:
            kwargs['ending_code'] = f'{self.main_end_code};\ndeinit();\n'
        
        new_name = None
        original_name = name
        if name in self.scope.env:
            if len(node.modifications) > 0:
                node.pos.error_here('Overload function modifications are not supported yet')
            
            new_name = self.get_unique_name(name)
            if (f := self.scope.env[name].func) is not None:
                f.add_overload(new_name, return_type, tuple(params))
            else:
                node.pos.error_here(f'Name \'{name}\' is used as a variable and not a function')
        else:
            if self.name_occupied(name):
                name = self.fix_name(name)
            
            func = Function(name, return_type, params, node.body)
            for mod in node.modifications:
                modification = self.c_manager.get_object(mod.name)
                if modification is not None:
                    func.add_modification(
                        mod.name, mod.pos, modification,
                        tuple(self.visit_ArgNode(arg) for arg in mod.args)
                    )
                elif modification is None:
                    mod.pos.error_here(f'Unknown function modification \'{mod.name}\'')
            
            self.scope.env[original_name] = EnvItem(name, Type('function'), node.pos, func)
        
        body = self.visit_Body(node.body, **kwargs)
        self.scope.env[original_name].free = body.free
        
        # return types of the `Body` are not reliable enough yet
        # if body.type != return_type:
        #     node.pos.error_here(f'Expected return type \'{return_type}\', got \'{body.type}\'')
        
        params_str = ', '.join(str(param) for param in params)
        if new_name is not None:
            name = new_name
        
        return Object(f"""{return_type.c_type} {name}({params_str}) {{
{'init();' if is_main_function else ''}
{self.main_init_code if is_main_function else ''}
{body}
}}
""", Type('nil'), node.pos)
    
    def visit_VarDecl(self, node: VarDecl) -> Object:
        if self.scope.parent is None:
            node.pos.error_here('Top level variables are not allowed')
        
        name = node.name
        value: Object = self.visit(node.value)
        type_ = self.visit_TypeNode(node.type) if node.type is not None else value.type
        if value.type != type_:
            node.pos.error_here(f'Expected type \'{type_}\', got \'{value.type}\'')
        
        original_name = name
        if self.name_occupied(name) and name not in self.scope.env:
            name = self.fix_name(name)
        
        if value.free is not None and not self.scope.has_free(value.free):
            self.scope.add_free(value.free)
        
        if (item := self.scope.env.get(name)) is not None:
            if node.type is not None:
                node.pos.error_here(f'Cannot redeclare \'{name}\' as a variable')
            elif node.is_const:
                node.pos.error_here(f'Cannot redeclare \'{name}\' as a constant')
            elif item.is_const:
                node.pos.error_here(f'Cannot redeclare \'{name}\' a constant')
            
            if node.op is not None:
                callee = f'{item.type.c_type}_{op_map[node.op]}_{value.type.c_type}'
                val = Object(item.name, item.type, node.pos)
                if self.c_manager.get_object(callee) is None:
                    node.pos.error_here(f'Operator \'{node.op}\' is not defined for types '\
                        f'\'{val.type}\' and \'{value.type}\'')
                
                value = self.call(callee, [Arg(val), Arg(value)], node.pos)
            
            if value.free is not None:
                self.scope.env[original_name].free = value.free.replace(Free(name, basic_name=name))\
                    if item.free is None else value.free.replace(item.free)
                self.scope.remove_free(value.free)
            
            return Object(f'{item.name} = {value}', item.type, node.pos)
        else:
            if node.op is not None:
                node.pos.error_here(f'\'{name}\' is not defined')
            
            free = Free(name, basic_name=name) if value.free is not None else None
            if free is not None and value.free is not None:
                self.scope.remove_free(value.free)
                free = free.replace(value.free)
                self.scope.add_free(free)
            
            self.scope.env[original_name] = EnvItem(
                name, type_, node.pos, is_const=node.is_const, free=free
            )
            
            const = 'const ' if node.is_const else ''
            return Object(f'{const}{type_.c_type} {name} = {str(value)}', type_, node.pos)
    
    def visit_ParamNode(self, node: ParamNode) -> Param:
        return Param(
            node.name, self.visit_TypeNode(node.type), node.ref,
            self.visit(node.default) if node.default is not None else None
        )
    
    def visit_ArgNode(self, node: ArgNode) -> Arg:
        return Arg(self.visit(node.expr), node.keyword)
    
    def visit_Value(self, node: Value) -> Object:
        if node.type == 'string':
            # slice to remove apostrophes and replace with double quotes
            node.value = f'"{node.value[1:-1]}"'
        
        return Object(node.value, Type(node.type), node.pos)
    
    def visit_DollarString(self, node: DollarString) -> Object:
        fmt = ''
        fmt_variables = []
        for part in node.nodes:
            if isinstance(part, Value):
                fmt += part.value
            else:
                b = self.visit(part)
                b_var = self.create_temp_var(b.type, node.pos)
                self.prepend_code(f'string {b_var} = {self.call(
    f"{b.type.c_type}_to_string", [Arg(b)], node.pos
)};')
                fmt_variables.append(str(b_var))
                fmt += '%s'
        
        code, buf_free = self.c_manager.fmt_length(self, node.pos, f'"{fmt}"', *fmt_variables)
        self.prepend_code(code)
        return Object.STRINGBUF(buf_free, node.pos)
    
    def visit_Identifier(self, node: Identifier) -> Object:
        if (item := self.scope.env.get(node.name)) is not None:
            if item.func is not None:
                return Object(item.name, Type('function'), node.pos)

            return Object(item.name, item.type, node.pos, free=item.free)
        elif node.name in self.valid_types:
            return Object(node.name, Type('type'), node.pos)
        else:
            node.pos.error_here(f'Name \'{node.name}\' is not defined')
    
    def visit_Nil(self, node: Nil) -> Object:
        return Object.NULL(node.pos)
    
    def visit_Brackets(self, node: Brackets) -> Object:
        expr = self.visit(node.expr)
        return Object(f'({expr})', expr.type, node.pos)
    
    def visit_Array(self, node: Array) -> Object:
        elements = [self.visit_ArgNode(arg) for arg in node.elements]
        
        arr_type = self.array_manager.define_array(self.visit_TypeNode(node.type))
        make_call = self.call(f'{arr_type.c_type}_make', [], node.pos)
        for elem in elements:
            self.call(f'{arr_type.c_type}_add', [Arg(make_call), elem], elem.value.position)
        
        return make_call
    
    def visit_Dict(self, node: Dict) -> Object:
        key_type = self.visit_TypeNode(node.key_type)
        value_type = self.visit_TypeNode(node.value_type)
        
        dict_type = self.dict_manager.define_dict(key_type, value_type)
        make_call = self.call(f'{dict_type.c_type}_make', [], node.pos)
        for key, value in node.elements.items():
            self.call(
                f'{dict_type.c_type}_set',
                [Arg(make_call), Arg(self.visit(key)), Arg(self.visit(value))],
                value.pos
            )
        
        return make_call
    
    def visit_Call(self, node: Call) -> Object:
        args = [self.visit_ArgNode(arg) for arg in node.args]
        return self.call(node.name, args, node.pos, True)
    
    def visit_Ternary(self, node: Ternary) -> Object:
        true, false = self.visit(node.if_true), self.visit(node.if_false)
        if true.type != false.type:
            node.pos.error_here('Ternary true and false types don\'t match')
        
        return Object(
            f'{self.condition(node.cond)} ? ({true}) : ({false})',
            true.type, node.pos
        )
    
    def visit_BinOp(self, node: BinOp) -> Object:
        op_name = op_map[node.op]
        left: Object = self.visit(node.left)
        right: Object = self.visit(node.right)
        return self.call_callee(
            f'{left.type.c_type}_{op_name}_{right.type.c_type}',
            [Arg(left), Arg(right)],
            f'Operator \'{node.op}\' is not defined for types \'{left.type}\' and \'{right.type}\'',
            node.pos
        )
    
    def visit_UOp(self, node: UOp) -> Object:
        op_name = op_map[node.op]
        value: Object = self.visit(node.value)
        return self.call_callee(
            f'{op_name}_{value.type.c_type}', [Arg(value)],
            f'Operator \'{node.op}\' is not defined for type \'{value.type}\'',
            node.pos
        )
    
    def visit_Attribute(self, node: Attribute) -> Object:
        obj: Object = self.visit(node.obj)
        callee = f'{obj.type.c_type}_{node.attr}'
        if (func := self.c_manager.get_object(callee)) is not None:
            args: list[Arg] = []
            if not getattr(func, 'is_static', False):
                args.append(Arg(obj))
            
            if getattr(func, 'is_method', False):
                if node.args is None:
                    node.pos.error_here(
                        f'Attribute \'{node.attr}\' is a method, but is used like a property'
                    )
                
                args.extend(self.visit_ArgNode(arg) for arg in node.args)
            elif getattr(func, 'is_property', False):
                if node.args is not None:
                    node.pos.error_here(
                        f'Attribute \'{node.attr}\' is a property, but is used like a method'
                    )
            else:
                node.pos.error_here(f'Invalid attribute \'{node.attr}\' on type \'{obj.type}\'')
            
            return self.call(callee, args, node.pos)
        else:
            node.pos.error_here(f'Attribute \'{node.attr}\' is not defined for type \'{obj.type}\'')
    
    def visit_New(self, node: New) -> Object:
        name = str(self.visit_Identifier(node.name))
        callee = f'{name}_new'
        if (func := self.c_manager.get_object(callee)) is not None:
            if not getattr(func, 'is_static', False):
                node.pos.error_here(f'Class instantiation method for \'{name}\' is not static')
            
            return self.call(callee, [self.visit_ArgNode(arg) for arg in node.args], node.pos)
        
        if name in self.valid_types:
            node.pos.error_here(f'Class instantiation method for \'{name}\' is not defined')
        
        node.name.pos.error_here(f'Class \'{name}\' is not defined')
    
    def visit_Index(self, node: Index) -> Object:
        obj: Object = self.visit(node.obj)
        index: Object = self.visit(node.index)
        callee = f'index_{obj.type.c_type}'
        if self.c_manager.get_object(callee) is None:
            node.pos.error_here(f'Cannot index type \'{obj.type}\'')
        
        return self.call(callee, [Arg(obj), Arg(index)], node.pos)
    
    def visit_Cast(self, node: Cast) -> Object:
        obj: Object = self.visit(node.obj)
        type = self.visit_TypeNode(node.type)
        return self.call_callee(
            f'{obj.type.c_type}_to_{type.c_type}', [Arg(obj)],
            f'Cannot cast type \'{obj.type}\' to \'{type}\'', node.pos
        )
    
    def visit_Enum(self, node: Enum) -> Object:
        name = node.name.name
        if self.name_occupied(name):
            node.name.pos.error_here(f'Name \'{name}\' is already used')
        
        self.c_enum(name, [field.name for field in node.members], node.pos)
        return Object(f'// Enum \'{name}\'', Type('nil'), node.pos)
    
    def visit_AttrAssign(self, node: AttrAssign) -> Object:
        obj: Object = self.visit(node.obj)
        value = self.visit(node.value)
        for attr in node.attr_chain:
            attr_callee = self.c_manager.get_object(f'{obj.type.c_type}_{attr}')
            if attr_callee is None:
                node.pos.error_here(f'Attribute \'{attr}\' is not defined on type \'{obj.type}\'')
            
            attr_type = attr_callee.return_type
            
            if node.op is not None:
                o = node.op
                value = self.call_callee(
                    f'{attr_type.c_type}_{op_map[o]}_{value.type.c_type}',
                    [Arg(self.call_callee(
                        f'{obj.type.c_type}_{attr}', [Arg(obj)],
                        f'Cannot get attribute \'{attr}\' on type \'{obj.type}\'', node.pos
                    )), Arg(value)],
                    f'Cannot perform operation \'{o}\' on types \'{obj.type}\' and \'{value.type}\'',
                    node.pos
                )
            
            obj = self.call_callee(
                f'{obj.type.c_type}_set_{attr}', [Arg(obj), Arg(value)],
                f'Cannot set attribute \'{attr}\' on type \'{obj.type}\'',
                node.pos
            )
        
        return obj
    
    def visit_Class(self, node: Class) -> Object:
        name = node.name
        if self.name_occupied(name):
            node.pos.error_here(f'Name \'{name}\' is already in use')
        
        self.scope.is_in_class = True
        code = self.class_manager.create_class(name, node.members)
        self.scope.is_in_class = False
        return Object(code, Type('nil'), node.pos)
