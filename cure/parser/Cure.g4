grammar Cure;

parse: stmt* EOF;

type: ID;

stmt
    : varAssign | funcAssign
    | whileStmt | ifStmt
    | expr
    ;

bodyStmts: stmt | RETURN expr | CONTINUE | BREAK;
body: LBRACE bodyStmts* RBRACE;

ifStmt: IF expr body elseifStmt* elseStmt?;
elseifStmt: ELSE IF expr body;
elseStmt: ELSE body;
whileStmt: WHILE expr body;

funcAssign: FUNC ID LPAREN params? RPAREN (RETURNS type)? body;
varAssign
    : MUTABLE? ID ASSIGN expr
    | ID op=(ADD | SUB | MUL | DIV | MOD)? ASSIGN expr
    ;

arg: expr;
args: arg (COMMA arg)*;

param: MUTABLE? type ID;
params: param (COMMA param)*;

atom
    : INT
    | FLOAT
    | STRING
    | BOOL
    | NIL
    | ID
    | LPAREN expr RPAREN
    ;

expr
    : LPAREN type RPAREN expr #cast
    | atom #atom_expr
    | NEW type LBRACK RBRACK #newArray
    | expr LPAREN args? RPAREN #call
    | expr DOT ID (LPAREN args? RPAREN)? #attr
    | expr IF expr ELSE expr #ternary
    | expr op=(MUL | DIV | MOD) expr #multiplication
    | expr op=(ADD | SUB) expr #addition
    | expr op=(EEQ | NEQ | GT | LT | GTE | LTE) expr #relational
    | expr op=(AND | OR) expr #logical
    | uop=(NOT | SUB | ADD) expr #unary
    ;


// Basic keywords
IF: 'if';
NEW: 'new';
FUNC: 'fn';
ELSE: 'else';
MUTABLE: 'mut';
RETURN: 'return';

// Loop keywords
WHILE: 'while';
BREAK: 'break';
CONTINUE: 'continue';

APOSTROPHE: '\'';

INT: '-'? [0-9]+;
FLOAT: '-'? [0-9]* '.' [0-9]+;
STRING: ('"' .*? '"' | APOSTROPHE .*? APOSTROPHE);
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
LBRACK: '[';
RBRACK: ']';
RARROW: '<-';
RETURNS: '->';

COMMENT: '//' .*? '\n' -> skip;
MULTILINE_COMMENT: '/*' .*? '*/' -> skip;
WHITESPACE: [\t\r\n ]+ -> skip;
OTHER: .;
