@echo off
antlr4 -Dlanguage=Python3 -visitor -no-listener -o ir/parser/ ir/Cure.g4
