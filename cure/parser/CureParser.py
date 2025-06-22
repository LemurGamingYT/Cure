# Generated from cure/parser/Cure.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,45,202,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,1,0,5,0,36,8,0,10,0,12,0,39,9,0,1,
        0,1,0,1,1,1,1,1,2,1,2,1,2,1,2,1,2,3,2,50,8,2,1,3,1,3,1,3,1,3,1,3,
        3,3,57,8,3,1,4,1,4,5,4,61,8,4,10,4,12,4,64,9,4,1,4,1,4,1,5,1,5,1,
        5,1,5,5,5,72,8,5,10,5,12,5,75,9,5,1,5,3,5,78,8,5,1,6,1,6,1,6,1,6,
        1,6,1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,3,9,96,8,9,1,9,1,
        9,1,9,3,9,101,8,9,1,9,1,9,1,10,3,10,106,8,10,1,10,1,10,1,10,1,10,
        1,10,3,10,113,8,10,1,10,1,10,3,10,117,8,10,1,11,1,11,1,12,1,12,1,
        12,5,12,124,8,12,10,12,12,12,127,9,12,1,13,1,13,1,13,1,14,1,14,1,
        14,5,14,135,8,14,10,14,12,14,138,9,14,1,15,1,15,1,15,1,15,1,15,1,
        15,1,15,1,15,1,15,1,15,3,15,150,8,15,1,16,1,16,1,16,1,16,1,16,1,
        16,1,16,1,16,1,16,3,16,161,8,16,1,16,1,16,1,16,1,16,1,16,1,16,1,
        16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,
        16,1,16,3,16,184,8,16,1,16,1,16,1,16,1,16,1,16,1,16,3,16,192,8,16,
        1,16,3,16,195,8,16,5,16,197,8,16,10,16,12,16,200,9,16,1,16,0,1,32,
        17,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,0,6,1,0,17,21,2,
        0,17,18,30,30,1,0,19,21,1,0,17,18,1,0,22,27,1,0,28,29,220,0,37,1,
        0,0,0,2,42,1,0,0,0,4,49,1,0,0,0,6,56,1,0,0,0,8,58,1,0,0,0,10,67,
        1,0,0,0,12,79,1,0,0,0,14,84,1,0,0,0,16,87,1,0,0,0,18,91,1,0,0,0,
        20,116,1,0,0,0,22,118,1,0,0,0,24,120,1,0,0,0,26,128,1,0,0,0,28,131,
        1,0,0,0,30,149,1,0,0,0,32,160,1,0,0,0,34,36,3,4,2,0,35,34,1,0,0,
        0,36,39,1,0,0,0,37,35,1,0,0,0,37,38,1,0,0,0,38,40,1,0,0,0,39,37,
        1,0,0,0,40,41,5,0,0,1,41,1,1,0,0,0,42,43,5,16,0,0,43,3,1,0,0,0,44,
        50,3,20,10,0,45,50,3,18,9,0,46,50,3,16,8,0,47,50,3,10,5,0,48,50,
        3,32,16,0,49,44,1,0,0,0,49,45,1,0,0,0,49,46,1,0,0,0,49,47,1,0,0,
        0,49,48,1,0,0,0,50,5,1,0,0,0,51,57,3,4,2,0,52,53,5,6,0,0,53,57,3,
        32,16,0,54,57,5,9,0,0,55,57,5,8,0,0,56,51,1,0,0,0,56,52,1,0,0,0,
        56,54,1,0,0,0,56,55,1,0,0,0,57,7,1,0,0,0,58,62,5,36,0,0,59,61,3,
        6,3,0,60,59,1,0,0,0,61,64,1,0,0,0,62,60,1,0,0,0,62,63,1,0,0,0,63,
        65,1,0,0,0,64,62,1,0,0,0,65,66,5,37,0,0,66,9,1,0,0,0,67,68,5,1,0,
        0,68,69,3,32,16,0,69,73,3,8,4,0,70,72,3,12,6,0,71,70,1,0,0,0,72,
        75,1,0,0,0,73,71,1,0,0,0,73,74,1,0,0,0,74,77,1,0,0,0,75,73,1,0,0,
        0,76,78,3,14,7,0,77,76,1,0,0,0,77,78,1,0,0,0,78,11,1,0,0,0,79,80,
        5,4,0,0,80,81,5,1,0,0,81,82,3,32,16,0,82,83,3,8,4,0,83,13,1,0,0,
        0,84,85,5,4,0,0,85,86,3,8,4,0,86,15,1,0,0,0,87,88,5,7,0,0,88,89,
        3,32,16,0,89,90,3,8,4,0,90,17,1,0,0,0,91,92,5,3,0,0,92,93,5,16,0,
        0,93,95,5,34,0,0,94,96,3,28,14,0,95,94,1,0,0,0,95,96,1,0,0,0,96,
        97,1,0,0,0,97,100,5,35,0,0,98,99,5,41,0,0,99,101,3,2,1,0,100,98,
        1,0,0,0,100,101,1,0,0,0,101,102,1,0,0,0,102,103,3,8,4,0,103,19,1,
        0,0,0,104,106,5,5,0,0,105,104,1,0,0,0,105,106,1,0,0,0,106,107,1,
        0,0,0,107,108,5,16,0,0,108,109,5,33,0,0,109,117,3,32,16,0,110,112,
        5,16,0,0,111,113,7,0,0,0,112,111,1,0,0,0,112,113,1,0,0,0,113,114,
        1,0,0,0,114,115,5,33,0,0,115,117,3,32,16,0,116,105,1,0,0,0,116,110,
        1,0,0,0,117,21,1,0,0,0,118,119,3,32,16,0,119,23,1,0,0,0,120,125,
        3,22,11,0,121,122,5,32,0,0,122,124,3,22,11,0,123,121,1,0,0,0,124,
        127,1,0,0,0,125,123,1,0,0,0,125,126,1,0,0,0,126,25,1,0,0,0,127,125,
        1,0,0,0,128,129,3,2,1,0,129,130,5,16,0,0,130,27,1,0,0,0,131,136,
        3,26,13,0,132,133,5,32,0,0,133,135,3,26,13,0,134,132,1,0,0,0,135,
        138,1,0,0,0,136,134,1,0,0,0,136,137,1,0,0,0,137,29,1,0,0,0,138,136,
        1,0,0,0,139,150,5,11,0,0,140,150,5,12,0,0,141,150,5,13,0,0,142,150,
        5,14,0,0,143,150,5,15,0,0,144,150,5,16,0,0,145,146,5,34,0,0,146,
        147,3,32,16,0,147,148,5,35,0,0,148,150,1,0,0,0,149,139,1,0,0,0,149,
        140,1,0,0,0,149,141,1,0,0,0,149,142,1,0,0,0,149,143,1,0,0,0,149,
        144,1,0,0,0,149,145,1,0,0,0,150,31,1,0,0,0,151,152,6,16,-1,0,152,
        153,5,34,0,0,153,154,3,2,1,0,154,155,5,35,0,0,155,156,3,32,16,10,
        156,161,1,0,0,0,157,161,3,30,15,0,158,159,7,1,0,0,159,161,3,32,16,
        1,160,151,1,0,0,0,160,157,1,0,0,0,160,158,1,0,0,0,161,198,1,0,0,
        0,162,163,10,6,0,0,163,164,5,1,0,0,164,165,3,32,16,0,165,166,5,4,
        0,0,166,167,3,32,16,7,167,197,1,0,0,0,168,169,10,5,0,0,169,170,7,
        2,0,0,170,197,3,32,16,6,171,172,10,4,0,0,172,173,7,3,0,0,173,197,
        3,32,16,5,174,175,10,3,0,0,175,176,7,4,0,0,176,197,3,32,16,4,177,
        178,10,2,0,0,178,179,7,5,0,0,179,197,3,32,16,3,180,181,10,8,0,0,
        181,183,5,34,0,0,182,184,3,24,12,0,183,182,1,0,0,0,183,184,1,0,0,
        0,184,185,1,0,0,0,185,197,5,35,0,0,186,187,10,7,0,0,187,188,5,31,
        0,0,188,194,5,16,0,0,189,191,5,34,0,0,190,192,3,24,12,0,191,190,
        1,0,0,0,191,192,1,0,0,0,192,193,1,0,0,0,193,195,5,35,0,0,194,189,
        1,0,0,0,194,195,1,0,0,0,195,197,1,0,0,0,196,162,1,0,0,0,196,168,
        1,0,0,0,196,171,1,0,0,0,196,174,1,0,0,0,196,177,1,0,0,0,196,180,
        1,0,0,0,196,186,1,0,0,0,197,200,1,0,0,0,198,196,1,0,0,0,198,199,
        1,0,0,0,199,33,1,0,0,0,200,198,1,0,0,0,20,37,49,56,62,73,77,95,100,
        105,112,116,125,136,149,160,183,191,194,196,198
    ]

class CureParser ( Parser ):

    grammarFileName = "Cure.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'new'", "'fn'", "'else'", "'const'", 
                     "'return'", "'while'", "'break'", "'continue'", "'''", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'nil'", "<INVALID>", "'+'", "'-'", "'*'", "'/'", "'%'", 
                     "'=='", "'!='", "'>'", "'<'", "'>='", "'<='", "'&&'", 
                     "'||'", "'!'", "'.'", "','", "'='", "'('", "')'", "'{'", 
                     "'}'", "'['", "']'", "'<-'", "'->'" ]

    symbolicNames = [ "<INVALID>", "IF", "NEW", "FUNC", "ELSE", "CONST", 
                      "RETURN", "WHILE", "BREAK", "CONTINUE", "APOSTROPHE", 
                      "INT", "FLOAT", "STRING", "BOOL", "NIL", "ID", "ADD", 
                      "SUB", "MUL", "DIV", "MOD", "EEQ", "NEQ", "GT", "LT", 
                      "GTE", "LTE", "AND", "OR", "NOT", "DOT", "COMMA", 
                      "ASSIGN", "LPAREN", "RPAREN", "LBRACE", "RBRACE", 
                      "LBRACK", "RBRACK", "RARROW", "RETURNS", "COMMENT", 
                      "MULTILINE_COMMENT", "WHITESPACE", "OTHER" ]

    RULE_parse = 0
    RULE_type = 1
    RULE_stmt = 2
    RULE_bodyStmts = 3
    RULE_body = 4
    RULE_ifStmt = 5
    RULE_elseifStmt = 6
    RULE_elseStmt = 7
    RULE_whileStmt = 8
    RULE_funcAssign = 9
    RULE_varAssign = 10
    RULE_arg = 11
    RULE_args = 12
    RULE_param = 13
    RULE_params = 14
    RULE_atom = 15
    RULE_expr = 16

    ruleNames =  [ "parse", "type", "stmt", "bodyStmts", "body", "ifStmt", 
                   "elseifStmt", "elseStmt", "whileStmt", "funcAssign", 
                   "varAssign", "arg", "args", "param", "params", "atom", 
                   "expr" ]

    EOF = Token.EOF
    IF=1
    NEW=2
    FUNC=3
    ELSE=4
    CONST=5
    RETURN=6
    WHILE=7
    BREAK=8
    CONTINUE=9
    APOSTROPHE=10
    INT=11
    FLOAT=12
    STRING=13
    BOOL=14
    NIL=15
    ID=16
    ADD=17
    SUB=18
    MUL=19
    DIV=20
    MOD=21
    EEQ=22
    NEQ=23
    GT=24
    LT=25
    GTE=26
    LTE=27
    AND=28
    OR=29
    NOT=30
    DOT=31
    COMMA=32
    ASSIGN=33
    LPAREN=34
    RPAREN=35
    LBRACE=36
    RBRACE=37
    LBRACK=38
    RBRACK=39
    RARROW=40
    RETURNS=41
    COMMENT=42
    MULTILINE_COMMENT=43
    WHITESPACE=44
    OTHER=45

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ParseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(CureParser.EOF, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.StmtContext)
            else:
                return self.getTypedRuleContext(CureParser.StmtContext,i)


        def getRuleIndex(self):
            return CureParser.RULE_parse

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse" ):
                return visitor.visitParse(self)
            else:
                return visitor.visitChildren(self)




    def parse(self):

        localctx = CureParser.ParseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_parse)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 18254133418) != 0):
                self.state = 34
                self.stmt()
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 40
            self.match(CureParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def getRuleIndex(self):
            return CureParser.RULE_type

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)




    def type_(self):

        localctx = CureParser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.match(CureParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varAssign(self):
            return self.getTypedRuleContext(CureParser.VarAssignContext,0)


        def funcAssign(self):
            return self.getTypedRuleContext(CureParser.FuncAssignContext,0)


        def whileStmt(self):
            return self.getTypedRuleContext(CureParser.WhileStmtContext,0)


        def ifStmt(self):
            return self.getTypedRuleContext(CureParser.IfStmtContext,0)


        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = CureParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_stmt)
        try:
            self.state = 49
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 44
                self.varAssign()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 45
                self.funcAssign()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 46
                self.whileStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 47
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 48
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyStmtsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmt(self):
            return self.getTypedRuleContext(CureParser.StmtContext,0)


        def RETURN(self):
            return self.getToken(CureParser.RETURN, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def CONTINUE(self):
            return self.getToken(CureParser.CONTINUE, 0)

        def BREAK(self):
            return self.getToken(CureParser.BREAK, 0)

        def getRuleIndex(self):
            return CureParser.RULE_bodyStmts

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBodyStmts" ):
                return visitor.visitBodyStmts(self)
            else:
                return visitor.visitChildren(self)




    def bodyStmts(self):

        localctx = CureParser.BodyStmtsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_bodyStmts)
        try:
            self.state = 56
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 3, 5, 7, 11, 12, 13, 14, 15, 16, 17, 18, 30, 34]:
                self.enterOuterAlt(localctx, 1)
                self.state = 51
                self.stmt()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 52
                self.match(CureParser.RETURN)
                self.state = 53
                self.expr(0)
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 3)
                self.state = 54
                self.match(CureParser.CONTINUE)
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 4)
                self.state = 55
                self.match(CureParser.BREAK)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(CureParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(CureParser.RBRACE, 0)

        def bodyStmts(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.BodyStmtsContext)
            else:
                return self.getTypedRuleContext(CureParser.BodyStmtsContext,i)


        def getRuleIndex(self):
            return CureParser.RULE_body

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBody" ):
                return visitor.visitBody(self)
            else:
                return visitor.visitChildren(self)




    def body(self):

        localctx = CureParser.BodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_body)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.match(CureParser.LBRACE)
            self.state = 62
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 18254134250) != 0):
                self.state = 59
                self.bodyStmts()
                self.state = 64
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 65
            self.match(CureParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(CureParser.IF, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def elseifStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ElseifStmtContext)
            else:
                return self.getTypedRuleContext(CureParser.ElseifStmtContext,i)


        def elseStmt(self):
            return self.getTypedRuleContext(CureParser.ElseStmtContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_ifStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = CureParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            self.match(CureParser.IF)
            self.state = 68
            self.expr(0)
            self.state = 69
            self.body()
            self.state = 73
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 70
                    self.elseifStmt() 
                self.state = 75
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

            self.state = 77
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 76
                self.elseStmt()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElseifStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ELSE(self):
            return self.getToken(CureParser.ELSE, 0)

        def IF(self):
            return self.getToken(CureParser.IF, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_elseifStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElseifStmt" ):
                return visitor.visitElseifStmt(self)
            else:
                return visitor.visitChildren(self)




    def elseifStmt(self):

        localctx = CureParser.ElseifStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_elseifStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            self.match(CureParser.ELSE)
            self.state = 80
            self.match(CureParser.IF)
            self.state = 81
            self.expr(0)
            self.state = 82
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElseStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ELSE(self):
            return self.getToken(CureParser.ELSE, 0)

        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_elseStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElseStmt" ):
                return visitor.visitElseStmt(self)
            else:
                return visitor.visitChildren(self)




    def elseStmt(self):

        localctx = CureParser.ElseStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_elseStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 84
            self.match(CureParser.ELSE)
            self.state = 85
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(CureParser.WHILE, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_whileStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStmt" ):
                return visitor.visitWhileStmt(self)
            else:
                return visitor.visitChildren(self)




    def whileStmt(self):

        localctx = CureParser.WhileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_whileStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            self.match(CureParser.WHILE)
            self.state = 88
            self.expr(0)
            self.state = 89
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncAssignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNC(self):
            return self.getToken(CureParser.FUNC, 0)

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)

        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def params(self):
            return self.getTypedRuleContext(CureParser.ParamsContext,0)


        def RETURNS(self):
            return self.getToken(CureParser.RETURNS, 0)

        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_funcAssign

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncAssign" ):
                return visitor.visitFuncAssign(self)
            else:
                return visitor.visitChildren(self)




    def funcAssign(self):

        localctx = CureParser.FuncAssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_funcAssign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            self.match(CureParser.FUNC)
            self.state = 92
            self.match(CureParser.ID)
            self.state = 93
            self.match(CureParser.LPAREN)
            self.state = 95
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16:
                self.state = 94
                self.params()


            self.state = 97
            self.match(CureParser.RPAREN)
            self.state = 100
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==41:
                self.state = 98
                self.match(CureParser.RETURNS)
                self.state = 99
                self.type_()


            self.state = 102
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarAssignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.op = None # Token

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(CureParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def CONST(self):
            return self.getToken(CureParser.CONST, 0)

        def ADD(self):
            return self.getToken(CureParser.ADD, 0)

        def SUB(self):
            return self.getToken(CureParser.SUB, 0)

        def MUL(self):
            return self.getToken(CureParser.MUL, 0)

        def DIV(self):
            return self.getToken(CureParser.DIV, 0)

        def MOD(self):
            return self.getToken(CureParser.MOD, 0)

        def getRuleIndex(self):
            return CureParser.RULE_varAssign

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarAssign" ):
                return visitor.visitVarAssign(self)
            else:
                return visitor.visitChildren(self)




    def varAssign(self):

        localctx = CureParser.VarAssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_varAssign)
        self._la = 0 # Token type
        try:
            self.state = 116
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 105
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==5:
                    self.state = 104
                    self.match(CureParser.CONST)


                self.state = 107
                self.match(CureParser.ID)
                self.state = 108
                self.match(CureParser.ASSIGN)
                self.state = 109
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 110
                self.match(CureParser.ID)
                self.state = 112
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 4063232) != 0):
                    self.state = 111
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4063232) != 0)):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 114
                self.match(CureParser.ASSIGN)
                self.state = 115
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_arg

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArg" ):
                return visitor.visitArg(self)
            else:
                return visitor.visitChildren(self)




    def arg(self):

        localctx = CureParser.ArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ArgContext)
            else:
                return self.getTypedRuleContext(CureParser.ArgContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CureParser.COMMA)
            else:
                return self.getToken(CureParser.COMMA, i)

        def getRuleIndex(self):
            return CureParser.RULE_args

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgs" ):
                return visitor.visitArgs(self)
            else:
                return visitor.visitChildren(self)




    def args(self):

        localctx = CureParser.ArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 120
            self.arg()
            self.state = 125
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 121
                self.match(CureParser.COMMA)
                self.state = 122
                self.arg()
                self.state = 127
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def getRuleIndex(self):
            return CureParser.RULE_param

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = CureParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_param)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 128
            self.type_()
            self.state = 129
            self.match(CureParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ParamContext)
            else:
                return self.getTypedRuleContext(CureParser.ParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CureParser.COMMA)
            else:
                return self.getToken(CureParser.COMMA, i)

        def getRuleIndex(self):
            return CureParser.RULE_params

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParams" ):
                return visitor.visitParams(self)
            else:
                return visitor.visitChildren(self)




    def params(self):

        localctx = CureParser.ParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self.param()
            self.state = 136
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 132
                self.match(CureParser.COMMA)
                self.state = 133
                self.param()
                self.state = 138
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(CureParser.INT, 0)

        def FLOAT(self):
            return self.getToken(CureParser.FLOAT, 0)

        def STRING(self):
            return self.getToken(CureParser.STRING, 0)

        def BOOL(self):
            return self.getToken(CureParser.BOOL, 0)

        def NIL(self):
            return self.getToken(CureParser.NIL, 0)

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)

        def getRuleIndex(self):
            return CureParser.RULE_atom

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom" ):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)




    def atom(self):

        localctx = CureParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_atom)
        try:
            self.state = 149
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                self.enterOuterAlt(localctx, 1)
                self.state = 139
                self.match(CureParser.INT)
                pass
            elif token in [12]:
                self.enterOuterAlt(localctx, 2)
                self.state = 140
                self.match(CureParser.FLOAT)
                pass
            elif token in [13]:
                self.enterOuterAlt(localctx, 3)
                self.state = 141
                self.match(CureParser.STRING)
                pass
            elif token in [14]:
                self.enterOuterAlt(localctx, 4)
                self.state = 142
                self.match(CureParser.BOOL)
                pass
            elif token in [15]:
                self.enterOuterAlt(localctx, 5)
                self.state = 143
                self.match(CureParser.NIL)
                pass
            elif token in [16]:
                self.enterOuterAlt(localctx, 6)
                self.state = 144
                self.match(CureParser.ID)
                pass
            elif token in [34]:
                self.enterOuterAlt(localctx, 7)
                self.state = 145
                self.match(CureParser.LPAREN)
                self.state = 146
                self.expr(0)
                self.state = 147
                self.match(CureParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CureParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class CallContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)
        def args(self):
            return self.getTypedRuleContext(CureParser.ArgsContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCall" ):
                return visitor.visitCall(self)
            else:
                return visitor.visitChildren(self)


    class CastContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)
        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)

        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)
        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCast" ):
                return visitor.visitCast(self)
            else:
                return visitor.visitChildren(self)


    class Atom_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atom(self):
            return self.getTypedRuleContext(CureParser.AtomContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom_expr" ):
                return visitor.visitAtom_expr(self)
            else:
                return visitor.visitChildren(self)


    class RelationalContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)

        def EEQ(self):
            return self.getToken(CureParser.EEQ, 0)
        def NEQ(self):
            return self.getToken(CureParser.NEQ, 0)
        def GT(self):
            return self.getToken(CureParser.GT, 0)
        def LT(self):
            return self.getToken(CureParser.LT, 0)
        def GTE(self):
            return self.getToken(CureParser.GTE, 0)
        def LTE(self):
            return self.getToken(CureParser.LTE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelational" ):
                return visitor.visitRelational(self)
            else:
                return visitor.visitChildren(self)


    class UnaryContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.uop = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)

        def NOT(self):
            return self.getToken(CureParser.NOT, 0)
        def SUB(self):
            return self.getToken(CureParser.SUB, 0)
        def ADD(self):
            return self.getToken(CureParser.ADD, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnary" ):
                return visitor.visitUnary(self)
            else:
                return visitor.visitChildren(self)


    class MultiplicationContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)

        def MUL(self):
            return self.getToken(CureParser.MUL, 0)
        def DIV(self):
            return self.getToken(CureParser.DIV, 0)
        def MOD(self):
            return self.getToken(CureParser.MOD, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplication" ):
                return visitor.visitMultiplication(self)
            else:
                return visitor.visitChildren(self)


    class AttrContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)

        def DOT(self):
            return self.getToken(CureParser.DOT, 0)
        def ID(self):
            return self.getToken(CureParser.ID, 0)
        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)
        def args(self):
            return self.getTypedRuleContext(CureParser.ArgsContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr" ):
                return visitor.visitAttr(self)
            else:
                return visitor.visitChildren(self)


    class TernaryContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)

        def IF(self):
            return self.getToken(CureParser.IF, 0)
        def ELSE(self):
            return self.getToken(CureParser.ELSE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTernary" ):
                return visitor.visitTernary(self)
            else:
                return visitor.visitChildren(self)


    class LogicalContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)

        def AND(self):
            return self.getToken(CureParser.AND, 0)
        def OR(self):
            return self.getToken(CureParser.OR, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogical" ):
                return visitor.visitLogical(self)
            else:
                return visitor.visitChildren(self)


    class AdditionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)

        def ADD(self):
            return self.getToken(CureParser.ADD, 0)
        def SUB(self):
            return self.getToken(CureParser.SUB, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddition" ):
                return visitor.visitAddition(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CureParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 32
        self.enterRecursionRule(localctx, 32, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 160
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                localctx = CureParser.CastContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 152
                self.match(CureParser.LPAREN)
                self.state = 153
                self.type_()
                self.state = 154
                self.match(CureParser.RPAREN)
                self.state = 155
                self.expr(10)
                pass

            elif la_ == 2:
                localctx = CureParser.Atom_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 157
                self.atom()
                pass

            elif la_ == 3:
                localctx = CureParser.UnaryContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 158
                localctx.uop = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1074135040) != 0)):
                    localctx.uop = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 159
                self.expr(1)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 198
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,19,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 196
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
                    if la_ == 1:
                        localctx = CureParser.TernaryContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 162
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 163
                        self.match(CureParser.IF)
                        self.state = 164
                        self.expr(0)
                        self.state = 165
                        self.match(CureParser.ELSE)
                        self.state = 166
                        self.expr(7)
                        pass

                    elif la_ == 2:
                        localctx = CureParser.MultiplicationContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 168
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 169
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3670016) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 170
                        self.expr(6)
                        pass

                    elif la_ == 3:
                        localctx = CureParser.AdditionContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 171
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 172
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==17 or _la==18):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 173
                        self.expr(5)
                        pass

                    elif la_ == 4:
                        localctx = CureParser.RelationalContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 174
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 175
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 264241152) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 176
                        self.expr(4)
                        pass

                    elif la_ == 5:
                        localctx = CureParser.LogicalContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 177
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 178
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==28 or _la==29):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 179
                        self.expr(3)
                        pass

                    elif la_ == 6:
                        localctx = CureParser.CallContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 180
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 181
                        self.match(CureParser.LPAREN)
                        self.state = 183
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & 18254133248) != 0):
                            self.state = 182
                            self.args()


                        self.state = 185
                        self.match(CureParser.RPAREN)
                        pass

                    elif la_ == 7:
                        localctx = CureParser.AttrContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 186
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 187
                        self.match(CureParser.DOT)
                        self.state = 188
                        self.match(CureParser.ID)
                        self.state = 194
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
                        if la_ == 1:
                            self.state = 189
                            self.match(CureParser.LPAREN)
                            self.state = 191
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 18254133248) != 0):
                                self.state = 190
                                self.args()


                            self.state = 193
                            self.match(CureParser.RPAREN)


                        pass

             
                self.state = 200
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,19,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[16] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 7)
         




