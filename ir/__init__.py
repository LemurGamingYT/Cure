from antlr4.error.ErrorListener import ErrorListener
from antlr4 import InputStream, CommonTokenStream
from antlr4.Token import CommonToken

from ir.parser.CureVisitor import CureVisitor
from ir.parser.CureParser import CureParser
from ir.parser.CureLexer import CureLexer
from ir.nodes import (
    Program, Body, TypeNode, ParamNode, ArgNode, Call, Return, Foreach, While,
    If, Use, VarDecl, Value, Identifier, Array, Dict, Brackets, BinOp, UOp, Attribute, New,
    Ternary, Position, Node, Break, Continue, FuncDecl, Nil, Index, DollarString, Cast, Enum,
    ClassProperty, ClassMethod, Class, AttrAssign, CreateTuple, RangeFor, Extern, Test, FuncType
)


op_map = {
    '+': 'add', '-': 'sub', '*': 'mul', '/': 'div', '%': 'mod', '==': 'eq', '!=': 'neq',
    '<': 'lt', '>': 'gt', '<=': 'lte', '>=': 'gte', '&&': 'and', '||': 'or', '!': 'not'
}


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
        if ctx.LPAREN() is not None:
            types = [self.visitType(t) for t in ctx.type_()]
            node = TypeNode(pos, 'tuple', tuple_types=types)
            if ctx.RETURNS() is not None:
                param_types = [self.visitType(param) for param in ctx.type_()[1:]]
                return_type = self.visitType(ctx.type_()[-1])
                return TypeNode(pos, 'function', func_type=FuncType(pos, return_type, param_types))
        else:
            name = ctx.ID().getText()
            if len(ctx.type_()) == 0:
                node = TypeNode(pos, name)
            elif len(ctx.type_()) == 1:
                node = TypeNode(pos, name, self.visitType(ctx.type_(0)))
            elif len(ctx.type_()) == 2:
                node = TypeNode(
                    pos, name, None,
                    (self.visitType(ctx.type_(0)), self.visitType(ctx.type_(1)))
                )
            else:
                pos.error_here(f'Invalid type \'{ctx.getText()}\'')
        
        if ctx.QUESTION() is not None:
            node.is_optional = True
        
        return node
    
    def visitUseStmt(self, ctx: CureParser.UseStmtContext) -> Use:
        pos = to_pos(ctx)
        if ctx.STRING().getText().startswith('$'):
            pos.error_here('Cannot use string concatenation in use statement')
        
        return Use(pos, ctx.STRING().getText()[1:-1])
    
    def visitIfStmt(self, ctx: CureParser.IfStmtContext) -> If:
        cond = self.visit(ctx.expr())
        body = self.visitBody(ctx.body())
        else_body = self.visitBody(ctx.elseStmt().body()) if ctx.elseStmt() is not None else None
        elseifs = []
        for elseif in ctx.elseifStmt():
            elseifs.append((self.visit(elseif.expr()), self.visitBody(elseif.body())))
        
        return If(to_pos(ctx), cond, body, else_body, elseifs)
    
    def visitWhileStmt(self, ctx: CureParser.WhileStmtContext) -> While:
        return While(to_pos(ctx), self.visit(ctx.expr()), self.visitBody(ctx.body()))

    def visitForeachStmt(self, ctx: CureParser.ForeachStmtContext) -> Foreach:
        return Foreach(
            to_pos(ctx), ctx.ID().getText(), self.visit(ctx.expr()),
            self.visitBody(ctx.body())
        )
    
    def visitRangeStmt(self, ctx: CureParser.RangeStmtContext) -> RangeFor:
        return RangeFor(
            to_pos(ctx), ctx.ID().getText(), self.visit(ctx.expr(0)), self.visit(ctx.expr(1)),
            self.visitBody(ctx.body())
        )
    
    def visitExternStmt(self, ctx: CureParser.ExternStmtContext) -> Extern:
        return Extern(to_pos(ctx), ctx.STRING().getText()[1:-1])
    
    def visitBodyStmts(self, ctx: CureParser.BodyStmtsContext) -> Node:
        if ctx.stmt() is not None:
            return self.visitStmt(ctx.stmt())
        elif ctx.RETURN() is not None:
            return Return(to_pos(ctx), self.visit(ctx.expr()))
        elif ctx.BREAK() is not None:
            return Break(to_pos(ctx))
        elif ctx.CONTINUE() is not None:
            return Continue(to_pos(ctx))
        else:
            to_pos(ctx).error_here('Invalid statement')
    
    def visitBody(self, ctx: CureParser.BodyContext) -> Body:
        return Body(to_pos(ctx), [self.visitBodyStmts(stmt) for stmt in ctx.bodyStmts()])
    
    def visitEnumAssign(self, ctx: CureParser.EnumAssignContext) -> Enum:
        return Enum(
            to_pos(ctx), Identifier(to_pos(ctx.ID(0)), ctx.ID(0).getText()),
            [Identifier(to_pos(i), i.getText()) for i in ctx.ID()[1:]]
        )
    
    def visitVarAssign(self, ctx: CureParser.VarAssignContext) -> VarDecl | AttrAssign:
        op: CommonToken | None = ctx.op
        pos = to_pos(ctx)
        if ctx.DOT() is not None:
            return AttrAssign(
                pos, Identifier(pos, ctx.ID(0).getText()), [ctx.ID(1).getText()],
                self.visit(ctx.expr()), op.text if op is not None else None
            )
        
        return VarDecl(
            pos, ctx.ID(0).getText(), self.visit(ctx.expr()),
            op.text if op is not None else None,
            self.visitType(ctx.type_()) if ctx.type_() is not None else None,
            ctx.CONST() is not None
        )
    
    def visitFuncModifications(self, ctx: CureParser.FuncModificationsContext) -> Call:
        return Call(
            to_pos(ctx), Identifier(to_pos(ctx), ctx.ID().getText()),
            self.visitArgs(ctx.args())
        )
    
    def visitFuncAssign(self, ctx: CureParser.FuncAssignContext) -> FuncDecl:
        returns = None
        if len(ctx.type_()) == 2:
            returns = self.visitType(ctx.type_(1))
        elif len(ctx.type_()) == 1:
            returns = self.visitType(ctx.type_(0))
        
        return FuncDecl(
            to_pos(ctx), ctx.ID(0).getText(), self.visitBody(ctx.body()),
            self.visitParams(ctx.params()),
            returns,
            [self.visitFuncModifications(mod) for mod in ctx.funcModifications()],
            [t.getText() for t in ctx.ID()[1:]],
            self.visitType(ctx.type_(0)) if len(ctx.type_()) == 2 else None
        )
    
    def visitClassProperty(self, ctx: CureParser.ClassPropertyContext) -> ClassProperty:
        return ClassProperty(
            to_pos(ctx), ctx.ID().getText(),
            self.visitType(ctx.type_()),
            self.visit(ctx.expr()) if ctx.expr() is not None else None,
            ctx.PRIVATE() is None
        )
    
    def visitMethodName(self, ctx: CureParser.MethodNameContext) -> str:
        if ctx.opname is not None:
            return ctx.opname.text

        ident = ctx.ID().getText()
        if ctx.TILDE() is not None:
            return '~' + ident
        
        return ident
    
    def visitClassMethod(self, ctx: CureParser.ClassMethodContext) -> ClassMethod:
        pos = to_pos(ctx)
        name = self.visitMethodName(ctx.methodName())
        return ClassMethod(
            pos, name, self.visitBody(ctx.body()),
            self.visitParams(ctx.params()) if ctx.params() is not None else [],
            self.visitType(ctx.type_()) if ctx.type_() is not None else None,
            [], [], None,
            ctx.PRIVATE() is None, ctx.STATIC() is not None, ctx.OVERRIDE() is not None
        )
    
    def visitClassDeclarations(self, ctx: CureParser.ClassDeclarationsContext | None)\
        -> list[ClassMethod | ClassProperty]:
        if ctx is None:
            return []
        
        methods = [self.visitClassMethod(func) for func in ctx.classMethod()]
        properties = [self.visitClassProperty(prop) for prop in ctx.classProperty()]
        return methods + properties
    
    def visitClassAssign(self, ctx: CureParser.ClassAssignContext) -> Class:
        return Class(
            to_pos(ctx), ctx.ID(0).getText(),
            self.visitClassDeclarations(ctx.classDeclarations()),
            [ident.getText() for ident in ctx.ID()[1:]]
        )
    
    def visitTestAssign(self, ctx: CureParser.TestAssignContext) -> Test:
        return Test(to_pos(ctx), ctx.ID().getText(), self.visitBody(ctx.body()))
    
    def visitParam(self, ctx: CureParser.ParamContext) -> ParamNode:
        return ParamNode(
            to_pos(ctx), ctx.ID().getText(), self.visitType(ctx.type_()),
            ctx.AMPERSAND() is not None, self.visit(ctx.expr()) if ctx.expr() is not None else None
        )
    
    def visitParams(self, ctx: CureParser.ParamsContext) -> list[ParamNode]:
        return [self.visitParam(param) for param in ctx.param()] if ctx is not None else []
    
    def visitArg(self, ctx: CureParser.ArgContext) -> ArgNode:
        return ArgNode(
            to_pos(ctx), self.visit(ctx.expr()),
            ctx.ID().getText() if ctx.ID() is not None else None
        )
    
    def visitArgs(self, ctx: CureParser.ArgsContext) -> list[ArgNode]:
        return [self.visitArg(arg) for arg in ctx.arg()] if ctx is not None else []

    def visitAtom(self, ctx: CureParser.AtomContext) -> Node:
        if ctx.INT() is not None:
            return Value(to_pos(ctx), ctx.getText(), 'int')
        elif ctx.FLOAT() is not None:
            return Value(to_pos(ctx), ctx.getText() + 'f', 'float')
        elif ctx.STRING() is not None:
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
            
            return Value(to_pos(ctx), ctx.getText(), 'string')
        elif ctx.BOOL() is not None:
            return Value(to_pos(ctx), ctx.getText(), 'bool')
        elif ctx.NIL() is not None:
            return Nil(to_pos(ctx))
        elif ctx.expr() is not None:
            return Brackets(to_pos(ctx), self.visit(ctx.expr()))
        elif ctx.ID() is not None:
            return Identifier(to_pos(ctx), ctx.ID().getText())
        elif ctx.LBRACE() is not None:
            if len(ctx.dict_element()) > 0 or len(ctx.type_()) == 2:
                return Dict(
                    to_pos(ctx),
                    self.visitType(ctx.type_(0)) if ctx.type_(0) is not None else None,
                    self.visitType(ctx.type_(1)) if ctx.type_(1) is not None else None,
                    {
                        self.visit(element.expr(0)) : self.visit(element.expr(1))
                        for element in ctx.dict_element()
                    }
                )
            elif len(ctx.dict_element()) == 0 and len(ctx.type_()) in {0, 1}:
                return Array(
                    to_pos(ctx), self.visitType(ctx.type_(0)) if ctx.type_(0) is not None else None,
                    self.visitArgs(ctx.args())
                )
        
        to_pos(ctx).error_here('Invalid atom')
    
    def visitGenericArgs(self, ctx: CureParser.GenericArgsContext) -> list[TypeNode]:
        return [self.visitType(t) for t in ctx.type_()]

    def visitCall(self, ctx: CureParser.CallContext) -> Call:
        return Call(
            to_pos(ctx), self.visit(ctx.expr()), self.visitArgs(ctx.args()),
            self.visitGenericArgs(ctx.genericArgs()) if ctx.genericArgs() is not None else []
        )
    
    def visitCast(self, ctx: CureParser.CastContext) -> Cast:
        return Cast(to_pos(ctx), self.visit(ctx.expr()), self.visitType(ctx.type_()))
    
    def visitAttr(self, ctx: CureParser.AttrContext) -> Attribute:
        args = None
        if ctx.LPAREN() is not None:
            args = self.visitArgs(ctx.args())
        
        return Attribute(
            to_pos(ctx), self.visit(ctx.expr()), ctx.ID().getText(),
            args, self.visitGenericArgs(ctx.genericArgs()) if ctx.genericArgs() is not None else []
        )
    
    def visitTernary(self, ctx: CureParser.TernaryContext) -> Ternary:
        return Ternary(
            to_pos(ctx), self.visit(ctx.expr(1)), self.visit(ctx.expr(0)),
            self.visit(ctx.expr(2))
        )
    
    def visitTuple_create(self, ctx: CureParser.Tuple_createContext) -> CreateTuple:
        return CreateTuple(to_pos(ctx), [self.visit(expr) for expr in ctx.expr()])

    def visitNew(self, ctx: CureParser.NewContext) -> New:
        return New(
            to_pos(ctx), Identifier(to_pos(ctx), ctx.ID().getText()),
            self.visitArgs(ctx.args())
        )
    
    def visitIndex(self, ctx: CureParser.IndexContext) -> Index:
        return Index(to_pos(ctx), self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))
    
    def binop(self, ctx) -> BinOp:
        return BinOp(
            to_pos(ctx), self.visit(ctx.expr(0)), ctx.op.text,
            self.visit(ctx.expr(1))
        )
    
    def visitMultiplication(self, ctx: CureParser.MultiplicationContext) -> BinOp:
        return self.binop(ctx)
    
    def visitAddition(self, ctx: CureParser.AdditionContext) -> BinOp:
        return self.binop(ctx)
    
    def visitRelational(self, ctx: CureParser.RelationalContext) -> BinOp:
        return self.binop(ctx)
    
    def visitLogical(self, ctx: CureParser.LogicalContext):
        return self.binop(ctx)
    
    def visitUnary(self, ctx: CureParser.UnaryContext) -> UOp:
        pos = to_pos(ctx)
        if ctx.uop is None:
            pos.error_here('Unary operator is missing')
        
        return UOp(pos, self.visit(ctx.expr()), ctx.uop.text)
