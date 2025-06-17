from ctypes import CFUNCTYPE, c_int
from dataclasses import dataclass
from sys import exit as sys_exit
from logging import debug, info
from time import perf_counter
from subprocess import run
from pprint import pformat
from pathlib import Path
from typing import cast

from llvmlite import binding as llvm

from cure.passes.code_generation import CodeGeneration
from cure.parser.ir_builder import CureIRBuilder
from cure.passes.analyser import Analyser
from cure import ir


@dataclass
class CompileOptions:
    optimize: bool


def parse(scope: ir.Scope, _: CompileOptions):
    info(f'Compiling {scope.file.as_posix()}')
    program = CureIRBuilder(scope.src).build()

    info(f'Parsed {scope.file.as_posix()}')
    debug(f'IR = {pformat(program)}')
    return program

def compile_to_str(scope: ir.Scope, options: CompileOptions):
    program = parse(scope, options)
    program = Analyser.run(scope, program)
    debug(f'Analysed IR = {pformat(program, indent=4)}')
    return CodeGeneration.run(scope, cast(ir.Program, program))

def compile_to_ll(scope: ir.Scope, options: CompileOptions):
    info(f'Compiling {scope.file.as_posix()} to an LLVM IR file (.ll)')
    code = compile_to_str(scope, options)
    debug(f'LLVM IR = {code}')
    ll_file = scope.file.with_suffix('.ll')
    ll_file.write_text(code)
    info(f'Wrote to {ll_file.as_posix()}')
    return ll_file

def compile_to_exe(scope: ir.Scope, options: CompileOptions):
    ll_file = compile_to_ll(scope, options)
    exe_file = scope.file.with_suffix(f'.{scope.target.exe_ext}')
    info(f'Compiling to executable file {exe_file.as_posix()} using clang')
    flags: list[str] = []
    if options.optimize:
        flags.append('-O2')
    
    flags_str = ' '.join(flags)
    run(f'clang {ll_file.absolute().as_posix()} -o {exe_file} {flags_str}')
    return exe_file

def jit(scope: ir.Scope, options: CompileOptions):
    opt = 0 if not options.optimize else 2

    code = compile_to_str(scope, options)
    target_machine = llvm.Target.from_default_triple().create_target_machine(opt=opt)
    backing_mod = llvm.parse_assembly(code)
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    engine.finalize_object()
    engine.run_static_constructors()

    main_ptr = engine.get_function_address('main')
    main = CFUNCTYPE(c_int)(main_ptr)

    debug('Running main function')
    start = perf_counter()
    res = main()
    end = perf_counter()
    debug(f'Main function executed in {(end - start) * 1000:.3f}ms and returned {res}')


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
            case 'run':
                self.__run()
            case 'help':
                self.__help()
            case _:
                print(f"""{HELP}
invalid action {action}'""")
    
    def get(self, arg_index: int):
        if len(self.args) <= arg_index:
            return None
        
        return self.args[arg_index]
    
    def flag(self, name: str):
        try:
            i = self.args.index(f'--{name}')
            if len(self.args) - 1 >= i:
                return True
            
            next_value = self.args[i + 1]
            if next_value.startswith('-'):
                return True
            
            return next_value
        except ValueError:
            return None
    
    def __help(self):
        print(HELP)

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
        
        optimize = self.flag('optimize')
        options = CompileOptions(optimize)

        scope = ir.Scope(file)
        compile_to_exe(scope, options)
    
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
        
        optimize = self.flag('optimize')
        options = CompileOptions(optimize)
        
        scope = ir.Scope(file)
        jit(scope, options)
