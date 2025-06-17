# Generated from cure/parser/Cure.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .CureParser import CureParser
else:
    from CureParser import CureParser

# This class defines a complete listener for a parse tree produced by CureParser.
class CureListener(ParseTreeListener):

    # Enter a parse tree produced by CureParser#parse.
    def enterParse(self, ctx:CureParser.ParseContext):
        pass

    # Exit a parse tree produced by CureParser#parse.
    def exitParse(self, ctx:CureParser.ParseContext):
        pass


    # Enter a parse tree produced by CureParser#type.
    def enterType(self, ctx:CureParser.TypeContext):
        pass

    # Exit a parse tree produced by CureParser#type.
    def exitType(self, ctx:CureParser.TypeContext):
        pass


    # Enter a parse tree produced by CureParser#stmt.
    def enterStmt(self, ctx:CureParser.StmtContext):
        pass

    # Exit a parse tree produced by CureParser#stmt.
    def exitStmt(self, ctx:CureParser.StmtContext):
        pass


    # Enter a parse tree produced by CureParser#bodyStmts.
    def enterBodyStmts(self, ctx:CureParser.BodyStmtsContext):
        pass

    # Exit a parse tree produced by CureParser#bodyStmts.
    def exitBodyStmts(self, ctx:CureParser.BodyStmtsContext):
        pass


    # Enter a parse tree produced by CureParser#body.
    def enterBody(self, ctx:CureParser.BodyContext):
        pass

    # Exit a parse tree produced by CureParser#body.
    def exitBody(self, ctx:CureParser.BodyContext):
        pass


    # Enter a parse tree produced by CureParser#ifStmt.
    def enterIfStmt(self, ctx:CureParser.IfStmtContext):
        pass

    # Exit a parse tree produced by CureParser#ifStmt.
    def exitIfStmt(self, ctx:CureParser.IfStmtContext):
        pass


    # Enter a parse tree produced by CureParser#elseifStmt.
    def enterElseifStmt(self, ctx:CureParser.ElseifStmtContext):
        pass

    # Exit a parse tree produced by CureParser#elseifStmt.
    def exitElseifStmt(self, ctx:CureParser.ElseifStmtContext):
        pass


    # Enter a parse tree produced by CureParser#elseStmt.
    def enterElseStmt(self, ctx:CureParser.ElseStmtContext):
        pass

    # Exit a parse tree produced by CureParser#elseStmt.
    def exitElseStmt(self, ctx:CureParser.ElseStmtContext):
        pass


    # Enter a parse tree produced by CureParser#whileStmt.
    def enterWhileStmt(self, ctx:CureParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by CureParser#whileStmt.
    def exitWhileStmt(self, ctx:CureParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by CureParser#funcAssign.
    def enterFuncAssign(self, ctx:CureParser.FuncAssignContext):
        pass

    # Exit a parse tree produced by CureParser#funcAssign.
    def exitFuncAssign(self, ctx:CureParser.FuncAssignContext):
        pass


    # Enter a parse tree produced by CureParser#varAssign.
    def enterVarAssign(self, ctx:CureParser.VarAssignContext):
        pass

    # Exit a parse tree produced by CureParser#varAssign.
    def exitVarAssign(self, ctx:CureParser.VarAssignContext):
        pass


    # Enter a parse tree produced by CureParser#arg.
    def enterArg(self, ctx:CureParser.ArgContext):
        pass

    # Exit a parse tree produced by CureParser#arg.
    def exitArg(self, ctx:CureParser.ArgContext):
        pass


    # Enter a parse tree produced by CureParser#args.
    def enterArgs(self, ctx:CureParser.ArgsContext):
        pass

    # Exit a parse tree produced by CureParser#args.
    def exitArgs(self, ctx:CureParser.ArgsContext):
        pass


    # Enter a parse tree produced by CureParser#param.
    def enterParam(self, ctx:CureParser.ParamContext):
        pass

    # Exit a parse tree produced by CureParser#param.
    def exitParam(self, ctx:CureParser.ParamContext):
        pass


    # Enter a parse tree produced by CureParser#params.
    def enterParams(self, ctx:CureParser.ParamsContext):
        pass

    # Exit a parse tree produced by CureParser#params.
    def exitParams(self, ctx:CureParser.ParamsContext):
        pass


    # Enter a parse tree produced by CureParser#atom.
    def enterAtom(self, ctx:CureParser.AtomContext):
        pass

    # Exit a parse tree produced by CureParser#atom.
    def exitAtom(self, ctx:CureParser.AtomContext):
        pass


    # Enter a parse tree produced by CureParser#call.
    def enterCall(self, ctx:CureParser.CallContext):
        pass

    # Exit a parse tree produced by CureParser#call.
    def exitCall(self, ctx:CureParser.CallContext):
        pass


    # Enter a parse tree produced by CureParser#cast.
    def enterCast(self, ctx:CureParser.CastContext):
        pass

    # Exit a parse tree produced by CureParser#cast.
    def exitCast(self, ctx:CureParser.CastContext):
        pass


    # Enter a parse tree produced by CureParser#atom_expr.
    def enterAtom_expr(self, ctx:CureParser.Atom_exprContext):
        pass

    # Exit a parse tree produced by CureParser#atom_expr.
    def exitAtom_expr(self, ctx:CureParser.Atom_exprContext):
        pass


    # Enter a parse tree produced by CureParser#relational.
    def enterRelational(self, ctx:CureParser.RelationalContext):
        pass

    # Exit a parse tree produced by CureParser#relational.
    def exitRelational(self, ctx:CureParser.RelationalContext):
        pass


    # Enter a parse tree produced by CureParser#unary.
    def enterUnary(self, ctx:CureParser.UnaryContext):
        pass

    # Exit a parse tree produced by CureParser#unary.
    def exitUnary(self, ctx:CureParser.UnaryContext):
        pass


    # Enter a parse tree produced by CureParser#multiplication.
    def enterMultiplication(self, ctx:CureParser.MultiplicationContext):
        pass

    # Exit a parse tree produced by CureParser#multiplication.
    def exitMultiplication(self, ctx:CureParser.MultiplicationContext):
        pass


    # Enter a parse tree produced by CureParser#attr.
    def enterAttr(self, ctx:CureParser.AttrContext):
        pass

    # Exit a parse tree produced by CureParser#attr.
    def exitAttr(self, ctx:CureParser.AttrContext):
        pass


    # Enter a parse tree produced by CureParser#ternary.
    def enterTernary(self, ctx:CureParser.TernaryContext):
        pass

    # Exit a parse tree produced by CureParser#ternary.
    def exitTernary(self, ctx:CureParser.TernaryContext):
        pass


    # Enter a parse tree produced by CureParser#logical.
    def enterLogical(self, ctx:CureParser.LogicalContext):
        pass

    # Exit a parse tree produced by CureParser#logical.
    def exitLogical(self, ctx:CureParser.LogicalContext):
        pass


    # Enter a parse tree produced by CureParser#addition.
    def enterAddition(self, ctx:CureParser.AdditionContext):
        pass

    # Exit a parse tree produced by CureParser#addition.
    def exitAddition(self, ctx:CureParser.AdditionContext):
        pass



del CureParser