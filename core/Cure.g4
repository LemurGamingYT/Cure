grammar Cure;

// Lexer rules

// Keywords
FUNC: 'func';
IF: 'if';
ELSE: 'else';
WHILE: 'while';
RETURN: 'return';
// COMPILETIME: 'comptime';

// Symbols
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
NOT: '!';

LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
ASSIGN: '=';
COMMA: ',';
DOT: '.';

// Datatypes
INT: '-'? [0-9]+;
FLOAT: '-'? [0-9]* '.' [0-9]+;
STRING: '"' .*? '"';
BOOL: 'true' | 'false';
NIL: 'nil';
ID: [a-zA-Z_][a-zA-Z_0-9]*;

// Skips
WHITESPACE: [\r\n\t ]+ -> skip;
COMMENT: '//' .*? '\n' -> skip;

// Parser rules

parse: stmt* EOF;

stmt: varAssignment | funcAssignment | ifStmt | whileStmt | expr;

bodyStmts: stmt | returnStmt;
body: LBRACE bodyStmts* RBRACE;

typeDecl: ID | ID DOT ID;

// Statements
ifStmt: IF expr body (ELSE IF expr body)* (ELSE body)?;
whileStmt: WHILE expr body;
returnStmt: RETURN expr;

// compileTimeStmt: COMPILETIME stmt;

// Assignments
varAssignment: typeDecl? ID ASSIGN expr;
funcAssignment: (FUNC | typeDecl) ID LPAREN params? RPAREN body;

// Expressions
arg: expr;
args: arg (COMMA arg)*;

param: typeDecl ID (ASSIGN expr)?;
params: param (COMMA param)*;

call: ID LPAREN args? RPAREN;

unaryExpr: (SUB | ADD | NOT) expr;

primary: INT | FLOAT | BOOL | ID | NIL | STRING;

expr
    : primary
    | call
    | expr op=(MUL | DIV | MOD) expr
    | expr op=(ADD | SUB) expr
    | expr op=(EEQ | NEQ | GT | GTE | LT | LTE) expr
    | expr DOT ID (LPAREN args? RPAREN)?
    | unaryExpr
    ;
