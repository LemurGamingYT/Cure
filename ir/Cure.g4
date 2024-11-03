grammar Cure;

parse: stmt* EOF;

type
    : ID (LBRACK type (COLON type)? RBRACK)? QUESTION?
    | LPAREN (type (COMMA type)*)? RPAREN RETURNS type
    | LPAREN (type (COMMA type)*)? RPAREN
    ;

stmt
    : varAssign | funcAssign | classAssign | enumAssign | testAssign
    | foreachStmt | whileStmt | ifStmt | useStmt | rangeStmt | externStmt
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
externStmt: EXTERN STRING;

methodName
    : (TILDE ID)
    | ID
    | opname=(ADD | SUB | MUL | DIV | MOD | EEQ | NEQ | LT | GT | GTE | LTE | AND | OR)
    ;

classProperty: (PUBLIC | PRIVATE)? type ID (ASSIGN expr)?;
classMethod
    : (PUBLIC | PRIVATE)? STATIC? FUNC OVERRIDE? name=methodName LPAREN params? RPAREN (RETURNS type)? body
    ;
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
testAssign: TEST ID body;

arg: (ID COLON)? expr;
args: arg (COMMA arg)*;

param: type AMPERSAND? ID (ASSIGN expr)?;
params: param (COMMA param)*;

dict_element: expr COLON expr;

genericArgs: LBRACK type (COMMA type)* RBRACK;
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
    : LPAREN type RPAREN expr #cast
    // | FUNC LPAREN params? RPAREN (RETURNS type)? body #lambda
    | atom #atom_expr
    | NEW ID LPAREN args? RPAREN #new
    | LPAREN (expr (COMMA expr)*)+ RPAREN #tuple_create
    | expr genericArgs? LPAREN args? RPAREN #call
    | expr DOT ID genericArgs? (LPAREN args? RPAREN)? #attr
    | expr IF expr ELSE expr #ternary
    // | LBRACE expr COLON ID IN expr RBRACE #list_comp
    | expr LBRACK expr RBRACK #index
    | expr op=(MUL | DIV | MOD) expr #multiplication
    | expr op=(ADD | SUB) expr #addition
    | expr op=(EEQ | NEQ | GT | LT | GTE | LTE) expr #relational
    | expr op=(AND | OR) expr #logical
    | uop=(NOT | SUB | ADD) expr #unary
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
TEST: 'test';
WHILE: 'while';
BREAK: 'break';
CONST: 'const';
RETURN: 'return';
EXTERN: 'extern';
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
TILDE: '~';
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
