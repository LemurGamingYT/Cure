from antlr4.error.ErrorListener import ErrorListener as ANTLRErrorListener
from antlr4 import InputStream, CommonTokenStream
from antlr4.Token import CommonToken

from cure.parser.CureVisitor import CureVisitor
from cure.parser.CureParser import CureParser
from cure.parser.CureLexer import CureLexer
from cure.ir import (
    Program, Scope, Position, Function, Param, Int, Float, String, Bool, Id, Return, Body, Call,
    Cast, Operation, New, Use, If, Elseif, While, Variable, Ternary, Bracketed, Attribute, Break,
    Continue, NewArray, Unsafe, Type, Ref, Noop, Class, ArrayInit,
    FunctionFlags, op_map
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
    
    def get_operator_overload_name(self, pos: Position, op_name: str, params: list[Param]):
        if len(params) > 2 or len(params) < 1:
            pos.comptime_error(
                self.scope, 'operator overload functions must have exactly 2 or 1 parameter'
            )
        
        if len(params) == 1:
            return f'{op_map[op_name]}_{params[0].type}'
        
        a, b = params
        return f'{a.type}_{op_map[op_name]}_{b.type}'
    
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
        pos = self.pos(ctx)
        type = self.scope.type_map.get(ctx.ID().getText())
        if type is None:
            type = Type(pos, ctx.ID().getText(), ctx.ID().getText())
        
        if ctx.AMPERSAND() is not None:
            type = type.as_reference()
        
        return type
    
    def visitArgs(self, ctx):
        return [self.visitArg(arg) for arg in ctx.arg()] if ctx is not None else []
    
    def visitArg(self, ctx):
        return self.visit(ctx.expr())
    
    def visitBodyStmt(self, ctx):
        if ctx.stmt():
            return self.visit(ctx.stmt())
        elif ctx.RETURN():
            expr = self.visit(ctx.expr())
            return Return(self.pos(ctx), expr.type, expr)
        elif ctx.BREAK():
            return Break(self.pos(ctx), self.scope.type_map.get('any'))
        elif ctx.CONTINUE():
            return Continue(self.pos(ctx), self.scope.type_map.get('any'))
    
    def visitBody(self, ctx):
        return Body(
            self.pos(ctx), self.scope.type_map.get('any'),
            [self.visitBodyStmt(stmt) for stmt in ctx.bodyStmt()]
        )
    
    def visitParams(self, ctx):
        return [self.visitParam(param) for param in ctx.param()] if ctx is not None else []
    
    def visitParam(self, ctx):
        return Param(
            self.pos(ctx), self.visitType(ctx.type_()), ctx.ID().getText(),
            ctx.MUTABLE() is not None
        )
    
    def visitGenericParams(self, ctx):
        return [self.visitGenericParam(param) for param in ctx.genericParam()]\
            if ctx is not None else []
    
    def visitGenericParam(self, ctx):
        return ctx.ID().getText()
    
    def visitFuncName(self, ctx):
        if ctx.type_() is not None:
            return (
                self.visitType(ctx.type_()),
                ctx.ID().getText() if ctx.ID() is not None else ctx.NEW().getText()
            )
        else:
            return ctx.getText()
    
    def visitFuncAssign(self, ctx):
        pos = self.pos(ctx)
        name = self.visitFuncName(ctx.funcName())
        params = self.visitParams(ctx.params())
        if isinstance(name, tuple):
            extend_type, name = name
        else:
            if name in op_map:
                name = self.get_operator_overload_name(pos, name, params)
            
            extend_type = None
        
        return Function(
            pos, self.visitType(ctx.return_type) if ctx.return_type is not None\
                else self.scope.type_map.get('nil'), name,
            params, self.visitBody(ctx.body()),
            flags=FunctionFlags(public=True), extend_type=extend_type
        )
    
    def visitVarAssign(self, ctx):
        return Variable(
            self.pos(ctx),
            self.visitType(ctx.type_()) if ctx.type_() is not None else self.scope.type_map.get('any'),
            ctx.ID().getText(), self.visit(ctx.expr()), ctx.MUTABLE() is not None,
            ctx.op.text if ctx.op is not None else None
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
    
    def visitUnsafeStmt(self, ctx):
        return Unsafe(self.pos(ctx), self.scope.type_map.get('any'), self.visitBody(ctx.body()))

    def visitUseStmt(self, ctx):
        return Use(self.pos(ctx), self.scope.type_map.get('any'), ctx.STRING().getText()[1:-1])
    
    def visitExternType(self, ctx):
        type_name = ctx.ID().getText()
        typ = self.scope.type_map.add(type_name)
        typ.is_external = True
        
        return Noop(self.pos(ctx), typ)

    def visitExternFunc(self, ctx):
        pos = self.pos(ctx)
        name = self.visitFuncName(ctx.funcName())
        params = self.visitParams(ctx.params())
        if isinstance(name, tuple):
            extend_type, name = name
        else:
            if name in op_map:
                name = self.get_operator_overload_name(pos, name, params)
            
            extend_type = None
        
        generic_params = self.visitGenericParams(ctx.genericParams())
        
        is_property = ctx.LPAREN() is None
        flags = FunctionFlags(property=is_property, method=not is_property,
                              static=ctx.STATIC() is not None)
        return Function(
            self.pos(ctx), self.visitType(ctx.return_type) if ctx.return_type is not None\
                else self.scope.type_map.get('nil'), name, params,
            flags=flags, extend_type=extend_type, generic_params=generic_params
        )

    def visitExternClass(self, ctx):
        pos = self.pos(ctx)
        name = ctx.ID().getText()
        generic_params = self.visitGenericParams(ctx.genericParams())
        methods = [self.visitExternFunc(m) for m in ctx.externFunc()]
        return Class(
            pos, self.scope.type_map.get('any'), name, methods, generic_params=generic_params
        )
    
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
    
    def visitNew(self, ctx):
        return New(
            self.pos(ctx), self.scope.type_map.get('any'), self.visitType(ctx.type_()),
            self.visitArgs(ctx.args())
        )
    
    def visitNewArray(self, ctx):
        return NewArray(
            self.pos(ctx), self.scope.type_map.get('any'), self.visitType(ctx.type_())
        )
    
    def visitArrayInit(self, ctx):
        return ArrayInit(
            self.pos(ctx), self.scope.type_map.get('any'), self.visitArgs(ctx.args())
        )
    
    def visitRef(self, ctx):
        object = self.visit(ctx.expr())
        return Ref(self.pos(ctx), object.type, object)
    
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
