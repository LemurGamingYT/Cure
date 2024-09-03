# Generated from ir/Cure.g4 by ANTLR 4.13.0
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
        4,1,51,317,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,1,0,5,0,48,8,0,10,0,12,0,51,9,0,1,0,1,0,
        1,1,1,1,1,1,1,1,1,1,3,1,60,8,1,1,1,1,1,3,1,64,8,1,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,1,2,3,2,74,8,2,1,3,1,3,1,3,1,3,1,3,3,3,81,8,3,1,4,
        1,4,5,4,85,8,4,10,4,12,4,88,9,4,1,4,1,4,1,5,1,5,1,5,1,5,5,5,96,8,
        5,10,5,12,5,99,9,5,1,5,3,5,102,8,5,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,
        7,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,9,1,10,1,10,1,10,1,11,1,
        11,1,11,1,11,1,11,1,11,5,11,131,8,11,10,11,12,11,134,9,11,3,11,136,
        8,11,1,11,1,11,1,12,1,12,1,12,1,12,3,12,144,8,12,1,12,1,12,1,12,
        1,13,5,13,150,8,13,10,13,12,13,153,9,13,1,13,1,13,1,13,1,13,3,13,
        159,8,13,1,13,1,13,1,13,3,13,164,8,13,1,13,1,13,1,14,3,14,169,8,
        14,1,14,3,14,172,8,14,1,14,1,14,3,14,176,8,14,1,14,1,14,1,14,1,15,
        1,15,3,15,183,8,15,1,15,1,15,1,16,1,16,1,16,5,16,190,8,16,10,16,
        12,16,193,9,16,1,17,1,17,3,17,197,8,17,1,17,1,17,1,17,3,17,202,8,
        17,1,18,1,18,1,18,5,18,207,8,18,10,18,12,18,210,9,18,1,19,1,19,1,
        19,1,19,1,20,1,20,1,20,3,20,219,8,20,1,20,1,20,1,21,1,21,1,21,3,
        21,226,8,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,
        21,5,21,239,8,21,10,21,12,21,242,9,21,3,21,244,8,21,1,21,1,21,1,
        21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,3,21,258,8,21,1,
        22,1,22,1,22,1,22,1,22,1,22,1,22,3,22,267,8,22,1,22,1,22,1,22,1,
        22,1,22,1,22,1,22,1,22,3,22,277,8,22,1,22,1,22,1,22,1,22,1,22,1,
        22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,
        22,1,22,1,22,1,22,1,22,3,22,302,8,22,1,22,3,22,305,8,22,1,22,1,22,
        1,22,1,22,1,22,5,22,312,8,22,10,22,12,22,315,9,22,1,22,0,1,44,23,
        0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,
        0,6,1,0,21,25,2,0,21,22,34,34,1,0,23,25,1,0,21,22,1,0,26,31,1,0,
        32,33,349,0,49,1,0,0,0,2,54,1,0,0,0,4,73,1,0,0,0,6,80,1,0,0,0,8,
        82,1,0,0,0,10,91,1,0,0,0,12,103,1,0,0,0,14,108,1,0,0,0,16,111,1,
        0,0,0,18,115,1,0,0,0,20,121,1,0,0,0,22,124,1,0,0,0,24,139,1,0,0,
        0,26,151,1,0,0,0,28,168,1,0,0,0,30,182,1,0,0,0,32,186,1,0,0,0,34,
        194,1,0,0,0,36,203,1,0,0,0,38,211,1,0,0,0,40,215,1,0,0,0,42,257,
        1,0,0,0,44,276,1,0,0,0,46,48,3,4,2,0,47,46,1,0,0,0,48,51,1,0,0,0,
        49,47,1,0,0,0,49,50,1,0,0,0,50,52,1,0,0,0,51,49,1,0,0,0,52,53,5,
        0,0,1,53,1,1,0,0,0,54,63,5,20,0,0,55,56,5,43,0,0,56,59,3,2,1,0,57,
        58,5,37,0,0,58,60,3,2,1,0,59,57,1,0,0,0,59,60,1,0,0,0,60,61,1,0,
        0,0,61,62,5,44,0,0,62,64,1,0,0,0,63,55,1,0,0,0,63,64,1,0,0,0,64,
        3,1,0,0,0,65,74,3,26,13,0,66,74,3,18,9,0,67,74,3,16,8,0,68,74,3,
        10,5,0,69,74,3,28,14,0,70,74,3,44,22,0,71,74,3,22,11,0,72,74,3,20,
        10,0,73,65,1,0,0,0,73,66,1,0,0,0,73,67,1,0,0,0,73,68,1,0,0,0,73,
        69,1,0,0,0,73,70,1,0,0,0,73,71,1,0,0,0,73,72,1,0,0,0,74,5,1,0,0,
        0,75,81,3,4,2,0,76,77,5,11,0,0,77,81,3,44,22,0,78,81,5,13,0,0,79,
        81,5,9,0,0,80,75,1,0,0,0,80,76,1,0,0,0,80,78,1,0,0,0,80,79,1,0,0,
        0,81,7,1,0,0,0,82,86,5,41,0,0,83,85,3,6,3,0,84,83,1,0,0,0,85,88,
        1,0,0,0,86,84,1,0,0,0,86,87,1,0,0,0,87,89,1,0,0,0,88,86,1,0,0,0,
        89,90,5,42,0,0,90,9,1,0,0,0,91,92,5,1,0,0,92,93,3,44,22,0,93,97,
        3,8,4,0,94,96,3,12,6,0,95,94,1,0,0,0,96,99,1,0,0,0,97,95,1,0,0,0,
        97,98,1,0,0,0,98,101,1,0,0,0,99,97,1,0,0,0,100,102,3,14,7,0,101,
        100,1,0,0,0,101,102,1,0,0,0,102,11,1,0,0,0,103,104,5,6,0,0,104,105,
        5,1,0,0,105,106,3,44,22,0,106,107,3,8,4,0,107,13,1,0,0,0,108,109,
        5,6,0,0,109,110,3,8,4,0,110,15,1,0,0,0,111,112,5,8,0,0,112,113,3,
        44,22,0,113,114,3,8,4,0,114,17,1,0,0,0,115,116,5,12,0,0,116,117,
        5,20,0,0,117,118,5,2,0,0,118,119,3,44,22,0,119,120,3,8,4,0,120,19,
        1,0,0,0,121,122,5,4,0,0,122,123,5,17,0,0,123,21,1,0,0,0,124,125,
        5,5,0,0,125,126,5,20,0,0,126,135,5,41,0,0,127,132,5,20,0,0,128,129,
        5,36,0,0,129,131,5,20,0,0,130,128,1,0,0,0,131,134,1,0,0,0,132,130,
        1,0,0,0,132,133,1,0,0,0,133,136,1,0,0,0,134,132,1,0,0,0,135,127,
        1,0,0,0,135,136,1,0,0,0,136,137,1,0,0,0,137,138,5,42,0,0,138,23,
        1,0,0,0,139,140,5,43,0,0,140,141,5,20,0,0,141,143,5,39,0,0,142,144,
        3,32,16,0,143,142,1,0,0,0,143,144,1,0,0,0,144,145,1,0,0,0,145,146,
        5,40,0,0,146,147,5,44,0,0,147,25,1,0,0,0,148,150,3,24,12,0,149,148,
        1,0,0,0,150,153,1,0,0,0,151,149,1,0,0,0,151,152,1,0,0,0,152,154,
        1,0,0,0,153,151,1,0,0,0,154,155,5,7,0,0,155,156,5,20,0,0,156,158,
        5,39,0,0,157,159,3,36,18,0,158,157,1,0,0,0,158,159,1,0,0,0,159,160,
        1,0,0,0,160,163,5,40,0,0,161,162,5,46,0,0,162,164,3,2,1,0,163,161,
        1,0,0,0,163,164,1,0,0,0,164,165,1,0,0,0,165,166,3,8,4,0,166,27,1,
        0,0,0,167,169,5,10,0,0,168,167,1,0,0,0,168,169,1,0,0,0,169,171,1,
        0,0,0,170,172,3,2,1,0,171,170,1,0,0,0,171,172,1,0,0,0,172,173,1,
        0,0,0,173,175,5,20,0,0,174,176,7,0,0,0,175,174,1,0,0,0,175,176,1,
        0,0,0,176,177,1,0,0,0,177,178,5,38,0,0,178,179,3,44,22,0,179,29,
        1,0,0,0,180,181,5,20,0,0,181,183,5,37,0,0,182,180,1,0,0,0,182,183,
        1,0,0,0,183,184,1,0,0,0,184,185,3,44,22,0,185,31,1,0,0,0,186,191,
        3,30,15,0,187,188,5,36,0,0,188,190,3,30,15,0,189,187,1,0,0,0,190,
        193,1,0,0,0,191,189,1,0,0,0,191,192,1,0,0,0,192,33,1,0,0,0,193,191,
        1,0,0,0,194,196,3,2,1,0,195,197,5,47,0,0,196,195,1,0,0,0,196,197,
        1,0,0,0,197,198,1,0,0,0,198,201,5,20,0,0,199,200,5,38,0,0,200,202,
        3,44,22,0,201,199,1,0,0,0,201,202,1,0,0,0,202,35,1,0,0,0,203,208,
        3,34,17,0,204,205,5,36,0,0,205,207,3,34,17,0,206,204,1,0,0,0,207,
        210,1,0,0,0,208,206,1,0,0,0,208,209,1,0,0,0,209,37,1,0,0,0,210,208,
        1,0,0,0,211,212,3,44,22,0,212,213,5,37,0,0,213,214,3,44,22,0,214,
        39,1,0,0,0,215,216,5,20,0,0,216,218,5,39,0,0,217,219,3,32,16,0,218,
        217,1,0,0,0,218,219,1,0,0,0,219,220,1,0,0,0,220,221,5,40,0,0,221,
        41,1,0,0,0,222,223,3,2,1,0,223,225,5,41,0,0,224,226,3,32,16,0,225,
        224,1,0,0,0,225,226,1,0,0,0,226,227,1,0,0,0,227,228,5,42,0,0,228,
        258,1,0,0,0,229,230,5,43,0,0,230,231,3,2,1,0,231,232,5,37,0,0,232,
        233,3,2,1,0,233,234,5,44,0,0,234,243,5,41,0,0,235,240,3,38,19,0,
        236,237,5,36,0,0,237,239,3,38,19,0,238,236,1,0,0,0,239,242,1,0,0,
        0,240,238,1,0,0,0,240,241,1,0,0,0,241,244,1,0,0,0,242,240,1,0,0,
        0,243,235,1,0,0,0,243,244,1,0,0,0,244,245,1,0,0,0,245,246,5,42,0,
        0,246,258,1,0,0,0,247,258,5,15,0,0,248,258,5,16,0,0,249,258,5,17,
        0,0,250,258,5,18,0,0,251,258,5,19,0,0,252,258,5,20,0,0,253,254,5,
        39,0,0,254,255,3,44,22,0,255,256,5,40,0,0,256,258,1,0,0,0,257,222,
        1,0,0,0,257,229,1,0,0,0,257,247,1,0,0,0,257,248,1,0,0,0,257,249,
        1,0,0,0,257,250,1,0,0,0,257,251,1,0,0,0,257,252,1,0,0,0,257,253,
        1,0,0,0,258,43,1,0,0,0,259,260,6,22,-1,0,260,277,3,40,20,0,261,277,
        3,42,21,0,262,263,5,3,0,0,263,264,5,20,0,0,264,266,5,39,0,0,265,
        267,3,32,16,0,266,265,1,0,0,0,266,267,1,0,0,0,267,268,1,0,0,0,268,
        277,5,40,0,0,269,270,5,39,0,0,270,271,3,2,1,0,271,272,5,40,0,0,272,
        273,3,44,22,7,273,277,1,0,0,0,274,275,7,1,0,0,275,277,3,44,22,1,
        276,259,1,0,0,0,276,261,1,0,0,0,276,262,1,0,0,0,276,269,1,0,0,0,
        276,274,1,0,0,0,277,313,1,0,0,0,278,279,10,9,0,0,279,280,5,1,0,0,
        280,281,3,44,22,0,281,282,5,6,0,0,282,283,3,44,22,10,283,312,1,0,
        0,0,284,285,10,5,0,0,285,286,7,2,0,0,286,312,3,44,22,6,287,288,10,
        4,0,0,288,289,7,3,0,0,289,312,3,44,22,5,290,291,10,3,0,0,291,292,
        7,4,0,0,292,312,3,44,22,4,293,294,10,2,0,0,294,295,7,5,0,0,295,312,
        3,44,22,3,296,297,10,10,0,0,297,298,5,35,0,0,298,304,5,20,0,0,299,
        301,5,39,0,0,300,302,3,32,16,0,301,300,1,0,0,0,301,302,1,0,0,0,302,
        303,1,0,0,0,303,305,5,40,0,0,304,299,1,0,0,0,304,305,1,0,0,0,305,
        312,1,0,0,0,306,307,10,6,0,0,307,308,5,43,0,0,308,309,3,44,22,0,
        309,310,5,44,0,0,310,312,1,0,0,0,311,278,1,0,0,0,311,284,1,0,0,0,
        311,287,1,0,0,0,311,290,1,0,0,0,311,293,1,0,0,0,311,296,1,0,0,0,
        311,306,1,0,0,0,312,315,1,0,0,0,313,311,1,0,0,0,313,314,1,0,0,0,
        314,45,1,0,0,0,315,313,1,0,0,0,33,49,59,63,73,80,86,97,101,132,135,
        143,151,158,163,168,171,175,182,191,196,201,208,218,225,240,243,
        257,266,276,301,304,311,313
    ]

class CureParser ( Parser ):

    grammarFileName = "Cure.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'in'", "'new'", "'use'", "'enum'", 
                     "'else'", "'func'", "'while'", "'break'", "'const'", 
                     "'return'", "'foreach'", "'continue'", "'''", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'nil'", "<INVALID>", 
                     "'+'", "'-'", "'*'", "'/'", "'%'", "'=='", "'!='", 
                     "'>'", "'<'", "'>='", "'<='", "'&&'", "'||'", "'!'", 
                     "'.'", "','", "':'", "'='", "'('", "')'", "'{'", "'}'", 
                     "'['", "']'", "'$'", "'->'", "'&'", "'=>'" ]

    symbolicNames = [ "<INVALID>", "IF", "IN", "NEW", "USE", "ENUM", "ELSE", 
                      "FUNC", "WHILE", "BREAK", "CONST", "RETURN", "FOREACH", 
                      "CONTINUE", "APOSTROPHE", "INT", "FLOAT", "STRING", 
                      "BOOL", "NIL", "ID", "ADD", "SUB", "MUL", "DIV", "MOD", 
                      "EEQ", "NEQ", "GT", "LT", "GTE", "LTE", "AND", "OR", 
                      "NOT", "DOT", "COMMA", "COLON", "ASSIGN", "LPAREN", 
                      "RPAREN", "LBRACE", "RBRACE", "LBRACK", "RBRACK", 
                      "DOLLAR", "RETURNS", "AMPERSAND", "ARROWASSIGN", "COMMENT", 
                      "MULTILINE_COMMENT", "WHITESPACE" ]

    RULE_parse = 0
    RULE_type = 1
    RULE_stmt = 2
    RULE_bodyStmts = 3
    RULE_body = 4
    RULE_ifStmt = 5
    RULE_elseifStmt = 6
    RULE_elseStmt = 7
    RULE_whileStmt = 8
    RULE_foreachStmt = 9
    RULE_useStmt = 10
    RULE_enumAssign = 11
    RULE_funcModifications = 12
    RULE_funcAssign = 13
    RULE_varAssign = 14
    RULE_arg = 15
    RULE_args = 16
    RULE_param = 17
    RULE_params = 18
    RULE_dict_element = 19
    RULE_call = 20
    RULE_atom = 21
    RULE_expr = 22

    ruleNames =  [ "parse", "type", "stmt", "bodyStmts", "body", "ifStmt", 
                   "elseifStmt", "elseStmt", "whileStmt", "foreachStmt", 
                   "useStmt", "enumAssign", "funcModifications", "funcAssign", 
                   "varAssign", "arg", "args", "param", "params", "dict_element", 
                   "call", "atom", "expr" ]

    EOF = Token.EOF
    IF=1
    IN=2
    NEW=3
    USE=4
    ENUM=5
    ELSE=6
    FUNC=7
    WHILE=8
    BREAK=9
    CONST=10
    RETURN=11
    FOREACH=12
    CONTINUE=13
    APOSTROPHE=14
    INT=15
    FLOAT=16
    STRING=17
    BOOL=18
    NIL=19
    ID=20
    ADD=21
    SUB=22
    MUL=23
    DIV=24
    MOD=25
    EEQ=26
    NEQ=27
    GT=28
    LT=29
    GTE=30
    LTE=31
    AND=32
    OR=33
    NOT=34
    DOT=35
    COMMA=36
    COLON=37
    ASSIGN=38
    LPAREN=39
    RPAREN=40
    LBRACE=41
    RBRACE=42
    LBRACK=43
    RBRACK=44
    DOLLAR=45
    RETURNS=46
    AMPERSAND=47
    ARROWASSIGN=48
    COMMENT=49
    MULTILINE_COMMENT=50
    WHITESPACE=51

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
            self.state = 49
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 9363037066682) != 0):
                self.state = 46
                self.stmt()
                self.state = 51
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 52
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

        def LBRACK(self):
            return self.getToken(CureParser.LBRACK, 0)

        def type_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.TypeContext)
            else:
                return self.getTypedRuleContext(CureParser.TypeContext,i)


        def RBRACK(self):
            return self.getToken(CureParser.RBRACK, 0)

        def COLON(self):
            return self.getToken(CureParser.COLON, 0)

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
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self.match(CureParser.ID)
            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==43:
                self.state = 55
                self.match(CureParser.LBRACK)
                self.state = 56
                self.type_()
                self.state = 59
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==37:
                    self.state = 57
                    self.match(CureParser.COLON)
                    self.state = 58
                    self.type_()


                self.state = 61
                self.match(CureParser.RBRACK)


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

        def funcAssign(self):
            return self.getTypedRuleContext(CureParser.FuncAssignContext,0)


        def foreachStmt(self):
            return self.getTypedRuleContext(CureParser.ForeachStmtContext,0)


        def whileStmt(self):
            return self.getTypedRuleContext(CureParser.WhileStmtContext,0)


        def ifStmt(self):
            return self.getTypedRuleContext(CureParser.IfStmtContext,0)


        def varAssign(self):
            return self.getTypedRuleContext(CureParser.VarAssignContext,0)


        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def enumAssign(self):
            return self.getTypedRuleContext(CureParser.EnumAssignContext,0)


        def useStmt(self):
            return self.getTypedRuleContext(CureParser.UseStmtContext,0)


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
            self.state = 73
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 65
                self.funcAssign()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 66
                self.foreachStmt()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 67
                self.whileStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 68
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 69
                self.varAssign()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 70
                self.expr(0)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 71
                self.enumAssign()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 72
                self.useStmt()
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
            self.state = 80
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 3, 4, 5, 7, 8, 10, 12, 15, 16, 17, 18, 19, 20, 21, 22, 34, 39, 43]:
                self.enterOuterAlt(localctx, 1)
                self.state = 75
                self.stmt()
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 2)
                self.state = 76
                self.match(CureParser.RETURN)
                self.state = 77
                self.expr(0)
                pass
            elif token in [13]:
                self.enterOuterAlt(localctx, 3)
                self.state = 78
                self.match(CureParser.CONTINUE)
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 4)
                self.state = 79
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
            self.state = 82
            self.match(CureParser.LBRACE)
            self.state = 86
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 9363037077434) != 0):
                self.state = 83
                self.bodyStmts()
                self.state = 88
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 89
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
            self.state = 91
            self.match(CureParser.IF)
            self.state = 92
            self.expr(0)
            self.state = 93
            self.body()
            self.state = 97
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 94
                    self.elseifStmt() 
                self.state = 99
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

            self.state = 101
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 100
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
            self.state = 103
            self.match(CureParser.ELSE)
            self.state = 104
            self.match(CureParser.IF)
            self.state = 105
            self.expr(0)
            self.state = 106
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
            self.state = 108
            self.match(CureParser.ELSE)
            self.state = 109
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
            self.state = 111
            self.match(CureParser.WHILE)
            self.state = 112
            self.expr(0)
            self.state = 113
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForeachStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOREACH(self):
            return self.getToken(CureParser.FOREACH, 0)

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def IN(self):
            return self.getToken(CureParser.IN, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_foreachStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForeachStmt" ):
                return visitor.visitForeachStmt(self)
            else:
                return visitor.visitChildren(self)




    def foreachStmt(self):

        localctx = CureParser.ForeachStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_foreachStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.match(CureParser.FOREACH)
            self.state = 116
            self.match(CureParser.ID)
            self.state = 117
            self.match(CureParser.IN)
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
            self.state = 121
            self.match(CureParser.USE)
            self.state = 122
            self.match(CureParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnumAssignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENUM(self):
            return self.getToken(CureParser.ENUM, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(CureParser.ID)
            else:
                return self.getToken(CureParser.ID, i)

        def LBRACE(self):
            return self.getToken(CureParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(CureParser.RBRACE, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CureParser.COMMA)
            else:
                return self.getToken(CureParser.COMMA, i)

        def getRuleIndex(self):
            return CureParser.RULE_enumAssign

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnumAssign" ):
                return visitor.visitEnumAssign(self)
            else:
                return visitor.visitChildren(self)




    def enumAssign(self):

        localctx = CureParser.EnumAssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_enumAssign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self.match(CureParser.ENUM)
            self.state = 125
            self.match(CureParser.ID)
            self.state = 126
            self.match(CureParser.LBRACE)
            self.state = 135
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==20:
                self.state = 127
                self.match(CureParser.ID)
                self.state = 132
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==36:
                    self.state = 128
                    self.match(CureParser.COMMA)
                    self.state = 129
                    self.match(CureParser.ID)
                    self.state = 134
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 137
            self.match(CureParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncModificationsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACK(self):
            return self.getToken(CureParser.LBRACK, 0)

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)

        def RBRACK(self):
            return self.getToken(CureParser.RBRACK, 0)

        def args(self):
            return self.getTypedRuleContext(CureParser.ArgsContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_funcModifications

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncModifications" ):
                return visitor.visitFuncModifications(self)
            else:
                return visitor.visitChildren(self)




    def funcModifications(self):

        localctx = CureParser.FuncModificationsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_funcModifications)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            self.match(CureParser.LBRACK)
            self.state = 140
            self.match(CureParser.ID)
            self.state = 141
            self.match(CureParser.LPAREN)
            self.state = 143
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 9363037061128) != 0):
                self.state = 142
                self.args()


            self.state = 145
            self.match(CureParser.RPAREN)
            self.state = 146
            self.match(CureParser.RBRACK)
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


        def funcModifications(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.FuncModificationsContext)
            else:
                return self.getTypedRuleContext(CureParser.FuncModificationsContext,i)


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
        self.enterRule(localctx, 26, self.RULE_funcAssign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==43:
                self.state = 148
                self.funcModifications()
                self.state = 153
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 154
            self.match(CureParser.FUNC)
            self.state = 155
            self.match(CureParser.ID)
            self.state = 156
            self.match(CureParser.LPAREN)
            self.state = 158
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==20:
                self.state = 157
                self.params()


            self.state = 160
            self.match(CureParser.RPAREN)
            self.state = 163
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==46:
                self.state = 161
                self.match(CureParser.RETURNS)
                self.state = 162
                self.type_()


            self.state = 165
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

        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


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
        self.enterRule(localctx, 28, self.RULE_varAssign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 168
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 167
                self.match(CureParser.CONST)


            self.state = 171
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.state = 170
                self.type_()


            self.state = 173
            self.match(CureParser.ID)
            self.state = 175
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 65011712) != 0):
                self.state = 174
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 65011712) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 177
            self.match(CureParser.ASSIGN)
            self.state = 178
            self.expr(0)
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


        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def COLON(self):
            return self.getToken(CureParser.COLON, 0)

        def getRuleIndex(self):
            return CureParser.RULE_arg

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArg" ):
                return visitor.visitArg(self)
            else:
                return visitor.visitChildren(self)




    def arg(self):

        localctx = CureParser.ArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 182
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.state = 180
                self.match(CureParser.ID)
                self.state = 181
                self.match(CureParser.COLON)


            self.state = 184
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
        self.enterRule(localctx, 32, self.RULE_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self.arg()
            self.state = 191
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==36:
                self.state = 187
                self.match(CureParser.COMMA)
                self.state = 188
                self.arg()
                self.state = 193
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

        def AMPERSAND(self):
            return self.getToken(CureParser.AMPERSAND, 0)

        def ASSIGN(self):
            return self.getToken(CureParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_param

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = CureParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            self.type_()
            self.state = 196
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==47:
                self.state = 195
                self.match(CureParser.AMPERSAND)


            self.state = 198
            self.match(CureParser.ID)
            self.state = 201
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==38:
                self.state = 199
                self.match(CureParser.ASSIGN)
                self.state = 200
                self.expr(0)


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
        self.enterRule(localctx, 36, self.RULE_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 203
            self.param()
            self.state = 208
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==36:
                self.state = 204
                self.match(CureParser.COMMA)
                self.state = 205
                self.param()
                self.state = 210
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Dict_elementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)


        def COLON(self):
            return self.getToken(CureParser.COLON, 0)

        def getRuleIndex(self):
            return CureParser.RULE_dict_element

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDict_element" ):
                return visitor.visitDict_element(self)
            else:
                return visitor.visitChildren(self)




    def dict_element(self):

        localctx = CureParser.Dict_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_dict_element)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 211
            self.expr(0)
            self.state = 212
            self.match(CureParser.COLON)
            self.state = 213
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)

        def args(self):
            return self.getTypedRuleContext(CureParser.ArgsContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_call

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCall" ):
                return visitor.visitCall(self)
            else:
                return visitor.visitChildren(self)




    def call(self):

        localctx = CureParser.CallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_call)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 215
            self.match(CureParser.ID)
            self.state = 216
            self.match(CureParser.LPAREN)
            self.state = 218
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 9363037061128) != 0):
                self.state = 217
                self.args()


            self.state = 220
            self.match(CureParser.RPAREN)
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

        def type_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.TypeContext)
            else:
                return self.getTypedRuleContext(CureParser.TypeContext,i)


        def LBRACE(self):
            return self.getToken(CureParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(CureParser.RBRACE, 0)

        def args(self):
            return self.getTypedRuleContext(CureParser.ArgsContext,0)


        def LBRACK(self):
            return self.getToken(CureParser.LBRACK, 0)

        def COLON(self):
            return self.getToken(CureParser.COLON, 0)

        def RBRACK(self):
            return self.getToken(CureParser.RBRACK, 0)

        def dict_element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.Dict_elementContext)
            else:
                return self.getTypedRuleContext(CureParser.Dict_elementContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CureParser.COMMA)
            else:
                return self.getToken(CureParser.COMMA, i)

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
        self.enterRule(localctx, 42, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.state = 257
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,26,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 222
                self.type_()
                self.state = 223
                self.match(CureParser.LBRACE)
                self.state = 225
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 9363037061128) != 0):
                    self.state = 224
                    self.args()


                self.state = 227
                self.match(CureParser.RBRACE)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 229
                self.match(CureParser.LBRACK)
                self.state = 230
                self.type_()
                self.state = 231
                self.match(CureParser.COLON)
                self.state = 232
                self.type_()
                self.state = 233
                self.match(CureParser.RBRACK)
                self.state = 234
                self.match(CureParser.LBRACE)
                self.state = 243
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 9363037061128) != 0):
                    self.state = 235
                    self.dict_element()
                    self.state = 240
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==36:
                        self.state = 236
                        self.match(CureParser.COMMA)
                        self.state = 237
                        self.dict_element()
                        self.state = 242
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 245
                self.match(CureParser.RBRACE)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 247
                self.match(CureParser.INT)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 248
                self.match(CureParser.FLOAT)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 249
                self.match(CureParser.STRING)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 250
                self.match(CureParser.BOOL)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 251
                self.match(CureParser.NIL)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 252
                self.match(CureParser.ID)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 253
                self.match(CureParser.LPAREN)
                self.state = 254
                self.expr(0)
                self.state = 255
                self.match(CureParser.RPAREN)
                pass


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
            self.uop = None # Token
            self.op = None # Token

        def call(self):
            return self.getTypedRuleContext(CureParser.CallContext,0)


        def atom(self):
            return self.getTypedRuleContext(CureParser.AtomContext,0)


        def NEW(self):
            return self.getToken(CureParser.NEW, 0)

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)

        def args(self):
            return self.getTypedRuleContext(CureParser.ArgsContext,0)


        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)


        def NOT(self):
            return self.getToken(CureParser.NOT, 0)

        def SUB(self):
            return self.getToken(CureParser.SUB, 0)

        def ADD(self):
            return self.getToken(CureParser.ADD, 0)

        def IF(self):
            return self.getToken(CureParser.IF, 0)

        def ELSE(self):
            return self.getToken(CureParser.ELSE, 0)

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

        def GT(self):
            return self.getToken(CureParser.GT, 0)

        def LT(self):
            return self.getToken(CureParser.LT, 0)

        def GTE(self):
            return self.getToken(CureParser.GTE, 0)

        def LTE(self):
            return self.getToken(CureParser.LTE, 0)

        def AND(self):
            return self.getToken(CureParser.AND, 0)

        def OR(self):
            return self.getToken(CureParser.OR, 0)

        def DOT(self):
            return self.getToken(CureParser.DOT, 0)

        def LBRACK(self):
            return self.getToken(CureParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(CureParser.RBRACK, 0)

        def getRuleIndex(self):
            return CureParser.RULE_expr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CureParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 44
        self.enterRecursionRule(localctx, 44, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 276
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
            if la_ == 1:
                self.state = 260
                self.call()
                pass

            elif la_ == 2:
                self.state = 261
                self.atom()
                pass

            elif la_ == 3:
                self.state = 262
                self.match(CureParser.NEW)
                self.state = 263
                self.match(CureParser.ID)
                self.state = 264
                self.match(CureParser.LPAREN)
                self.state = 266
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 9363037061128) != 0):
                    self.state = 265
                    self.args()


                self.state = 268
                self.match(CureParser.RPAREN)
                pass

            elif la_ == 4:
                self.state = 269
                self.match(CureParser.LPAREN)
                self.state = 270
                self.type_()
                self.state = 271
                self.match(CureParser.RPAREN)
                self.state = 272
                self.expr(7)
                pass

            elif la_ == 5:
                self.state = 274
                localctx.uop = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 17186160640) != 0)):
                    localctx.uop = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 275
                self.expr(1)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 313
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,32,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 311
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,31,self._ctx)
                    if la_ == 1:
                        localctx = CureParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 278
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 279
                        self.match(CureParser.IF)
                        self.state = 280
                        self.expr(0)
                        self.state = 281
                        self.match(CureParser.ELSE)
                        self.state = 282
                        self.expr(10)
                        pass

                    elif la_ == 2:
                        localctx = CureParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 284
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 285
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 58720256) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 286
                        self.expr(6)
                        pass

                    elif la_ == 3:
                        localctx = CureParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 287
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 288
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==21 or _la==22):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 289
                        self.expr(5)
                        pass

                    elif la_ == 4:
                        localctx = CureParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 290
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 291
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4227858432) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 292
                        self.expr(4)
                        pass

                    elif la_ == 5:
                        localctx = CureParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 293
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 294
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==32 or _la==33):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 295
                        self.expr(3)
                        pass

                    elif la_ == 6:
                        localctx = CureParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 296
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 297
                        self.match(CureParser.DOT)
                        self.state = 298
                        self.match(CureParser.ID)
                        self.state = 304
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
                        if la_ == 1:
                            self.state = 299
                            self.match(CureParser.LPAREN)
                            self.state = 301
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 9363037061128) != 0):
                                self.state = 300
                                self.args()


                            self.state = 303
                            self.match(CureParser.RPAREN)


                        pass

                    elif la_ == 7:
                        localctx = CureParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 306
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 307
                        self.match(CureParser.LBRACK)
                        self.state = 308
                        self.expr(0)
                        self.state = 309
                        self.match(CureParser.RBRACK)
                        pass

             
                self.state = 315
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
        self._predicates[22] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 6)
         




