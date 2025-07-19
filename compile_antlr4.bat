@echo off
antlr4 -Dlanguage=Python3 -o cure/parser -visitor -no-listener cure/Cure.g4
