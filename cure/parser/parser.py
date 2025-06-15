from typing import Any

from rply.lexer import LexerStream
from rply import ParserGenerator
from rply.token import Token

from cure.parser.constants import TOKENS, PRECEDENCE
from cure.ir import (
    Node, Program, Function, Int, Float, String, Bool, Nil, Id, Param, Body, Type, Return, BinaryOp,
    UnaryOp, Call, Variable, If, Elif, While, Attribute,
    Position, TypeManager
)


def get_pos(token: Any) -> Position:
    if isinstance(token, Token):
        if token.source_pos is not None:
            line, col = token.source_pos.lineno, token.source_pos.colno
        else:
            line, col = 0, 0
    elif isinstance(token, Node):
        line, col = token.pos.line, token.pos.column
    else:
        line, col = token.line, token.column
    
    return Position(line, col)


class CureParser(ParserGenerator):
    def __init__(self, src: str):
        super().__init__(TOKENS, PRECEDENCE)

        @self.production('program :')
        @self.production('program : stmts')
        def program(p):
            return Program(Position.zero(), p[0] if len(p) == 1 else [])
        
        @self.production('type : id')
        def type(p):
            return TypeManager.get(p[0].value)
        
        @self.production('stmts : stmt')
        @self.production('stmts : stmts stmt')
        def stmts(p):
            return p[0] + [p[1]] if len(p) == 2 else [p[0]]
        
        @self.production('stmt : expr')
        @self.production('stmt : function')
        @self.production('stmt : return')
        @self.production('stmt : variable')
        @self.production('stmt : if_stmt')
        @self.production('stmt : while_stmt')
        def stmt(p):
            return p[0]
        
        @self.production('return : RETURN expr')
        def return_(p):
            return Return(get_pos(p[0]), p[1])
        
        @self.production('body : { stmts }')
        def body(p):
            return Body(get_pos(p[0]), p[1])
        
        @self.production('body : { }')
        def body_empty(p):
            return Body(get_pos(p[0]), [])
        
        @self.production('param : type id')
        def param(p):
            return Param(get_pos(p[0]), p[1].value, p[0])
        
        @self.production('params : param')
        @self.production('params : params , param')
        def params(p):
            return p[0] + [p[2]] if len(p) == 3 else [p[0]]
        
        @self.production('function : FN id ( params ) -> type body')
        @self.production('function : FN id ( params ) body')
        def function(p):
            name = p[1].value
            params = p[3]
            if len(p) == 8:
                ret_type = p[6]
                body = p[7]
            else:
                ret_type = Type.nil()
                body = p[5]
            
            return Function(get_pos(p[0]), name, params, ret_type, body)
        
        @self.production('function : FN id ( ) -> type body')
        @self.production('function : FN id ( ) body')
        def function_no_params(p):
            name = p[1].value
            if len(p) == 7:
                ret_type = p[5]
                body = p[6]
            else:
                ret_type = Type.nil()
                body = p[4]

            return Function(get_pos(p[0]), name, [], ret_type, body)
        
        @self.production('variable : id = expr')
        def variable(p):
            return Variable(get_pos(p[0]), p[0].value, p[2])
        
        # If statement without else
        @self.production('if_stmt : IF expr body')
        def if_stmt(p):
            return If(get_pos(p[0]), p[1], p[2])
        
        # If statement with else
        @self.production('if_stmt : IF expr body ELSE body')
        def if_else_stmt(p):
            return If(get_pos(p[0]), p[1], p[2], p[4])
        
        # If statement with elif chain
        @self.production('if_stmt : IF expr body elif_chain')
        def if_elif_stmt(p):
            return If(get_pos(p[0]), p[1], p[2], None, p[3])
        
        # If statement with elif chain and else
        @self.production('if_stmt : IF expr body elif_chain ELSE body')
        def if_elif_else_stmt(p):
            return If(get_pos(p[0]), p[1], p[2], p[5], p[3])
        
        # Elif chain (one or more elif statements)
        @self.production('elif_chain : elif_stmt')
        def elif_chain_single(p):
            return [p[0]]
        
        @self.production('elif_chain : elif_chain elif_stmt')
        def elif_chain_multiple(p):
            return p[0] + [p[1]]
        
        # Single elif statement
        @self.production('elif_stmt : ELSE IF expr body')
        def elif_stmt(p):
            return Elif(get_pos(p[0]), p[2], p[3])
        
        @self.production('while_stmt : WHILE expr body')
        def while_stmt(p):
            return While(get_pos(p[0]), p[1], p[2])
        
        @self.production('arg : expr')
        def arg(p):
            return p[0]
        
        @self.production('args : arg')
        @self.production('args : args , arg')
        def args(p):
            return p[0] + [p[2]] if len(p) == 3 else [p[0]]
        
        @self.production('expr : ( expr )')
        def expr_group(p):
            return p[1]
        
        @self.production('expr : id ( args )')
        def call(p):
            return Call(get_pos(p[0]), p[0].value, p[2])
        
        @self.production('expr : id ( )')
        def empty_call(p):
            return Call(get_pos(p[0]), p[0].value)
        
        @self.production('expr : expr + expr')
        @self.production('expr : expr - expr')
        @self.production('expr : expr * expr')
        @self.production('expr : expr / expr')
        @self.production('expr : expr % expr')
        @self.production('expr : expr == expr')
        @self.production('expr : expr != expr')
        @self.production('expr : expr < expr')
        @self.production('expr : expr > expr')
        @self.production('expr : expr <= expr')
        @self.production('expr : expr >= expr')
        @self.production('expr : expr and expr')
        @self.production('expr : expr or expr')
        def expr_binary_op(p):
            return BinaryOp(get_pos(p[1]), p[0], p[1].value, p[2])

        @self.production('expr : ! expr')
        def expr_unary_op(p):
            return UnaryOp(get_pos(p[0]), p[0].value, p[1])
        
        @self.production('expr : int')
        @self.production('expr : float')
        @self.production('expr : string')
        @self.production('expr : bool')
        @self.production('expr : nil')
        @self.production('expr : id')
        def atom(p):
            pos = get_pos(p[0])
            value = p[0].value
            match p[0].name:
                case 'int':
                    return Int(pos, int(value))
                case 'float':
                    return Float(pos, float(value))
                case 'string':
                    return String(pos, value[1:-1])
                case 'bool':
                    return Bool(pos, value == 'true')
                case 'nil':
                    return Nil(pos)
                case 'id':
                    return Id(pos, value)
        
        @self.production('expr : expr . id')
        def property(p):
            return Attribute(get_pos(p[0]), p[0], p[2].value)
        
        @self.production('expr : expr . id ( )')
        @self.production('expr : expr . id ( args )')
        def method(p):
            return Attribute(get_pos(p[0]), p[0], p[2].value, p[4] if len(p) == 6 else [])
        
        @self.error
        def error_handle(token: Token):
            pos = get_pos(token)
            pos.comptime_error(f'unexpected token {token.value}', src)
    
    def parse(self, tokens: LexerStream) -> Node:
        return self.build().parse(tokens)
