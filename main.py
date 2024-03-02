from argparse import ArgumentParser
from sys import exit as sys_exit
from os import system as shell
from pathlib import Path

from antlr4 import CommonTokenStream, FileStream

from parser.CureParser import CureParser
from parser.CureLexer import CureLexer
from compiler import Compiler


def build_file(f: Path, should_build: bool = True, file_extension: str = '.c') -> Path:
    fstream = FileStream(f.absolute().as_posix())
    lexer = CureLexer(fstream)
    tokens = CommonTokenStream(lexer)

    parser = CureParser(tokens)
    tree = parser.parse()

    compiler = Compiler()
    src = compiler.visitParse(tree)

    c_file = f.with_suffix(file_extension)
    cure_h = Path('compiler/cure.h')
    rel_path = cure_h.relative_to(c_file, walk_up=True).as_posix()[3:].replace('\\', '/')

    c_file.write_text(f'#include "{rel_path}"\n\n\n{src}')
    if args.build and should_build:
        exe_file = f.with_suffix('.exe')
        shell(f'gcc -o {exe_file} {c_file}{" -O2" if args.release else ""}')

        if args.run:
            shell(exe_file.absolute().as_posix())

        if args.clean:
            c_file.unlink()


def main() -> None:
    if args.input.is_dir():
        for f in args.input.iterdir():
            if f.is_file() and f.suffix == '.cure':
                build_file(f)
    else:
        build_file(args.input)



if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Cure compiler')

    arg_parser.add_argument('input', type=Path, help='File or directory to compile')
    arg_parser.add_argument('-b', '--build', action='store_true', help='Build the file to an exe')
    arg_parser.add_argument('--run', action='store_true', help='Run the exe file after building')
    arg_parser.add_argument('-c', '--clean', action='store_true', help='Clean after building')
    arg_parser.add_argument('--release', action='store_true', help='Add -O2 flag while building exe')

    args = arg_parser.parse_args()
    
    if not args.build and args.run:
        print('--run can only be used with --build')
        sys_exit(1)

    main()
