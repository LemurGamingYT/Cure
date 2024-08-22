from pathlib import Path
from os import getcwd
import inspect
from dataclasses import fields

from antlr4.error.ErrorListener import ErrorListener
from antlr4 import InputStream, CommonTokenStream

from cure.objects import (
    Scope, Position, Object, Param, EnvItem, Function, Free, validate_args, Type
)
from cure.parser.CureVisitor import CureVisitor
from cure.parser.CureParser import CureParser
from cure.parser.CureLexer import CureLexer
from cure.array_manager import ArrayManager
from cure.dict_manager import DictManager
from cure.c_manager import CManager


LIBS_PATH = Path(__file__).parent / 'std'
op_map = {
    '+': 'add', '-': 'sub', '*': 'mul', '/': 'div', '%': 'mod', '==': 'eq', '!=': 'neq',
    '<': 'lt', '>': 'gt', '<=': 'lte', '>=': 'gte', '&&': 'and', '||': 'or', '!': 'not'
}

def to_pos(ctx) -> Position | None:
    if hasattr(ctx, 'start'):
        src = str(ctx.start.getTokenSource().inputStream)
        return Position(ctx.start.line, ctx.start.column, src)
    elif hasattr(ctx, 'getSymbol'):
        src = str(ctx.getSymbol().getTokenSource().inputStream)
        return Position(ctx.getSymbol().line, ctx.getSymbol().column, src)

class CureErrorListener(ErrorListener):
    def syntaxError(self, _, offending_symbol, line, column, _msg, _e):
        Position(line, column, str(offending_symbol.getInputStream())).error_here(
            f'Invalid syntax \'{offending_symbol.text}\' at line {line}, column {column}'
        )

class CureCompiler(CureVisitor):
    VERSION = '0.0.1'
    
    def __init__(self) -> None:
        self.top_level_code = ''
        self.scope = Scope()
        
        self.valid_types = [
            'int', 'float', 'bool', 'string', 'nil', 'Math', 'System', 'Time', 'hex', 'bin'
        ]
        self.library_classes = []
        self.extra_compile_args = []
        
        self.c_manager = CManager(self)
        self.dict_manager = DictManager(self)
        self.array_manager = ArrayManager(self)
        
        str_array = self.array_manager.define_array(Type('string'))
        
        POS_ZERO = Position(0, 0, '')
        code, name = self.c_manager.array_from_c_array(
            self, POS_ZERO,
            Type('string'), '__argv'
        )
        
        self.scope.env['init'] = EnvItem('init', Type('function'), POS_ZERO)
        self.scope.env['args'] = EnvItem('args', str_array, POS_ZERO)
        self.add_toplevel_code(f"""{str_array.c_type} args;
void init() {{
{code}
args = {name};
}}
""")
        
    
    def compile(self, src: str) -> str:
        """Compile .cure file.

        Args:
            src (str): The source code of the .cure file.

        Returns:
            str: The output C code.
        """
        
        lexer = CureLexer(InputStream(src))
        parser = CureParser(CommonTokenStream(lexer))
        parser.removeErrorListeners()
        parser.addErrorListener(CureErrorListener())
        return self.visit(parser.parse())
    
    def enter_scope(self, params: list[Param] | None = None, **kwargs) -> None:
        """Enter into a new scope with a new name environment.
        
        Args:
            params (list[Param] | None, optional): The parameters of a function. This will add
            them to the resulting scope. Defaults to None.
        """
        
        kwargs.pop('env', None)
        kwargs.pop('parent', None)
        
        self.scope = Scope(self.scope, env=self.scope.env.copy(), **kwargs)
        
        if params is not None:
            for param in params:
                self.scope.env[param.name] = EnvItem(
                    f'*({param.name})' if param.ref else param.name,
                    param.type, Position(0, 0, '')
                )
    
    def exit_scope(self) -> None:
        """Exit out of a scope and restore the previous scope."""
        
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
    ) -> str:
        """Create a temporary variable. Handles adding freeing, creating a unique name (if one
        if not given) and adding the variable to the scope.

        Args:
            type_ (Type): The type of the variable.
            pos (Position): The position.
            name (str | None, optional): The name of the variable. Defaults to None where it will
            generate a unique name.
            free (Free | None, optional): The `Free` structure of the variable. Defaults to None.

        Returns:
            str: The output name.
        """
        
        if name is None:
            name = self.get_unique_name()
        
        if free is not None and free.object_name == '':
            free.object_name = name
        
        self.scope.env[name] = EnvItem(name, type_, pos, reserved=True, free=free)
        if free is not None:
            self.scope.add_free(free)
        
        return name
    
    def add_toplevel_code(self, code: str) -> None:
        self.top_level_code += code + '\n'
    
    def add_toplevel_constant(self, name: str, type: Type, value: str | None = None,
                              add_code: bool = True) -> None:
        if add_code:
            if value is None:
                Position(0, 0, '').warn_here(f'Constant \'{name}\' has no value, skipping adding it.')
            
            self.add_toplevel_code(f'const {type.c_type} {name} = {value};')
        
        self.scope.env[name] = EnvItem(name, type, Position(0, 0, ''))
    
    def prepend_code(self, code: str) -> None:
        self.scope.prepended_code += code
    
    def append_code(self, code: str) -> None:
        self.scope.appended_code += code
    
    def add_end_code(self, code: str) -> None:
        self.scope.ending_code += code
    
    def get_end_code(self) -> str:
        return '\n'.join(
            f'{v.free_name}({v.object_name});'
            for v in self.scope.free_vars
            if v not in self.scope.parent.free_vars
        ) + '\n' + self.scope.ending_code
    
    def body_str(self, contexts, params: list[Param] | None = None, **kwargs) ->\
        tuple[str, list[Object], Free]:
        """Convert the input into a string. Also returns the compiled `Object`'s and the `Free`
        structure of the body, only if a `Free` structure is given when a `return` is used.
        
        Args:
            contexts (list[Object] | CureParser.BodyContext): The contexts to compile.
            params (list[Param] | None, optional): The parameters of the function. Defaults to None.

        Returns:
            tuple[str, list[Object], Free]: The string, the compiled `Object`'s and the `Free`
        """
        
        if isinstance(contexts, CureParser.BodyContext):
            contexts = contexts.bodyStmts()
        
        if params is None:
            params = []
        
        self.enter_scope(params, **kwargs)
        
        free = None
        code = []
        object_code = []
        for ctx in contexts:
            stmt = self.visit(ctx)
            if isinstance(ctx, CureParser.BodyStmtsContext) and ctx.RETURN() is not None:
                expr_code = stmt.code.removeprefix('return ')
                if expr_code in [v.object_name for v in self.scope.free_vars]:
                    for v in self.scope.free_vars:
                        if v.object_name == expr_code:
                            self.scope.free_vars.remove(v)
                            free = v
            
            if self.scope.prepended_code != '':
                code.append(self.scope.prepended_code + '\n')
                self.scope.prepended_code = ''
            
            code.append(stmt.code)
            object_code.append(stmt)
            if self.scope.appended_code != '':
                code.append(self.scope.appended_code + '\n')
                self.scope.appended_code = ''
        
        self.exit_scope()
        return '\n'.join(stmt + ';' for stmt in code), object_code, free
    
    def call(self, name: str, args: list[Object], call_position: Position,
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
            obj = func(self, call_position, *args)
            if item.free is None:
                return Object(obj.code, obj.type, call_position)
            elif item.free.object_name != '':
                call_position.warn_here(
                    f'Overriding free variable \'{item.free.object_name}\', may cause memory issues'
                )
            
            temp_var = self.create_temp_var(obj.type, call_position, free=item.free)
            item.free.object_name = temp_var
            self.prepend_code(f'{obj.type.c_type} {temp_var} = {obj.code}')
            return Object(temp_var, obj.type, call_position, free=item.free)
        elif (c_func := self.c_manager.get_object(name)) is not None:
            if not getattr(c_func, 'can_user_call', False) and by_user:
                call_position.error_here(f'Name \'{name}\' is not defined')
            
            arg_types = tuple(arg.type.c_type for arg in args)
            call_func, params = None, None
            param_types = getattr(c_func, 'param_types', ())
            if validate_args(arg_types, param_types):
                call_func = c_func
                params = param_types
            else:
                for k, v in getattr(c_func, 'overloads', {}).items():
                    if validate_args(arg_types, k[0]):
                        if v is None:
                            v = c_func
                        
                        call_func = v
                        params = k[0]
                        break
            
            if call_func is None and params is None:
                arg_types_str = ', '.join(type_ for type_ in arg_types)
                call_position.error_here(
                    f'No matching overload for \'{name}\' with arguments {arg_types_str}'
                )
            
            has_greedy = '*' in params
            if len(args) != len(params) and not has_greedy:
                call_position.error_here(
                    f'\'{name}\' takes {len(params)} arguments, but {len(args)} were given'
                )
            
            has_self = inspect.signature(call_func).parameters.get('self') is not None
            if not has_self:
                return call_func(self, call_position, *args)
                
            s = call_func.__repr__()
            cls = globals().get(s.split('.')[0].split()[1])
            if cls is None:
                call_position.error_here(f'Failed to call \'{name}\'')
            
            return call_func(cls(self), self, call_position, *args)
        
        if item is None:
            call_position.error_here(f'Name \'{name}\' is not defined')
        
        call_position.error_here(f'Name \'{name}\' is not a function')

    
    def condition(self, expr: CureParser.ExprContext) -> Object:
        """Converts an expression into an `Object`, used in `if` statements.

        Args:
            expr (CureParser.ExprContext): The expression to convert.

        Returns:
            Object: The resulting `Object`, which is a boolean.
        """
        
        cond = self.visitExpr(expr)
        return self.call(f'{cond.type}_to_bool', [cond], cond.position)
    
    def use(self, lib_name: str, pos: Position) -> None:
        """Use a Cure library.

        Args:
            lib_name (str): The name of the library.
            pos (Position): The position.
        """
        
        for lib in LIBS_PATH.iterdir():
            if lib.stem == lib_name:
                rel_path = lib.relative_to(getcwd(), walk_up=True)
                if rel_path.is_dir():
                    lib_path = rel_path.as_posix().replace('/', '.')
                else:
                    lib_path = rel_path.as_posix().replace('/', '.')[:-3]
                
                exec(f"""from {lib_path} import {lib_name}
if {lib_name} not in [type(cls) for cls in libraries]:
    lib = {lib_name}(self)
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
            pos.error_here(f'Library \'{lib_name}\' not found')
    
    
    def visitParse(self, ctx: CureParser.ParseContext) -> str:
        body, _, _ = self.body_str(ctx.stmt())
        return f'{self.top_level_code}\n{body}'
    
    def visitType(self, ctx: CureParser.TypeContext) -> Type:
        txt = ctx.ID().getText()
        for class_ in self.library_classes:
            if (get_type := getattr(class_, 'get_type', None)) is not None:
                if (res := get_type(ctx)) is not None:
                    return res
        
        if txt not in self.valid_types and txt not in {'array', 'dict'}:
            to_pos(ctx).error_here(f'Invalid type \'{txt}\'')
        
        if ctx.type_(0) is not None:
            if txt == 'array':
                array_type = self.visitType(ctx.type_(0))
                self.array_manager.define_array(array_type)
                return Type(f'{txt}[{array_type}]', f'{array_type}_{txt}')
            elif txt == 'dict':
                key_type = self.visitType(ctx.type_(0))
                value_type = self.visitType(ctx.type_(1))
                self.dict_manager.define_dict(key_type, value_type)
                return Type(f'{txt}[{key_type}: {value_type}]', f'{key_type}_{value_type}_{txt}')
        
        return Type(txt)
    
    def visitUseStmt(self, ctx: CureParser.UseStmtContext) -> Object:
        lib_name = ctx.STRING().getText()[1:-1]
        pos = to_pos(ctx)
        
        self.use(lib_name, pos)

        return Object('', Type('nil'), pos)
    
    def visitIfStmt(self, ctx: CureParser.IfStmtContext) -> Object:
        cond = self.condition(ctx.expr())
        kwargs = {field.name: getattr(self.scope, field.name) for field in fields(self.scope)}
        body, _, _ = self.body_str(ctx.body(), **kwargs)
        else_body_code, _, _ = self.body_str(ctx.elseStmt().body(), **kwargs) if ctx.elseStmt()\
            is not None else '', [], None
        
        elseif_bodies = []
        for elseif in ctx.elseifStmt():
            elseif_body, _, _ = self.body_str(elseif.body(), **kwargs)
            elseif_bodies.append(f""" else if ({self.condition(elseif.expr()).code}) {{
{elseif_body}
}}
""")
        elseif_bodies = '\n'.join(elseif_bodies)
        
        return Object(
            f"""if ({cond.code}) {{\n{body}\n}}{elseif_bodies}{f""" else {{
{else_body_code[0]}
}}
""" if else_body_code != '' else ''}
""",
            Type('nil'), to_pos(ctx)
        )
    
    def visitWhileStmt(self, ctx: CureParser.WhileStmtContext) -> Object:
        cond = self.condition(ctx.expr())
        body, _, _ = self.body_str(ctx.body(), is_in_loop=True)
        return Object(
            f'while ({cond.code}) {{\n{body}\n}}',
            Type('nil'), to_pos(ctx)
        )
    
    def visitForeachStmt(self, ctx: CureParser.ForeachStmtContext) -> Object:
        loop_name = ctx.ID().getText()
        pos = to_pos(ctx)
        if self.name_occupied(loop_name):
            pos.error_here(f'\'{loop_name}\' is already defined')
        
        expr = self.visitExpr(ctx.expr())
        
        iter_method = self.c_manager.get_object(f'iter_{expr.type.c_type}')
        if iter_method is None:
            pos.error_here(f'\'{expr.type}\' does not support iteration')
        
        len_callee = self.c_manager.get_object(f'{expr.type.c_type}_length')
        if len_callee is None:
            pos.error_here(f'\'{expr.type}\' does not support iteration')
        
        len_expr = self.call(f'{expr.type.c_type}_length', [expr], pos)
        
        i = self.create_temp_var(Type('int'), pos)
        loop_obj = Object(i, Type('int'), pos)
        
        self.enter_scope(is_in_loop=True)
        
        iter_var = self.create_temp_var(iter_method.return_type, pos, loop_name)
        iter_call = self.call(f'iter_{expr.type.c_type}', [expr, loop_obj], pos)
        str_body, _, _ = self.body_str(ctx.body(), is_in_loop=True)

        out = Object(f"""for (int {i} = 0; {i} < {len_expr.code}; {i}++) {{
{self.scope.prepended_code}
{iter_method.return_type} {iter_var} = {iter_call.code};
{str_body}
{self.scope.appended_code}
{self.scope.ending_code}
}}
""", Type('nil'), pos)
        
        self.exit_scope()
        return out
    
    def visitBodyStmts(self, ctx: CureParser.BodyStmtsContext) -> Object:
        if ctx.RETURN() is not None:
            expr = self.visitExpr(ctx.expr())
            self.prepend_code(self.get_end_code())
            return Object(f'return {expr.code}', expr.type, to_pos(ctx), expr.free)
        elif ctx.stmt() is not None:
            return self.visitStmt(ctx.stmt())
        elif ctx.BREAK() is not None:
            pos = to_pos(ctx)
            if not self.scope.is_in_loop:
                pos.error_here('\'break\' used outside a loop')
            
            self.prepend_code(self.get_end_code())
            return Object('break', Type('nil'), pos)
        elif ctx.CONTINUE() is not None:
            pos = to_pos(ctx)
            if not self.scope.is_in_loop:
                pos.error_here('\'continue\' used outside a loop')
            
            self.prepend_code(self.get_end_code())
            return Object('continue', Type('nil'), pos)
    
    def visitBody(self, ctx: CureParser.BodyContext) -> list[Object]:
        return [self.visitBodyStmts(stmt) for stmt in ctx.bodyStmts()]
    
    def visitVarAssign(self, ctx: CureParser.VarAssignContext) -> Object:
        name = ctx.ID().getText()
        pos = to_pos(ctx)
        expr = self.visitExpr(ctx.expr())
        type_ = self.visitType(ctx.type_()) if ctx.type_() is not None else expr.type
        if expr.type != type_:
            pos.error_here(f'Expected type \'{type_}\', got \'{expr.type}\'')
        
        if self.name_occupied(name) and name not in self.scope.env:
            pos.error_here(f'Name \'{name}\' is already occupied')
        
        if (item := self.scope.env.get(name)) is not None:
            if ctx.type_() is not None:
                pos.error_here(f'Cannot redeclare \'{name}\' as variable')
            
            if ctx.op is not None:
                op = ctx.op.text
                callee = f'{item.type}_{op_map[op]}_{expr.type}'
                val = Object(item.name, item.type, pos)
                if self.c_manager.get_object(callee) is None:
                    pos.error_here(f'Operator \'{op}\' is not defined for types \'{val.type}\''\
                        f'and \'{expr.type}\'')

                expr = self.call(callee, [val, expr], pos)
            
            return Object(f'{item.name} = {expr.code}', item.type, pos)
        else:
            if ctx.op is not None:
                pos.error_here(f'\'{name}\' is not defined')
            
            self.scope.env[name] = EnvItem(name, type_, pos, free=expr.free)
            return Object(f'{type_.c_type} {name} = {expr.code}', type_, pos)
    
    def visitFuncAssign(self, ctx: CureParser.FuncAssignContext) -> Object:
        name = ctx.ID().getText()
        pos = to_pos(ctx.FUNC())
        
        params = self.visitParams(ctx.params())
        return_type = self.visitType(ctx.type_()) if ctx.type_() is not None else Type('nil')
        
        new_name = None
        if name in self.scope.env:
            new_name = self.get_unique_name(name)
            self.scope.env[name].func.add_overload(
                new_name, return_type,
                [param.type for param in params]
            )
        elif self.name_occupied(name):
            pos.error_here(f'Name \'{name}\' is already occupied')
        else:
            func = Function(name, return_type, params, ctx.body())
            for mod in ctx.funcModifications():
                mod_name = mod.ID().getText()
                args = self.visitArgs(mod.args()) if mod.args() is not None else []
                modification = self.c_manager.get_object(mod_name)
                if modification is not None:
                    func.add_modification(mod_name, to_pos(mod), modification, args)
                elif modification is None:
                    pos.error_here(f'Unknown function modification \'{mod_name}\'')
            
            self.scope.env[name] = EnvItem(name, Type('function'), pos, func)
        
        kwargs = {}
        if name == 'main':
            kwargs['ending_code'] = 'free(args.elements);'
        
        body_str, _, free = self.body_str(ctx.body(), params, **kwargs)
        
        self.scope.env[name].free = Free(free_name=free.free_name) if free is not None else None
        
        params_str = ', '.join(
            f'{param.type.c_type}{"*" if param.ref else ""} {param.name}'
            for param in params
        )
        
        if new_name is not None:
            name = new_name
        
        return Object(f"""{return_type.c_type} {name}({params_str}) {{
{body_str}
}}
""", Type('nil'), pos)
    
    def visitParam(self, ctx: CureParser.ParamContext) -> Param:
        return Param(ctx.ID().getText(), self.visitType(ctx.type_()), ctx.AMPERSAND() is not None)
    
    def visitParams(self, ctx: CureParser.ParamsContext) -> list[Param]:
        return [self.visitParam(param) for param in ctx.param()] if ctx is not None else []
    
    def visitArg(self, ctx: CureParser.ArgContext) -> Object:
        return self.visitExpr(ctx.expr())
    
    def visitArgs(self, ctx: CureParser.ArgsContext) -> list[Object]:
        return [self.visitArg(arg) for arg in ctx.arg()] if ctx is not None else []
    
    def visitAtom(self, ctx: CureParser.AtomContext) -> Object:
        pos = to_pos(ctx)
        if ctx.INT() is not None:
            return Object(ctx.getText(), Type('int'), pos)
        elif ctx.FLOAT() is not None:
            return Object(ctx.getText() + 'f', Type('float'), pos)
        elif ctx.STRING() is not None:
            return Object(ctx.getText(), Type('string'), pos)
        elif ctx.BOOL() is not None:
            return Object(ctx.getText(), Type('bool'), pos)
        elif ctx.NIL() is not None:
            return Object('NULL', Type('nil'), pos)
        elif ctx.HEX() is not None:
            return Object(ctx.getText(), Type('hex'), pos)
        elif ctx.BIN() is not None:
            return Object(ctx.getText(), Type('bin'), pos)
        elif ctx.ID() is not None:
            name = ctx.getText()
            if (item := self.scope.env.get(name)) is not None:
                if item.func is not None:
                    return Object(item.name, Type('function'), pos)
                
                return Object(item.name, item.type, pos)
            elif name in self.valid_types:
                return Object(name, Type('type'), pos)
            else:
                pos.error_here(f'Name \'{name}\' is not defined')
        elif ctx.expr() is not None:
            expr = self.visitExpr(ctx.expr())
            expr.code = f'({expr.code})'
            return expr
        elif ctx.type_() is not None:
            if ctx.dict_element():
                key_type = self.visitType(ctx.type_(0))
                value_type = self.visitType(ctx.type_(1))
                
                self.dict_manager.define_dict(key_type, value_type)
                make_call = self.call(f'{key_type}_{value_type}_dict_make', [], pos)
                for elem in ctx.dict_element():
                    key = self.visitExpr(elem.expr(0))
                    value = self.visitExpr(elem.expr(1))
                    
                    self.call(f'{key_type}_{value_type}_dict_set', [make_call, key, value], pos)
                
                return make_call
            else:
                args = self.visitArgs(ctx.args())
                type = self.visitType(ctx.type_(0))
                pos = to_pos(ctx)
                
                self.array_manager.define_array(type)
                
                make_call = self.call(f'{type}_array_make', [], pos)
                
                for arg in args:
                    self.call(f'{type}_array_add', [make_call, arg], pos)
                
                return make_call
        else:
            to_pos(ctx).error_here(f'Invalid atom \'{ctx.getText()}\'')
    
    def visitCall(self, ctx: CureParser.CallContext) -> Object:
        return self.call(ctx.ID().getText(), self.visitArgs(ctx.args()), to_pos(ctx), True)
    
    def visitExpr(self, ctx: CureParser.ExprContext) -> Object:
        if ctx.atom() is not None:
            return self.visitAtom(ctx.atom())
        elif ctx.call() is not None:
            return self.visitCall(ctx.call())
        elif ctx.op is not None:
            pos = to_pos(ctx)
            op = ctx.op.text
            op_name = op_map[op]
            left = self.visitExpr(ctx.expr(0))
            right = self.visitExpr(ctx.expr(1))
            callee = f'{left.type.c_type}_{op_name}_{right.type.c_type}'
            if self.c_manager.get_object(callee) is None:
                pos.error_here(f'Operator \'{op}\' is not defined for types \'{left.type}\''\
                    f'and \'{right.type}\'')

            return self.call(callee, [left, right], pos)
        elif ctx.uop is not None:
            pos = to_pos(ctx)
            op = ctx.uop.text
            op_name = op_map[op]
            expr = self.visitExpr(ctx.expr(0))
            callee = f'{op_name}_{expr.type.c_type}'
            if self.c_manager.get_object(callee) is None:
                pos.error_here(f'Operator \'{op}\' is not defined for type \'{expr.type}\'')

            return self.call(callee, [expr], pos)
        elif ctx.DOT() is not None:
            pos = to_pos(ctx)
            expr = self.visitExpr(ctx.expr(0))
            attr = ctx.ID().getText()
            callee = f'{expr.type.c_type}_{attr}'
            if (func := self.c_manager.get_object(callee)) is not None:
                args = []
                if not getattr(func, 'is_static', False):
                    args.append(expr)
                
                if getattr(func, 'is_method', False):
                    if ctx.LPAREN() is None:
                        pos.error_here(
                            f'Attribute \'{attr}\' is method, but is accessed like a property'
                        )
                    
                    args.extend(self.visitArgs(ctx.args()))
                elif getattr(func, 'is_property', False):
                    if ctx.LPAREN() is not None:
                        pos.error_here(f'Attribute \'{attr}\' is property, not a function')
                else:
                    pos.error_here(f'Invalid attribute \'{attr}\' on type \'{expr.type}\'')
                
                return self.call(callee, args, pos)
            else:
                pos.error_here(f'Attribute \'{attr}\' is not defined for type \'{expr.type}\'')
        elif ctx.NEW() is not None:
            pos = to_pos(ctx)
            cls = ctx.ID().getText()
            args = self.visitArgs(ctx.args())
            callee = f'{cls}_new'
            if (func := self.c_manager.get_object(callee)) is not None:
                if not getattr(func, 'is_static', False):
                    pos.error_here(f'Class \'{cls}\' Instantiation method is not static')
                
                return self.call(callee, args, pos)
            
            pos.error_here(f'Cannot instantiate class \'{cls}\'')
