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
"""
