from argparse import ArgumentParser, Namespace
from subprocess import run, CompletedProcess
from sys import exit as sys_exit
from multiprocessing import Pool
from platform import system
from pathlib import Path
from shutil import which

from colorama import init, Fore, Style

from codegen import cure_to_c

init()


def format_c_file(file: Path) -> None:
    if which('clang-format') is not None:
        run(['clang-format', '-i', file.as_posix()])

def compile_file(file: Path, args: Namespace) -> None:
    c_file = file.with_suffix('.c')
    exe_file = file.with_suffix('.exe' if system() == 'Windows' else '.')
    
    codegen, _ = cure_to_c(file, c_file)
    if codegen.scope.env.get('main') is None:
        err = f'{file.as_posix()} does not have a main function'
        print(f'{Fore.RED}{Style.BRIGHT}{err}{Style.RESET_ALL}')
        sys_exit(1)
    
    if not args.test:
        format_c_file(c_file)
    
    compargs = [c_file.as_posix(), '-o', exe_file.as_posix(), *codegen.extra_compile_args]
    if args.optimize:
        compargs.append('-O2')
    
    process_exit: CompletedProcess[bytes]
    if which('gcc') is not None:
        process_exit = run(['gcc', *compargs])
    elif which('clang') is not None:
        process_exit = run(['clang', *compargs])
    else:
        print(f'{Fore.RED}{Style.BRIGHT}gcc or clang is not installed{Style.RESET_ALL}')
        sys_exit(1)
    
    if args.test:
        if process_exit.returncode != 0:
            format_c_file(c_file)
            print(f'{Fore.RED}{Style.BRIGHT}{file.as_posix()} test failed{Style.RESET_ALL}')
            sys_exit(1)

        c_file.unlink()
        
        if not args.keep_exe:
            exe_file.unlink()
        
        print(f'{Fore.GREEN}{Style.BRIGHT}{file.as_posix()} test passed{Style.RESET_ALL}')

def compile_dir(file: Path, args: Namespace) -> None:
    for f in file.iterdir():
        if f.is_file() and f.suffix == '.cure':
            compile_file(f, args)
        else:
            compile(f, args)

def compile(file: Path, args: Namespace) -> None:
    if file.is_file() and file.suffix == '.cure':
        compile_file(file, args)
    elif file.is_dir():
        compile_dir(file, args)
    else:
        print(f'{Fore.RED}{Style.BRIGHT}{file.as_posix()} does not exist{Style.RESET_ALL}')

def _file_compile(a) -> None:
    file, args = a
    compile_file(file, args)

def main() -> None:
    arg_parser = ArgumentParser(description='Cure compiler')
    arg_parser.add_argument('file', type=Path, help='File to compile')
    arg_parser.add_argument('--optimize', action='store_true', help='Optimize generated code')
    arg_parser.add_argument('--test', action='store_true', help='Run tests')
    arg_parser.add_argument('--keep-exe', action='store_true',
                            help='Keep the executable files when using --test')
    args = arg_parser.parse_args()
    
    if args.test:
        def _add_files(file: Path) -> None:
            if file.is_file() and file.suffix == '.cure':
                if file.name in {'local_file.cure', 'local_file.h'}:
                    return
                
                files.append(file)
            elif file.is_dir():
                for f in file.iterdir():
                    _add_files(f)
        
        files: list[Path] = []
        _add_files(Path('examples'))

        with Pool(3) as pool:
            pool.map(_file_compile, [(file, args) for file in files])
    else:
        compile(args.file, args)


if __name__ == '__main__':
    main()
