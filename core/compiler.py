from api import (
    Program, Assignment, Arg, Args, Call, FuncDef, Param, Params, Return, Body, Include, BinaryOp,
    GetAttr, If, While, UnaryOp
)
from core.std.objects import Int, Float, String, Bool, Nil, Id
from core.std import public_functions, public_classes
from core.parser.CureVisitor import CureVisitor
from core.parser.CureParser import CureParser


type_map = {
    'string': 'std::string',
}


INDENT_SIZE = 2
class Compiler(CureVisitor):
    def __init__(self, current_indent_level: int = 0):
        self.indent_level = current_indent_level

        self.includes = set()
        self.outside_objects = []
    
    def increase_indent(self) -> None:
        self.indent_level += INDENT_SIZE
    
    def decrease_indent(self) -> None:
        self.indent_level -= INDENT_SIZE
    
    def compile(self, tree: CureParser.ParseContext):
        return self.visitParse(tree)
    
    def visitParse(self, ctx: CureParser.ParseContext):
        body = []
        for stmt in ctx.stmt():
            out = self.visit(stmt)
            if out is None:
                continue
            elif isinstance(out, list):
                body.extend(out)
            else:
                body.append(out)
        
        self.increase_indent()
        body.append(Return(Int(0)))
        main_func = FuncDef('main', 'int', Params([]), Body(body, self.indent_level))
        self.decrease_indent()
        return Program(
            [Include(include) for include in self.includes] + self.outside_objects + [main_func]
        )

    def visitIfStmt(self, ctx: CureParser.IfStmtContext):
        condition = self.visit(ctx.expr(0))

        if len(ctx.ELSE()) == 1:
            return If(condition, self.visit(ctx.body(0)), self.visit(ctx.body(1)))
        elif len(ctx.ELSE()) == 0:
            return If(condition, self.visit(ctx.body(0)))
        else:
            return If(
                condition,
                self.visit(ctx.body(0)),
                elseif={
                    self.visit(ctx.expr(i)): self.visit(ctx.body(i)) for i in range(1, len(ctx.body()))
                }
            )

    def visitWhileStmt(self, ctx: CureParser.WhileStmtContext):
        return While(self.visit(ctx.expr()), self.visit(ctx.body()))

    def visitBody(self, ctx: CureParser.BodyContext) -> Body:
        self.increase_indent()
        b = Body([self.visit(stmt) for stmt in ctx.bodyStmts()], self.indent_level)
        self.decrease_indent()
        return b

    # def visitCompileTimeStmt(self, ctx: CureParser.CompileTimeStmtContext) -> CompileTime:
    #     return CompileTime(self.visit(ctx.stmt()))
    
    def visitVarAssignment(self, ctx: CureParser.VarAssignmentContext) -> Assignment:
        return Assignment(
            ctx.ID().getText(),
            self.visit(ctx.expr()),
            self.visit(ctx.typeDecl()) if ctx.typeDecl() is not None else 'auto'
        )
    
    def visitFuncAssignment(self, ctx: CureParser.FuncAssignmentContext) -> None:
        self.outside_objects.append(FuncDef(
            ctx.ID().getText(),
            self.visit(ctx.typeDecl()),
            self.visit(ctx.params()) if ctx.params() is not None else Params([]),
            self.visit(ctx.body())
        ))
    
    def visitReturnStmt(self, ctx: CureParser.ReturnStmtContext) -> Return:
        return Return(self.visit(ctx.expr()))
    
    def visitTypeDecl(self, ctx: CureParser.TypeDeclContext) -> str:
        if ctx.ID(0).getText() in type_map and len(ctx.ID()) == 1:
            return type_map[ctx.ID(0).getText()]

        return ctx.ID(0).getText() if len(ctx.ID()) == 1 else\
            f'{ctx.ID(0).getText()}->{ctx.ID(1).getText()}'
    
    def visitArg(self, ctx: CureParser.ArgContext) -> Arg:
        return Arg(self.visit(ctx.expr()))
    
    def visitArgs(self, ctx: CureParser.ArgsContext) -> Args:
        return Args([self.visit(arg) for arg in ctx.arg()])
    
    def visitParam(self, ctx: CureParser.ParamContext) -> Param:
        return Param(
            ctx.ID().getText(),
            self.visit(ctx.typeDecl()),
            self.visit(ctx.expr()) if ctx.expr() else None
        )
    
    def visitParams(self, ctx: CureParser.ParamsContext) -> Params:
        return Params([self.visit(param) for param in ctx.param()])
    
    def visitCall(self, ctx: CureParser.CallContext) -> Call:
        args = self.visit(ctx.args()) if ctx.args() else Args([])
        if ctx.ID().getText() in public_functions:
            return public_functions[ctx.ID().getText()](self, args)
        
        return Call(ctx.ID().getText(), args)
    
    def visitExpr(self, ctx: CureParser.ExprContext):
        if ctx.primary():
            return self.visit(ctx.primary())
        elif ctx.call():
            return self.visit(ctx.call())
        elif ctx.expr() and ctx.ID():
            obj = self.visit(ctx.expr(0))
            if isinstance(obj, Id) and obj.value in public_classes:
                return getattr(public_classes[obj.value], '_' + ctx.ID().getText())(
                    self,
                    self.visit(ctx.args()) if ctx.args() else Args([])
                )
            
            return GetAttr(
                self.visit(ctx.expr(0)),
                ctx.ID().getText(),
                self.visit(ctx.args()) if ctx.args() else None
            )
        elif ctx.expr() and ctx.op:
            return BinaryOp(self.visit(ctx.expr(0)), self.visit(ctx.expr(1)), ctx.op.text)
        elif ctx.unaryExpr():
            return self.visit(ctx.unaryExpr())

    def visitUnaryExpr(self, ctx:CureParser.UnaryExprContext) -> UnaryOp:
        return UnaryOp(self.visit(ctx.expr()), ctx.ADD() or ctx.SUB() or ctx.NOT())
    
    def visitPrimary(self, ctx: CureParser.PrimaryContext) -> Int | Float | String | Id | Bool | Nil:
        txt = ctx.getText()
        if ctx.INT():
            return Int(int(txt))
        elif ctx.FLOAT():
            return Float(float(txt))
        elif ctx.STRING():
            return String(txt)
        elif ctx.ID():
            return Id(txt)
        elif ctx.BOOL():
            return Bool(txt)
        else:
            return Nil()
