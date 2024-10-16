grammar Cure;

parse: stmt* EOF;

type
    : ID (LBRACK type (COLON type)? RBRACK)? QUESTION?
    | LPAREN (type (COMMA type)*)? RPAREN
    // | LPAREN (type (COMMA type)*)? RPAREN RETURNS type
    ;

stmt
    : varAssign | funcAssign | classAssign | enumAssign
    | foreachStmt | whileStmt | ifStmt | useStmt | rangeStmt
    | expr
    ;

bodyStmts: stmt | RETURN expr | CONTINUE | BREAK;
body: LBRACE bodyStmts* RBRACE;

ifStmt: IF expr body elseifStmt* elseStmt?;
elseifStmt: ELSE IF expr body;
elseStmt: ELSE body;
whileStmt: WHILE expr body;
rangeStmt: FOR ID IN expr DOUBLEDOT expr body;
foreachStmt: FOREACH ID IN expr body;
useStmt: USE STRING;

classProperty: (PUBLIC | PRIVATE)? type ID (ASSIGN expr)?;
classMethod: (PUBLIC | PRIVATE)? STATIC? FUNC OVERRIDE? ID LPAREN params? RPAREN (RETURNS type)? body;
classDeclarations
    : (classMethod | classProperty)+
    ;
classAssign
    : CLASS ID (RARROW ID)? LBRACE classDeclarations? RBRACE
    ;
enumAssign: ENUM ID LBRACE (ID (COMMA ID)*)? RBRACE;
funcModifications: LBRACK ID LPAREN args? RPAREN RBRACK;
funcAssign
    : funcModifications* FUNC (type DOT)? ID (LBRACK ID (COMMA ID)* RBRACK)? LPAREN params? RPAREN (RETURNS type)? body
    ;
varAssign
    : CONST? type? ID op=(ADD | SUB | MUL | DIV | MOD)? ASSIGN expr
    | ID DOT ID op=(ADD | SUB | MUL | DIV | MOD)? ASSIGN expr
    ;

arg: (ID COLON)? expr;
args: arg (COMMA arg)*;

param: type AMPERSAND? ID (ASSIGN expr)?;
params: param (COMMA param)*;

dict_element: expr COLON expr;

genericArgs: LBRACK type (COMMA type)* RBRACK;
call: ID genericArgs? LPAREN args? RPAREN;
atom
    : (LBRACK type COLON type RBRACK)? LBRACE (dict_element (COMMA dict_element)*)? RBRACE
    | type? LBRACE args? RBRACE
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
    // | FUNC LPAREN params? RPAREN (RETURNS type)? body
    | atom
    | LPAREN type RPAREN expr
    | expr DOT ID genericArgs? (LPAREN args? RPAREN)?
    | expr IF expr ELSE expr
    | LPAREN (expr (COMMA expr)*)+ RPAREN
    // | LBRACE expr COLON ID IN expr RBRACE
    | NEW ID LPAREN args? RPAREN
    | expr LBRACK expr RBRACK
    | expr op=(MUL | DIV | MOD) expr
    | expr op=(ADD | SUB) expr
    | expr op=(EEQ | NEQ | GT | LT | GTE | LTE) expr
    | expr op=(AND | OR) expr
    | uop=(NOT | SUB | ADD) expr
    ;


// Basic keywords
IF: 'if';
IN: 'in';
NEW: 'new';
USE: 'use';
FOR: 'for';
ENUM: 'enum';
ELSE: 'else';
FUNC: 'func';
WHILE: 'while';
BREAK: 'break';
CONST: 'const';
RETURN: 'return';
FOREACH: 'foreach';
CONTINUE: 'continue';

// Class keywords
CLASS: 'class';
STATIC: 'static';
PUBLIC: 'public';
PRIVATE: 'private';
OVERRIDE: 'override';

APOSTROPHE: '\'';

INT: '-'? [0-9]+;
FLOAT: '-'? [0-9]* '.' [0-9]+;
STRING: DOLLAR? ('"' .*? '"' | APOSTROPHE .*? APOSTROPHE);
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

DOUBLEDOT: '..';
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
RARROW: '<-';
QUESTION: '?';
RETURNS: '->';
AMPERSAND: '&';
ARROWASSIGN: '=>';

COMMENT: '//' .*? '\n' -> skip;
MULTILINE_COMMENT: '/*' .*? '*/' -> skip;
WHITESPACE: [\t\r\n ]+ -> skip;
OTHER: .;
