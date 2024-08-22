@echo off
antlr4 -Dlanguage=Python3 -visitor -no-listener -o cure/parser/ cure/Cure.g4
