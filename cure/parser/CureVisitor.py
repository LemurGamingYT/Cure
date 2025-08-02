# Generated from cure/Cure.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .CureParser import CureParser
else:
    from CureParser import CureParser

# This class defines a complete generic visitor for a parse tree produced by CureParser.

class CureVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CureParser#program.
    def visitProgram(self, ctx:CureParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#type.
    def visitType(self, ctx:CureParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#stmt.
    def visitStmt(self, ctx:CureParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#stmtBody.
    def visitStmtBody(self, ctx:CureParser.StmtBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#return.
    def visitReturn(self, ctx:CureParser.ReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#break.
    def visitBreak(self, ctx:CureParser.BreakContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#continue.
    def visitContinue(self, ctx:CureParser.ContinueContext):
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


    # Visit a parse tree produced by CureParser#forRangeStmt.
    def visitForRangeStmt(self, ctx:CureParser.ForRangeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#useStmt.
    def visitUseStmt(self, ctx:CureParser.UseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#externFunc.
    def visitExternFunc(self, ctx:CureParser.ExternFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#externClass.
    def visitExternClass(self, ctx:CureParser.ExternClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#externStmt.
    def visitExternStmt(self, ctx:CureParser.ExternStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#funcName.
    def visitFuncName(self, ctx:CureParser.FuncNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#functionSignature.
    def visitFunctionSignature(self, ctx:CureParser.FunctionSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#funcAssign.
    def visitFuncAssign(self, ctx:CureParser.FuncAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#varAssign.
    def visitVarAssign(self, ctx:CureParser.VarAssignContext):
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


    # Visit a parse tree produced by CureParser#genericParam.
    def visitGenericParam(self, ctx:CureParser.GenericParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#genericParams.
    def visitGenericParams(self, ctx:CureParser.GenericParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#new.
    def visitNew(self, ctx:CureParser.NewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#string.
    def visitString(self, ctx:CureParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#bool.
    def visitBool(self, ctx:CureParser.BoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#arrayInit.
    def visitArrayInit(self, ctx:CureParser.ArrayInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#newArray.
    def visitNewArray(self, ctx:CureParser.NewArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#unary.
    def visitUnary(self, ctx:CureParser.UnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#float.
    def visitFloat(self, ctx:CureParser.FloatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#int.
    def visitInt(self, ctx:CureParser.IntContext):
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


    # Visit a parse tree produced by CureParser#paren.
    def visitParen(self, ctx:CureParser.ParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#relational.
    def visitRelational(self, ctx:CureParser.RelationalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CureParser#id.
    def visitId(self, ctx:CureParser.IdContext):
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