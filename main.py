from argparse import ArgumentParser, Namespace
from sys import exit as sys_exit
from subprocess import run
from pathlib import Path
from shutil import which

from colorama import init, Fore, Style

from codegen.target import Target, get_target_from_string, get_current_target
from codegen import cure_to_c
# from repl import repl

init()


examples = (Path(__file__).parent / 'examples').absolute()


def format_c_file(file: Path) -> None:
    if which('clang-format') is not None:
        run(['clang-format', '-i', file.as_posix()])

def compile_file(file: Path, args: Namespace):
    c_file = file.with_suffix('.c')
    exe_file = file.with_suffix('.exe' if args.target == Target.WINDOWS else '')
    
    codegen, _ = cure_to_c(file, c_file, args.target)
    if codegen.scope.env.get('main') is None:
        err = f'{file.as_posix()} does not have a main function'
        print(f'{Fore.RED}{Style.BRIGHT}{err}{Style.RESET_ALL}')
        sys_exit(1)
    
    if args.test:
        codegen.extra_compile_args.append('-DTEST')
    else:
        format_c_file(c_file)
    
    compargs = [c_file.as_posix(), '-o', exe_file.as_posix(), *codegen.extra_compile_args]
    if args.optimize:
        compargs.append('-O2')
    
    if args.target == get_current_target():
        if which('gcc') is not None:
            run(['gcc', *compargs])
        elif which('clang') is not None:
            run(['clang', *compargs])
        else:
            print(f'{Fore.RED}{Style.BRIGHT}gcc or clang is not installed{Style.RESET_ALL}')
            sys_exit(1)
    else:
        skip_msg = 'Skipping compilation: Target does not match current OS'
        print(f'{Fore.CYAN}{Style.BRIGHT}{skip_msg}{Style.RESET_ALL}')
    
    if args.test and len(codegen.preprocessor.tests) > 0:
        ret = run([exe_file.as_posix()])
        if ret.returncode != 0:
            print(f'{Fore.RED}{Style.BRIGHT}{file.as_posix()} failed{Style.RESET_ALL}')
            sys_exit(1)
        
        print(f'{Fore.GREEN}{Style.BRIGHT}{file.as_posix()} test passed{Style.RESET_ALL}')
        
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

def test(
    file: Path, exclude_files: list[Path], args: Namespace, run_exe: bool = False
) -> tuple[int, int]:
    files = []
    for f in file.glob('**/*.cure'):
        should_add = True
        for exclude in exclude_files:
            if exclude.is_file() and f == exclude:
                should_add = False
                break
            
            if exclude.is_dir() and f.parent == exclude:
                should_add = False
                break
        
        if should_add:
            files.append(f)
    
    total_tests = len(files)
    tests_passed = total_tests

    for file in files:
        strf = file.as_posix()
        try:
            c_file, exe_file = compile_file(file, args)
            if run_exe:
                ret = run([exe_file.as_posix()])
                if ret.returncode != 0:
                    print(f'{Fore.RED}{Style.BRIGHT}{strf} returned {ret.returncode}{Style.RESET_ALL}')
                    tests_passed -= 1
            
            if not args.keep_files:
                c_file.unlink()
                exe_file.unlink()
            
            print(f'{Fore.GREEN}{Style.BRIGHT}{strf} test passed{Style.RESET_ALL}')
        except (SystemExit, Exception) as e:
            err = f'{Fore.RED}{Style.BRIGHT}{strf} test failed'
            if isinstance(e, Exception):
                err += f' due to: {e}'
            
            print(err + Style.RESET_ALL)
            tests_passed -= 1
    
    return tests_passed, total_tests

def rm_recursive(parent: Path, extension: str) -> None:
    for f in parent.glob(f'**/*.{extension}'):
        f.unlink()

def main() -> None:
    arg_parser = ArgumentParser(description='Cure compiler')
    arg_parser.add_argument('file', type=Path, default=None, nargs='?', help='File to compile')
    arg_parser.add_argument('--optimize', action='store_true', help='Optimize generated code')
    arg_parser.add_argument('--test', action='store_true', help='Run tests')
    arg_parser.add_argument('--keep-files', action='store_true',
                            help='Keep the executable and c files when using --test')
    arg_parser.add_argument('--clean', action='store_true',
                            help='Clean up the examples/ folder by deleting the .c and .exe files')
    arg_parser.add_argument('--target', type=str, default=None, help='Target to compile for')
    args = arg_parser.parse_args()
    
    if args.target is not None:
        args.target = get_target_from_string(args.target)
        if args.target is None:
            print(f'{Fore.RED}{Style.BRIGHT}Invalid target{Style.RESET_ALL}')
            print(f'Valid targets: {", ".join(target.name.title() for target in list(Target))}')
            return
    else:
        args.target = get_current_target()
    
    if args.file is not None:
        compile(args.file, args)
        return
    
    if args.optimize:
        print('--optimize can only be used with a file')
        return
    
    if args.test:
        tests_passed, total_tests = test(
            examples, [examples / 'tests', examples / 'libraries/local_file.cure'], args
        )
        print(f'{Style.BRIGHT}{tests_passed}/{total_tests} tests passed{Style.RESET_ALL}')
        
        print(f'{Style.BRIGHT}Executing examples/tests/{Style.RESET_ALL}')
        tests_passed, total_tests = test(examples / 'tests', [], args, True)
        print(f'{Style.BRIGHT}{tests_passed}/{total_tests} tests passed{Style.RESET_ALL}')
    elif args.keep_files:
        print('--keep-exe can only be used with --test')
        return
    
    if args.clean:
        rm_recursive(examples, 'c')
        rm_recursive(examples, 'exe')
        rm_recursive(examples, 'h')
        return
    
    # repl()


if __name__ == '__main__':
    main()
