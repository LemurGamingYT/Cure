from argparse import ArgumentParser, Namespace
from sys import exit as sys_exit
from platform import system
from subprocess import run
from pathlib import Path
from shutil import which

from colorama import init, Fore, Style

from codegen import cure_to_c

init()


def format_c_file(file: Path) -> None:
    if which('clang-format') is not None:
        run(['clang-format', '-i', file.as_posix()])

def compile_file(file: Path, args: Namespace):
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
    
    if which('gcc') is not None:
        run(['gcc', *compargs])
    elif which('clang') is not None:
        run(['clang', *compargs])
    else:
        print(f'{Fore.RED}{Style.BRIGHT}gcc or clang is not installed{Style.RESET_ALL}')
        sys_exit(1)
    
    return c_file, exe_file

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

def main() -> None:
    arg_parser = ArgumentParser(description='Cure compiler')
    arg_parser.add_argument('file', type=Path, default='', nargs='?', help='File to compile')
    arg_parser.add_argument('--optimize', action='store_true', help='Optimize generated code')
    arg_parser.add_argument('--test', action='store_true', help='Run tests')
    arg_parser.add_argument('--keep-files', action='store_true',
                            help='Keep the executable and c files when using --test')
    arg_parser.add_argument('--clean', action='store_true',
                            help='Clean up the examples/ folder by deleting the .c and .exe files')
    args = arg_parser.parse_args()
    
    if args.file != Path('.'):
        compile(args.file, args)
        return
    
    if args.optimize:
        print('--optimize can only be used with a file')
        return
    
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
        total_tests = len(files)
        tests_passed = total_tests

        for file in files:
            try:
                c_file, exe_file = compile_file(file, args)
                if not args.keep_files:
                    c_file.unlink()
                    exe_file.unlink()
                
                print(f'{Fore.GREEN}{Style.BRIGHT}{file.as_posix()} test passed{Style.RESET_ALL}')
            except (SystemExit, Exception) as e:
                err = f'{Fore.RED}{Style.BRIGHT}{file.as_posix()} test failed'
                if isinstance(e, Exception):
                    err += f' due to: {e}'
                
                print(err + Style.RESET_ALL)
                tests_passed -= 1
        
        print(f'{Style.BRIGHT}{tests_passed}/{total_tests} tests passed{Style.RESET_ALL}')
    elif args.keep_exe:
        print('--keep-exe can only be used with --test')
        return
    
    if args.clean:
        c_files = (Path(__file__).parent / 'examples').glob('**/*.c')
        exe_files = (Path(__file__).parent / 'examples').glob('**/*.exe')
        for f in c_files:
            f.unlink()
        
        for f in exe_files:
            f.unlink()


if __name__ == '__main__':
    main()
