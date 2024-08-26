grammar Cure;

parse: stmt* EOF;

type: ID (LBRACK type (COLON type)? RBRACK)?;

stmt
    : funcAssign
    | foreachStmt | whileStmt | ifStmt
    | varAssign
    | expr
    | useStmt
    ;

bodyStmts: stmt | RETURN expr | CONTINUE | BREAK;
body: LBRACE bodyStmts* RBRACE;

ifStmt: IF expr body elseifStmt* elseStmt?;
elseifStmt: ELSE IF expr body;
elseStmt: ELSE body;
whileStmt: WHILE expr body;
foreachStmt: FOREACH ID IN expr body;
useStmt: USE STRING;

funcModifications: LBRACK ID LPAREN args? RPAREN RBRACK;
funcAssign: funcModifications* FUNC ID LPAREN params? RPAREN (RETURNS type)? body;
varAssign: CONST? type? ID op=(ADD | SUB | MUL | DIV | MOD)? ASSIGN expr;

arg: expr;
args: arg (COMMA arg)*;

param: type AMPERSAND? ID;
params: param (COMMA param)*;

dict_element: expr COLON expr;

call: ID LPAREN args? RPAREN;
atom
    : type LBRACE args? RBRACE
    | LBRACK type COLON type RBRACK LBRACE (dict_element (COMMA dict_element)*)? RBRACE
    | BIN
    | HEX
    | INT
    | FLOAT
    | STRING
    | BOOL
    | NIL
    | ID
    | LPAREN expr RPAREN
    ;

expr
    : expr DOT ID (LPAREN args? RPAREN)?
    | call
    | atom
    | uop=NOT expr | uop=SUB expr
    | expr op=(ADD | SUB) expr
    | expr op=(MUL | DIV | MOD) expr
    | expr op=(EEQ | NEQ | GT | LT | GTE | LTE) expr
    | expr op=(AND | OR) expr
    | expr IF expr ELSE expr
    | NEW ID LPAREN args? RPAREN
    | expr LBRACK expr RBRACK
    ;


IF: 'if';
IN: 'in';
NEW: 'new';
USE: 'use';
ELSE: 'else';
FUNC: 'func';
WHILE: 'while';
BREAK: 'break';
CONST: 'const';
RETURN: 'return';
FOREACH: 'foreach';
CONTINUE: 'continue';

APOSTROPHE: '\'';

INT: '-'? [0-9]+;
FLOAT: '-'? [0-9]* '.' [0-9]+;
STRING: DOLLAR? '"' .*? '"' | APOSTROPHE .*? APOSTROPHE;
HEX: '0x' [0-9a-fA-F]+;
BOOL: 'true' | 'false';
BIN: '0b' [0-1]+;
NIL: 'nil';
ID: [a-zA-Z_][a-zA-Z_0-9]*;

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
MOD: '%';
EEQ: '==';
NEQ: '!=';
GT: '>';
LT: '<';
GTE: '>=';
LTE: '<=';
AND: '&&';
OR: '||';
NOT: '!';

DOT: '.';
COMMA: ',';
COLON: ':';
ASSIGN: '=';
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACK: '[';
RBRACK: ']';
DOLLAR: '$';
RETURNS: '->';
AMPERSAND: '&';

COMMENT: '//' .*? '\n' -> skip;
MULTILINE_COMMENT: '/*' .*? '*/' -> skip;
WHITESPACE: [\t\r\n ]+ -> skip;
