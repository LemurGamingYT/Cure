from logging import debug, info, error
from ctypes import CFUNCTYPE, c_int
from sys import exit as sys_exit
from time import perf_counter
from subprocess import run
from pprint import pformat
from pathlib import Path
from typing import cast

from llvmlite import binding as llvm

from cure.passes.code_generation import CodeGeneration
from cure.passes.analyser import Analyser
from cure.parser.parser import CureParser
from cure.parser.lexer import CureLexer
from cure import ir


def parse(scope: ir.Scope):
    info(f'Compiling {scope.file.as_posix()}')
    lexer = CureLexer()
    tokens = lexer.lex(scope.src)

    parser = CureParser(scope.src)
    program = cast(ir.Program, parser.parse(tokens))

    info(f'Parsed {scope.file.as_posix()}')
    debug(f'IR = {pformat(program)}')
    return program

def compile_and_run(scope: ir.Scope):
    program = parse(scope)
    program = Analyser.run(scope, program)
    debug(f'Analysed IR = {pformat(program, indent=4)}')
    code = CodeGeneration.run(scope, cast(ir.Program, program))

    info('Creating and verifying assembly code')
    llvm_ir = llvm.parse_assembly(code)

    try:
        llvm_ir.verify()
    except RuntimeError as e:
        print('An error occurred while generating code')
        error(f'{e.args}')
        return 1

    info('Created and verified assembly code')
    info('Creating target machine')
    target_machine = llvm.Target.from_default_triple().create_target_machine()
    engine = llvm.create_mcjit_compiler(llvm_ir, target_machine)
    engine.finalize_object()

    info('Created target machine')
    info('Running main function')
    entry = engine.get_function_address('main')
    if entry == 0:
        print('no main function')
        error('Main function address is null')
    
    info(f'Found main function address: {hex(entry)}')

    cfunc = CFUNCTYPE(c_int)(entry)

    info('Running program')
    start = perf_counter()
    try:
        res = cfunc()
    except Exception as e:
        error(f'Runtime error: {e}')
        return 1

    end = perf_counter()
    info(f'Executed in {(end - start) * 1000:.3f}ms and returned {res}')
    return res

def compile_to_str(scope: ir.Scope):
    program = parse(scope)
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
    # flags = ['-fno-omit-frame-pointer', '-fsanitize=address']
    # flags_str = ' '.join(flags)
    run(f'clang {ll_file.absolute().as_posix()} -o {exe_file}')
    return exe_file


HELP = """usage: cure [action] [options]

actions: build, help
"""


class CureArgParser:
    def __init__(self, args: list[str]):
        self.args = args

    def parse(self):
        if len(self.args) == 1:
            self.__help()
            return
        
        action = self.args[1]
        match action:
            case 'build':
                self.__build()
            # case 'run':
            #     self.__run() # crashes for some reason
            case 'help':
                self.__help()
            case _:
                print(f"""{HELP}
invalid action {action}'""")
    
    def get(self, arg_index: int):
        if len(self.args) <= arg_index:
            return None
        
        return self.args[arg_index]
    
    def __help(self):
        print(HELP)
    
    def __run(self):
        file_str = self.get(2)
        if file_str is None:
            print("""cure run [file]
file argument not given""")
            sys_exit(1)
        
        file = Path(file_str)
        if not file.exists():
            print("""cure run [file]
file does not exist""")
            sys_exit(1)
        
        if not file.is_file():
            print("""cure run [file]
file is not a file""")
            sys_exit(1)
        
        scope = ir.Scope(file)
        compile_and_run(scope)

    def __build(self):
        file_str = self.get(2)
        if file_str is None:
            print("""cure build [file]
file argument not given""")
            sys_exit(1)
        
        file = Path(file_str)
        if not file.exists():
            print("""cure build [file]
file does not exist""")
            sys_exit(1)
        
        if not file.is_file():
            print("""cure build [file]
file is not a file""")
            sys_exit(1)
        
        scope = ir.Scope(file)
        compile_to_exe(scope)
