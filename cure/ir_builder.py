from antlr4.error.ErrorListener import ErrorListener as ANTLRErrorListener
from antlr4 import InputStream, CommonTokenStream
from antlr4.Token import CommonToken

from cure.parser.CureVisitor import CureVisitor
from cure.parser.CureParser import CureParser
from cure.parser.CureLexer import CureLexer
from cure.ir import (
    Program, Scope, Position, Function, Param, Int, Float, String, Bool, Id, Return, Body, Call,
    Cast, Operation, Use, If, While, Variable, Ternary, Bracketed, Attribute, Break, Continue, Type,
    Class, NewArray, ArrayInit, ForRange, New, Elseif
)


class ErrorListener(ANTLRErrorListener):
    def __init__(self, scope: Scope):
        self.scope = scope
    
    def syntaxError(self, _, offendingSymbol: CommonToken, line: int, column: int, _msg, _e):
        pos = Position(line, column)
        pos.comptime_error(self.scope, f'invalid syntax \'{offendingSymbol.text}\'')

class IRBuilder(CureVisitor):
    def __init__(self, scope: Scope):
        self.scope = scope
    
    def pos(self, ctx):
        return Position(ctx.start.line, ctx.start.column)
    
    def build(self):
        lexer = CureLexer(InputStream(self.scope.src))
        parser = CureParser(CommonTokenStream(lexer))
        parser.removeErrorListeners()
        parser.addErrorListener(ErrorListener(self.scope))
        return self.visitProgram(parser.program())
    
    def visitProgram(self, ctx):
        return Program(
            self.pos(ctx), self.scope.type_map.get('any'), [self.visit(stmt) for stmt in ctx.stmt()]
        )
    
    def visitType(self, ctx):
        if ctx.LBRACK() is not None:
            typ = self.visitType(ctx.type_())
            return Type(self.pos(ctx), typ.type, typ.display, typ)
        
        txt = ctx.ID().getText()
        return Type(self.pos(ctx), txt, txt)
    
    def visitArgs(self, ctx):
        return [self.visitArg(arg) for arg in ctx.arg()] if ctx is not None else []
    
    def visitArg(self, ctx):
        return self.visit(ctx.expr())
    
    def visitStmtBody(self, ctx):
        return self.visit(ctx.stmt())
    
    def visitReturn(self, ctx):
        expr = self.visit(ctx.expr())
        return Return(self.pos(ctx), expr.type, expr)
    
    def visitBreak(self, ctx):
        return Break(self.pos(ctx), self.scope.type_map.get('any'))
    
    def visitContinue(self, ctx):
        return Continue(self.pos(ctx), self.scope.type_map.get('any'))
    
    def visitBody(self, ctx):
        return Body(
            self.pos(ctx), self.scope.type_map.get('any'),
            [self.visit(stmt) for stmt in ctx.bodyStmt()]
        )
    
    def visitParams(self, ctx):
        return [self.visitParam(param) for param in ctx.param()] if ctx is not None else []
    
    def visitParam(self, ctx):
        return Param(
            self.pos(ctx), self.visitType(ctx.type_()), ctx.ID().getText(),
            ctx.MUTABLE() is not None
        )
    
    def visitGenericParams(self, ctx):
        return [self.visitGenericParam(param) for param in ctx.genericParam()] if ctx is not None\
            else []
    
    def visitGenericParam(self, ctx):
        return ctx.ID().getText()
    
    def visitFuncName(self, ctx):
        extend_type = None
        if ctx.extend_type is not None:
            extend_type = self.visitType(ctx.extend_type)
        
        name = ctx.ID().getText() if ctx.ID() is not None else 'new'
        return extend_type, name
    
    def visitFunctionSignature(self, ctx):
        extend_type, name = self.visitFuncName(ctx.funcName())
        return Function(
            self.pos(ctx), self.scope.type_map.get('function'), name,
            self.visitType(ctx.return_type) if ctx.return_type is not None else\
                self.scope.type_map.get('nil'), self.visitParams(ctx.params()),
            generic_names=self.visitGenericParams(ctx.genericParams()),
            extend_type=extend_type
        )
    
    def visitFuncAssign(self, ctx):
        func = self.visitFunctionSignature(ctx.functionSignature())
        func.body = self.visitBody(ctx.body())
        return func
    
    def visitExternFunc(self, ctx):
        func = self.visitFunctionSignature(ctx.functionSignature())
        func.flags.static = ctx.STATIC() is not None
        func.flags.property = ctx.PROPERTY() is not None
        func.flags.method = ctx.METHOD() is not None
        func.flags.internal = ctx.INTERNAL() is not None
        return func
    
    def visitExternClass(self, ctx):
        return Class(
            self.pos(ctx), self.scope.type_map.get('any'), ctx.ID().getText(),
            self.visitBody(ctx.body()).nodes, self.visitGenericParams(ctx.genericParams()),
            ctx.INTERNAL() is not None
        )
    
    def visitVarAssign(self, ctx):
        return Variable(
            self.pos(ctx), self.scope.type_map.get('any'), ctx.ID().getText(), self.visit(ctx.expr()),
            ctx.MUTABLE() is not None, ctx.op.text if ctx.op is not None else None
        )
    
    def visitIfStmt(self, ctx):
        return If(
            self.pos(ctx), self.scope.type_map.get('any'), self.visit(ctx.expr()),
            self.visitBody(ctx.body()), self.visitElseStmt(ctx.elseStmt()),
            [self.visitElseifStmt(elseif) for elseif in ctx.elseifStmt()]
        )
    
    def visitElseStmt(self, ctx):
        return self.visitBody(ctx.body()) if ctx is not None else None
    
    def visitElseifStmt(self, ctx):
        return Elseif(
            self.pos(ctx), self.scope.type_map.get('any'),
            self.visit(ctx.expr()), self.visitBody(ctx.body())
        )
    
    def visitWhileStmt(self, ctx):
        return While(
            self.pos(ctx), self.scope.type_map.get('any'), self.visit(ctx.expr()),
            self.visitBody(ctx.body())
        )
    
    def visitForRangeStmt(self, ctx):
        return ForRange(
            self.pos(ctx), self.scope.type_map.get('any'), ctx.ID().getText(),
            self.visit(ctx.expr(0)), self.visit(ctx.expr(1)), self.visitBody(ctx.body())
        )
    
    def visitUseStmt(self, ctx):
        return Use(self.pos(ctx), self.scope.type_map.get('any'), ctx.STRING().getText()[1:-1])
    
    def visitInt(self, ctx):
        return Int(self.pos(ctx), self.scope.type_map.get('int'), int(ctx.getText()))
    
    def visitFloat(self, ctx):
        return Float(self.pos(ctx), self.scope.type_map.get('float'), float(ctx.getText()))
    
    def visitString(self, ctx):
        return String(self.pos(ctx), self.scope.type_map.get('string'), ctx.getText()[1:-1])
    
    def visitBool(self, ctx):
        return Bool(self.pos(ctx), self.scope.type_map.get('bool'), ctx.getText() == 'true')
    
    def visitId(self, ctx):
        return Id(self.pos(ctx), self.scope.type_map.get('any'), ctx.getText())
    
    def visitNew(self, ctx):
        return New(
            self.pos(ctx), self.scope.type_map.get('any'), self.visitType(ctx.type_()),
            self.visitArgs(ctx.args())
        )
    
    def visitNewArray(self, ctx):
        return NewArray(self.pos(ctx), self.scope.type_map.get('any'), self.visitType(ctx.type_()))
    
    def visitArrayInit(self, ctx):
        return ArrayInit(self.pos(ctx), self.scope.type_map.get('any'), self.visitArgs(ctx.args()))
    
    def visitCall(self, ctx):
        return Call(
            self.pos(ctx), self.scope.type_map.get('any'),
            Id(self.pos(ctx), self.scope.type_map.get('any'), ctx.ID().getText()),
            self.visitArgs(ctx.args())
        )
    
    def visitParen(self, ctx):
        expr = self.visit(ctx.expr())
        return Bracketed(self.pos(ctx), expr.type, expr)
    
    def visitCast(self, ctx):
        return Cast(self.pos(ctx), self.visitType(ctx.type_()), self.visit(ctx.expr()))
    
    def visitAttr(self, ctx):
        return Attribute(
            self.pos(ctx), self.scope.type_map.get('any'), self.visit(ctx.expr()), ctx.ID().getText(),
            self.visitArgs(ctx.args()) if ctx.LPAREN() is not None else None
        )
    
    def visitTernary(self, ctx):
        return Ternary(
            self.pos(ctx), self.scope.type_map.get('any'), self.visit(ctx.expr(1)),
            self.visit(ctx.expr(0)), self.visit(ctx.expr(2))
        )
    
    def visitOperation(self, ctx):
        pos = self.pos(ctx)
        op = ctx.op.text
        if isinstance(ctx.expr(), list):
            left, right = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        else:
            left, right = self.visit(ctx.expr()), None
        
        return Operation(pos, self.scope.type_map.get('any'), op, left, right)
    
    def visitAddition(self, ctx):
        return self.visitOperation(ctx)
    
    def visitMultiplication(self, ctx):
        return self.visitOperation(ctx)
    
    def visitRelational(self, ctx):
        return self.visitOperation(ctx)
    
    def visitLogical(self, ctx):
        return self.visitOperation(ctx)
    
    def visitUnary(self, ctx):
        return self.visitOperation(ctx)
