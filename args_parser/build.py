from dataclasses import dataclass, field
from subprocess import run
from pathlib import Path
from shutil import which
from logging import info

from codegen.target import Target, get_current_target
from codegen import cure_to_c


@dataclass(slots=True, unsafe_hash=True, frozen=True)
class CompileConfig:
    file: Path
    target: Target
    output: Path | None = field(default=None)
    is_testing: bool = field(default=False)
    is_release: bool = field(default=False)

@dataclass(slots=True, unsafe_hash=True, frozen=True)
class CompileResult:
    output: Path | None = field(default=None)
    error: str | None = field(default=None)
    
    @property
    def success(self) -> bool:
        return self.error is None


def format_c_file(path: Path) -> None:
    if which('clang-format') is None:
        return

    run(['clang-format', '-i', path.as_posix()])

def compile_file(config: CompileConfig) -> CompileResult:
    """Compile a `.cure` file to an executable file.

    Args:
        config (CompileConfig): The configurations for the compilation.

    Returns:
        CompileResult: The `CompileResult` instance containing the `Path` to the executable file and
        a possible error string.
    """
    
    c_file = config.file.with_suffix('.c')
    exe_file = config.output or config.file.with_suffix(config.target.exe_ext())
    codegen, _ = cure_to_c(config.file, c_file, config.target)
    if codegen.scope.env.get('main') is None:
        return CompileResult(error='No main function found')

    if config.is_testing:
        # don't format the C file if testing, it will slow down the tests
        codegen.extra_compile_args.append('-DTEST')
    else:
        format_c_file(c_file)
    
    if config.is_release:
        codegen.extra_compile_args.append('-O3')
    
    if config.target != get_current_target():
        msg = 'Target does not match current OS, skipping compilation'
        info(msg)
        return CompileResult(error=msg)
    else:
        compargs = [c_file.as_posix(), '-o', exe_file.as_posix(), *codegen.extra_compile_args]
        if which('gcc') is not None:
            run(['gcc', *compargs])
            info(f'Compiling \'{c_file.name}\' with gcc')
        elif which('clang') is not None:
            run(['clang', *compargs])
            info(f'Compiling \'{c_file.name}\' with clang')
        else:
            return CompileResult(error='Could not find a supported C compiler')
    
    return CompileResult(exe_file)
