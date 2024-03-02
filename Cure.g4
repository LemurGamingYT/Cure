grammar Cure;

parse: stmt* EOF;

type: ID (DOT ID)*;

stmt: varAssign | funcAssign | ifStmt | whileStmt | expr;

bodyStmts: stmt | RETURN expr;
body: LBRACE bodyStmts* RBRACE;

ifStmt: IF expr body elseifStmt* elseStmt?;
elseifStmt: ELSE IF expr body;
elseStmt: ELSE body;
whileStmt: WHILE expr body;

funcAssign: FUNC ID LPAREN params? RPAREN (RETURNS type)? body;
varAssign: type? ID ASSIGN expr;

arg: expr;
args: arg (COMMA arg)*;

param: type? ID;
params: param (COMMA param)*;

call: ID LPAREN args? RPAREN;
atom: INT | FLOAT | STRING | BOOL | NIL | ID | LPAREN expr RPAREN;

expr
    : call
    | expr DOT ID (LPAREN args? RPAREN)?
    | atom
    | NOT expr
    | expr op=(ADD | SUB) expr
    | expr op=(MUL | DIV | MOD) expr
    | expr op=(EEQ | NEQ | GT | LT | GTE | LTE) expr
    | expr op=(AND | OR) expr
    ;


IF: 'if';
ELSE: 'else';
FUNC: 'func';
WHILE: 'while';
RETURN: 'return';

INT: '-'? [0-9]+;
FLOAT: '-'? [0-9]* '.' [0-9]+;
STRING: '"' .*? '"';
BOOL: 'true' | 'false';
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
ASSIGN: '=';
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
RETURNS: '->';

COMMENT: '//' .*? '\n' -> skip;
WHITESPACE: [\t\r\n ]+ -> skip;
