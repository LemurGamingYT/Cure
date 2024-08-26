from argparse import ArgumentParser
from platform import system
from subprocess import run
from pathlib import Path
from shutil import which

from codegen import CodeGen
from ir import IRBuilder


def compile_file(file: Path, args) -> None:
    c_file = file.with_suffix('.c')
    exe_file = file.with_suffix('.exe' if system() == 'Windows' else '.')
    
    builder = IRBuilder()
    program = builder.build(file.read_text('utf-8'))
    
    codegen = CodeGen()
    generated_code = codegen.generate(program)
    c_file.write_text(generated_code, 'utf-8')
    
    if which('clang-format') is not None:
        run(['clang-format', '-i', c_file.as_posix()])
    
    compargs = [c_file.as_posix(), '-o', exe_file.as_posix(), *codegen.extra_compile_args]
    if args.optimize:
        compargs.append('-O2')
    
    if which('gcc') is not None:
        run(['gcc', *compargs])
    elif which('clang') is not None:
        run(['clang', *compargs])
    else:
        print('gcc or clang is not installed')

def compile(file: Path, args) -> None:
    if file.is_file():
        compile_file(file, args)
    elif file.is_dir():
        for f in file.iterdir():
            if f.is_file() and f.suffix == '.cure':
                print(f'Compiling {f.name}')
                
                compile_file(f, args)
            elif f.is_dir():
                compile(f, args)
    else:
        print('File or directory not found')

def main() -> None:
    arg_parser = ArgumentParser(description='Cure compiler')
    arg_parser.add_argument('file', type=Path, help='File to compile')
    arg_parser.add_argument('-opt', '--optimize',
                            action='store_true', help='Optimize generated code')
    args = arg_parser.parse_args()
    
    file: Path = args.file
    compile(file, args)


if __name__ == '__main__':
    main()
