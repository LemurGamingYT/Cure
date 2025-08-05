grammar Cure;

program: stmt* EOF;

type
    : ID
    // | type LT type+ GT
    | type LBRACK RBRACK
    // | type AMPERSAND
    ;

stmt
    : varAssign | funcAssign
    | whileStmt | ifStmt | forRangeStmt
    | useStmt | externStmt
    | expr
    ;

bodyStmt
    : stmt # stmtBody
    | RETURN expr #return
    | BREAK #break
    | CONTINUE #continue
    ;

body: LBRACE bodyStmt* RBRACE;

ifStmt: IF expr body elseifStmt* elseStmt?;
elseifStmt: ELSE IF expr body;
elseStmt: ELSE body;
whileStmt: WHILE expr body;
forRangeStmt: FOR ID IN expr DOUBLEDOT expr body;
useStmt: USE STRING;
externFunc: EXTERN INTERNAL? STATIC? (PROPERTY | METHOD)? functionSignature;
externClass: EXTERN INTERNAL? CLASS ID genericParams? body;
externStmt: externFunc | externClass;

funcName: (extend_type=type DOT)? (ID | NEW);

functionSignature
    : FUNC funcName genericParams? LPAREN params? RPAREN (RETURNS return_type=type)?
    ;

funcAssign: functionSignature body;
varAssign
    : ID op=(ADD | SUB | MUL | DIV | MOD)? ASSIGN expr
    | MUTABLE? ID ASSIGN expr
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
    | NEW type LPAREN args? RPAREN #new
    | NEW type LBRACK RBRACK #newArray
    | LBRACK args? RBRACK #arrayInit // make args optional so we can do the error message
    | expr IF expr ELSE expr #ternary
    | expr DOT ID LPAREN args? RPAREN #method
    | expr DOT ID #property
    | expr op=(MUL | DIV | MOD) expr #multiplication
    | expr op=(ADD | SUB) expr #addition
    | expr op=(EEQ | NEQ | GT | LT | GTE | LTE) expr #relational
    | expr op=(AND | OR) expr #logical
    | op=(NOT | SUB | ADD) expr #unary
    ;


// Basic keywords
IF: 'if';
IN: 'in';
FOR: 'for';
USE: 'use';
FUNC: 'fn';
ELSE: 'else';
MUTABLE: 'mut';
STATIC: 'static';
RETURN: 'return';

// Extern keywords
EXTERN: 'extern';
METHOD: 'method';
PROPERTY: 'property';
INTERNAL: 'internal';

// Loop keywords
WHILE: 'while';
BREAK: 'break';
CONTINUE: 'continue';

// Class keywords
NEW: 'new';
CLASS: 'class';

APOSTROPHE: '\'';

INT: '-'? [0-9]+;
FLOAT: '-'? [0-9]* '.' [0-9]+;
STRING: /* DOLLAR? */ '"' .*? '"' | APOSTROPHE .*? APOSTROPHE;
BOOL: 'true' | 'false';
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
// DOLLAR: '$';
ASSIGN: '=';
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACK: '[';
RBRACK: ']';
RETURNS: '->';
AMPERSAND: '&';

COMMENT: '//' .*? '\n' -> skip;
MULTILINE_COMMENT: '/*' .*? '*/' -> skip;
WHITESPACE: [\t\r\n ]+ -> skip;
OTHER: .;
