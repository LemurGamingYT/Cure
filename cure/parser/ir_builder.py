from antlr4 import InputStream, CommonTokenStream, RuleContext
from antlr4.error.ErrorListener import ErrorListener
from antlr4.Token import Token

from cure.parser.CureVisitor import CureVisitor
from cure.parser.CureParser import CureParser
from cure.parser.CureLexer import CureLexer
from cure import ir


def to_pos(ctx):
    if isinstance(ctx, Token):
        return ir.Position(ctx.line, ctx.column)
    elif isinstance(ctx, RuleContext):
        return ir.Position(ctx.start.line, ctx.start.column)
    
    raise NotImplementedError


class CureErrorListener(ErrorListener):
    def __init__(self, src: str):
        self.src = src

    def syntaxError(self, _, offendingSymbol: Token, line, column, _msg, _e):
        pos = ir.Position(line, column)
        pos.comptime_error(f'invalid syntax \'{offendingSymbol.text}\'', self.src)


class CureIRBuilder(CureVisitor):
    def __init__(self, scope: ir.Scope):
        self.src = scope.src
        self.scope = scope

    def build(self):
        lexer = CureLexer(InputStream(self.src))
        parser = CureParser(CommonTokenStream(lexer))
        parser.removeErrorListeners()
        parser.addErrorListener(CureErrorListener(self.src))
        return self.visit(parser.parse())


    def visitOperation(self, ctx):
        op = ctx.op.text
        if isinstance(ctx.expr(), list):
            left, right = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
            return ir.BinaryOp(to_pos(ctx), self.scope.type_map.get('any'), left, op, right)
        else:
            left = self.visit(ctx.expr())
            return ir.UnaryOp(to_pos(ctx), self.scope.type_map.get('any'), op, left)

    
    def visitAddition(self, ctx):
        return self.visitOperation(ctx)
    
    def visitArg(self, ctx):
        return self.visit(ctx.expr())
    
    def visitArgs(self, ctx):
        return [self.visit(arg) for arg in ctx.arg()] if ctx is not None else []
    
    def visitAtom(self, ctx):
        pos = to_pos(ctx)
        txt = ctx.getText()
        if ctx.INT() is not None:
            return ir.Int(pos, self.scope.type_map.get('int'), int(txt))
        elif ctx.FLOAT() is not None:
            return ir.Float(pos, self.scope.type_map.get('float'), float(txt))
        elif ctx.STRING() is not None:
            return ir.String(pos, self.scope.type_map.get('string'), txt[1:-1])
        elif ctx.BOOL() is not None:
            return ir.Bool(pos, self.scope.type_map.get('bool'), True if txt == 'true' else False)
        elif ctx.NIL() is not None:
            return ir.Nil(pos, self.scope.type_map.get('nil'))
        elif ctx.ID() is not None:
            return ir.Id(to_pos(ctx), self.scope.type_map.get('any'), txt)
        elif ctx.expr() is not None:
            return self.visit(ctx.expr())
        
        raise NotImplementedError
    
    def visitAttr(self, ctx):
        args = None
        if ctx.LPAREN() is not None:
            args = self.visitArgs(ctx.args())
        
        return ir.Attribute(
            to_pos(ctx), self.scope.type_map.get('any'),
            self.visit(ctx.expr()), ctx.ID().getText(), args
        )
    
    def visitBody(self, ctx):
        return ir.Body(
            to_pos(ctx), self.scope.type_map.get('any'),
            [self.visit(stmt) for stmt in ctx.bodyStmts()]
        )
    
    def visitBodyStmts(self, ctx):
        if ctx.RETURN() is not None:
            value = self.visit(ctx.expr())
            return ir.Return(to_pos(ctx), value.type, value)
        elif ctx.stmt() is not None:
            return self.visit(ctx.stmt())
        
        raise NotImplementedError
    
    def visitCall(self, ctx):
        pos = to_pos(ctx)
        callee = self.visit(ctx.expr())
        if not isinstance(callee, ir.Id):
            pos.comptime_error('invalid callee', self.src)
        
        return ir.Call(
            to_pos(ctx), self.scope.type_map.get('any'), callee.name, self.visitArgs(ctx.args())
        )
    
    def visitCast(self, ctx):
        return ir.Cast(to_pos(ctx), self.visit(ctx.type_()), self.visit(ctx.expr()))
    
    def visitElseifStmt(self, ctx):
        return ir.Elif(
            to_pos(ctx), self.scope.type_map.get('any'),
            self.visit(ctx.expr()), self.visit(ctx.body())
        )
    
    def visitElseStmt(self, ctx):
        return self.visit(ctx.body()) if ctx is not None else None
    
    def visitFuncAssign(self, ctx):
        return ir.Function(
            to_pos(ctx),
            self.visit(ctx.type_()) if ctx.type_() is not None else self.scope.type_map.get('nil'),
            ctx.ID().getText(), self.visitParams(ctx.params()),
            self.visit(ctx.body())
        )
    
    def visitIfStmt(self, ctx):
        return ir.If(
            to_pos(ctx), self.scope.type_map.get('any'),
            self.visit(ctx.expr()), self.visit(ctx.body()), self.visitElseStmt(ctx.elseStmt()),
            [self.visit(elseif) for elseif in ctx.elseifStmt()]
        )
    
    def visitLogical(self, ctx):
        return self.visitOperation(ctx)
    
    def visitMultiplication(self, ctx):
        return self.visitOperation(ctx)
    
    def visitNewArray(self, ctx):
        pos = to_pos(ctx)
        element_type = self.visit(ctx.type_())
        capacity = ir.Int(pos, 10)
        return ir.NewArray(pos, self.scope.type_map.get('any'), element_type, capacity)
    
    def visitParam(self, ctx):
        return ir.Param(
            to_pos(ctx), self.visit(ctx.type_()), ctx.ID().getText(),
            ctx.MUTABLE() is not None
        )
    
    def visitParams(self, ctx):
        return [self.visit(param) for param in ctx.param()] if ctx is not None else []
    
    def visitParse(self, ctx):
        return ir.Program(
            to_pos(ctx), self.scope.type_map.get('any'), [self.visit(stmt) for stmt in ctx.stmt()]
        )
    
    def visitRelational(self, ctx):
        return self.visitOperation(ctx)
    
    def visitTernary(self, ctx):
        return ir.Ternary(
            to_pos(ctx), self.scope.type_map.get('any'),
            self.visit(ctx.expr(1)), self.visit(ctx.expr(0)), self.visit(ctx.expr(2))
        )
    
    def visitType(self, ctx):
        return self.scope.type_map.get(ctx.ID().getText())
    
    def visitUnary(self, ctx):
        return self.visitOperation(ctx)
    
    def visitVarAssign(self, ctx):
        return ir.Variable(
            to_pos(ctx), self.scope.type_map.get('any'), ctx.ID().getText(), self.visit(ctx.expr()),
            ctx.MUTABLE() is not None
        )
    
    def visitWhileStmt(self, ctx):
        return ir.While(
            to_pos(ctx), self.scope.type_map.get('any'),
            self.visit(ctx.expr()), self.visit(ctx.body())
        )
