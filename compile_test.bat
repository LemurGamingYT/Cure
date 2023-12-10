@echo off
python main.py examples/test.cure
g++ examples/test.cpp -o examples/test.exe
.\examples\test.exe
