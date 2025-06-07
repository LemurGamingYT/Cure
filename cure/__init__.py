from subprocess import run
from typing import cast

from cure.passes.code_generation import CodeGeneration
from cure.passes.analyser import Analyser
from cure.parser.parser import CureParser
from cure.parser.lexer import CureLexer
from cure import ir


def compile_to_str(scope: ir.Scope):
    lexer = CureLexer()
    tokens = lexer.lex(scope.src)

    parser = CureParser(scope.src)
    program = cast(ir.Program, parser.parse(tokens))
    
    program = Analyser.run(scope, program)
    return CodeGeneration.run(scope, cast(ir.Program, program))

def compile_to_ll(scope: ir.Scope):
    code = compile_to_str(scope)
    ll_file = scope.file.with_suffix('.ll')
    ll_file.write_text(code)
    return ll_file

def compile_to_exe(scope: ir.Scope):
    ll_file = compile_to_ll(scope)
    exe_file = scope.file.with_suffix(f'.{scope.target.exe_ext}')
    run(f'clang {ll_file.absolute().as_posix()} -o {exe_file}')
