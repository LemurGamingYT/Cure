from sys import exit as sys_exit
from logging import debug, info
from subprocess import run
from pprint import pformat
from pathlib import Path
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
    # flags = ['-fno-omit-frame-pointer', '-fsanitize=address']
    # flags_str = ' '.join(flags)
    run(f'clang {ll_file.absolute().as_posix()} -o {exe_file}')
    return exe_file


class CureArgParser:
    def __init__(self, args: list[str]):
        self.args = args
    
    def get_actions(self):
        for k, v in self.__dict__.items():
            print(k, v)
        
        return []

    def parse(self):
        if len(self.args) == 1:
            self.__help()
            return
        
        action = self.args[1]
        match action:
            case 'build':
                self.__build()
            case 'help':
                self.__help()
            case _:
                actions = self.get_actions()
                print(f"""cure [action] [options]
invalid action {action}'
possible actions: {', '.join(actions)}""")
    
    def get(self, arg_index: int):
        if len(self.args) <= arg_index:
            return None
        
        return self.args[arg_index]
    
    def __help(self):
        print('cure [action] [options]')

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
