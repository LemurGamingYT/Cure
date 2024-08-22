from typing import NoReturn, Union, Iterable, Callable
from dataclasses import dataclass, field
from re import compile as re_compile
from sys import exit as sys_exit

from colorama import init, Fore, Style

from cure.parser.CureParser import CureParser
init()


ID_REGEX = re_compile(r'\w+')
kwargs = {'slots': True, 'unsafe_hash': True}

def replace_any_params(args: list['Object'], param_types: tuple[str]) -> tuple[str]:
    return tuple(
        arg.type if arg.type != 'any' else param_type
        for arg, param_type in zip(args, param_types)
    )

def validate_args(arg_types: Iterable[str], param_types: Iterable[str]) -> bool:
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
    c_type: str | None = field(default=None)
    
    def __post_init__(self) -> None:
        if self.c_type is None:
            self.c_type = self.type
    
    def __repr__(self) -> str:
        return self.type
    
    def __str__(self) -> str:
        return self.__repr__()

@dataclass(**kwargs)
class Scope:
    parent: Union['Scope', None] = field(default=None)
    prepended_code: str = field(default='')
    appended_code: str = field(default='')
    ending_code: str = field(default='')
    free_vars: list['Free'] = field(default_factory=list)
    env: dict = field(default_factory=dict)
    is_in_loop: bool = field(default=False)
    
    def add_free(self, free: 'Free') -> None:
        self.free_vars.append(free)
    
    def get_type(self, name: str) -> Type | None:
        if (item := self.env.get(name)) is not None:
            return item.func.returns if item.func is not None else item.type

@dataclass(**kwargs)
class Position:
    line: int
    column: int
    src: str = field(repr=False)
    
    def error_here(self, msg: str) -> NoReturn:
        print(self.src.splitlines()[self.line - 1])
        print(f'{Fore.RED}{Style.BRIGHT}{" " * self.column}^\n{msg}{Style.RESET_ALL}')
        sys_exit(1)
    
    def warn_here(self, msg: str) -> None:
        print(self.src.splitlines()[self.line - 1])
        print(f'{Fore.YELLOW}{Style.BRIGHT}{" " * self.column}^\n{msg}{Style.RESET_ALL}')
    
    def info_here(self, msg: str) -> None:
        print(self.src.splitlines()[self.line - 1])
        print(f'{Fore.CYAN}{Style.BRIGHT}{" " * self.column}^\n{msg}{Style.RESET_ALL}')

@dataclass(**kwargs)
class Free:
    object_name: str = field(default='')
    free_name: str = field(default='free')

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

@dataclass(**kwargs)
class Param:
    name: str
    type: Type
    ref: bool = field(default=False)

@dataclass(**kwargs)
class Function:
    name: str
    returns: Type
    params: list[Param] = field(default_factory=list)
    body: CureParser.BodyContext | None = field(default_factory=None)
    overloads: dict = field(default_factory=dict)
    callables: list[tuple[Callable, tuple]] = field(default_factory=list)
    
    def __call__(self, compiler, call_position: Position, *args: Object) -> Object | None:
        if (item := compiler.scope.env.get(self.name)) is not None:
            if item.func is not None and item.func.name == self.name:
                for c, mod_args in self.callables:
                    c(compiler, call_position, args, mod_args)
                
                new_args = []
                for arg, param in zip(args, self.params):
                    if param.ref:
                        if ID_REGEX.fullmatch(arg.code) is None:
                            call_position.error_here(f'Cannot modify a non-variable \'{arg.code}\'')
                        
                        arg.code = f'&({arg.code})'
                    
                    new_args.append(arg)
                
                callee, return_type = self.get_callee(args, call_position)
                return Object(
                    f'{callee}({", ".join(arg.code for arg in args)})',
                    return_type, call_position
                )
    
    def add_modification(self, name: str, pos: Position, func: Callable,
                         args: tuple[Object, ...]) -> None:
        param_types = func.param_types
        if not validate_args(tuple(arg.type.c_type for arg in args), param_types):
            pos.error_here(f'No matching overload for modification \'{name}\'')
        
        self.callables.append((func, args))
    
    def add_overload(self, name: str, returns: Type, param_types: Iterable[str]) -> None:
        self.overloads[(tuple(param_types), returns)] = name
    
    def get_callee(self, args: list['Object'], pos: Position) -> tuple[str, str]:
        param_types = replace_any_params(args, [param.type for param in self.params])
        arg_types = tuple(arg.type for arg in args)
        
        if validate_args(arg_types, param_types):
            return self.name, self.returns
        
        for info, func in self.overloads.items():
            if validate_args(arg_types, info[0]):
                return func, info[1]
        
        pos.error_here(
            f'No matching overload for \'{self.name}\' with arguments {", ".join(arg_types)}'
        )
