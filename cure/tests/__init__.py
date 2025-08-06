from contextlib import suppress
from subprocess import run
from shutil import rmtree
from pathlib import Path

from colorama import Fore, Style

from cure import create_scope, compile_to_str, compile_to_exe


def format_file(file: Path):
    return file.relative_to(Path.cwd()).as_posix()

def test_compiler():
    compiler_dir = Path.cwd() / 'cure' / 'tests' / 'compiler'
    files = list(compiler_dir.glob('*.cure'))
    num_files = len(files)

    fails = []
    for file in files:
        print(f'Compiling file {file.as_posix()}')
        if file.stem.startswith('pass'):
            try:
                scope = create_scope(file)
                compile_to_str(scope)
            except SystemExit:
                fails.append(file)
        elif file.stem.startswith('fail'):
            with suppress(SystemExit):
                scope = create_scope(file)
                compile_to_str(scope)
                fails.append(file)
    
    return fails, num_files

def test_examples():
    examples_dir = Path.cwd() / 'examples'
    files = list(examples_dir.glob('*.cure'))
    num_files = len(files)

    fails = []
    for file in files:
        print(f'Compiling file {file.as_posix()}')
        scope = create_scope(file)
        if file.stem.startswith('pass'):
            try:
                scope = create_scope(file)
                compile_to_str(scope)
            except SystemExit:
                fails.append(file)
        elif file.stem.startswith('fail'):
            with suppress(SystemExit):
                scope = create_scope(file)
                compile_to_str(scope)
                fails.append(file)
    
    return fails, num_files

def test_runtime():
    runtime_dir = Path.cwd() / 'cure' / 'tests' / 'runtime'
    files = list(runtime_dir.glob('*.cure'))
    num_files = len(files)

    fails = []
    for file in files:
        print(f'Compiling file {file.as_posix()}')
        scope = create_scope(file)

        try:
            exec_file = compile_to_exe(scope)
            if exec_file is None:
                fails.append(file)
                continue

            print(f'Running file {file.as_posix()}')
            res = run(exec_file)
            if res.returncode != 0:
                fails.append(file)
        except SystemExit:
            fails.append(file)
    
    build_dir = runtime_dir / 'build'
    if build_dir.exists():
        rmtree(build_dir)
    
    build_files = runtime_dir.glob('*.exe')
    for file in build_files:
        file.unlink()
    
    return fails, num_files

def test():
    compile_fails, compile_num_files = test_compiler()
    runtime_fails, runtime_num_files = test_runtime()
    examples_fails, examples_num_files = test_examples()

    total_num_files = compile_num_files + runtime_num_files + examples_num_files
    all_fails = compile_fails + runtime_fails + examples_fails
    success = len(all_fails) == 0
    if success:
        print(f'{Fore.GREEN}{Style.BRIGHT}All tests passed{Style.RESET_ALL}')
    else:
        passed = f'{total_num_files - len(all_fails)}/{total_num_files}'
        print(f'{Fore.RED}{Style.BRIGHT}Some tests failed: {passed}{Style.RESET_ALL}')

        all_fails_str = ', '.join(format_file(file) for file in all_fails)
        print(f'fails: {all_fails_str}')
