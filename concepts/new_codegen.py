"""Idea for a new codegen class to make it less error prone, more readable, standardised and
easier to use.

Easily create new scopes:
with codegen.If(condition, codegen.Body(if_body), codegen.Body(else_body), None) as if_body:
    pass

This should generate
if condition {
    if_body
} else {
    else_body
}
(None is given for the elseifs, indicating that there is no else ifs)


This could also be used in conjunction with another idea:
don't compile straight to C code, but instead compile to a High Level Bytecode-like language
This could then be compiled to C. This bytecode language would be like C but with all the syntax
taken out.

Process:
print.cure -> print.cil -> print.c -> print.exe

Example:
TYPEDEF char* string
FUNC main [ (int, argc), (string*, argv) ]
VAR i int = (INT 0)
LOOPWHILE ((GET i) LT (INT 100))
(POSTINCREMENT i)
ENDLOOPWHILE
RETURN (INT 0)
ENDFUNC

equivalent C code
typedef char* string;
int main(int argc, string* argv) {
    int i = 0;
    while (i < 100) {
        i++;
    }
    
    return 0;
}
"""
