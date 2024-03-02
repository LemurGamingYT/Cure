from .constants import Type, OP_RETURN_TYPES, OP_FUNC_NAMES, Statement, error, EnvItem, ATTRIBUTES
from compiler.std.funcs import public_funcs
from parser.CureVisitor import CureVisitor
from parser.CureParser import CureParser


class Compiler(CureVisitor):
    def __init__(self) -> None:
        self.env = {
            'Math': EnvItem('Math', Type.math, False),
            'System': EnvItem('System', Type.system, False),
            # 'Logger': EnvItem('Logger', Type.logger, False),
            'Mem': EnvItem('Mem', Type.mem, False)
        }

        self.indentation = ''


    def indent(self) -> None:
        self.indentation += '\t'

    def deindent(self) -> None:
        self.indentation = self.indentation[:-4]


    def check_frees(self) -> str:
        frees = ''
        for i, (name, item) in enumerate(self.env.items()):
            if item.requires_free:
                nl = '\n'
                if i == len(self.env.items()) - 1:
                    nl = ''

                frees += f'{"\t"}free({name});{nl}'

        return frees


    @staticmethod
    def str_to_type(s: str) -> Type:
        match s:
            case 'int' | 'Int':
                return Type.int
            case 'float' | 'Float':
                return Type.float
            case 'string' | 'String':
                return Type.string
            case 'bool' | 'Bool':
                return Type.bool
            case 'nil' | 'Nil':
                return Type.nil
            case _:
                error('Type', f'Unknown type \'{s}\'')


    def remove_non_functions(self) -> None:
        self.isolate_functions = False

        new_env = {}
        for name, item in self.env.items():
            if item.is_func:
                new_env[name] = item

        self.env = new_env


    def run_function_body(self, body: CureParser.BodyContext, params: list[Statement]) -> Statement:
        for param in params:
            p_name = param.code.split(' ')[1]
            self.env[p_name] = EnvItem(p_name, param.type, False)

        body = self.visitBody(body)
        for param in params:
            p_name = param.code.split(' ')[1]
            self.env[p_name] = EnvItem(p_name, param.type, False)

        return body


    # def collect_func_defs(self, ctx: CureParser.FuncAssignContext) -> None:
    #     name = ctx.ID().getText()
    #     params = self.visitParams(ctx.params())
    #     ret_type = self.visitType(ctx.type_()) if ctx.type_() is not None else None
    #     if ret_type is None:
    #         ret_type = Type.nil

    #     self.env[name] = EnvItem(name, ret_type, True)
    #     body = self.run_function_body(ctx.body(), params)

    #     if ret_type == Type.nil and body.stmt_is_returning:
    #         self.env[name] = EnvItem(name, ret_type, True)

    def visitParse(self, ctx: CureParser.ParseContext) -> str:
        stmts = []
        for stmt in ctx.stmt():
            stmts.append(f'{self.indentation}{self.visitStmt(stmt).code}')
        
        if self.env.get('main') is None:
            error('Parse', 'No main function found')

        return '\n'.join(stmts)

    def visitType(self, ctx: CureParser.TypeContext) -> Type:
        return self.str_to_type(ctx.ID(0).getText())
    
    def visitIfStmt(self, ctx: CureParser.IfStmtContext) -> Statement:
        cond = self.visitExpr(ctx.expr())
        body = self.visitBody(ctx.body())
        else_ = f""" else {{
{self.visitElseStmt(ctx.elseStmt()).code}
{self.indentation}}}""" if ctx.elseStmt() else ''
        return Statement(
            f'if ({cond.str_type}_bool({cond.code})) {{\n{body.code}\n{self.indentation}}}{else_}',
            cond.type
        )

    def visitElseStmt(self, ctx: CureParser.ElseStmtContext) -> Statement:
        return self.visitBody(ctx.body())
    
    def visitWhileStmt(self, ctx: CureParser.WhileStmtContext) -> Statement:
        cond = self.visitExpr(ctx.expr())
        body = self.visitBody(ctx.body())
        return Statement(
            f'while ({cond.str_type}_bool({cond.code})) {{\n{body.code}\n{self.indentation}}}',
            cond.type
        )

    def visitVarAssign(self, ctx: CureParser.VarAssignContext) -> Statement:
        name = ctx.ID().getText()
        value = self.visitExpr(ctx.expr())
        if ctx.type_():
            typ = self.visitType(ctx.type_())
        else:
            typ = value.type

        if name in self.env:
            return Statement(f'{name} = {value.code}', typ)

        requires_freeing = False
        if typ == Type.string:
            requires_freeing = True
        
        self.env[name] = EnvItem(name, typ, False, requires_freeing)

        return Statement(f'{typ.str_type} {name} = {value.code}', typ)

    def visitFuncAssign(self, ctx: CureParser.FuncAssignContext) -> Statement:
        name = ctx.ID().getText()
        params = self.visitParams(ctx.params())

        ret_type = self.visitType(ctx.type_()) if ctx.type_() is not None else None
        if ret_type is None:
            ret_type = Type.nil

        self.env[name] = EnvItem(name, ret_type, True)
        body = self.run_function_body(ctx.body(), params)

        main_ps = 'int argc, char** argv[]' if name == 'main' else ''
        typ = 'int' if name == 'main' else ret_type.str_type.title()
        return Statement(
            f"""{typ} {name}({main_ps}{', '.join(p.code for p in params)}) {{
{body.code}{f'\n{self.check_frees()}\n{'\t'}return 0;' if name == 'main' else ''}
}}\n""",
            ret_type
        )
    
    def visitBodyStmts(self, ctx: CureParser.BodyStmtsContext) -> Statement:
        if ctx.stmt():
            return self.visitStmt(ctx.stmt())
        elif ctx.RETURN():
            expr = self.visitExpr(ctx.expr())
            return Statement(f'return {expr.code}', expr.type, True)

    def visitBody(self, ctx: CureParser.BodyContext) -> Statement:
        self.indent()
        stmts = []
        typ = Type.nil
        for stmt in ctx.bodyStmts():
            is_return = stmt.RETURN() is not None

            stmt = self.visitBodyStmts(stmt)
            stmt.code = f'{self.indentation}{stmt.code};'
            stmts.append(stmt)

            if is_return:
                typ = stmt.type

        self.deindent()
        return Statement('\n'.join(s.code for s in stmts), typ, typ != Type.nil)

    def visitArg(self, ctx: CureParser.ArgContext) -> Statement:
        return self.visitExpr(ctx.expr())

    def visitArgs(self, ctx: CureParser.ArgsContext) -> list[Statement]:
        return [self.visitArg(arg) for arg in ctx.arg()] if ctx is not None else []

    def visitParam(self, ctx: CureParser.ParamContext) -> Statement:
        typ = self.visitType(ctx.type_())
        return Statement(f'{typ.str_type} {ctx.ID().getText()}', typ)

    def visitParams(self, ctx: CureParser.ParamsContext) -> list[Statement]:
        return [self.visitParam(param) for param in ctx.param()] if ctx is not None else []

    def visitAtom(self, ctx: CureParser.AtomContext) -> Statement:
        if ctx.INT():
            return Statement(ctx.getText(), Type.int)
        elif ctx.FLOAT():
            return Statement(ctx.getText(), Type.float)
        elif ctx.STRING():
            return Statement(ctx.getText(), Type.string)
        elif ctx.BOOL():
            return Statement(ctx.getText(), Type.bool)
        elif ctx.NIL():
            return Statement(ctx.getText(), Type.nil)
        elif ctx.ID():
            if ctx.getText() in self.env:
                return Statement(ctx.getText(), self.env[ctx.getText()].type)
            
            error('Name', f'Name \'{ctx.getText()}\' not found')
        elif ctx.expr():
            return self.visitExpr(ctx.expr())

    def visitCall(self, ctx: CureParser.ExprContext) -> Statement:
        name = ctx.ID().getText()
        args = self.visitArgs(ctx.args())
        
        if name in public_funcs:
            return public_funcs[name](self, args)
        
        if not name in self.env:
            error('Name', f'Name \'{name}\' not found')

        return Statement(f'{name}({", ".join(a.code for a in args)})', self.env[name].type)

    def visitExpr(self, ctx: CureParser.ExprContext) -> Statement:
        if ctx.atom():
            return self.visitAtom(ctx.atom())
        elif ctx.call():
            return self.visitCall(ctx.call())
        elif ctx.DOT():
            left = self.visitExpr(ctx.expr(0))
            attr = ctx.ID().getText()
            attrs = ATTRIBUTES.get(left.type)
            if attrs is None:
                error('Type', f'\'{left.str_type}\' has no attributes')

            a = attrs.get(attr)
            if ctx.LPAREN():
                args = self.visitArgs(ctx.args())
                if a.is_method:
                    if not a.static:
                        args.insert(0, left)

                    return Statement(
                        f'{left.str_type}_{attr}({", ".join(a.code for a in args)})',
                        a.type
                    )
                else:
                    error('Type', f'\'{attr}\' is not a method')

            if a.static:
                return Statement(f'{left.str_type}_{attr}()', a.type)

            return Statement(f'{left.str_type}_{attr}({left.code})', a.type)
        elif ctx.NOT():
            left = self.visitExpr(ctx.expr(0))
            op_type = OP_RETURN_TYPES['!'].get(left.type)
            return Statement(f'not_{left.str_type}({left.code})', op_type)
        elif ctx.op:
            left = self.visitExpr(ctx.expr(0))
            right = self.visitExpr(ctx.expr(1))

            op = ctx.op.text

            ltyp = left.type
            rtyp = right.type
            op_type = OP_RETURN_TYPES[op].get((ltyp, rtyp))
            if op_type is None:
                error(
                    'Type',
                    f'Invalid types \'{ltyp.str_type}\' and \'{rtyp.str_type}\' for operator \'{op}\''
                )

            return Statement(
                f'{ltyp.str_type}_{OP_FUNC_NAMES[op]}_{rtyp.str_type}({left.code}, {right.code})',
                op_type
            )
