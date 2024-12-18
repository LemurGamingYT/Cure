from importlib import import_module
from typing import Callable
from logging import debug
from pathlib import Path

from codegen.c_manager import STD_PATH
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
        
        try:
            module = import_module(f'codegen.std.{lib_path}')
        except ModuleNotFoundError:
            pos.error_here(f'Library \'{lib_name}\' not found')
        
        lib_type = module.__dict__.get(lib.stem)
        if lib_type is None:
            pos.error_here(f'Library \'{lib_name}\' does not have a library class')
        
        if lib_type in [type(cls) for cls in self.dependencies]:
            return
        
        lib_class = lib_type(self.codegen)
        if not getattr(lib_class, 'CAN_USE', True) and Path.cwd().name != 'Cure':
            pos.error_here(f'Library \'{lib_name}\' cannot be used')
        
        self.dependencies.append(lib_class)
        objects = self.codegen.c_manager.get_all_objects(lib_class)
        for k, v in objects.items():
            setattr(self.codegen.c_manager, k, v)
    
    def use_from_folder(self, lib_name: str, folder: Path, pos: Position) -> bool:
        """Tries to use a Cure library from a specific `Path`.

        Args:
            lib_name (str): The name of the library.
            folder (Path): The `Path` of the folder.
            pos (Position): The position.
        
        Returns:
            bool: Whether the library was used.
        """
        
        lib_name_path = folder / lib_name
        for lib in folder.iterdir():
            if self.is_file_target_lib(lib, lib_name_path):
                self.use_builtin(lib, lib_name, lib, pos)
                return True
            
            if lib.is_file():
                continue
            
            has_sub_directories = any(f.is_dir() and f.name != '__pycache__' for f in lib.iterdir())
            if not has_sub_directories:
                continue
            
            if self.use_from_folder(lib_name, lib, pos):
                return True
        
        return False
    
    def use(self, lib_name: str, pos: Position) -> None:
        """Use a Cure library.

        Args:
            lib_name (str): The name of the library.
            pos (Position): The position.
        """
        
        debug(f'Using name \'{lib_name}\'')
        
        if self.use_from_folder(lib_name, STD_PATH, pos):
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
                self.codegen.c_manager.add_objects(sub_codegen.c_manager, self.codegen.c_manager)
                self.codegen.metadata['valid_types'] |= sub_codegen.metadata['valid_types']
                
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
