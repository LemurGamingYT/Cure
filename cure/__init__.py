from sys import exit as sys_exit
from subprocess import run
from logging import info
from pathlib import Path

from colorama import Fore, Style

from cure.ir import Scope, Position, STDLIB_PATH
from cure.ir_builder import IRBuilder


def compile_to_str(scope: Scope):
    ir_builder = IRBuilder(scope)
    program = ir_builder.build()
    return program.analyse(scope).codegen(scope)

def compile_cmake(build_dir: Path = Path.cwd(), **kwargs):
    kwargs_str = ' '.join(f'{k}={v}' for k, v in kwargs.items())
    make_build_cmd = f'cmake -B {build_dir.as_posix()} {kwargs_str} -G "Ninja"'
    build_cmd = f'cmake --build {build_dir.as_posix()}'
    return run(f'{make_build_cmd} && {build_cmd}', shell=True)

def compile_to_exe(scope: Scope):
    code = compile_to_str(scope)
    info(f'Generated code: {code}')

    build_dir = scope.file.parent.absolute() / 'build'
    build_dir.mkdir(exist_ok=True)

    cmake_name = scope.file.stem
    build_type = 'Debug'

    cfile = build_dir / 'main.c'
    cfile.write_text(code)

    cfiles = [f' {file.as_posix()}' for file in scope.dependencies if file.suffix == '.c']

    cmakelists = build_dir / 'CMakeLists.txt'
    cmakelists.write_text(f"""cmake_minimum_required(VERSION 3.10)
project({cmake_name} LANGUAGES C)
set(CMAKE_BUILD_TYPE "{build_type}")
set(SOURCES {cfile.as_posix()}{''.join(cfiles)})

add_executable({cmake_name} ${{SOURCES}})

target_include_directories({cmake_name} PRIVATE {STDLIB_PATH.absolute().as_posix()})

if (MSVC)
    target_compile_options({cmake_name} PRIVATE /W4)
else()
    target_compile_options({cmake_name} PRIVATE -Wall -Wextra -Wpedantic)
endif()
""")
    
    kwargs = {'-S': cmakelists.parent.as_posix()}
    ret_code = compile_cmake(build_dir, **kwargs)
    if ret_code.returncode != 0:
        print(f'{Fore.RED}error: failed to build{Style.RESET_ALL}')
        sys_exit(1)
    
    exec_name = f'{cmake_name}.exe'
    exec_file = build_dir / exec_name
    new_exec_path = scope.file.parent / exec_name
    if new_exec_path.exists():
        new_exec_path.unlink()
    
    exec_file.rename(new_exec_path)


class ArgParser:
    def __init__(self, args: list[str]):
        self.args = args
    
    def parse(self):
        action = self.arg(0)
        match action:
            case 'build':
                self.build()
            case _:
                print('Usage: cure <action> <file>')
                if action is None:
                    print('No action')
                else:
                    print(f'Unknown action \'{action}\'')
                
                sys_exit(1)

    def arg(self, index: int):
        if index < len(self.args):
            return self.args[index]
        
        return None
    
    def build(self, file_path: str | None = None):
        if file_path is None:
            file_path = self.arg(1)
        
        if file_path is None:
            print('Usage: cure build <file>')
            print('No file')
            sys_exit(1)
        
        path = Path(file_path)
        if not path.exists():
            print('Usage: cure build <file>')
            print(f'File \'{file_path}\' does not exist')
            sys_exit(1)
        
        if not path.is_file():
            print('Usage: cure build <file>')
            print(f'File \'{file_path}\' is not a file')
            sys_exit(1)
        
        scope = Scope(path)
        scope.use(Position.zero(), 'builtins')
        compile_to_exe(scope)
