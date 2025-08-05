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
        4,1,54,312,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,1,0,5,0,52,8,0,10,0,
        12,0,55,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,67,8,1,10,
        1,12,1,70,9,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,80,8,2,1,3,1,3,
        1,3,1,3,1,3,3,3,87,8,3,1,4,1,4,5,4,91,8,4,10,4,12,4,94,9,4,1,4,1,
        4,1,5,1,5,1,5,1,5,5,5,102,8,5,10,5,12,5,105,9,5,1,5,3,5,108,8,5,
        1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,
        1,9,1,9,1,9,1,9,1,10,1,10,1,10,1,11,1,11,3,11,135,8,11,1,11,3,11,
        138,8,11,1,11,3,11,141,8,11,1,11,1,11,1,12,1,12,3,12,147,8,12,1,
        12,1,12,1,12,3,12,152,8,12,1,12,1,12,1,13,1,13,3,13,158,8,13,1,14,
        1,14,1,14,3,14,163,8,14,1,14,1,14,1,15,1,15,1,15,3,15,170,8,15,1,
        15,1,15,3,15,174,8,15,1,15,1,15,1,15,3,15,179,8,15,1,16,1,16,1,16,
        1,17,1,17,3,17,186,8,17,1,17,1,17,1,17,3,17,191,8,17,1,17,1,17,1,
        17,3,17,196,8,17,1,18,1,18,1,19,1,19,1,19,5,19,203,8,19,10,19,12,
        19,206,9,19,1,20,3,20,209,8,20,1,20,1,20,1,20,1,21,1,21,1,21,5,21,
        217,8,21,10,21,12,21,220,9,21,1,22,1,22,1,23,1,23,1,23,1,23,5,23,
        228,8,23,10,23,12,23,231,9,23,1,23,1,23,1,24,1,24,1,24,1,24,1,24,
        1,24,1,24,1,24,1,24,3,24,244,8,24,1,24,1,24,1,24,1,24,1,24,1,24,
        1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,3,24,260,8,24,1,24,1,24,
        1,24,1,24,1,24,1,24,1,24,1,24,1,24,3,24,271,8,24,1,24,1,24,1,24,
        3,24,276,8,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,
        1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,
        3,24,301,8,24,1,24,1,24,1,24,1,24,5,24,307,8,24,10,24,12,24,310,
        9,24,1,24,0,2,2,48,25,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,
        32,34,36,38,40,42,44,46,48,0,8,1,0,11,12,2,0,17,17,24,24,1,0,25,
        29,2,0,25,26,38,38,1,0,27,29,1,0,25,26,1,0,30,35,1,0,36,37,341,0,
        53,1,0,0,0,2,58,1,0,0,0,4,79,1,0,0,0,6,86,1,0,0,0,8,88,1,0,0,0,10,
        97,1,0,0,0,12,109,1,0,0,0,14,114,1,0,0,0,16,117,1,0,0,0,18,121,1,
        0,0,0,20,129,1,0,0,0,22,132,1,0,0,0,24,144,1,0,0,0,26,157,1,0,0,
        0,28,162,1,0,0,0,30,166,1,0,0,0,32,180,1,0,0,0,34,195,1,0,0,0,36,
        197,1,0,0,0,38,199,1,0,0,0,40,208,1,0,0,0,42,213,1,0,0,0,44,221,
        1,0,0,0,46,223,1,0,0,0,48,275,1,0,0,0,50,52,3,4,2,0,51,50,1,0,0,
        0,52,55,1,0,0,0,53,51,1,0,0,0,53,54,1,0,0,0,54,56,1,0,0,0,55,53,
        1,0,0,0,56,57,5,0,0,1,57,1,1,0,0,0,58,59,6,1,-1,0,59,60,5,24,0,0,
        60,68,1,0,0,0,61,62,10,2,0,0,62,63,5,47,0,0,63,67,5,48,0,0,64,65,
        10,1,0,0,65,67,5,50,0,0,66,61,1,0,0,0,66,64,1,0,0,0,67,70,1,0,0,
        0,68,66,1,0,0,0,68,69,1,0,0,0,69,3,1,0,0,0,70,68,1,0,0,0,71,80,3,
        34,17,0,72,80,3,32,16,0,73,80,3,16,8,0,74,80,3,10,5,0,75,80,3,18,
        9,0,76,80,3,20,10,0,77,80,3,26,13,0,78,80,3,48,24,0,79,71,1,0,0,
        0,79,72,1,0,0,0,79,73,1,0,0,0,79,74,1,0,0,0,79,75,1,0,0,0,79,76,
        1,0,0,0,79,77,1,0,0,0,79,78,1,0,0,0,80,5,1,0,0,0,81,87,3,4,2,0,82,
        83,5,9,0,0,83,87,3,48,24,0,84,87,5,15,0,0,85,87,5,16,0,0,86,81,1,
        0,0,0,86,82,1,0,0,0,86,84,1,0,0,0,86,85,1,0,0,0,87,7,1,0,0,0,88,
        92,5,45,0,0,89,91,3,6,3,0,90,89,1,0,0,0,91,94,1,0,0,0,92,90,1,0,
        0,0,92,93,1,0,0,0,93,95,1,0,0,0,94,92,1,0,0,0,95,96,5,46,0,0,96,
        9,1,0,0,0,97,98,5,1,0,0,98,99,3,48,24,0,99,103,3,8,4,0,100,102,3,
        12,6,0,101,100,1,0,0,0,102,105,1,0,0,0,103,101,1,0,0,0,103,104,1,
        0,0,0,104,107,1,0,0,0,105,103,1,0,0,0,106,108,3,14,7,0,107,106,1,
        0,0,0,107,108,1,0,0,0,108,11,1,0,0,0,109,110,5,6,0,0,110,111,5,1,
        0,0,111,112,3,48,24,0,112,113,3,8,4,0,113,13,1,0,0,0,114,115,5,6,
        0,0,115,116,3,8,4,0,116,15,1,0,0,0,117,118,5,14,0,0,118,119,3,48,
        24,0,119,120,3,8,4,0,120,17,1,0,0,0,121,122,5,3,0,0,122,123,5,24,
        0,0,123,124,5,2,0,0,124,125,3,48,24,0,125,126,5,39,0,0,126,127,3,
        48,24,0,127,128,3,8,4,0,128,19,1,0,0,0,129,130,5,4,0,0,130,131,5,
        22,0,0,131,21,1,0,0,0,132,134,5,10,0,0,133,135,5,13,0,0,134,133,
        1,0,0,0,134,135,1,0,0,0,135,137,1,0,0,0,136,138,5,8,0,0,137,136,
        1,0,0,0,137,138,1,0,0,0,138,140,1,0,0,0,139,141,7,0,0,0,140,139,
        1,0,0,0,140,141,1,0,0,0,141,142,1,0,0,0,142,143,3,30,15,0,143,23,
        1,0,0,0,144,146,5,10,0,0,145,147,5,13,0,0,146,145,1,0,0,0,146,147,
        1,0,0,0,147,148,1,0,0,0,148,149,5,18,0,0,149,151,5,24,0,0,150,152,
        3,46,23,0,151,150,1,0,0,0,151,152,1,0,0,0,152,153,1,0,0,0,153,154,
        3,8,4,0,154,25,1,0,0,0,155,158,3,22,11,0,156,158,3,24,12,0,157,155,
        1,0,0,0,157,156,1,0,0,0,158,27,1,0,0,0,159,160,3,2,1,0,160,161,5,
        40,0,0,161,163,1,0,0,0,162,159,1,0,0,0,162,163,1,0,0,0,163,164,1,
        0,0,0,164,165,7,1,0,0,165,29,1,0,0,0,166,167,5,5,0,0,167,169,3,28,
        14,0,168,170,3,46,23,0,169,168,1,0,0,0,169,170,1,0,0,0,170,171,1,
        0,0,0,171,173,5,43,0,0,172,174,3,42,21,0,173,172,1,0,0,0,173,174,
        1,0,0,0,174,175,1,0,0,0,175,178,5,44,0,0,176,177,5,49,0,0,177,179,
        3,2,1,0,178,176,1,0,0,0,178,179,1,0,0,0,179,31,1,0,0,0,180,181,3,
        30,15,0,181,182,3,8,4,0,182,33,1,0,0,0,183,185,5,24,0,0,184,186,
        7,2,0,0,185,184,1,0,0,0,185,186,1,0,0,0,186,187,1,0,0,0,187,188,
        5,42,0,0,188,196,3,48,24,0,189,191,5,7,0,0,190,189,1,0,0,0,190,191,
        1,0,0,0,191,192,1,0,0,0,192,193,5,24,0,0,193,194,5,42,0,0,194,196,
        3,48,24,0,195,183,1,0,0,0,195,190,1,0,0,0,196,35,1,0,0,0,197,198,
        3,48,24,0,198,37,1,0,0,0,199,204,3,36,18,0,200,201,5,41,0,0,201,
        203,3,36,18,0,202,200,1,0,0,0,203,206,1,0,0,0,204,202,1,0,0,0,204,
        205,1,0,0,0,205,39,1,0,0,0,206,204,1,0,0,0,207,209,5,7,0,0,208,207,
        1,0,0,0,208,209,1,0,0,0,209,210,1,0,0,0,210,211,3,2,1,0,211,212,
        5,24,0,0,212,41,1,0,0,0,213,218,3,40,20,0,214,215,5,41,0,0,215,217,
        3,40,20,0,216,214,1,0,0,0,217,220,1,0,0,0,218,216,1,0,0,0,218,219,
        1,0,0,0,219,43,1,0,0,0,220,218,1,0,0,0,221,222,5,24,0,0,222,45,1,
        0,0,0,223,224,5,33,0,0,224,229,3,44,22,0,225,226,5,41,0,0,226,228,
        3,44,22,0,227,225,1,0,0,0,228,231,1,0,0,0,229,227,1,0,0,0,229,230,
        1,0,0,0,230,232,1,0,0,0,231,229,1,0,0,0,232,233,5,32,0,0,233,47,
        1,0,0,0,234,235,6,24,-1,0,235,236,5,43,0,0,236,237,3,2,1,0,237,238,
        5,44,0,0,238,239,3,48,24,19,239,276,1,0,0,0,240,241,5,24,0,0,241,
        243,5,43,0,0,242,244,3,38,19,0,243,242,1,0,0,0,243,244,1,0,0,0,244,
        245,1,0,0,0,245,276,5,44,0,0,246,247,5,43,0,0,247,248,3,48,24,0,
        248,249,5,44,0,0,249,276,1,0,0,0,250,276,5,20,0,0,251,276,5,21,0,
        0,252,276,5,22,0,0,253,276,5,23,0,0,254,276,5,24,0,0,255,256,5,17,
        0,0,256,257,3,2,1,0,257,259,5,43,0,0,258,260,3,38,19,0,259,258,1,
        0,0,0,259,260,1,0,0,0,260,261,1,0,0,0,261,262,5,44,0,0,262,276,1,
        0,0,0,263,264,5,17,0,0,264,265,3,2,1,0,265,266,5,47,0,0,266,267,
        5,48,0,0,267,276,1,0,0,0,268,270,5,47,0,0,269,271,3,38,19,0,270,
        269,1,0,0,0,270,271,1,0,0,0,271,272,1,0,0,0,272,276,5,48,0,0,273,
        274,7,3,0,0,274,276,3,48,24,1,275,234,1,0,0,0,275,240,1,0,0,0,275,
        246,1,0,0,0,275,250,1,0,0,0,275,251,1,0,0,0,275,252,1,0,0,0,275,
        253,1,0,0,0,275,254,1,0,0,0,275,255,1,0,0,0,275,263,1,0,0,0,275,
        268,1,0,0,0,275,273,1,0,0,0,276,308,1,0,0,0,277,278,10,8,0,0,278,
        279,5,1,0,0,279,280,3,48,24,0,280,281,5,6,0,0,281,282,3,48,24,9,
        282,307,1,0,0,0,283,284,10,5,0,0,284,285,7,4,0,0,285,307,3,48,24,
        6,286,287,10,4,0,0,287,288,7,5,0,0,288,307,3,48,24,5,289,290,10,
        3,0,0,290,291,7,6,0,0,291,307,3,48,24,4,292,293,10,2,0,0,293,294,
        7,7,0,0,294,307,3,48,24,3,295,296,10,7,0,0,296,297,5,40,0,0,297,
        298,5,24,0,0,298,300,5,43,0,0,299,301,3,38,19,0,300,299,1,0,0,0,
        300,301,1,0,0,0,301,302,1,0,0,0,302,307,5,44,0,0,303,304,10,6,0,
        0,304,305,5,40,0,0,305,307,5,24,0,0,306,277,1,0,0,0,306,283,1,0,
        0,0,306,286,1,0,0,0,306,289,1,0,0,0,306,292,1,0,0,0,306,295,1,0,
        0,0,306,303,1,0,0,0,307,310,1,0,0,0,308,306,1,0,0,0,308,309,1,0,
        0,0,309,49,1,0,0,0,310,308,1,0,0,0,32,53,66,68,79,86,92,103,107,
        134,137,140,146,151,157,162,169,173,178,185,190,195,204,208,218,
        229,243,259,270,275,300,306,308
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

        def AMPERSAND(self):
            return self.getToken(CureParser.AMPERSAND, 0)

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
            self.state = 68
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 66
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = CureParser.TypeContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_type)
                        self.state = 61
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 62
                        self.match(CureParser.LBRACK)
                        self.state = 63
                        self.match(CureParser.RBRACK)
                        pass

                    elif la_ == 2:
                        localctx = CureParser.TypeContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_type)
                        self.state = 64
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 65
                        self.match(CureParser.AMPERSAND)
                        pass

             
                self.state = 70
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

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
            self.state = 79
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 71
                self.varAssign()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 72
                self.funcAssign()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 73
                self.whileStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 74
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 75
                self.forRangeStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 76
                self.useStmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 77
                self.externStmt()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 78
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
            self.state = 86
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 3, 4, 5, 7, 10, 14, 17, 20, 21, 22, 23, 24, 25, 26, 38, 43, 47]:
                localctx = CureParser.StmtBodyContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 81
                self.stmt()
                pass
            elif token in [9]:
                localctx = CureParser.ReturnContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 82
                self.match(CureParser.RETURN)
                self.state = 83
                self.expr(0)
                pass
            elif token in [15]:
                localctx = CureParser.BreakContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 84
                self.match(CureParser.BREAK)
                pass
            elif token in [16]:
                localctx = CureParser.ContinueContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 85
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
            self.state = 88
            self.match(CureParser.LBRACE)
            self.state = 92
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 149808592701114) != 0):
                self.state = 89
                self.bodyStmt()
                self.state = 94
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 95
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
            self.state = 97
            self.match(CureParser.IF)
            self.state = 98
            self.expr(0)
            self.state = 99
            self.body()
            self.state = 103
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 100
                    self.elseifStmt() 
                self.state = 105
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

            self.state = 107
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 106
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
            self.state = 109
            self.match(CureParser.ELSE)
            self.state = 110
            self.match(CureParser.IF)
            self.state = 111
            self.expr(0)
            self.state = 112
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
            self.state = 114
            self.match(CureParser.ELSE)
            self.state = 115
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
            self.state = 117
            self.match(CureParser.WHILE)
            self.state = 118
            self.expr(0)
            self.state = 119
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
            self.state = 121
            self.match(CureParser.FOR)
            self.state = 122
            self.match(CureParser.ID)
            self.state = 123
            self.match(CureParser.IN)
            self.state = 124
            self.expr(0)
            self.state = 125
            self.match(CureParser.DOUBLEDOT)
            self.state = 126
            self.expr(0)
            self.state = 127
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
            self.state = 129
            self.match(CureParser.USE)
            self.state = 130
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
            self.state = 132
            self.match(CureParser.EXTERN)
            self.state = 134
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 133
                self.match(CureParser.INTERNAL)


            self.state = 137
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 136
                self.match(CureParser.STATIC)


            self.state = 140
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11 or _la==12:
                self.state = 139
                _la = self._input.LA(1)
                if not(_la==11 or _la==12):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 142
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
            self.state = 144
            self.match(CureParser.EXTERN)
            self.state = 146
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 145
                self.match(CureParser.INTERNAL)


            self.state = 148
            self.match(CureParser.CLASS)
            self.state = 149
            self.match(CureParser.ID)
            self.state = 151
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==33:
                self.state = 150
                self.genericParams()


            self.state = 153
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
            self.state = 157
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 155
                self.externFunc()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 156
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
            self.state = 162
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.state = 159
                localctx.extend_type = self.type_(0)
                self.state = 160
                self.match(CureParser.DOT)


            self.state = 164
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
            self.state = 166
            self.match(CureParser.FUNC)
            self.state = 167
            self.funcName()
            self.state = 169
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==33:
                self.state = 168
                self.genericParams()


            self.state = 171
            self.match(CureParser.LPAREN)
            self.state = 173
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7 or _la==24:
                self.state = 172
                self.params()


            self.state = 175
            self.match(CureParser.RPAREN)
            self.state = 178
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==49:
                self.state = 176
                self.match(CureParser.RETURNS)
                self.state = 177
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
            self.state = 180
            self.functionSignature()
            self.state = 181
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
            self.state = 195
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 183
                self.match(CureParser.ID)
                self.state = 185
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1040187392) != 0):
                    self.state = 184
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1040187392) != 0)):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 187
                self.match(CureParser.ASSIGN)
                self.state = 188
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 190
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 189
                    self.match(CureParser.MUTABLE)


                self.state = 192
                self.match(CureParser.ID)
                self.state = 193
                self.match(CureParser.ASSIGN)
                self.state = 194
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
            self.state = 197
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
            self.state = 199
            self.arg()
            self.state = 204
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==41:
                self.state = 200
                self.match(CureParser.COMMA)
                self.state = 201
                self.arg()
                self.state = 206
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
            self.state = 208
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 207
                self.match(CureParser.MUTABLE)


            self.state = 210
            self.type_(0)
            self.state = 211
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
            self.state = 213
            self.param()
            self.state = 218
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==41:
                self.state = 214
                self.match(CureParser.COMMA)
                self.state = 215
                self.param()
                self.state = 220
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
            self.state = 221
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
            self.state = 223
            self.match(CureParser.LT)
            self.state = 224
            self.genericParam()
            self.state = 229
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==41:
                self.state = 225
                self.match(CureParser.COMMA)
                self.state = 226
                self.genericParam()
                self.state = 231
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 232
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
            self.state = 275
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
            if la_ == 1:
                localctx = CureParser.CastContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 235
                self.match(CureParser.LPAREN)
                self.state = 236
                self.type_(0)
                self.state = 237
                self.match(CureParser.RPAREN)
                self.state = 238
                self.expr(19)
                pass

            elif la_ == 2:
                localctx = CureParser.CallContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 240
                self.match(CureParser.ID)
                self.state = 241
                self.match(CureParser.LPAREN)
                self.state = 243
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 149808592584704) != 0):
                    self.state = 242
                    self.args()


                self.state = 245
                self.match(CureParser.RPAREN)
                pass

            elif la_ == 3:
                localctx = CureParser.ParenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 246
                self.match(CureParser.LPAREN)
                self.state = 247
                self.expr(0)
                self.state = 248
                self.match(CureParser.RPAREN)
                pass

            elif la_ == 4:
                localctx = CureParser.IntContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 250
                self.match(CureParser.INT)
                pass

            elif la_ == 5:
                localctx = CureParser.FloatContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 251
                self.match(CureParser.FLOAT)
                pass

            elif la_ == 6:
                localctx = CureParser.StringContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 252
                self.match(CureParser.STRING)
                pass

            elif la_ == 7:
                localctx = CureParser.BoolContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 253
                self.match(CureParser.BOOL)
                pass

            elif la_ == 8:
                localctx = CureParser.IdContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 254
                self.match(CureParser.ID)
                pass

            elif la_ == 9:
                localctx = CureParser.NewContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 255
                self.match(CureParser.NEW)
                self.state = 256
                self.type_(0)
                self.state = 257
                self.match(CureParser.LPAREN)
                self.state = 259
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 149808592584704) != 0):
                    self.state = 258
                    self.args()


                self.state = 261
                self.match(CureParser.RPAREN)
                pass

            elif la_ == 10:
                localctx = CureParser.NewArrayContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 263
                self.match(CureParser.NEW)
                self.state = 264
                self.type_(0)
                self.state = 265
                self.match(CureParser.LBRACK)
                self.state = 266
                self.match(CureParser.RBRACK)
                pass

            elif la_ == 11:
                localctx = CureParser.ArrayInitContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 268
                self.match(CureParser.LBRACK)
                self.state = 270
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 149808592584704) != 0):
                    self.state = 269
                    self.args()


                self.state = 272
                self.match(CureParser.RBRACK)
                pass

            elif la_ == 12:
                localctx = CureParser.UnaryContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 273
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 274978570240) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 274
                self.expr(1)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 308
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,31,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 306
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
                    if la_ == 1:
                        localctx = CureParser.TernaryContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 277
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 278
                        self.match(CureParser.IF)
                        self.state = 279
                        self.expr(0)
                        self.state = 280
                        self.match(CureParser.ELSE)
                        self.state = 281
                        self.expr(9)
                        pass

                    elif la_ == 2:
                        localctx = CureParser.MultiplicationContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 283
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 284
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 939524096) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 285
                        self.expr(6)
                        pass

                    elif la_ == 3:
                        localctx = CureParser.AdditionContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 286
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 287
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==25 or _la==26):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 288
                        self.expr(5)
                        pass

                    elif la_ == 4:
                        localctx = CureParser.RelationalContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 289
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 290
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 67645734912) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 291
                        self.expr(4)
                        pass

                    elif la_ == 5:
                        localctx = CureParser.LogicalContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 292
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 293
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==36 or _la==37):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 294
                        self.expr(3)
                        pass

                    elif la_ == 6:
                        localctx = CureParser.MethodContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 295
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 296
                        self.match(CureParser.DOT)
                        self.state = 297
                        self.match(CureParser.ID)
                        self.state = 298
                        self.match(CureParser.LPAREN)
                        self.state = 300
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & 149808592584704) != 0):
                            self.state = 299
                            self.args()


                        self.state = 302
                        self.match(CureParser.RPAREN)
                        pass

                    elif la_ == 7:
                        localctx = CureParser.PropertyContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 303
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 304
                        self.match(CureParser.DOT)
                        self.state = 305
                        self.match(CureParser.ID)
                        pass

             
                self.state = 310
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,31,self._ctx)

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
                return self.precpred(self._ctx, 2)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 6)
         




