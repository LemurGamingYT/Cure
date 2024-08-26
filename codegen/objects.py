from typing import Union, Iterable, Callable
from dataclasses import dataclass, field
from re import compile as re_compile

from ir.nodes import Position, Body


ID_REGEX = re_compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
kwargs = {'slots': True, 'unsafe_hash': True}

def validate_args(arg_types: tuple[str, ...], param_types: tuple[str, ...]) -> bool:
    has_greedy = '*' in param_types
    if len(arg_types) != len(param_types) and not has_greedy:
        return False
    
    for arg_type, param_type in zip(arg_types, param_types):
        if param_type == 'any':
            continue
        elif param_type == '*':
            return True

        if arg_type != param_type:
            return False

    return True

@dataclass(**kwargs)
class Type:
    type: str
    c_type: str = field(default='')
    
    def __post_init__(self) -> None:
        if self.c_type == '':
            self.c_type = self.type
    
    def __repr__(self) -> str:
        return self.type
    
    def __str__(self) -> str:
        return self.__repr__()

@dataclass(**kwargs)
class Scope:
    parent: Union['Scope', None] = field(default=None)
    prepended_code: str = field(default='')
    ending_code: str = field(default='')
    appended_code: str = field(default='')
    free_vars: set['Free'] = field(default_factory=set)
    local_free_vars: set['Free'] = field(default_factory=set)
    env: dict = field(default_factory=dict)
    is_in_loop: bool = field(default=False)
    
    def add_free(self, free: 'Free') -> None:
        self.free_vars.add(free)
        self.local_free_vars.add(free)
    
    def remove_free(self, free: 'Free') -> None:
        if free in self.free_vars:
            self.free_vars.remove(free)

        if free in self.local_free_vars:
            self.local_free_vars.remove(free)

@dataclass(**kwargs)
class Free:
    object_name: str = field(default='')
    free_name: str = field(default='free')
    
    @property
    def code(self) -> str:
        return f'{self.free_name}({self.object_name});'

@dataclass(**kwargs)
class Object:
    code: str
    type: Type
    position: Position
    free: Free | None = field(default=None)

@dataclass(**kwargs)
class EnvItem:
    name: str
    type: Type
    defined_at: Position
    func: Union['Function', None] = field(default=None)
    reserved: bool = field(default=False)
    free: Free | None = field(default=None)
    is_const: bool = field(default=False)

@dataclass(**kwargs)
class Param:
    name: str
    type: Type
    ref: bool = field(default=False)
    
    def __str__(self) -> str:
        return f'{self.type}{"*" if self.ref else ""} {self.name}'

@dataclass(**kwargs)
class Function:
    name: str
    returns: Type
    params: list[Param] = field(default_factory=list)
    body: Body | None = field(default=None)
    overloads: dict = field(default_factory=dict)
    callables: list[tuple[Callable, tuple]] = field(default_factory=list)
    body_objects: list[Object] = field(default_factory=list)
    
    def __call__(self, compiler, call_position: Position, *args: Object) -> Object | None:
        for item in compiler.scope.env.values():
            if item.func is not None and item.func.name == self.name:
                for c, mod_args in self.callables:
                    c(compiler, self, call_position, args, mod_args)
                
                new_args = []
                for arg, param in zip(args, self.params):
                    if param.ref:
                        if ID_REGEX.fullmatch(arg.code) is None:
                            call_position.error_here(f'Cannot modify a non-variable \'{arg.code}\'')
                        
                        arg.code = f'&({arg.code})'
                    
                    new_args.append(arg)
                
                callee, return_type = self.get_callee(list(args), call_position)
                return Object(
                    f'{callee}({", ".join(arg.code for arg in args)})',
                    return_type, call_position
                )
        
        return None
    
    def add_modification(self, name: str, pos: Position, func: Callable,
                         args: tuple[Object, ...]) -> None:
        param_types = getattr(func, 'param_types', ())
        if not validate_args(tuple(arg.type.c_type for arg in args), param_types):
            pos.error_here(f'No matching overload for modification \'{name}\'')
        
        self.callables.append((func, args))
    
    def add_overload(self, name: str, returns: Type, param_types: Iterable[str]) -> None:
        self.overloads[(tuple(param_types), returns)] = name
    
    def get_callee(self, args: list['Object'], pos: Position) -> tuple[str, Type]:
        param_types = tuple(param.type.c_type for param in self.params)
        arg_types = tuple(arg.type.c_type for arg in args)
        
        if validate_args(arg_types, param_types):
            return self.name, self.returns
        
        for info, func in self.overloads.items():
            if validate_args(arg_types, info[0]):
                return func, info[1]
        
        pos.error_here(
            f'No matching overload for \'{self.name}\' with arguments {", ".join(arg_types)}'
        )
