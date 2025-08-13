from logging import debug, info, error
from sys import exit as sys_exit
# from pprint import pformat
from subprocess import run
from pathlib import Path

from colorama import Fore, Style

from cure.ir import Scope, STDLIB_PATH, Position
from cure.ir_builder import IRBuilder


def parse(scope: Scope):
    ir_builder = IRBuilder(scope)
    program = ir_builder.build()
    # debug(f'Parsed program: {pformat(program)}')
    return program

def compile_to_str(scope: Scope):
    program = parse(scope)
    return program.analyse(scope).codegen(scope)

def compile_cmake(build_dir: Path = Path.cwd(), **kwargs):
    kwargs_str = ' '.join(f'{k}={v}' for k, v in kwargs.items())
    make_build_cmd = f'cmake -B {build_dir.as_posix()} {kwargs_str} -G "Ninja"'
    build_cmd = f'cmake --build {build_dir.as_posix()}'
    debug(f'Running CMake commands ({make_build_cmd} and {build_cmd})')
    return run(f'{make_build_cmd} && {build_cmd}', shell=True)

def compile_to_exe(scope: Scope):
    code = compile_to_str(scope)

    build_dir = scope.file.parent.absolute() / 'build'
    build_dir.mkdir(exist_ok=True)
    debug(f'Build Directory = {build_dir}')

    cmake_name = scope.file.stem
    build_type = 'Debug'
    debug(f'Build Type = {build_type}')
    debug(f'CMake Name = {cmake_name}')

    main_file = build_dir / 'main.cpp'
    main_file.write_text(code)
    debug(f'main.cpp = {main_file}')

    code_files = ' '.join([main_file.as_posix()] + [
        file.as_posix() for file in scope.dependencies
        if file.suffix == '.cpp'
    ])

    cmake_code = f"""cmake_minimum_required(VERSION 3.10)
project({cmake_name} LANGUAGES CXX)
# set(CMAKE_MESSAGE_LOG_LEVEL "WARNING")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE "{build_type}")
set(SOURCES {code_files})

add_executable({cmake_name} ${{SOURCES}})

target_include_directories({cmake_name} PRIVATE {STDLIB_PATH.absolute().as_posix()})

if (MSVC)
    target_compile_options({cmake_name} PRIVATE /W4)
else()
    target_compile_options({cmake_name} PRIVATE -Wall -Wextra -Wpedantic)
endif()

add_definitions(-D{scope.target.macro_name}=1)
"""
    
    for dep in scope.dependencies:
        if dep.name != 'packages.txt':
            continue

        packages = [line.strip() for line in dep.read_text().splitlines()]
        for package_name in packages:
            cmake_code += f"""
find_package({package_name} REQUIRED)
include_directories(${{{package_name.upper()}_INCLUDE_DIRS}})
target_link_libraries({cmake_name} PRIVATE ${{{package_name.upper()}_LIBRARIES}})
"""

    libs = [dep for dep in scope.dependencies if dep.is_dir()]
    for lib in libs:
        cmake_code += f"""
add_subdirectory({lib.as_posix()} ${{CMAKE_CURRENT_BINARY_DIR}}/{lib.name})
target_link_libraries({cmake_name} PRIVATE {lib.name})
target_include_directories({cmake_name} PRIVATE {lib.as_posix()}/include)
"""

    cmakelists = build_dir / 'CMakeLists.txt'
    cmakelists.write_text(cmake_code)
    
    kwargs = {'-S': cmakelists.parent.as_posix()}
    ret_code = compile_cmake(build_dir, **kwargs)
    if ret_code.returncode != 0:
        print(f'{Fore.RED}error: failed to build{Style.RESET_ALL}')
        return
    
    exec_name = f'{cmake_name}.exe'
    debug(f'Executable Name = {exec_name}')

    exec_file = build_dir / exec_name
    debug(f'Built Executable File = {exec_file}')

    new_exec_path = scope.file.parent / exec_name
    if new_exec_path.exists():
        new_exec_path.unlink()
    
    exec_file.rename(new_exec_path)

    debug(f'Executable File = {new_exec_path}')
    return new_exec_path

def create_scope(file: Path):
    scope = Scope(file)
    scope.use(Position(0, 0), 'builtins')
    return scope


class ArgParser:
    def __init__(self, args: list[str]):
        self.args = args
    
    def parse(self):
        action = self.arg(0)
        debug(f'CLI Action = {action}')
        match action:
            case 'build':
                self.build()
            case 'test':
                self.test()
            case _:
                error(f'Unknown action {action}')

                print('Usage: cure <action> <file>')
                if action is None:
                    print('No action')
                else:
                    print(f'Unknown action \'{action}\'')
                
                sys_exit(1)

    def arg(self, index: int):
        if index < len(self.args):
            return self.args[index]
        
        debug(f'No arg at index {index}')
        return None
    
    def test(self):
        from cure.tests import test
        test()
    
    def build(self, file_path: str | None = None):
        if file_path is None:
            file_path = self.arg(1)
        
        debug(f'File Path = {file_path}')
        if file_path is None:
            print('Usage: cure build <file>')
            print('No file')
            sys_exit(1)
        
        path = Path(file_path)
        debug(f'Path = {path}')
        if not path.exists():
            print('Usage: cure build <file>')
            print(f'File \'{file_path}\' does not exist')
            sys_exit(1)
        
        if not path.is_file():
            print('Usage: cure build <file>')
            print(f'File \'{file_path}\' is not a file')
            sys_exit(1)
        
        scope = create_scope(path)

        info('Compiling to executable')
        exec_path = compile_to_exe(scope)
        info(f'Compiled to executable at path {exec_path}')
