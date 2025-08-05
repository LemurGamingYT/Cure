# Generated from cure/Cure.g4 by ANTLR 4.13.0
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
        4,1,54,310,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,1,0,5,0,52,8,0,10,0,
        12,0,55,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,5,1,65,8,1,10,1,12,1,
        68,9,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,78,8,2,1,3,1,3,1,3,1,
        3,1,3,3,3,85,8,3,1,4,1,4,5,4,89,8,4,10,4,12,4,92,9,4,1,4,1,4,1,5,
        1,5,1,5,1,5,5,5,100,8,5,10,5,12,5,103,9,5,1,5,3,5,106,8,5,1,6,1,
        6,1,6,1,6,1,6,1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,
        9,1,9,1,9,1,10,1,10,1,10,1,11,1,11,3,11,133,8,11,1,11,3,11,136,8,
        11,1,11,3,11,139,8,11,1,11,1,11,1,12,1,12,3,12,145,8,12,1,12,1,12,
        1,12,3,12,150,8,12,1,12,1,12,1,13,1,13,3,13,156,8,13,1,14,1,14,1,
        14,3,14,161,8,14,1,14,1,14,1,15,1,15,1,15,3,15,168,8,15,1,15,1,15,
        3,15,172,8,15,1,15,1,15,1,15,3,15,177,8,15,1,16,1,16,1,16,1,17,1,
        17,3,17,184,8,17,1,17,1,17,1,17,3,17,189,8,17,1,17,1,17,1,17,3,17,
        194,8,17,1,18,1,18,1,19,1,19,1,19,5,19,201,8,19,10,19,12,19,204,
        9,19,1,20,3,20,207,8,20,1,20,1,20,1,20,1,21,1,21,1,21,5,21,215,8,
        21,10,21,12,21,218,9,21,1,22,1,22,1,23,1,23,1,23,1,23,5,23,226,8,
        23,10,23,12,23,229,9,23,1,23,1,23,1,24,1,24,1,24,1,24,1,24,1,24,
        1,24,1,24,1,24,3,24,242,8,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,
        1,24,1,24,1,24,1,24,1,24,1,24,1,24,3,24,258,8,24,1,24,1,24,1,24,
        1,24,1,24,1,24,1,24,1,24,1,24,3,24,269,8,24,1,24,1,24,1,24,3,24,
        274,8,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,
        1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,3,24,
        299,8,24,1,24,1,24,1,24,1,24,5,24,305,8,24,10,24,12,24,308,9,24,
        1,24,0,2,2,48,25,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,
        36,38,40,42,44,46,48,0,8,1,0,11,12,2,0,17,17,24,24,1,0,25,29,2,0,
        25,26,38,38,1,0,27,29,1,0,25,26,1,0,30,35,1,0,36,37,338,0,53,1,0,
        0,0,2,58,1,0,0,0,4,77,1,0,0,0,6,84,1,0,0,0,8,86,1,0,0,0,10,95,1,
        0,0,0,12,107,1,0,0,0,14,112,1,0,0,0,16,115,1,0,0,0,18,119,1,0,0,
        0,20,127,1,0,0,0,22,130,1,0,0,0,24,142,1,0,0,0,26,155,1,0,0,0,28,
        160,1,0,0,0,30,164,1,0,0,0,32,178,1,0,0,0,34,193,1,0,0,0,36,195,
        1,0,0,0,38,197,1,0,0,0,40,206,1,0,0,0,42,211,1,0,0,0,44,219,1,0,
        0,0,46,221,1,0,0,0,48,273,1,0,0,0,50,52,3,4,2,0,51,50,1,0,0,0,52,
        55,1,0,0,0,53,51,1,0,0,0,53,54,1,0,0,0,54,56,1,0,0,0,55,53,1,0,0,
        0,56,57,5,0,0,1,57,1,1,0,0,0,58,59,6,1,-1,0,59,60,5,24,0,0,60,66,
        1,0,0,0,61,62,10,1,0,0,62,63,5,47,0,0,63,65,5,48,0,0,64,61,1,0,0,
        0,65,68,1,0,0,0,66,64,1,0,0,0,66,67,1,0,0,0,67,3,1,0,0,0,68,66,1,
        0,0,0,69,78,3,34,17,0,70,78,3,32,16,0,71,78,3,16,8,0,72,78,3,10,
        5,0,73,78,3,18,9,0,74,78,3,20,10,0,75,78,3,26,13,0,76,78,3,48,24,
        0,77,69,1,0,0,0,77,70,1,0,0,0,77,71,1,0,0,0,77,72,1,0,0,0,77,73,
        1,0,0,0,77,74,1,0,0,0,77,75,1,0,0,0,77,76,1,0,0,0,78,5,1,0,0,0,79,
        85,3,4,2,0,80,81,5,9,0,0,81,85,3,48,24,0,82,85,5,15,0,0,83,85,5,
        16,0,0,84,79,1,0,0,0,84,80,1,0,0,0,84,82,1,0,0,0,84,83,1,0,0,0,85,
        7,1,0,0,0,86,90,5,45,0,0,87,89,3,6,3,0,88,87,1,0,0,0,89,92,1,0,0,
        0,90,88,1,0,0,0,90,91,1,0,0,0,91,93,1,0,0,0,92,90,1,0,0,0,93,94,
        5,46,0,0,94,9,1,0,0,0,95,96,5,1,0,0,96,97,3,48,24,0,97,101,3,8,4,
        0,98,100,3,12,6,0,99,98,1,0,0,0,100,103,1,0,0,0,101,99,1,0,0,0,101,
        102,1,0,0,0,102,105,1,0,0,0,103,101,1,0,0,0,104,106,3,14,7,0,105,
        104,1,0,0,0,105,106,1,0,0,0,106,11,1,0,0,0,107,108,5,6,0,0,108,109,
        5,1,0,0,109,110,3,48,24,0,110,111,3,8,4,0,111,13,1,0,0,0,112,113,
        5,6,0,0,113,114,3,8,4,0,114,15,1,0,0,0,115,116,5,14,0,0,116,117,
        3,48,24,0,117,118,3,8,4,0,118,17,1,0,0,0,119,120,5,3,0,0,120,121,
        5,24,0,0,121,122,5,2,0,0,122,123,3,48,24,0,123,124,5,39,0,0,124,
        125,3,48,24,0,125,126,3,8,4,0,126,19,1,0,0,0,127,128,5,4,0,0,128,
        129,5,22,0,0,129,21,1,0,0,0,130,132,5,10,0,0,131,133,5,13,0,0,132,
        131,1,0,0,0,132,133,1,0,0,0,133,135,1,0,0,0,134,136,5,8,0,0,135,
        134,1,0,0,0,135,136,1,0,0,0,136,138,1,0,0,0,137,139,7,0,0,0,138,
        137,1,0,0,0,138,139,1,0,0,0,139,140,1,0,0,0,140,141,3,30,15,0,141,
        23,1,0,0,0,142,144,5,10,0,0,143,145,5,13,0,0,144,143,1,0,0,0,144,
        145,1,0,0,0,145,146,1,0,0,0,146,147,5,18,0,0,147,149,5,24,0,0,148,
        150,3,46,23,0,149,148,1,0,0,0,149,150,1,0,0,0,150,151,1,0,0,0,151,
        152,3,8,4,0,152,25,1,0,0,0,153,156,3,22,11,0,154,156,3,24,12,0,155,
        153,1,0,0,0,155,154,1,0,0,0,156,27,1,0,0,0,157,158,3,2,1,0,158,159,
        5,40,0,0,159,161,1,0,0,0,160,157,1,0,0,0,160,161,1,0,0,0,161,162,
        1,0,0,0,162,163,7,1,0,0,163,29,1,0,0,0,164,165,5,5,0,0,165,167,3,
        28,14,0,166,168,3,46,23,0,167,166,1,0,0,0,167,168,1,0,0,0,168,169,
        1,0,0,0,169,171,5,43,0,0,170,172,3,42,21,0,171,170,1,0,0,0,171,172,
        1,0,0,0,172,173,1,0,0,0,173,176,5,44,0,0,174,175,5,49,0,0,175,177,
        3,2,1,0,176,174,1,0,0,0,176,177,1,0,0,0,177,31,1,0,0,0,178,179,3,
        30,15,0,179,180,3,8,4,0,180,33,1,0,0,0,181,183,5,24,0,0,182,184,
        7,2,0,0,183,182,1,0,0,0,183,184,1,0,0,0,184,185,1,0,0,0,185,186,
        5,42,0,0,186,194,3,48,24,0,187,189,5,7,0,0,188,187,1,0,0,0,188,189,
        1,0,0,0,189,190,1,0,0,0,190,191,5,24,0,0,191,192,5,42,0,0,192,194,
        3,48,24,0,193,181,1,0,0,0,193,188,1,0,0,0,194,35,1,0,0,0,195,196,
        3,48,24,0,196,37,1,0,0,0,197,202,3,36,18,0,198,199,5,41,0,0,199,
        201,3,36,18,0,200,198,1,0,0,0,201,204,1,0,0,0,202,200,1,0,0,0,202,
        203,1,0,0,0,203,39,1,0,0,0,204,202,1,0,0,0,205,207,5,7,0,0,206,205,
        1,0,0,0,206,207,1,0,0,0,207,208,1,0,0,0,208,209,3,2,1,0,209,210,
        5,24,0,0,210,41,1,0,0,0,211,216,3,40,20,0,212,213,5,41,0,0,213,215,
        3,40,20,0,214,212,1,0,0,0,215,218,1,0,0,0,216,214,1,0,0,0,216,217,
        1,0,0,0,217,43,1,0,0,0,218,216,1,0,0,0,219,220,5,24,0,0,220,45,1,
        0,0,0,221,222,5,33,0,0,222,227,3,44,22,0,223,224,5,41,0,0,224,226,
        3,44,22,0,225,223,1,0,0,0,226,229,1,0,0,0,227,225,1,0,0,0,227,228,
        1,0,0,0,228,230,1,0,0,0,229,227,1,0,0,0,230,231,5,32,0,0,231,47,
        1,0,0,0,232,233,6,24,-1,0,233,234,5,43,0,0,234,235,3,2,1,0,235,236,
        5,44,0,0,236,237,3,48,24,19,237,274,1,0,0,0,238,239,5,24,0,0,239,
        241,5,43,0,0,240,242,3,38,19,0,241,240,1,0,0,0,241,242,1,0,0,0,242,
        243,1,0,0,0,243,274,5,44,0,0,244,245,5,43,0,0,245,246,3,48,24,0,
        246,247,5,44,0,0,247,274,1,0,0,0,248,274,5,20,0,0,249,274,5,21,0,
        0,250,274,5,22,0,0,251,274,5,23,0,0,252,274,5,24,0,0,253,254,5,17,
        0,0,254,255,3,2,1,0,255,257,5,43,0,0,256,258,3,38,19,0,257,256,1,
        0,0,0,257,258,1,0,0,0,258,259,1,0,0,0,259,260,5,44,0,0,260,274,1,
        0,0,0,261,262,5,17,0,0,262,263,3,2,1,0,263,264,5,47,0,0,264,265,
        5,48,0,0,265,274,1,0,0,0,266,268,5,47,0,0,267,269,3,38,19,0,268,
        267,1,0,0,0,268,269,1,0,0,0,269,270,1,0,0,0,270,274,5,48,0,0,271,
        272,7,3,0,0,272,274,3,48,24,1,273,232,1,0,0,0,273,238,1,0,0,0,273,
        244,1,0,0,0,273,248,1,0,0,0,273,249,1,0,0,0,273,250,1,0,0,0,273,
        251,1,0,0,0,273,252,1,0,0,0,273,253,1,0,0,0,273,261,1,0,0,0,273,
        266,1,0,0,0,273,271,1,0,0,0,274,306,1,0,0,0,275,276,10,8,0,0,276,
        277,5,1,0,0,277,278,3,48,24,0,278,279,5,6,0,0,279,280,3,48,24,9,
        280,305,1,0,0,0,281,282,10,5,0,0,282,283,7,4,0,0,283,305,3,48,24,
        6,284,285,10,4,0,0,285,286,7,5,0,0,286,305,3,48,24,5,287,288,10,
        3,0,0,288,289,7,6,0,0,289,305,3,48,24,4,290,291,10,2,0,0,291,292,
        7,7,0,0,292,305,3,48,24,3,293,294,10,7,0,0,294,295,5,40,0,0,295,
        296,5,24,0,0,296,298,5,43,0,0,297,299,3,38,19,0,298,297,1,0,0,0,
        298,299,1,0,0,0,299,300,1,0,0,0,300,305,5,44,0,0,301,302,10,6,0,
        0,302,303,5,40,0,0,303,305,5,24,0,0,304,275,1,0,0,0,304,281,1,0,
        0,0,304,284,1,0,0,0,304,287,1,0,0,0,304,290,1,0,0,0,304,293,1,0,
        0,0,304,301,1,0,0,0,305,308,1,0,0,0,306,304,1,0,0,0,306,307,1,0,
        0,0,307,49,1,0,0,0,308,306,1,0,0,0,31,53,66,77,84,90,101,105,132,
        135,138,144,149,155,160,167,171,176,183,188,193,202,206,216,227,
        241,257,268,273,298,304,306
    ]

class CureParser ( Parser ):

    grammarFileName = "Cure.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'in'", "'for'", "'use'", "'fn'", 
                     "'else'", "'mut'", "'static'", "'return'", "'extern'", 
                     "'method'", "'property'", "'internal'", "'while'", 
                     "'break'", "'continue'", "'new'", "'class'", "'''", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'+'", "'-'", "'*'", "'/'", "'%'", "'=='", 
                     "'!='", "'>'", "'<'", "'>='", "'<='", "'&&'", "'||'", 
                     "'!'", "'..'", "'.'", "','", "'='", "'('", "')'", "'{'", 
                     "'}'", "'['", "']'", "'->'", "'&'" ]

    symbolicNames = [ "<INVALID>", "IF", "IN", "FOR", "USE", "FUNC", "ELSE", 
                      "MUTABLE", "STATIC", "RETURN", "EXTERN", "METHOD", 
                      "PROPERTY", "INTERNAL", "WHILE", "BREAK", "CONTINUE", 
                      "NEW", "CLASS", "APOSTROPHE", "INT", "FLOAT", "STRING", 
                      "BOOL", "ID", "ADD", "SUB", "MUL", "DIV", "MOD", "EEQ", 
                      "NEQ", "GT", "LT", "GTE", "LTE", "AND", "OR", "NOT", 
                      "DOUBLEDOT", "DOT", "COMMA", "ASSIGN", "LPAREN", "RPAREN", 
                      "LBRACE", "RBRACE", "LBRACK", "RBRACK", "RETURNS", 
                      "AMPERSAND", "COMMENT", "MULTILINE_COMMENT", "WHITESPACE", 
                      "OTHER" ]

    RULE_program = 0
    RULE_type = 1
    RULE_stmt = 2
    RULE_bodyStmt = 3
    RULE_body = 4
    RULE_ifStmt = 5
    RULE_elseifStmt = 6
    RULE_elseStmt = 7
    RULE_whileStmt = 8
    RULE_forRangeStmt = 9
    RULE_useStmt = 10
    RULE_externFunc = 11
    RULE_externClass = 12
    RULE_externStmt = 13
    RULE_funcName = 14
    RULE_functionSignature = 15
    RULE_funcAssign = 16
    RULE_varAssign = 17
    RULE_arg = 18
    RULE_args = 19
    RULE_param = 20
    RULE_params = 21
    RULE_genericParam = 22
    RULE_genericParams = 23
    RULE_expr = 24

    ruleNames =  [ "program", "type", "stmt", "bodyStmt", "body", "ifStmt", 
                   "elseifStmt", "elseStmt", "whileStmt", "forRangeStmt", 
                   "useStmt", "externFunc", "externClass", "externStmt", 
                   "funcName", "functionSignature", "funcAssign", "varAssign", 
                   "arg", "args", "param", "params", "genericParam", "genericParams", 
                   "expr" ]

    EOF = Token.EOF
    IF=1
    IN=2
    FOR=3
    USE=4
    FUNC=5
    ELSE=6
    MUTABLE=7
    STATIC=8
    RETURN=9
    EXTERN=10
    METHOD=11
    PROPERTY=12
    INTERNAL=13
    WHILE=14
    BREAK=15
    CONTINUE=16
    NEW=17
    CLASS=18
    APOSTROPHE=19
    INT=20
    FLOAT=21
    STRING=22
    BOOL=23
    ID=24
    ADD=25
    SUB=26
    MUL=27
    DIV=28
    MOD=29
    EEQ=30
    NEQ=31
    GT=32
    LT=33
    GTE=34
    LTE=35
    AND=36
    OR=37
    NOT=38
    DOUBLEDOT=39
    DOT=40
    COMMA=41
    ASSIGN=42
    LPAREN=43
    RPAREN=44
    LBRACE=45
    RBRACE=46
    LBRACK=47
    RBRACK=48
    RETURNS=49
    AMPERSAND=50
    COMMENT=51
    MULTILINE_COMMENT=52
    WHITESPACE=53
    OTHER=54

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
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
            return CureParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = CureParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 149808592602298) != 0):
                self.state = 50
                self.stmt()
                self.state = 55
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 56
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

        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


        def LBRACK(self):
            return self.getToken(CureParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(CureParser.RBRACK, 0)

        def getRuleIndex(self):
            return CureParser.RULE_type

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)



    def type_(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CureParser.TypeContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_type, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(CureParser.ID)
            self._ctx.stop = self._input.LT(-1)
            self.state = 66
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = CureParser.TypeContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_type)
                    self.state = 61
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 62
                    self.match(CureParser.LBRACK)
                    self.state = 63
                    self.match(CureParser.RBRACK) 
                self.state = 68
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
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


        def forRangeStmt(self):
            return self.getTypedRuleContext(CureParser.ForRangeStmtContext,0)


        def useStmt(self):
            return self.getTypedRuleContext(CureParser.UseStmtContext,0)


        def externStmt(self):
            return self.getTypedRuleContext(CureParser.ExternStmtContext,0)


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
            self.state = 77
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 69
                self.varAssign()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 70
                self.funcAssign()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 71
                self.whileStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 72
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 73
                self.forRangeStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 74
                self.useStmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 75
                self.externStmt()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 76
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CureParser.RULE_bodyStmt

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class BreakContext(BodyStmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.BodyStmtContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BREAK(self):
            return self.getToken(CureParser.BREAK, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreak" ):
                return visitor.visitBreak(self)
            else:
                return visitor.visitChildren(self)


    class StmtBodyContext(BodyStmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.BodyStmtContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def stmt(self):
            return self.getTypedRuleContext(CureParser.StmtContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmtBody" ):
                return visitor.visitStmtBody(self)
            else:
                return visitor.visitChildren(self)


    class ContinueContext(BodyStmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.BodyStmtContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def CONTINUE(self):
            return self.getToken(CureParser.CONTINUE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinue" ):
                return visitor.visitContinue(self)
            else:
                return visitor.visitChildren(self)


    class ReturnContext(BodyStmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.BodyStmtContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def RETURN(self):
            return self.getToken(CureParser.RETURN, 0)
        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturn" ):
                return visitor.visitReturn(self)
            else:
                return visitor.visitChildren(self)



    def bodyStmt(self):

        localctx = CureParser.BodyStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_bodyStmt)
        try:
            self.state = 84
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 3, 4, 5, 7, 10, 14, 17, 20, 21, 22, 23, 24, 25, 26, 38, 43, 47]:
                localctx = CureParser.StmtBodyContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 79
                self.stmt()
                pass
            elif token in [9]:
                localctx = CureParser.ReturnContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 80
                self.match(CureParser.RETURN)
                self.state = 81
                self.expr(0)
                pass
            elif token in [15]:
                localctx = CureParser.BreakContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 82
                self.match(CureParser.BREAK)
                pass
            elif token in [16]:
                localctx = CureParser.ContinueContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 83
                self.match(CureParser.CONTINUE)
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

        def bodyStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.BodyStmtContext)
            else:
                return self.getTypedRuleContext(CureParser.BodyStmtContext,i)


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
            self.state = 86
            self.match(CureParser.LBRACE)
            self.state = 90
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 149808592701114) != 0):
                self.state = 87
                self.bodyStmt()
                self.state = 92
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 93
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
            self.state = 95
            self.match(CureParser.IF)
            self.state = 96
            self.expr(0)
            self.state = 97
            self.body()
            self.state = 101
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 98
                    self.elseifStmt() 
                self.state = 103
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

            self.state = 105
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 104
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
            self.state = 107
            self.match(CureParser.ELSE)
            self.state = 108
            self.match(CureParser.IF)
            self.state = 109
            self.expr(0)
            self.state = 110
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
            self.state = 112
            self.match(CureParser.ELSE)
            self.state = 113
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
            self.state = 115
            self.match(CureParser.WHILE)
            self.state = 116
            self.expr(0)
            self.state = 117
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForRangeStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(CureParser.FOR, 0)

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def IN(self):
            return self.getToken(CureParser.IN, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)


        def DOUBLEDOT(self):
            return self.getToken(CureParser.DOUBLEDOT, 0)

        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_forRangeStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForRangeStmt" ):
                return visitor.visitForRangeStmt(self)
            else:
                return visitor.visitChildren(self)




    def forRangeStmt(self):

        localctx = CureParser.ForRangeStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_forRangeStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            self.match(CureParser.FOR)
            self.state = 120
            self.match(CureParser.ID)
            self.state = 121
            self.match(CureParser.IN)
            self.state = 122
            self.expr(0)
            self.state = 123
            self.match(CureParser.DOUBLEDOT)
            self.state = 124
            self.expr(0)
            self.state = 125
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UseStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def USE(self):
            return self.getToken(CureParser.USE, 0)

        def STRING(self):
            return self.getToken(CureParser.STRING, 0)

        def getRuleIndex(self):
            return CureParser.RULE_useStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUseStmt" ):
                return visitor.visitUseStmt(self)
            else:
                return visitor.visitChildren(self)




    def useStmt(self):

        localctx = CureParser.UseStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_useStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 127
            self.match(CureParser.USE)
            self.state = 128
            self.match(CureParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExternFuncContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXTERN(self):
            return self.getToken(CureParser.EXTERN, 0)

        def functionSignature(self):
            return self.getTypedRuleContext(CureParser.FunctionSignatureContext,0)


        def INTERNAL(self):
            return self.getToken(CureParser.INTERNAL, 0)

        def STATIC(self):
            return self.getToken(CureParser.STATIC, 0)

        def PROPERTY(self):
            return self.getToken(CureParser.PROPERTY, 0)

        def METHOD(self):
            return self.getToken(CureParser.METHOD, 0)

        def getRuleIndex(self):
            return CureParser.RULE_externFunc

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExternFunc" ):
                return visitor.visitExternFunc(self)
            else:
                return visitor.visitChildren(self)




    def externFunc(self):

        localctx = CureParser.ExternFuncContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_externFunc)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 130
            self.match(CureParser.EXTERN)
            self.state = 132
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 131
                self.match(CureParser.INTERNAL)


            self.state = 135
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 134
                self.match(CureParser.STATIC)


            self.state = 138
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11 or _la==12:
                self.state = 137
                _la = self._input.LA(1)
                if not(_la==11 or _la==12):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 140
            self.functionSignature()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExternClassContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXTERN(self):
            return self.getToken(CureParser.EXTERN, 0)

        def CLASS(self):
            return self.getToken(CureParser.CLASS, 0)

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def INTERNAL(self):
            return self.getToken(CureParser.INTERNAL, 0)

        def genericParams(self):
            return self.getTypedRuleContext(CureParser.GenericParamsContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_externClass

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExternClass" ):
                return visitor.visitExternClass(self)
            else:
                return visitor.visitChildren(self)




    def externClass(self):

        localctx = CureParser.ExternClassContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_externClass)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 142
            self.match(CureParser.EXTERN)
            self.state = 144
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 143
                self.match(CureParser.INTERNAL)


            self.state = 146
            self.match(CureParser.CLASS)
            self.state = 147
            self.match(CureParser.ID)
            self.state = 149
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==33:
                self.state = 148
                self.genericParams()


            self.state = 151
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExternStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def externFunc(self):
            return self.getTypedRuleContext(CureParser.ExternFuncContext,0)


        def externClass(self):
            return self.getTypedRuleContext(CureParser.ExternClassContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_externStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExternStmt" ):
                return visitor.visitExternStmt(self)
            else:
                return visitor.visitChildren(self)




    def externStmt(self):

        localctx = CureParser.ExternStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_externStmt)
        try:
            self.state = 155
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 153
                self.externFunc()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 154
                self.externClass()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.extend_type = None # TypeContext

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def NEW(self):
            return self.getToken(CureParser.NEW, 0)

        def DOT(self):
            return self.getToken(CureParser.DOT, 0)

        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_funcName

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncName" ):
                return visitor.visitFuncName(self)
            else:
                return visitor.visitChildren(self)




    def funcName(self):

        localctx = CureParser.FuncNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_funcName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 160
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.state = 157
                localctx.extend_type = self.type_(0)
                self.state = 158
                self.match(CureParser.DOT)


            self.state = 162
            _la = self._input.LA(1)
            if not(_la==17 or _la==24):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionSignatureContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.return_type = None # TypeContext

        def FUNC(self):
            return self.getToken(CureParser.FUNC, 0)

        def funcName(self):
            return self.getTypedRuleContext(CureParser.FuncNameContext,0)


        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)

        def genericParams(self):
            return self.getTypedRuleContext(CureParser.GenericParamsContext,0)


        def params(self):
            return self.getTypedRuleContext(CureParser.ParamsContext,0)


        def RETURNS(self):
            return self.getToken(CureParser.RETURNS, 0)

        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_functionSignature

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionSignature" ):
                return visitor.visitFunctionSignature(self)
            else:
                return visitor.visitChildren(self)




    def functionSignature(self):

        localctx = CureParser.FunctionSignatureContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_functionSignature)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 164
            self.match(CureParser.FUNC)
            self.state = 165
            self.funcName()
            self.state = 167
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==33:
                self.state = 166
                self.genericParams()


            self.state = 169
            self.match(CureParser.LPAREN)
            self.state = 171
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7 or _la==24:
                self.state = 170
                self.params()


            self.state = 173
            self.match(CureParser.RPAREN)
            self.state = 176
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==49:
                self.state = 174
                self.match(CureParser.RETURNS)
                self.state = 175
                localctx.return_type = self.type_(0)


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

        def functionSignature(self):
            return self.getTypedRuleContext(CureParser.FunctionSignatureContext,0)


        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_funcAssign

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncAssign" ):
                return visitor.visitFuncAssign(self)
            else:
                return visitor.visitChildren(self)




    def funcAssign(self):

        localctx = CureParser.FuncAssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_funcAssign)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            self.functionSignature()
            self.state = 179
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

        def MUTABLE(self):
            return self.getToken(CureParser.MUTABLE, 0)

        def getRuleIndex(self):
            return CureParser.RULE_varAssign

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarAssign" ):
                return visitor.visitVarAssign(self)
            else:
                return visitor.visitChildren(self)




    def varAssign(self):

        localctx = CureParser.VarAssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_varAssign)
        self._la = 0 # Token type
        try:
            self.state = 193
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 181
                self.match(CureParser.ID)
                self.state = 183
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1040187392) != 0):
                    self.state = 182
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1040187392) != 0)):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 185
                self.match(CureParser.ASSIGN)
                self.state = 186
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 188
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 187
                    self.match(CureParser.MUTABLE)


                self.state = 190
                self.match(CureParser.ID)
                self.state = 191
                self.match(CureParser.ASSIGN)
                self.state = 192
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
        self.enterRule(localctx, 36, self.RULE_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 195
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
        self.enterRule(localctx, 38, self.RULE_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 197
            self.arg()
            self.state = 202
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==41:
                self.state = 198
                self.match(CureParser.COMMA)
                self.state = 199
                self.arg()
                self.state = 204
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

        def MUTABLE(self):
            return self.getToken(CureParser.MUTABLE, 0)

        def getRuleIndex(self):
            return CureParser.RULE_param

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = CureParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 206
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 205
                self.match(CureParser.MUTABLE)


            self.state = 208
            self.type_(0)
            self.state = 209
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
        self.enterRule(localctx, 42, self.RULE_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 211
            self.param()
            self.state = 216
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==41:
                self.state = 212
                self.match(CureParser.COMMA)
                self.state = 213
                self.param()
                self.state = 218
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GenericParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def getRuleIndex(self):
            return CureParser.RULE_genericParam

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGenericParam" ):
                return visitor.visitGenericParam(self)
            else:
                return visitor.visitChildren(self)




    def genericParam(self):

        localctx = CureParser.GenericParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_genericParam)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 219
            self.match(CureParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GenericParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LT(self):
            return self.getToken(CureParser.LT, 0)

        def genericParam(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.GenericParamContext)
            else:
                return self.getTypedRuleContext(CureParser.GenericParamContext,i)


        def GT(self):
            return self.getToken(CureParser.GT, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CureParser.COMMA)
            else:
                return self.getToken(CureParser.COMMA, i)

        def getRuleIndex(self):
            return CureParser.RULE_genericParams

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGenericParams" ):
                return visitor.visitGenericParams(self)
            else:
                return visitor.visitChildren(self)




    def genericParams(self):

        localctx = CureParser.GenericParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_genericParams)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 221
            self.match(CureParser.LT)
            self.state = 222
            self.genericParam()
            self.state = 227
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==41:
                self.state = 223
                self.match(CureParser.COMMA)
                self.state = 224
                self.genericParam()
                self.state = 229
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 230
            self.match(CureParser.GT)
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


    class NewContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NEW(self):
            return self.getToken(CureParser.NEW, 0)
        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)
        def args(self):
            return self.getTypedRuleContext(CureParser.ArgsContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNew" ):
                return visitor.visitNew(self)
            else:
                return visitor.visitChildren(self)


    class StringContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(CureParser.STRING, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)


    class BoolContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BOOL(self):
            return self.getToken(CureParser.BOOL, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBool" ):
                return visitor.visitBool(self)
            else:
                return visitor.visitChildren(self)


    class MethodContext(ExprContext):

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
            if hasattr( visitor, "visitMethod" ):
                return visitor.visitMethod(self)
            else:
                return visitor.visitChildren(self)


    class ArrayInitContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LBRACK(self):
            return self.getToken(CureParser.LBRACK, 0)
        def RBRACK(self):
            return self.getToken(CureParser.RBRACK, 0)
        def args(self):
            return self.getTypedRuleContext(CureParser.ArgsContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayInit" ):
                return visitor.visitArrayInit(self)
            else:
                return visitor.visitChildren(self)


    class NewArrayContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NEW(self):
            return self.getToken(CureParser.NEW, 0)
        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)

        def LBRACK(self):
            return self.getToken(CureParser.LBRACK, 0)
        def RBRACK(self):
            return self.getToken(CureParser.RBRACK, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNewArray" ):
                return visitor.visitNewArray(self)
            else:
                return visitor.visitChildren(self)


    class UnaryContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
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


    class FloatContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FLOAT(self):
            return self.getToken(CureParser.FLOAT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloat" ):
                return visitor.visitFloat(self)
            else:
                return visitor.visitChildren(self)


    class IntContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(CureParser.INT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInt" ):
                return visitor.visitInt(self)
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


    class CallContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(CureParser.ID, 0)
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


    class ParenContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)
        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)

        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParen" ):
                return visitor.visitParen(self)
            else:
                return visitor.visitChildren(self)


    class PropertyContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)

        def DOT(self):
            return self.getToken(CureParser.DOT, 0)
        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProperty" ):
                return visitor.visitProperty(self)
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


    class IdContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitId" ):
                return visitor.visitId(self)
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
        _startState = 48
        self.enterRecursionRule(localctx, 48, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 273
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,27,self._ctx)
            if la_ == 1:
                localctx = CureParser.CastContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 233
                self.match(CureParser.LPAREN)
                self.state = 234
                self.type_(0)
                self.state = 235
                self.match(CureParser.RPAREN)
                self.state = 236
                self.expr(19)
                pass

            elif la_ == 2:
                localctx = CureParser.CallContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 238
                self.match(CureParser.ID)
                self.state = 239
                self.match(CureParser.LPAREN)
                self.state = 241
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 149808592584704) != 0):
                    self.state = 240
                    self.args()


                self.state = 243
                self.match(CureParser.RPAREN)
                pass

            elif la_ == 3:
                localctx = CureParser.ParenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 244
                self.match(CureParser.LPAREN)
                self.state = 245
                self.expr(0)
                self.state = 246
                self.match(CureParser.RPAREN)
                pass

            elif la_ == 4:
                localctx = CureParser.IntContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 248
                self.match(CureParser.INT)
                pass

            elif la_ == 5:
                localctx = CureParser.FloatContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 249
                self.match(CureParser.FLOAT)
                pass

            elif la_ == 6:
                localctx = CureParser.StringContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 250
                self.match(CureParser.STRING)
                pass

            elif la_ == 7:
                localctx = CureParser.BoolContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 251
                self.match(CureParser.BOOL)
                pass

            elif la_ == 8:
                localctx = CureParser.IdContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 252
                self.match(CureParser.ID)
                pass

            elif la_ == 9:
                localctx = CureParser.NewContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 253
                self.match(CureParser.NEW)
                self.state = 254
                self.type_(0)
                self.state = 255
                self.match(CureParser.LPAREN)
                self.state = 257
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 149808592584704) != 0):
                    self.state = 256
                    self.args()


                self.state = 259
                self.match(CureParser.RPAREN)
                pass

            elif la_ == 10:
                localctx = CureParser.NewArrayContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 261
                self.match(CureParser.NEW)
                self.state = 262
                self.type_(0)
                self.state = 263
                self.match(CureParser.LBRACK)
                self.state = 264
                self.match(CureParser.RBRACK)
                pass

            elif la_ == 11:
                localctx = CureParser.ArrayInitContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 266
                self.match(CureParser.LBRACK)
                self.state = 268
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 149808592584704) != 0):
                    self.state = 267
                    self.args()


                self.state = 270
                self.match(CureParser.RBRACK)
                pass

            elif la_ == 12:
                localctx = CureParser.UnaryContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 271
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 274978570240) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 272
                self.expr(1)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 306
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,30,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 304
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,29,self._ctx)
                    if la_ == 1:
                        localctx = CureParser.TernaryContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 275
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 276
                        self.match(CureParser.IF)
                        self.state = 277
                        self.expr(0)
                        self.state = 278
                        self.match(CureParser.ELSE)
                        self.state = 279
                        self.expr(9)
                        pass

                    elif la_ == 2:
                        localctx = CureParser.MultiplicationContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 281
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 282
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 939524096) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 283
                        self.expr(6)
                        pass

                    elif la_ == 3:
                        localctx = CureParser.AdditionContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 284
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 285
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==25 or _la==26):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 286
                        self.expr(5)
                        pass

                    elif la_ == 4:
                        localctx = CureParser.RelationalContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 287
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 288
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 67645734912) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 289
                        self.expr(4)
                        pass

                    elif la_ == 5:
                        localctx = CureParser.LogicalContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 290
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 291
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==36 or _la==37):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 292
                        self.expr(3)
                        pass

                    elif la_ == 6:
                        localctx = CureParser.MethodContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 293
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 294
                        self.match(CureParser.DOT)
                        self.state = 295
                        self.match(CureParser.ID)
                        self.state = 296
                        self.match(CureParser.LPAREN)
                        self.state = 298
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & 149808592584704) != 0):
                            self.state = 297
                            self.args()


                        self.state = 300
                        self.match(CureParser.RPAREN)
                        pass

                    elif la_ == 7:
                        localctx = CureParser.PropertyContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 301
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 302
                        self.match(CureParser.DOT)
                        self.state = 303
                        self.match(CureParser.ID)
                        pass

             
                self.state = 308
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,30,self._ctx)

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
        self._predicates[1] = self.type_sempred
        self._predicates[24] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def type_sempred(self, localctx:TypeContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 6)
         




