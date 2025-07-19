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
        4,1,50,320,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,1,0,5,0,52,8,0,10,0,
        12,0,55,9,0,1,0,1,0,1,1,1,1,3,1,61,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,3,2,71,8,2,1,3,1,3,1,3,1,3,1,3,3,3,78,8,3,1,4,1,4,5,4,82,8,
        4,10,4,12,4,85,9,4,1,4,1,4,1,5,1,5,1,5,1,5,5,5,93,8,5,10,5,12,5,
        96,9,5,1,5,3,5,99,8,5,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,8,1,8,1,
        8,1,8,1,9,1,9,1,9,1,10,1,10,1,10,1,11,1,11,1,11,1,11,1,12,1,12,3,
        12,125,8,12,1,12,1,12,1,12,3,12,130,8,12,1,12,1,12,3,12,134,8,12,
        1,12,3,12,137,8,12,1,12,1,12,3,12,141,8,12,1,13,1,13,1,13,1,13,3,
        13,147,8,13,1,13,1,13,5,13,151,8,13,10,13,12,13,154,9,13,1,13,1,
        13,1,14,1,14,1,14,3,14,161,8,14,1,15,1,15,1,15,1,15,1,15,1,15,1,
        15,1,15,1,15,1,15,1,15,3,15,174,8,15,1,16,1,16,1,16,1,16,3,16,180,
        8,16,1,16,1,16,1,16,3,16,185,8,16,1,16,1,16,1,17,1,17,3,17,191,8,
        17,1,17,1,17,1,17,3,17,196,8,17,1,17,3,17,199,8,17,1,17,1,17,1,17,
        3,17,204,8,17,1,18,1,18,1,19,1,19,1,19,5,19,211,8,19,10,19,12,19,
        214,9,19,1,20,3,20,217,8,20,1,20,1,20,1,20,1,21,1,21,1,21,5,21,225,
        8,21,10,21,12,21,228,9,21,1,22,1,22,1,23,1,23,1,23,1,23,5,23,236,
        8,23,10,23,12,23,239,9,23,1,23,1,23,1,24,1,24,1,24,1,24,1,24,1,24,
        1,24,1,24,1,24,3,24,252,8,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,
        1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,3,24,270,8,24,1,24,
        1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,3,24,
        285,8,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,
        1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,3,24,
        310,8,24,1,24,3,24,313,8,24,5,24,315,8,24,10,24,12,24,318,9,24,1,
        24,0,1,48,25,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,
        38,40,42,44,46,48,0,7,1,0,23,36,1,0,23,27,2,0,23,24,36,36,1,0,25,
        27,1,0,23,24,1,0,28,33,1,0,34,35,354,0,53,1,0,0,0,2,58,1,0,0,0,4,
        70,1,0,0,0,6,77,1,0,0,0,8,79,1,0,0,0,10,88,1,0,0,0,12,100,1,0,0,
        0,14,105,1,0,0,0,16,108,1,0,0,0,18,112,1,0,0,0,20,115,1,0,0,0,22,
        118,1,0,0,0,24,122,1,0,0,0,26,142,1,0,0,0,28,160,1,0,0,0,30,173,
        1,0,0,0,32,175,1,0,0,0,34,203,1,0,0,0,36,205,1,0,0,0,38,207,1,0,
        0,0,40,216,1,0,0,0,42,221,1,0,0,0,44,229,1,0,0,0,46,231,1,0,0,0,
        48,284,1,0,0,0,50,52,3,4,2,0,51,50,1,0,0,0,52,55,1,0,0,0,53,51,1,
        0,0,0,53,54,1,0,0,0,54,56,1,0,0,0,55,53,1,0,0,0,56,57,5,0,0,1,57,
        1,1,0,0,0,58,60,5,21,0,0,59,61,5,22,0,0,60,59,1,0,0,0,60,61,1,0,
        0,0,61,3,1,0,0,0,62,71,3,34,17,0,63,71,3,32,16,0,64,71,3,16,8,0,
        65,71,3,10,5,0,66,71,3,18,9,0,67,71,3,20,10,0,68,71,3,28,14,0,69,
        71,3,48,24,0,70,62,1,0,0,0,70,63,1,0,0,0,70,64,1,0,0,0,70,65,1,0,
        0,0,70,66,1,0,0,0,70,67,1,0,0,0,70,68,1,0,0,0,70,69,1,0,0,0,71,5,
        1,0,0,0,72,78,3,4,2,0,73,74,5,9,0,0,74,78,3,48,24,0,75,78,5,13,0,
        0,76,78,5,14,0,0,77,72,1,0,0,0,77,73,1,0,0,0,77,75,1,0,0,0,77,76,
        1,0,0,0,78,7,1,0,0,0,79,83,5,42,0,0,80,82,3,6,3,0,81,80,1,0,0,0,
        82,85,1,0,0,0,83,81,1,0,0,0,83,84,1,0,0,0,84,86,1,0,0,0,85,83,1,
        0,0,0,86,87,5,43,0,0,87,9,1,0,0,0,88,89,5,2,0,0,89,90,3,48,24,0,
        90,94,3,8,4,0,91,93,3,12,6,0,92,91,1,0,0,0,93,96,1,0,0,0,94,92,1,
        0,0,0,94,95,1,0,0,0,95,98,1,0,0,0,96,94,1,0,0,0,97,99,3,14,7,0,98,
        97,1,0,0,0,98,99,1,0,0,0,99,11,1,0,0,0,100,101,5,6,0,0,101,102,5,
        2,0,0,102,103,3,48,24,0,103,104,3,8,4,0,104,13,1,0,0,0,105,106,5,
        6,0,0,106,107,3,8,4,0,107,15,1,0,0,0,108,109,5,12,0,0,109,110,3,
        48,24,0,110,111,3,8,4,0,111,17,1,0,0,0,112,113,5,3,0,0,113,114,5,
        19,0,0,114,19,1,0,0,0,115,116,5,8,0,0,116,117,3,8,4,0,117,21,1,0,
        0,0,118,119,5,10,0,0,119,120,5,1,0,0,120,121,5,21,0,0,121,23,1,0,
        0,0,122,124,5,10,0,0,123,125,5,11,0,0,124,123,1,0,0,0,124,125,1,
        0,0,0,125,126,1,0,0,0,126,127,5,5,0,0,127,129,3,30,15,0,128,130,
        3,46,23,0,129,128,1,0,0,0,129,130,1,0,0,0,130,136,1,0,0,0,131,133,
        5,40,0,0,132,134,3,42,21,0,133,132,1,0,0,0,133,134,1,0,0,0,134,135,
        1,0,0,0,135,137,5,41,0,0,136,131,1,0,0,0,136,137,1,0,0,0,137,140,
        1,0,0,0,138,139,5,46,0,0,139,141,3,2,1,0,140,138,1,0,0,0,140,141,
        1,0,0,0,141,25,1,0,0,0,142,143,5,10,0,0,143,144,5,15,0,0,144,146,
        5,21,0,0,145,147,3,46,23,0,146,145,1,0,0,0,146,147,1,0,0,0,147,148,
        1,0,0,0,148,152,5,42,0,0,149,151,3,24,12,0,150,149,1,0,0,0,151,154,
        1,0,0,0,152,150,1,0,0,0,152,153,1,0,0,0,153,155,1,0,0,0,154,152,
        1,0,0,0,155,156,5,43,0,0,156,27,1,0,0,0,157,161,3,22,11,0,158,161,
        3,24,12,0,159,161,3,26,13,0,160,157,1,0,0,0,160,158,1,0,0,0,160,
        159,1,0,0,0,161,29,1,0,0,0,162,174,5,21,0,0,163,174,5,4,0,0,164,
        165,3,2,1,0,165,166,5,37,0,0,166,167,5,21,0,0,167,174,1,0,0,0,168,
        169,3,2,1,0,169,170,5,37,0,0,170,171,5,4,0,0,171,174,1,0,0,0,172,
        174,7,0,0,0,173,162,1,0,0,0,173,163,1,0,0,0,173,164,1,0,0,0,173,
        168,1,0,0,0,173,172,1,0,0,0,174,31,1,0,0,0,175,176,5,5,0,0,176,177,
        3,30,15,0,177,179,5,40,0,0,178,180,3,42,21,0,179,178,1,0,0,0,179,
        180,1,0,0,0,180,181,1,0,0,0,181,184,5,41,0,0,182,183,5,46,0,0,183,
        185,3,2,1,0,184,182,1,0,0,0,184,185,1,0,0,0,185,186,1,0,0,0,186,
        187,3,8,4,0,187,33,1,0,0,0,188,190,5,21,0,0,189,191,7,1,0,0,190,
        189,1,0,0,0,190,191,1,0,0,0,191,192,1,0,0,0,192,193,5,39,0,0,193,
        204,3,48,24,0,194,196,5,7,0,0,195,194,1,0,0,0,195,196,1,0,0,0,196,
        198,1,0,0,0,197,199,3,2,1,0,198,197,1,0,0,0,198,199,1,0,0,0,199,
        200,1,0,0,0,200,201,5,21,0,0,201,202,5,39,0,0,202,204,3,48,24,0,
        203,188,1,0,0,0,203,195,1,0,0,0,204,35,1,0,0,0,205,206,3,48,24,0,
        206,37,1,0,0,0,207,212,3,36,18,0,208,209,5,38,0,0,209,211,3,36,18,
        0,210,208,1,0,0,0,211,214,1,0,0,0,212,210,1,0,0,0,212,213,1,0,0,
        0,213,39,1,0,0,0,214,212,1,0,0,0,215,217,5,7,0,0,216,215,1,0,0,0,
        216,217,1,0,0,0,217,218,1,0,0,0,218,219,3,2,1,0,219,220,5,21,0,0,
        220,41,1,0,0,0,221,226,3,40,20,0,222,223,5,38,0,0,223,225,3,40,20,
        0,224,222,1,0,0,0,225,228,1,0,0,0,226,224,1,0,0,0,226,227,1,0,0,
        0,227,43,1,0,0,0,228,226,1,0,0,0,229,230,5,21,0,0,230,45,1,0,0,0,
        231,232,5,31,0,0,232,237,3,44,22,0,233,234,5,38,0,0,234,236,3,44,
        22,0,235,233,1,0,0,0,236,239,1,0,0,0,237,235,1,0,0,0,237,238,1,0,
        0,0,238,240,1,0,0,0,239,237,1,0,0,0,240,241,5,30,0,0,241,47,1,0,
        0,0,242,243,6,24,-1,0,243,244,5,40,0,0,244,245,3,2,1,0,245,246,5,
        41,0,0,246,247,3,48,24,19,247,285,1,0,0,0,248,249,5,21,0,0,249,251,
        5,40,0,0,250,252,3,38,19,0,251,250,1,0,0,0,251,252,1,0,0,0,252,253,
        1,0,0,0,253,285,5,41,0,0,254,255,5,40,0,0,255,256,3,48,24,0,256,
        257,5,41,0,0,257,285,1,0,0,0,258,285,5,17,0,0,259,285,5,18,0,0,260,
        285,5,19,0,0,261,285,5,20,0,0,262,285,5,21,0,0,263,264,5,22,0,0,
        264,285,3,48,24,11,265,266,5,4,0,0,266,267,3,2,1,0,267,269,5,40,
        0,0,268,270,3,38,19,0,269,268,1,0,0,0,269,270,1,0,0,0,270,271,1,
        0,0,0,271,272,5,41,0,0,272,285,1,0,0,0,273,274,5,4,0,0,274,275,3,
        2,1,0,275,276,5,44,0,0,276,277,5,45,0,0,277,285,1,0,0,0,278,279,
        5,44,0,0,279,280,3,38,19,0,280,281,5,45,0,0,281,285,1,0,0,0,282,
        283,7,2,0,0,283,285,3,48,24,1,284,242,1,0,0,0,284,248,1,0,0,0,284,
        254,1,0,0,0,284,258,1,0,0,0,284,259,1,0,0,0,284,260,1,0,0,0,284,
        261,1,0,0,0,284,262,1,0,0,0,284,263,1,0,0,0,284,265,1,0,0,0,284,
        273,1,0,0,0,284,278,1,0,0,0,284,282,1,0,0,0,285,316,1,0,0,0,286,
        287,10,7,0,0,287,288,5,2,0,0,288,289,3,48,24,0,289,290,5,6,0,0,290,
        291,3,48,24,8,291,315,1,0,0,0,292,293,10,5,0,0,293,294,7,3,0,0,294,
        315,3,48,24,6,295,296,10,4,0,0,296,297,7,4,0,0,297,315,3,48,24,5,
        298,299,10,3,0,0,299,300,7,5,0,0,300,315,3,48,24,4,301,302,10,2,
        0,0,302,303,7,6,0,0,303,315,3,48,24,3,304,305,10,6,0,0,305,306,5,
        37,0,0,306,312,5,21,0,0,307,309,5,40,0,0,308,310,3,38,19,0,309,308,
        1,0,0,0,309,310,1,0,0,0,310,311,1,0,0,0,311,313,5,41,0,0,312,307,
        1,0,0,0,312,313,1,0,0,0,313,315,1,0,0,0,314,286,1,0,0,0,314,292,
        1,0,0,0,314,295,1,0,0,0,314,298,1,0,0,0,314,301,1,0,0,0,314,304,
        1,0,0,0,315,318,1,0,0,0,316,314,1,0,0,0,316,317,1,0,0,0,317,49,1,
        0,0,0,318,316,1,0,0,0,33,53,60,70,77,83,94,98,124,129,133,136,140,
        146,152,160,173,179,184,190,195,198,203,212,216,226,237,251,269,
        284,309,312,314,316
    ]

class CureParser ( Parser ):

    grammarFileName = "Cure.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'type'", "'if'", "'use'", "'new'", "'fn'", 
                     "'else'", "'mut'", "'unsafe'", "'return'", "'extern'", 
                     "'static'", "'while'", "'break'", "'continue'", "'class'", 
                     "'''", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'&'", "'+'", "'-'", "'*'", "'/'", "'%'", 
                     "'=='", "'!='", "'>'", "'<'", "'>='", "'<='", "'&&'", 
                     "'||'", "'!'", "'.'", "','", "'='", "'('", "')'", "'{'", 
                     "'}'", "'['", "']'", "'->'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "IF", "USE", "NEW", "FUNC", 
                      "ELSE", "MUTABLE", "UNSAFE", "RETURN", "EXTERN", "STATIC", 
                      "WHILE", "BREAK", "CONTINUE", "CLASS", "APOSTROPHE", 
                      "INT", "FLOAT", "STRING", "BOOL", "ID", "AMPERSAND", 
                      "ADD", "SUB", "MUL", "DIV", "MOD", "EEQ", "NEQ", "GT", 
                      "LT", "GTE", "LTE", "AND", "OR", "NOT", "DOT", "COMMA", 
                      "ASSIGN", "LPAREN", "RPAREN", "LBRACE", "RBRACE", 
                      "LBRACK", "RBRACK", "RETURNS", "COMMENT", "MULTILINE_COMMENT", 
                      "WHITESPACE", "OTHER" ]

    RULE_program = 0
    RULE_type = 1
    RULE_stmt = 2
    RULE_bodyStmt = 3
    RULE_body = 4
    RULE_ifStmt = 5
    RULE_elseifStmt = 6
    RULE_elseStmt = 7
    RULE_whileStmt = 8
    RULE_useStmt = 9
    RULE_unsafeStmt = 10
    RULE_externType = 11
    RULE_externFunc = 12
    RULE_externClass = 13
    RULE_externStmt = 14
    RULE_funcName = 15
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
                   "elseifStmt", "elseStmt", "whileStmt", "useStmt", "unsafeStmt", 
                   "externType", "externFunc", "externClass", "externStmt", 
                   "funcName", "funcAssign", "varAssign", "arg", "args", 
                   "param", "params", "genericParam", "genericParams", "expr" ]

    EOF = Token.EOF
    T__0=1
    IF=2
    USE=3
    NEW=4
    FUNC=5
    ELSE=6
    MUTABLE=7
    UNSAFE=8
    RETURN=9
    EXTERN=10
    STATIC=11
    WHILE=12
    BREAK=13
    CONTINUE=14
    CLASS=15
    APOSTROPHE=16
    INT=17
    FLOAT=18
    STRING=19
    BOOL=20
    ID=21
    AMPERSAND=22
    ADD=23
    SUB=24
    MUL=25
    DIV=26
    MOD=27
    EEQ=28
    NEQ=29
    GT=30
    LT=31
    GTE=32
    LTE=33
    AND=34
    OR=35
    NOT=36
    DOT=37
    COMMA=38
    ASSIGN=39
    LPAREN=40
    RPAREN=41
    LBRACE=42
    RBRACE=43
    LBRACK=44
    RBRACK=45
    RETURNS=46
    COMMENT=47
    MULTILINE_COMMENT=48
    WHITESPACE=49
    OTHER=50

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
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 18760450577852) != 0):
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

        def AMPERSAND(self):
            return self.getToken(CureParser.AMPERSAND, 0)

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
            self.state = 58
            self.match(CureParser.ID)
            self.state = 60
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.state = 59
                self.match(CureParser.AMPERSAND)


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


        def useStmt(self):
            return self.getTypedRuleContext(CureParser.UseStmtContext,0)


        def unsafeStmt(self):
            return self.getTypedRuleContext(CureParser.UnsafeStmtContext,0)


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
            self.state = 70
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 62
                self.varAssign()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 63
                self.funcAssign()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 64
                self.whileStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 65
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 66
                self.useStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 67
                self.unsafeStmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 68
                self.externStmt()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 69
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

        def stmt(self):
            return self.getTypedRuleContext(CureParser.StmtContext,0)


        def RETURN(self):
            return self.getToken(CureParser.RETURN, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def BREAK(self):
            return self.getToken(CureParser.BREAK, 0)

        def CONTINUE(self):
            return self.getToken(CureParser.CONTINUE, 0)

        def getRuleIndex(self):
            return CureParser.RULE_bodyStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBodyStmt" ):
                return visitor.visitBodyStmt(self)
            else:
                return visitor.visitChildren(self)




    def bodyStmt(self):

        localctx = CureParser.BodyStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_bodyStmt)
        try:
            self.state = 77
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2, 3, 4, 5, 7, 8, 10, 12, 17, 18, 19, 20, 21, 22, 23, 24, 36, 40, 44]:
                self.enterOuterAlt(localctx, 1)
                self.state = 72
                self.stmt()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 2)
                self.state = 73
                self.match(CureParser.RETURN)
                self.state = 74
                self.expr(0)
                pass
            elif token in [13]:
                self.enterOuterAlt(localctx, 3)
                self.state = 75
                self.match(CureParser.BREAK)
                pass
            elif token in [14]:
                self.enterOuterAlt(localctx, 4)
                self.state = 76
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
            self.state = 79
            self.match(CureParser.LBRACE)
            self.state = 83
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 18760450602940) != 0):
                self.state = 80
                self.bodyStmt()
                self.state = 85
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 86
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
            self.state = 88
            self.match(CureParser.IF)
            self.state = 89
            self.expr(0)
            self.state = 90
            self.body()
            self.state = 94
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 91
                    self.elseifStmt() 
                self.state = 96
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

            self.state = 98
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 97
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
            self.state = 100
            self.match(CureParser.ELSE)
            self.state = 101
            self.match(CureParser.IF)
            self.state = 102
            self.expr(0)
            self.state = 103
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
            self.state = 105
            self.match(CureParser.ELSE)
            self.state = 106
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
            self.state = 108
            self.match(CureParser.WHILE)
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
        self.enterRule(localctx, 18, self.RULE_useStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            self.match(CureParser.USE)
            self.state = 113
            self.match(CureParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnsafeStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def UNSAFE(self):
            return self.getToken(CureParser.UNSAFE, 0)

        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_unsafeStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnsafeStmt" ):
                return visitor.visitUnsafeStmt(self)
            else:
                return visitor.visitChildren(self)




    def unsafeStmt(self):

        localctx = CureParser.UnsafeStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_unsafeStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.match(CureParser.UNSAFE)
            self.state = 116
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExternTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXTERN(self):
            return self.getToken(CureParser.EXTERN, 0)

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def getRuleIndex(self):
            return CureParser.RULE_externType

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExternType" ):
                return visitor.visitExternType(self)
            else:
                return visitor.visitChildren(self)




    def externType(self):

        localctx = CureParser.ExternTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_externType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.match(CureParser.EXTERN)
            self.state = 119
            self.match(CureParser.T__0)
            self.state = 120
            self.match(CureParser.ID)
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
            self.return_type = None # TypeContext

        def EXTERN(self):
            return self.getToken(CureParser.EXTERN, 0)

        def FUNC(self):
            return self.getToken(CureParser.FUNC, 0)

        def funcName(self):
            return self.getTypedRuleContext(CureParser.FuncNameContext,0)


        def STATIC(self):
            return self.getToken(CureParser.STATIC, 0)

        def genericParams(self):
            return self.getTypedRuleContext(CureParser.GenericParamsContext,0)


        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)

        def RETURNS(self):
            return self.getToken(CureParser.RETURNS, 0)

        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


        def params(self):
            return self.getTypedRuleContext(CureParser.ParamsContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_externFunc

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExternFunc" ):
                return visitor.visitExternFunc(self)
            else:
                return visitor.visitChildren(self)




    def externFunc(self):

        localctx = CureParser.ExternFuncContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_externFunc)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 122
            self.match(CureParser.EXTERN)
            self.state = 124
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11:
                self.state = 123
                self.match(CureParser.STATIC)


            self.state = 126
            self.match(CureParser.FUNC)
            self.state = 127
            self.funcName()
            self.state = 129
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==31:
                self.state = 128
                self.genericParams()


            self.state = 136
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.state = 131
                self.match(CureParser.LPAREN)
                self.state = 133
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7 or _la==21:
                    self.state = 132
                    self.params()


                self.state = 135
                self.match(CureParser.RPAREN)


            self.state = 140
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==46:
                self.state = 138
                self.match(CureParser.RETURNS)
                self.state = 139
                localctx.return_type = self.type_()


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

        def LBRACE(self):
            return self.getToken(CureParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(CureParser.RBRACE, 0)

        def genericParams(self):
            return self.getTypedRuleContext(CureParser.GenericParamsContext,0)


        def externFunc(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExternFuncContext)
            else:
                return self.getTypedRuleContext(CureParser.ExternFuncContext,i)


        def getRuleIndex(self):
            return CureParser.RULE_externClass

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExternClass" ):
                return visitor.visitExternClass(self)
            else:
                return visitor.visitChildren(self)




    def externClass(self):

        localctx = CureParser.ExternClassContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_externClass)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 142
            self.match(CureParser.EXTERN)
            self.state = 143
            self.match(CureParser.CLASS)
            self.state = 144
            self.match(CureParser.ID)
            self.state = 146
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==31:
                self.state = 145
                self.genericParams()


            self.state = 148
            self.match(CureParser.LBRACE)
            self.state = 152
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10:
                self.state = 149
                self.externFunc()
                self.state = 154
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 155
            self.match(CureParser.RBRACE)
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

        def externType(self):
            return self.getTypedRuleContext(CureParser.ExternTypeContext,0)


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
        self.enterRule(localctx, 28, self.RULE_externStmt)
        try:
            self.state = 160
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 157
                self.externType()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 158
                self.externFunc()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 159
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
            self.op = None # Token

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def NEW(self):
            return self.getToken(CureParser.NEW, 0)

        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


        def DOT(self):
            return self.getToken(CureParser.DOT, 0)

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

        def EEQ(self):
            return self.getToken(CureParser.EEQ, 0)

        def NEQ(self):
            return self.getToken(CureParser.NEQ, 0)

        def LT(self):
            return self.getToken(CureParser.LT, 0)

        def GT(self):
            return self.getToken(CureParser.GT, 0)

        def LTE(self):
            return self.getToken(CureParser.LTE, 0)

        def GTE(self):
            return self.getToken(CureParser.GTE, 0)

        def AND(self):
            return self.getToken(CureParser.AND, 0)

        def OR(self):
            return self.getToken(CureParser.OR, 0)

        def NOT(self):
            return self.getToken(CureParser.NOT, 0)

        def getRuleIndex(self):
            return CureParser.RULE_funcName

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncName" ):
                return visitor.visitFuncName(self)
            else:
                return visitor.visitChildren(self)




    def funcName(self):

        localctx = CureParser.FuncNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_funcName)
        self._la = 0 # Token type
        try:
            self.state = 173
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 162
                self.match(CureParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 163
                self.match(CureParser.NEW)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 164
                self.type_()
                self.state = 165
                self.match(CureParser.DOT)
                self.state = 166
                self.match(CureParser.ID)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 168
                self.type_()
                self.state = 169
                self.match(CureParser.DOT)
                self.state = 170
                self.match(CureParser.NEW)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 172
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 137430564864) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass


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
            self.return_type = None # TypeContext

        def FUNC(self):
            return self.getToken(CureParser.FUNC, 0)

        def funcName(self):
            return self.getTypedRuleContext(CureParser.FuncNameContext,0)


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
        self.enterRule(localctx, 32, self.RULE_funcAssign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175
            self.match(CureParser.FUNC)
            self.state = 176
            self.funcName()
            self.state = 177
            self.match(CureParser.LPAREN)
            self.state = 179
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7 or _la==21:
                self.state = 178
                self.params()


            self.state = 181
            self.match(CureParser.RPAREN)
            self.state = 184
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==46:
                self.state = 182
                self.match(CureParser.RETURNS)
                self.state = 183
                localctx.return_type = self.type_()


            self.state = 186
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

        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


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
            self.state = 203
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 188
                self.match(CureParser.ID)
                self.state = 190
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 260046848) != 0):
                    self.state = 189
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 260046848) != 0)):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 192
                self.match(CureParser.ASSIGN)
                self.state = 193
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 195
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 194
                    self.match(CureParser.MUTABLE)


                self.state = 198
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
                if la_ == 1:
                    self.state = 197
                    self.type_()


                self.state = 200
                self.match(CureParser.ID)
                self.state = 201
                self.match(CureParser.ASSIGN)
                self.state = 202
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
            self.state = 205
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
            self.state = 207
            self.arg()
            self.state = 212
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 208
                self.match(CureParser.COMMA)
                self.state = 209
                self.arg()
                self.state = 214
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
            self.state = 216
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 215
                self.match(CureParser.MUTABLE)


            self.state = 218
            self.type_()
            self.state = 219
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
            self.state = 221
            self.param()
            self.state = 226
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 222
                self.match(CureParser.COMMA)
                self.state = 223
                self.param()
                self.state = 228
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
            self.state = 229
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
            self.state = 231
            self.match(CureParser.LT)
            self.state = 232
            self.genericParam()
            self.state = 237
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 233
                self.match(CureParser.COMMA)
                self.state = 234
                self.genericParam()
                self.state = 239
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 240
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


    class ArrayInitContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LBRACK(self):
            return self.getToken(CureParser.LBRACK, 0)
        def args(self):
            return self.getTypedRuleContext(CureParser.ArgsContext,0)

        def RBRACK(self):
            return self.getToken(CureParser.RBRACK, 0)

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


    class RefContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def AMPERSAND(self):
            return self.getToken(CureParser.AMPERSAND, 0)
        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRef" ):
                return visitor.visitRef(self)
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
            self.state = 284
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
            if la_ == 1:
                localctx = CureParser.CastContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 243
                self.match(CureParser.LPAREN)
                self.state = 244
                self.type_()
                self.state = 245
                self.match(CureParser.RPAREN)
                self.state = 246
                self.expr(19)
                pass

            elif la_ == 2:
                localctx = CureParser.CallContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 248
                self.match(CureParser.ID)
                self.state = 249
                self.match(CureParser.LPAREN)
                self.state = 251
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 18760450572304) != 0):
                    self.state = 250
                    self.args()


                self.state = 253
                self.match(CureParser.RPAREN)
                pass

            elif la_ == 3:
                localctx = CureParser.ParenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 254
                self.match(CureParser.LPAREN)
                self.state = 255
                self.expr(0)
                self.state = 256
                self.match(CureParser.RPAREN)
                pass

            elif la_ == 4:
                localctx = CureParser.IntContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 258
                self.match(CureParser.INT)
                pass

            elif la_ == 5:
                localctx = CureParser.FloatContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 259
                self.match(CureParser.FLOAT)
                pass

            elif la_ == 6:
                localctx = CureParser.StringContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 260
                self.match(CureParser.STRING)
                pass

            elif la_ == 7:
                localctx = CureParser.BoolContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 261
                self.match(CureParser.BOOL)
                pass

            elif la_ == 8:
                localctx = CureParser.IdContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 262
                self.match(CureParser.ID)
                pass

            elif la_ == 9:
                localctx = CureParser.RefContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 263
                self.match(CureParser.AMPERSAND)
                self.state = 264
                self.expr(11)
                pass

            elif la_ == 10:
                localctx = CureParser.NewContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 265
                self.match(CureParser.NEW)
                self.state = 266
                self.type_()
                self.state = 267
                self.match(CureParser.LPAREN)
                self.state = 269
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 18760450572304) != 0):
                    self.state = 268
                    self.args()


                self.state = 271
                self.match(CureParser.RPAREN)
                pass

            elif la_ == 11:
                localctx = CureParser.NewArrayContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 273
                self.match(CureParser.NEW)
                self.state = 274
                self.type_()
                self.state = 275
                self.match(CureParser.LBRACK)
                self.state = 276
                self.match(CureParser.RBRACK)
                pass

            elif la_ == 12:
                localctx = CureParser.ArrayInitContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 278
                self.match(CureParser.LBRACK)
                self.state = 279
                self.args()
                self.state = 280
                self.match(CureParser.RBRACK)
                pass

            elif la_ == 13:
                localctx = CureParser.UnaryContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 282
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 68744642560) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 283
                self.expr(1)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 316
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,32,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 314
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,31,self._ctx)
                    if la_ == 1:
                        localctx = CureParser.TernaryContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 286
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 287
                        self.match(CureParser.IF)
                        self.state = 288
                        self.expr(0)
                        self.state = 289
                        self.match(CureParser.ELSE)
                        self.state = 290
                        self.expr(8)
                        pass

                    elif la_ == 2:
                        localctx = CureParser.MultiplicationContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 292
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 293
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 234881024) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 294
                        self.expr(6)
                        pass

                    elif la_ == 3:
                        localctx = CureParser.AdditionContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 295
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 296
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==23 or _la==24):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 297
                        self.expr(5)
                        pass

                    elif la_ == 4:
                        localctx = CureParser.RelationalContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 298
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 299
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 16911433728) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 300
                        self.expr(4)
                        pass

                    elif la_ == 5:
                        localctx = CureParser.LogicalContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 301
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 302
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==34 or _la==35):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 303
                        self.expr(3)
                        pass

                    elif la_ == 6:
                        localctx = CureParser.AttrContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 304
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 305
                        self.match(CureParser.DOT)
                        self.state = 306
                        self.match(CureParser.ID)
                        self.state = 312
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
                        if la_ == 1:
                            self.state = 307
                            self.match(CureParser.LPAREN)
                            self.state = 309
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 18760450572304) != 0):
                                self.state = 308
                                self.args()


                            self.state = 311
                            self.match(CureParser.RPAREN)


                        pass

             
                self.state = 318
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,32,self._ctx)

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
        self._predicates[24] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 6)
         




