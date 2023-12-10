from antlr4 import CommonTokenStream, FileStream

from core.parser.CureParser import CureParser
from core.parser.CureLexer import CureLexer
from core.compiler import Compiler
from api import ASTVisitor

from argparse import ArgumentParser
from time import perf_counter
from pathlib import Path


def report_time(file: Path, start: float, end: float):
    print(f'Time to execute for file {file}: {(end - start) * 1000:.4f}ms')


def output_to(file: Path, output: Path | None, out: str) -> None:
    if output:
        if output.is_dir():
            (output / file.name).write_text(out)
        else:
            output.write_text(out)
    else:
        file.with_suffix('.cpp').write_text(out)


def main():
    arg_parser = ArgumentParser(description='Cure compiler')
    
    arg_parser.add_argument('file', type=Path, help='File to compile')
    arg_parser.add_argument('-o', '--output', type=Path, help='Output C++ file to path')
    
    args = arg_parser.parse_args()
    
    if args.file.is_file():
        start = perf_counter()
        
        lexer = CureLexer(FileStream(args.file.absolute().as_posix()))
        parser = CureParser(CommonTokenStream(lexer))
        tree = parser.parse()
        
        compiler = Compiler()
        program = compiler.compile(tree)
        
        output_to(args.file, args.output, ASTVisitor().visit(program))
        
        end = perf_counter()
        
        report_time(args.file, start, end)
    elif args.file.is_dir():
        for file in args.file.rglob('*.cure'):
            start = perf_counter()

            lexer = CureLexer(FileStream(file.absolute().as_posix()))
            parser = CureParser(CommonTokenStream(lexer))
            tree = parser.parse()

            compiler = Compiler()
            program = compiler.compile(tree)

            output_to(file, args.output, ASTVisitor().visit(program))

            end = perf_counter()

            report_time(file, start, end)
    else:
        print(f'File {args.file} does not exist')


if __name__ == '__main__':
    main()
