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
    env: dict[str, 'EnvItem'] = field(default_factory=dict)
    is_in_loop: bool = field(default=False)
    
    def add_free(self, free: 'Free') -> None:
        self.free_vars.add(free)
        self.local_free_vars.add(free)
    
    def remove_free(self, free: 'Free') -> None:
        if free in self.free_vars:
            self.free_vars.remove(free)

        if not self.has_free(free):
            self.local_free_vars.remove(free)
    
    def has_free(self, free: 'Free') -> bool:
        for f in self.local_free_vars:
            if f.object_name == free.object_name and f.free_name == free.free_name:
                return True
        
        for f in self.free_vars:
            if f.object_name == free.object_name and f.free_name == free.free_name:
                return True

        return False

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
    
    @staticmethod
    def NULL(position: Position) -> 'Object':
        return Object('NULL', Type('nil'), position)
    
    def __str__(self) -> str:
        return self.code

@dataclass(**kwargs)
class EnvItem:
    name: str
    type: Type
    defined_at: Position
    func: Union['Function', None] = field(default=None)
    reserved: bool = field(default=False)
    free: Free | None = field(default=None)
    is_const: bool = field(default=False)
    references: int = field(default=0)
    
    def increment_references(self, _) -> None:
        self.references += 1
    
    def decrement_references(self, codegen) -> None:
        self.references -= 1
        if self.references == 0 and self.free is not None:
            codegen.append_code(self.free.code)

@dataclass(**kwargs)
class Arg:
    value: Object
    name: str | None = field(default=None)

@dataclass(**kwargs)
class Param:
    name: str
    type: Type
    ref: bool = field(default=False)
    default: Object | None = field(default=None)
    
    def __str__(self) -> str:
        return f'{self.type.c_type}{"*" if self.ref else ""} {self.name}'

@dataclass(**kwargs)
class Function:
    name: str
    returns: Type
    params: list[Param] = field(default_factory=list)
    body: Body | None = field(default=None)
    overloads: dict = field(default_factory=dict)
    callables: list[tuple[Callable, tuple]] = field(default_factory=list)
    body_objects: list[Object] = field(default_factory=list)
    
    def __call__(self, compiler, call_position: Position, *args: Arg) -> Object | None:
        for item in compiler.scope.env.values():
            if item.func is not None and item.func.name == self.name:
                for c, mod_args in self.callables:
                    c(
                        compiler, self, call_position,
                        [arg.value for arg in args],
                        [arg.value for arg in mod_args]
                    )
                
                new_args: list[Arg | None] = [None] * len(self.params)
                arg: Arg | None
                for i, arg in enumerate(args):
                    if arg.name is None:
                        new_args[i] = arg
                    else:
                        param_index = next((
                            i for i, p in enumerate(self.params)
                            if p.name == arg.name
                        ), None)
                        if param_index is None:
                            arg.value.position.error_here(f'Unknown keyword argument \'{arg.name}\'')
                        
                        new_args[param_index] = arg
                
                for i, (param, arg) in enumerate(zip(self.params, new_args)):
                    if arg is None:
                        if param.default is not None:
                            new_args[i] = Arg(param.default, param.name)
                        else:
                            call_position.error_here(f'Missing required argument \'{param.name}\'')
                
                for arg, param in zip(new_args, self.params):
                    if param.ref and arg is not None:
                        var_name = arg.value.code
                        if ID_REGEX.fullmatch(var_name) is None:
                            arg.value.position.error_here('Cannot modify a non-variable')
                        
                        if (var := compiler.scope.env.get(var_name)) is not None:
                            if var.func is not None:
                                arg.value.position.error_here('Cannot modify a function')
                            elif var.is_const:
                                arg.value.position.error_here('Cannot modify a constant')
                            elif var.reserved:
                                arg.value.position.error_here('Cannot modify a non-variable')
                        
                        arg.value.code = f'&({var_name})'
                
                if len(new_args) != len(self.params):
                    call_position.error_here(
                        f'Expected {len(self.params)} arguments, got {len(new_args)}'
                    )
                
                if None in new_args:
                    call_position.error_here(f'Missing required argument \'{param.name}\'')
                
                # bypassing mypy
                passing_args: list[Arg] = [arg for arg in new_args if arg is not None]
                callee, return_type = self.get_callee(passing_args, call_position)
                return Object(
                    f'{callee}({", ".join(arg.value.code for arg in passing_args)})',
                    return_type, call_position
                )
        
        return None
    
    def add_modification(self, name: str, pos: Position, func: Callable,
                         args: tuple[Arg, ...]) -> None:
        param_types = getattr(func, 'param_types', ())
        if not validate_args(tuple(arg.value.type.c_type for arg in args), param_types):
            pos.error_here(f'No matching overload for modification \'{name}\'')
        
        self.callables.append((func, args))
    
    def add_overload(self, name: str, returns: Type, param_types: Iterable[str]) -> None:
        self.overloads[(tuple(param_types), returns)] = name
    
    def get_callee(self, args: list[Arg], pos: Position) -> tuple[str, Type]:
        param_types = tuple(param.type.c_type for param in self.params)
        arg_types = tuple(arg.value.type.c_type for arg in args)
        fname = self.name
        
        if validate_args(arg_types, param_types):
            return fname, self.returns
        
        for info, func in self.overloads.items():
            if validate_args(arg_types, info[0]):
                return func, info[1]
        
        arg_types_str = ', '.join(arg_types)
        pos.error_here(f'No matching overload for \'{fname}\' with arguments {arg_types_str}')
