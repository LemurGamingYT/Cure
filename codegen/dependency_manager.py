from typing import Callable
from pathlib import Path

from codegen.c_manager import STD_PATH, CManager
from codegen.objects import Position


class DependencyManager:
    def __init__(self, codegen, strtoc: Callable) -> None:
        self.codegen = codegen
        
        self.running_file: Path | None = None
        self.strtoc = strtoc
        
        self.dependencies: list[type] = []
    
    def is_file_target_lib(self, a: Path, b: Path) -> bool:
        return a == b or a.stem == b.stem
        
    def use_builtin(self, lib: Path, lib_name: str, p: Path, pos: Position) -> None:
        rel_path = p.relative_to(STD_PATH)
        lib_path = rel_path.as_posix().replace('/', '.')
        if lib_path.endswith('.py'):
            lib_path = lib_path.removesuffix('.py')
        
        exec(f"""from .std.{lib_path} import {lib.stem}
if {lib.stem} not in [type(cls) for cls in dependencies]:
    lib = {lib.stem}(self)
    if not getattr(lib, 'CAN_USE', True):
        pos.error_here(f'Library \\'{lib_name}\\' cannot be used')
    
    dependencies.append(lib)
    objects = CManager.get_all_objects(lib)
    for k, v in objects.items():
        setattr(c_manager, k, v)
""", globals(), {
    'c_manager': self.codegen.c_manager, 'self': self.codegen, 'dependencies': self.dependencies,
    'pos': pos, 'CManager': CManager
})
    
    def use(self, lib_name: str, pos: Position) -> None:
        """Use a Cure library.

        Args:
            lib_name (str): The name of the library.
            pos (Position): The position.
        """
        
        lib_name_path = STD_PATH / lib_name
        if lib_name_path.is_dir():
            lib_name_path = lib_name_path.absolute()
        
        for lib in STD_PATH.iterdir():
            lib_path = lib
            if self.is_file_target_lib(lib_path, lib_name_path):
                self.use_builtin(lib_name_path, lib_name, lib_path, pos)
                return
            
            if not lib.is_dir():
                continue
            
            has_sub_directories = any(f.is_dir() and f.name != '__pycache__' for f in lib.iterdir())
            if not has_sub_directories:
                continue
            
            for f in lib.iterdir():
                if not f.is_dir():
                    continue
                
                lib_path /= f
                if self.is_file_target_lib(lib_path, lib_name_path):
                    self.use_builtin(lib_name_path, lib_name, lib_path, pos)
                    return
        else:
            full_lib_name = lib_name
            lib = Path(lib_name)
            if not lib.is_absolute() or not lib.exists():
                if self.running_file is None:
                    pos.error_here('Cannot perform relative imports without a proper filename')
                
                lib = self.running_file.parent.joinpath(lib)
            
            if lib == self.running_file:
                pos.error_here('Cannot use current file')
            
            if lib.exists() and lib.is_file():
                header = lib.with_suffix('.h')
                sub_codegen, code = self.strtoc(lib.read_text('utf-8'))
                self.codegen.scope.env |= sub_codegen.scope.env
                
                header.write_text(f"""#pragma once
#ifdef __cplusplus
extern "C" {{
#endif
{code}
#ifdef __cplusplus
}}
#endif
""")
                self.codegen.c_manager.include(f'"{header.absolute().as_posix()}"', self.codegen)
            else:
                pos.error_here(f'Library \'{full_lib_name}\' not found')
