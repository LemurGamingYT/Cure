grammar Cure;

program: stmt* EOF;

type: ID AMPERSAND?;

stmt
    : varAssign | funcAssign
    | whileStmt | ifStmt | useStmt
    | unsafeStmt | externStmt
    | expr
    ;

bodyStmt: stmt | RETURN expr | BREAK | CONTINUE;
body: LBRACE bodyStmt* RBRACE;

ifStmt: IF expr body elseifStmt* elseStmt?;
elseifStmt: ELSE IF expr body;
elseStmt: ELSE body;
whileStmt: WHILE expr body;
useStmt: USE STRING;
unsafeStmt: UNSAFE body;

externType: EXTERN 'type' ID;
externFunc: EXTERN STATIC? FUNC funcName genericParams? (LPAREN params? RPAREN)? (RETURNS return_type=type)?;
externClass: EXTERN CLASS ID genericParams? LBRACE externFunc* RBRACE;
externStmt: externType | externFunc | externClass;

funcName
    : ID
    | NEW
    | type DOT ID
    | type DOT NEW
    | op=(ADD | SUB | MUL | DIV | MOD | EEQ | NEQ | LT | GT | LTE | GTE | AND | OR | NOT)
    ;

funcAssign
    : FUNC funcName LPAREN params? RPAREN (RETURNS return_type=type)? body
    ;
varAssign
    : ID op=(ADD | SUB | MUL | DIV | MOD)? ASSIGN expr
    | MUTABLE? type? ID ASSIGN expr
    ;

arg: expr;
args: arg (COMMA arg)*;

param: MUTABLE? type ID;
params: param (COMMA param)*;

genericParam: ID;
genericParams: LT genericParam (COMMA genericParam)* GT;

expr
    : LPAREN type RPAREN expr #cast
    | ID LPAREN args? RPAREN #call
    | LPAREN expr RPAREN #paren
    | INT #int
    | FLOAT #float
    | STRING #string
    | BOOL #bool
    | ID #id
    | AMPERSAND expr #ref
    | NEW type LPAREN args? RPAREN #new
    | NEW type LBRACK RBRACK #newArray
    | LBRACK args RBRACK #arrayInit
    | expr IF expr ELSE expr #ternary
    | expr DOT ID (LPAREN args? RPAREN)? #attr
    | expr op=(MUL | DIV | MOD) expr #multiplication
    | expr op=(ADD | SUB) expr #addition
    | expr op=(EEQ | NEQ | GT | LT | GTE | LTE) expr #relational
    | expr op=(AND | OR) expr #logical
    | op=(NOT | SUB | ADD) expr #unary
    ;


// Basic keywords
IF: 'if';
USE: 'use';
NEW: 'new';
FUNC: 'fn';
ELSE: 'else';
MUTABLE: 'mut';
UNSAFE: 'unsafe';
RETURN: 'return';
EXTERN: 'extern';
STATIC: 'static';

// Loop keywords
WHILE: 'while';
BREAK: 'break';
CONTINUE: 'continue';

// Class keywords
CLASS: 'class';

APOSTROPHE: '\'';

INT: '-'? [0-9]+;
FLOAT: '-'? [0-9]* '.' [0-9]+;
STRING: '"' .*? '"' | APOSTROPHE .*? APOSTROPHE;
BOOL: 'true' | 'false';
ID: [a-zA-Z_][a-zA-Z_0-9]*;

AMPERSAND: '&';

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
RETURNS: '->';

COMMENT: '//' .*? '\n' -> skip;
MULTILINE_COMMENT: '/*' .*? '*/' -> skip;
WHITESPACE: [\t\r\n ]+ -> skip;
OTHER: .;
