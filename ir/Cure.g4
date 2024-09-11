grammar Cure;

parse: stmt* EOF;

type: ID (LBRACK type (COLON type)? RBRACK)?;

stmt
    : funcAssign
    | foreachStmt | whileStmt | ifStmt
    | varAssign
    | expr
    // | classAssign
    | enumAssign
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

classDeclarations
    : funcAssign+
    ;
classAssign: CLASS ID LBRACE classDeclarations? RBRACE;
enumAssign: ENUM ID LBRACE (ID (COMMA ID)*)? RBRACE;
funcModifications: LBRACK ID LPAREN args? RPAREN RBRACK;
funcAssign: funcModifications* FUNC ID LPAREN params? RPAREN (RETURNS type)? body;
varAssign: CONST? type? ID op=(ADD | SUB | MUL | DIV | MOD)? ASSIGN expr;

arg: (ID COLON)? expr;
args: arg (COMMA arg)*;

param: type AMPERSAND? ID (ASSIGN expr)?;
params: param (COMMA param)*;

dict_element: expr COLON expr;

call: ID LPAREN args? RPAREN;
atom
    : type LBRACE args? RBRACE
    | LBRACK type COLON type RBRACK LBRACE (dict_element (COMMA dict_element)*)? RBRACE
    | INT
    | FLOAT
    | STRING
    | BOOL
    | NIL
    | ID
    | LPAREN expr RPAREN
    ;

expr
    : call
    | atom
    | expr DOT ID (LPAREN args? RPAREN)?
    // | LBRACE expr COLON ID IN expr RBRACE
    | expr IF expr ELSE expr
    | NEW ID LPAREN args? RPAREN
    | LPAREN type RPAREN expr
    | expr LBRACK expr RBRACK
    | expr op=(MUL | DIV | MOD) expr
    | expr op=(ADD | SUB) expr
    | expr op=(EEQ | NEQ | GT | LT | GTE | LTE) expr
    | expr op=(AND | OR) expr
    | uop=(NOT | SUB | ADD) expr
    ;


IF: 'if';
IN: 'in';
NEW: 'new';
USE: 'use';
ENUM: 'enum';
ELSE: 'else';
FUNC: 'func';
WHILE: 'while';
BREAK: 'break';
CONST: 'const';
CLASS: 'class';
RETURN: 'return';
FOREACH: 'foreach';
CONTINUE: 'continue';

APOSTROPHE: '\'';

INT: '-'? [0-9]+;
FLOAT: '-'? [0-9]* '.' [0-9]+;
STRING: DOLLAR? '"' .*? '"' | APOSTROPHE .*? APOSTROPHE;
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
ARROWASSIGN: '=>';

COMMENT: '//' .*? '\n' -> skip;
MULTILINE_COMMENT: '/*' .*? '*/' -> skip;
WHITESPACE: [\t\r\n ]+ -> skip;
