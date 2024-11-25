# Generated from ir/Cure.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .CureParser import CureParser
else:
    from CureParser import CureParser

# This class defines a complete generic visitor for a parse tree produced by CureParser.

class CureVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CureParser#parse.
    def visitParse(self, ctx:CureParser.ParseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#type.
    def visitType(self, ctx:CureParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#stmt.
    def visitStmt(self, ctx:CureParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#bodyStmts.
    def visitBodyStmts(self, ctx:CureParser.BodyStmtsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#body.
    def visitBody(self, ctx:CureParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#ifStmt.
    def visitIfStmt(self, ctx:CureParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#elseifStmt.
    def visitElseifStmt(self, ctx:CureParser.ElseifStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#elseStmt.
    def visitElseStmt(self, ctx:CureParser.ElseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#whileStmt.
    def visitWhileStmt(self, ctx:CureParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#rangeStmt.
    def visitRangeStmt(self, ctx:CureParser.RangeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#foreachStmt.
    def visitForeachStmt(self, ctx:CureParser.ForeachStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#useStmt.
    def visitUseStmt(self, ctx:CureParser.UseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#externStmt.
    def visitExternStmt(self, ctx:CureParser.ExternStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#methodName.
    def visitMethodName(self, ctx:CureParser.MethodNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#classProperty.
    def visitClassProperty(self, ctx:CureParser.ClassPropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#classMethod.
    def visitClassMethod(self, ctx:CureParser.ClassMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#classDeclarations.
    def visitClassDeclarations(self, ctx:CureParser.ClassDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#interfaceMethod.
    def visitInterfaceMethod(self, ctx:CureParser.InterfaceMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#interfaceDeclarations.
    def visitInterfaceDeclarations(self, ctx:CureParser.InterfaceDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#classAssign.
    def visitClassAssign(self, ctx:CureParser.ClassAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#interfaceAssign.
    def visitInterfaceAssign(self, ctx:CureParser.InterfaceAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#enumAssign.
    def visitEnumAssign(self, ctx:CureParser.EnumAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#funcModifications.
    def visitFuncModifications(self, ctx:CureParser.FuncModificationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#funcAssign.
    def visitFuncAssign(self, ctx:CureParser.FuncAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#varAssign.
    def visitVarAssign(self, ctx:CureParser.VarAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#testAssign.
    def visitTestAssign(self, ctx:CureParser.TestAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#arg.
    def visitArg(self, ctx:CureParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#args.
    def visitArgs(self, ctx:CureParser.ArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#param.
    def visitParam(self, ctx:CureParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#params.
    def visitParams(self, ctx:CureParser.ParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#dict_element.
    def visitDict_element(self, ctx:CureParser.Dict_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#genericArgs.
    def visitGenericArgs(self, ctx:CureParser.GenericArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#atom.
    def visitAtom(self, ctx:CureParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#new.
    def visitNew(self, ctx:CureParser.NewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#tuple_create.
    def visitTuple_create(self, ctx:CureParser.Tuple_createContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#index.
    def visitIndex(self, ctx:CureParser.IndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#unary.
    def visitUnary(self, ctx:CureParser.UnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#logical.
    def visitLogical(self, ctx:CureParser.LogicalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#call.
    def visitCall(self, ctx:CureParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#cast.
    def visitCast(self, ctx:CureParser.CastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#new_array.
    def visitNew_array(self, ctx:CureParser.New_arrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#atom_expr.
    def visitAtom_expr(self, ctx:CureParser.Atom_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#relational.
    def visitRelational(self, ctx:CureParser.RelationalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#multiplication.
    def visitMultiplication(self, ctx:CureParser.MultiplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#attr.
    def visitAttr(self, ctx:CureParser.AttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#ternary.
    def visitTernary(self, ctx:CureParser.TernaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#addition.
    def visitAddition(self, ctx:CureParser.AdditionContext):
        return self.visitChildren(ctx)



del CureParser