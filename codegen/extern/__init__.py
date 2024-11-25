from importlib import import_module
from pathlib import Path

from codegen.objects import Position, Type, EnvItem


EXTERNAL_PYTHON_PATH = Path(__file__).parent

class ExternalManager:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
    
    def replace_header_name(self, name: str) -> str:
        return name.replace('.h', '_h')
    
    def add_symbol(self, symbol_object) -> None:
        if callable(symbol_object):
            self.codegen.c_manager.add_func(symbol_object.name, symbol_object)
        elif isinstance(symbol_object, Type):
            self.codegen.type_checker.add_type(symbol_object)
        elif isinstance(symbol_object, EnvItem):
            self.codegen.scope.env[symbol_object.name] = symbol_object
    
    def add_file(self, file: Path, pos: Position, name: str) -> bool:
        module = import_module(f'codegen.extern.{file.stem}')
        cls = getattr(module, file.stem, None)
        if cls is None:
            pos.error_here(f'Invalid header \'{file.stem}\'')
        
        external_class = cls(self.codegen)
        header_symbols = self.codegen.c_manager.get_all_objects(external_class)
        if self.replace_header_name(file.stem) == name or name == 'C':
            for func in header_symbols.values():
                self.add_symbol(func)
            
            return True
        
        for func in header_symbols:
            if (func_name := getattr(func, 'name', None)) is None or func_name != '_' + name:
                continue
            
            self.add_symbol(func)
            return True
        
        return False
    
    def add_external(self, name: str, pos: Position) -> None:
        name = self.replace_header_name(name)
        has_added_symbols = False
        for file in EXTERNAL_PYTHON_PATH.glob('*.py'):
            if not file.is_file() or file.stem == '__init__':
                continue
            
            if self.add_file(file, pos, name):
                has_added_symbols = True
        
        if not has_added_symbols:
            pos.error_here(f'Unknown external declaration \'{name}\'')
