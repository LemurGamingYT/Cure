from rply.lexer import LexerStream
from rply import LexerGenerator

from cure.parser.constants import TOKENS, IGNORES


class CureLexer(LexerGenerator):
    def __init__(self):
        super().__init__()
        
        for name, pattern in TOKENS.items():
            self.add(name, pattern)
        
        for pattern in IGNORES:
            self.ignore(pattern)
    
    def lex(self, src: str) -> LexerStream:
        return self.build().lex(src)
