@echo off
antlr4 -o core/parser/ -visitor -no-listener -Dlanguage=Python3 core/Cure.g4
