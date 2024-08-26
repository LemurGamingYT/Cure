from antlr4.error.ErrorListener import ErrorListener
from antlr4 import InputStream, CommonTokenStream
from antlr4.Token import CommonToken

from ir.parser.CureVisitor import CureVisitor
from ir.parser.CureParser import CureParser
from ir.parser.CureLexer import CureLexer
from ir.nodes import (
    Program, Body, TypeNode, ParamNode, ArgNode, Call, Return, Foreach, While,
    If, Use, VarDecl, Value, Identifier, Array, Dict, Brackets, BinOp, UOp, Attribute, New,
    Ternary, Position, Node, Break, Continue, FuncDecl, Nil, Index, DollarString
)


def to_pos(ctx) -> Position:
    if hasattr(ctx, 'start'):
        src = str(ctx.start.getTokenSource().inputStream)
        return Position(ctx.start.line, ctx.start.column, src)
    elif hasattr(ctx, 'getSymbol'):
        src = str(ctx.getSymbol().getTokenSource().inputStream)
        return Position(ctx.getSymbol().line, ctx.getSymbol().column, src)
    
    return Position(0, 0, '')

class CureErrorListener(ErrorListener):
    def syntaxError(self, _, offending_symbol, line, column, _msg, _e):
        Position(line, column, str(offending_symbol.getInputStream())).error_here(
            f'Invalid syntax \'{offending_symbol.text}\' at line {line}, column {column}'
        )

class IRBuilder(CureVisitor):
    def build(self, src: str) -> Program:
        """Compile .cure file.

        Args:
            src (str): The source code of the .cure file.

        Returns:
            Program: The output IR tree.
        """
        
        lexer = CureLexer(InputStream(src))
        parser = CureParser(CommonTokenStream(lexer))
        parser.removeErrorListeners()
        parser.addErrorListener(CureErrorListener())
        return self.visit(parser.parse())
    
    
    def visitParse(self, ctx: CureParser.ParseContext) -> Program:
        return Program(to_pos(ctx), [self.visitStmt(stmt) for stmt in ctx.stmt()])
    
    def visitType(self, ctx: CureParser.TypeContext) -> TypeNode:
        pos = to_pos(ctx)
        name = ctx.ID().getText()
        if len(ctx.type_()) == 0:
            return TypeNode(pos, name)
        elif len(ctx.type_()) == 1:
            return TypeNode(pos, name, self.visitType(ctx.type_(0)))
        elif len(ctx.type_()) == 2:
            return TypeNode(
                pos, name, None,
                (self.visitType(ctx.type_(0)), self.visitType(ctx.type_(1)))
            )
        else:
            pos.error_here(f'Invalid type \'{ctx.getText()}\'')
    
    def visitUseStmt(self, ctx: CureParser.UseStmtContext) -> Use:
        pos = to_pos(ctx)
        if ctx.STRING().getText().startswith('$'):
            pos.error_here('Cannot use string concatenation in use statement')
        
        return Use(pos, ctx.STRING().getText()[1:-1])
    
    def visitIfStmt(self, ctx: CureParser.IfStmtContext) -> If:
        cond = self.visitExpr(ctx.expr())
        body = self.visitBody(ctx.body())
        else_body = self.visitBody(ctx.elseStmt().body()) if ctx.elseStmt() is not None else None
        elseifs = []
        for elseif in ctx.elseifStmt():
            elseifs.append((self.visitExpr(elseif.expr()), self.visitBody(elseif.body())))
        
        return If(to_pos(ctx), cond, body, else_body, elseifs)
    
    def visitWhileStmt(self, ctx: CureParser.WhileStmtContext) -> While:
        return While(to_pos(ctx), self.visitExpr(ctx.expr()), self.visitBody(ctx.body()))

    def visitForeachStmt(self, ctx: CureParser.ForeachStmtContext) -> Foreach:
        return Foreach(
            to_pos(ctx), ctx.ID().getText(), self.visitExpr(ctx.expr()),
            self.visitBody(ctx.body())
        )
    
    def visitBodyStmts(self, ctx: CureParser.BodyStmtsContext) -> Node:
        if ctx.stmt() is not None:
            return self.visitStmt(ctx.stmt())
        elif ctx.RETURN() is not None:
            return Return(to_pos(ctx), self.visitExpr(ctx.expr()))
        elif ctx.BREAK() is not None:
            return Break(to_pos(ctx))
        elif ctx.CONTINUE() is not None:
            return Continue(to_pos(ctx))
        else:
            to_pos(ctx).error_here('Invalid statement')
    
    def visitBody(self, ctx: CureParser.BodyContext) -> Body:
        return Body(to_pos(ctx), [self.visitBodyStmts(stmt) for stmt in ctx.bodyStmts()])
    
    def visitVarAssign(self, ctx: CureParser.VarAssignContext) -> VarDecl:
        op: CommonToken | None = ctx.op
        return VarDecl(
            to_pos(ctx), ctx.ID().getText(), self.visitExpr(ctx.expr()),
            op.text if op is not None else None,
            self.visitType(ctx.type_()) if ctx.type_() is not None else None,
            ctx.CONST() is not None
        )
    
    def visitFuncModifications(self, ctx: CureParser.FuncModificationsContext) -> Call:
        return Call(to_pos(ctx), ctx.ID().getText(), self.visitArgs(ctx.args()))
    
    def visitFuncAssign(self, ctx: CureParser.FuncAssignContext) -> FuncDecl:
        return FuncDecl(
            to_pos(ctx), ctx.ID().getText(), self.visitBody(ctx.body()),
            self.visitParams(ctx.params()),
            self.visitType(ctx.type_()) if ctx.type_() is not None else None,
            [self.visitFuncModifications(mod) for mod in ctx.funcModifications()]
        )
    
    def visitParam(self, ctx: CureParser.ParamContext) -> ParamNode:
        return ParamNode(
            to_pos(ctx), ctx.ID().getText(), self.visitType(ctx.type_()),
            ctx.AMPERSAND() is not None
        )
    
    def visitParams(self, ctx: CureParser.ParamsContext) -> list[ParamNode]:
        return [self.visitParam(param) for param in ctx.param()] if ctx is not None else []
    
    def visitArg(self, ctx: CureParser.ArgContext) -> ArgNode:
        return ArgNode(to_pos(ctx), self.visitExpr(ctx.expr()))
    
    def visitArgs(self, ctx: CureParser.ArgsContext) -> list[ArgNode]:
        return [self.visitArg(arg) for arg in ctx.arg()] if ctx is not None else []
    
    def visitAtom(self, ctx: CureParser.AtomContext) -> Node:
        if ctx.INT() is not None or ctx.FLOAT() is not None or ctx.STRING() is not None\
            or ctx.BOOL() is not None or ctx.BIN() is not None or ctx.HEX() is not None:
            type = ''
            if ctx.INT() is not None:
                type = 'int'
            elif ctx.FLOAT() is not None:
                type = 'float'
            elif ctx.STRING() is not None:
                type = 'string'
                txt = ctx.getText()
                if len(txt) > 0 and txt[0] == '$':
                    nodes: list[Node] = []
                    
                    s = txt[2:-1]
                    i = 0
                    while i < len(s):
                        char = s[i]
                        if char == '{':
                            i += 1
                            expr = ''
                            while s[i] != '}':
                                expr += s[i]
                                i += 1
                            
                            nodes.append(*self.build(expr).nodes)
                        else:
                            nodes.append(Value(to_pos(ctx), char, 'string'))
                        
                        i += 1
                    
                    return DollarString(to_pos(ctx), nodes)
            elif ctx.BOOL() is not None:
                type = 'bool'
            elif ctx.BIN() is not None:
                type = 'bin'
            elif ctx.HEX() is not None:
                type = 'hex'
            
            return Value(to_pos(ctx), ctx.getText(), type)
        elif ctx.NIL() is not None:
            return Nil(to_pos(ctx))
        elif ctx.expr() is not None:
            return Brackets(to_pos(ctx), self.visitExpr(ctx.expr()))
        elif ctx.ID() is not None:
            return Identifier(to_pos(ctx), ctx.ID().getText())
        elif len(ctx.type_()) > 0:
            if len(ctx.dict_element()) > 0:
                return Dict(
                    to_pos(ctx), self.visitType(ctx.type_(0)), self.visitType(ctx.type_(1)),
                    {
                        self.visitExpr(element.expr(0)) : self.visitExpr(element.expr(1))
                        for element in ctx.dict_element()
                    }
                )
            else:
                return Array(
                    to_pos(ctx), self.visitType(ctx.type_(0)),
                    self.visitArgs(ctx.args())
                )
        else:
            to_pos(ctx).error_here('Invalid atom')
    
    def visitCall(self, ctx: CureParser.CallContext) -> Call:
        return Call(to_pos(ctx), ctx.ID().getText(), self.visitArgs(ctx.args()))
    
    def visitExpr(self, ctx: CureParser.ExprContext) -> Node:
        if ctx.atom() is not None:
            return self.visitAtom(ctx.atom())
        elif ctx.call() is not None:
            return self.visitCall(ctx.call())
        elif ctx.op is not None:
            return BinOp(
                to_pos(ctx), self.visitExpr(ctx.expr(0)), ctx.op.text,
                self.visitExpr(ctx.expr(1))
            )
        elif ctx.uop is not None:
            return UOp(to_pos(ctx), self.visitExpr(ctx.expr(0)), ctx.uop.text)
        elif ctx.DOT() is not None:
            args = None
            if ctx.LPAREN() is not None:
                args = self.visitArgs(ctx.args())
            return Attribute(
                to_pos(ctx), self.visitExpr(ctx.expr(0)), ctx.ID().getText(),
                args
            )
        elif ctx.NEW() is not None:
            return New(
                to_pos(ctx), Identifier(to_pos(ctx), ctx.ID().getText()),
                self.visitArgs(ctx.args())
            )
        elif ctx.IF() is not None:
            return Ternary(
                to_pos(ctx), self.visitExpr(ctx.expr(1)), self.visitExpr(ctx.expr(0)),
                self.visitExpr(ctx.expr(2))
            )
        elif ctx.LBRACK() is not None:
            return Index(to_pos(ctx), self.visitExpr(ctx.expr(0)), self.visitExpr(ctx.expr(1)))
        else:
            to_pos(ctx).error_here('Invalid expression')