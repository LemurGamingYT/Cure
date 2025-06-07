from logging import debug, info
from subprocess import run
from pprint import pformat
from typing import cast

from cure.passes.code_generation import CodeGeneration
from cure.passes.analyser import Analyser
from cure.parser.parser import CureParser
from cure.parser.lexer import CureLexer
from cure import ir


def compile_to_str(scope: ir.Scope):
    info(f'Compiling {scope.file.as_posix()} to string')
    lexer = CureLexer()
    tokens = lexer.lex(scope.src)

    parser = CureParser(scope.src)
    program = cast(ir.Program, parser.parse(tokens))
    
    info(f'Parsed {scope.file.as_posix()}')
    debug(f'IR = {pformat(program, indent=4)}')
    program = Analyser.run(scope, program)
    debug(f'Analysed IR = {pformat(program, indent=4)}')
    return CodeGeneration.run(scope, cast(ir.Program, program))

def compile_to_ll(scope: ir.Scope):
    info(f'Compiling {scope.file.as_posix()} to an LLVM IR file (.ll)')
    code = compile_to_str(scope)
    debug(f'LLVM IR = {code}')
    ll_file = scope.file.with_suffix('.ll')
    ll_file.write_text(code)
    info(f'Wrote to {ll_file.as_posix()}')
    return ll_file

def compile_to_exe(scope: ir.Scope):
    ll_file = compile_to_ll(scope)
    exe_file = scope.file.with_suffix(f'.{scope.target.exe_ext}')
    info(f'Compiling to executable file {exe_file.as_posix()} using clang')
    run(f'clang {ll_file.absolute().as_posix()} -o {exe_file}')
    return exe_file
