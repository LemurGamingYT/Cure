from dataclasses import dataclass, field
from sys import argv, exit as sys_exit
from subprocess import run
from logging import info
from pathlib import Path
from json import loads

from colorama import Fore, Style

from args_parser.project_writer import cli_project_create, is_project, ask_user
from codegen.target import get_current_target, get_target_from_string, Target
from args_parser.build import compile_file, CompileConfig
from codegen.objects import CURE_VERSION


TARGETS = {target.name.title() for target in list(Target)}
USAGE = 'Usage: cure <action> [options]'
HELP = f"""{USAGE}

Actions:
    init        Initialise a new Cure Project in the current directory
    build       Build a Cure file or project to an executable file
    run         Build and Run a Cure file
    help        Print this help and exit
    version     Print the current Cure version and exit
    clean       Remove all executable and c files
"""

@dataclass(slots=True, unsafe_hash=True, frozen=True)
class ParseResult:
    success: bool = field(default=True)
    error: str | None = field(default=None)
    output: Path | None = field(default=None)
    
    def __str__(self) -> str:
        if self.success:
            return ''
        
        return 'An error occurred' if self.error is None else self.error
    
    def __repr__(self) -> str:
        return self.__str__()

class CureArgumentParser:
    def __init__(self) -> None:
        if len(argv) <= 1:
            print(HELP)
            sys_exit(1)
    
    def parse_args(self) -> ParseResult:
        action = argv[1]
        match action:
            case 'version':
                print(CURE_VERSION)
            case 'help':
                print(HELP)
            case 'init':
                success, err = cli_project_create()
                return ParseResult(success, err)
            case 'build':
                return self.build(None if len(argv) <= 2 else Path(argv[2]))
            case 'run':
                result = self.build(None if len(argv) <= 2 else Path(argv[2]))
                if not result.success or result.output is None:
                    return result
                
                res = run([result.output.as_posix()])
                if res.returncode != 0:
                    return ParseResult(False, f'{result.output.stem} returned {res.returncode}')
            case 'test':
                path = Path.cwd() if len(argv) <= 2 else Path(argv[2])
                tests = path.rglob('*.cure')
                total_tests = len(list(tests))
                passed_tests = total_tests
                for file in path.rglob('*.cure'):
                    try:
                        result = self.build(file)
                        if not result.success or result.output is None:
                            sys_exit(1) # causes the SystemExit except block to run
                    except SystemExit:
                        passed_tests -= 1
                        print(f'{Fore.RED}{Style.BRIGHT}{file} failed{Style.RESET_ALL}')
                
                if total_tests > passed_tests:
                    print(f'{Fore.RED}{Style.BRIGHT}Some tests failed ({passed_tests}/{total_tests})'\
                        f'{Style.RESET_ALL}')
                else:
                    print(f'{Fore.GREEN}{Style.BRIGHT}All tests passed ({total_tests} in total)'\
                        f'{Style.RESET_ALL}')
            case 'clean':
                path = Path.cwd() if len(argv) <= 2 else Path(argv[2])
                for c_file in path.rglob('*.c'):
                    c_file.unlink()
                
                for exe_file in path.rglob('*.exe'):
                    exe_file.unlink()
            case _:
                return ParseResult(
                    False, f'Invalid action \'{action}\', try `cure help` to view possible actions'
                )
        
        return ParseResult()
    
    def get_output_path(self) -> Path | None | ParseResult:
        output: Path | None = None
        for i, arg in enumerate(argv):
            if arg != '-o':
                continue
            
            if len(argv) < i + 1:
                return ParseResult(False, '-o needs a file after it')
            
            output = Path(argv[i + 1])
            if not output.exists():
                return ParseResult(False, f'{output} does not exist (set as output in -o)')
            
            break
        
        return output # type: ignore
    
    def get_target(self) -> Target | ParseResult:
        target: Target | None = get_current_target()
        for arg in argv:
            if not arg.startswith('--target'):
                continue
            
            if not arg.startswith('--target='):
                arg = ask_user(
                    'What target do you want to target', TARGETS,
                    f'Please enter a valid target, possible targets: {list(TARGETS)}'
                )
            else:
                if len(arg.split('=')) <= 1:
                    return ParseResult(False, 'Enter a target (e.g. --target=Windows)')
                
                arg = arg.split('=')[1]
            
            target = get_target_from_string(arg)
            if target is None:
                return ParseResult(False, f'Invalid target, possible targets: {list(TARGETS)}')
            
            break
        
        return target # type: ignore
    
    def build_project(self) -> ParseResult:
        path = Path.cwd()
        if not is_project(path):
            return ParseResult(False, f'Current directory ({path}) is not a Cure Project')
        
        json = loads((path / 'project.json').read_text('utf-8'))
        main_file = json.get('main-file')
        if main_file is None:
            return ParseResult(False, 'Invalid main file')
        
        return self.build(main_file)
    
    def build(self, file: Path | None = None) -> ParseResult:
        if len(argv) <= 2 and file is None:
            return self.build_project()
        
        target = self.get_target()
        if isinstance(target, ParseResult):
            return target
        
        output = self.get_output_path()
        if isinstance(output, ParseResult):
            return output
        
        config = CompileConfig(
            file, target, output, # type: ignore
            '--test' in argv, '--release' in argv
        )
        
        result = compile_file(config)
        if not result.success:
            return ParseResult(result.success, result.error)
        
        info(f'Compiled to {result.output}')
        return ParseResult(output=result.output)
