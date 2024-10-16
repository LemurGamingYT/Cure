from dataclasses import dataclass, field
from re import compile as re_compile
from typing import Union, Any

from ir.nodes import Position, ClassMembers


# allows for dereferencing pointers to be used as identifiers such as *(this) for classes
ID_REGEX = re_compile(r'(\w+)|(\*\(\w+\))')
INT_REGEX = re_compile(r'\d+')
POS_ZERO = Position(0, 0, '')

kwargs = {'slots': True, 'unsafe_hash': True}

@dataclass(**kwargs)
class Arg:
    value: 'Object'
    name: str | None = field(default=None)

@dataclass(**kwargs)
class Param:
    name: str
    type: 'Type'
    ref: bool = field(default=False)
    default: Union['Object', None] = field(default=None)
    
    def __str__(self) -> str:
        if self.type.function_info is not None:
            return self.type.c_type
        
        return f'{self.get_type()} {self.name}'
    
    def get_type(self) -> str:
        return f'{self.type.c_type}{"*" if self.ref else ""}'
    
    def USE(self) -> str:
        return f'*({self.name})' if self.ref else self.name

@dataclass(**kwargs)
class Type:
    type: str
    c_type: str = field(default='')
    compatible_types: tuple[str, ...] = field(default_factory=tuple[str, ...])
    function_info: tuple[tuple['Type', ...], 'Type', str] | None = field(default=None)
    tuple_types: list['Type'] | None = field(default=None)
    
    def __post_init__(self) -> None:
        if self.c_type == '':
            self.c_type = self.type
    
    def __repr__(self) -> str:
        return self.type
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Type):
            if self.type == other.type:
                return True
            
            return other.type in self.compatible_types or self.type in other.compatible_types
        
        return False
    
    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

@dataclass(**kwargs)
class CodeType:
    batches: list[str] = field(default_factory=list)
    
    @property
    def is_empty(self) -> bool:
        return len(self.batches) == 0
    
    def __str__(self) -> str:
        return '\n'.join(self.batches)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __add__(self, other: Any) -> 'CodeType':
        if isinstance(other, str):
            self.batches.append(other)
        elif isinstance(other, CodeType):
            self.batches.append(str(other))
        
        return self
    
    def __sub__(self, other: Any) -> 'CodeType':
        if isinstance(other, int):
            self.batches = self.batches[:-other]
        
        return self
    
    def reset(self) -> None:
        """Resets all of the batches for this `CodeType`"""
        
        self.batches = []
    
    def remove_recent_batch(self) -> None:
        """Removes the most recent batch from the `CodeType's batches`
        This means that when the `CodeType` is converted to a string, the most recent
        string that was added will not be included in the output"""
        
        self.batches = self.batches[:-1]
    

@dataclass(**kwargs)
class Scope:
    parent: Union['Scope', None] = field(default=None)
    prepended_code: CodeType = field(default_factory=CodeType)
    ending_code: CodeType = field(default_factory=CodeType)
    appended_code: CodeType = field(default_factory=CodeType)
    free_vars: set['Free'] = field(default_factory=set)
    local_free_vars: set['Free'] = field(default_factory=set)
    env: dict[str, 'EnvItem'] = field(default_factory=dict)
    is_in_loop: bool = field(default=False)
    is_in_class: bool = field(default=False)
    assigning_to_variable: str | None = field(default=None)
    
    
    @property
    def toplevel(self) -> 'Scope':
        top = self
        while top.parent is not None:
            top = top.parent
        
        return top
    
    @property
    def is_toplevel(self) -> bool:
        return self.parent is None
    
    def add_free(self, free: 'Free') -> None:
        self.free_vars.add(free)
        self.local_free_vars.add(free)
    
    def remove_free(self, free: 'Free') -> None:
        for i, f in enumerate(self.local_free_vars):
            if f == free:
                local_free_vars = list(self.local_free_vars)
                local_free_vars.pop(i)
                self.local_free_vars = set(local_free_vars)

        for i, f in enumerate(self.free_vars):
            if f == free:
                free_vars = list(self.free_vars)
                free_vars.pop(i)
                self.free_vars = set(free_vars)
    
    def has_free(self, free: 'Free') -> bool:
        for f in self.local_free_vars:
            if f == free:
                return True
        
        for f in self.free_vars:
            if f == free:
                return True

        return False

@dataclass(**kwargs)
class Free:
    object_name: str = field(default='')
    free_name: str = field(default='free')
    basic_name: str = field(default='')
    
    @property
    def code(self) -> str:
        return f'{self.free_name}({self.object_name});'
    
    def replace(self, with_free: 'Free') -> 'Free':
        return Free(
            with_free.object_name.replace(with_free.basic_name, self.basic_name),
            free_name=with_free.free_name, basic_name=self.basic_name
        )
    
    def replace_from_class(self, with_free: 'Free') -> 'Free':
        return Free(
            with_free.object_name.replace(self.basic_name, with_free.basic_name),
            free_name=with_free.free_name, basic_name=self.basic_name
        )
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Free):
            return self.object_name == other.object_name and self.free_name == other.free_name
        
        return False

@dataclass(**kwargs)
class Object:
    code: str
    type: Type
    position: Position = field(default=POS_ZERO)
    free: Free | None = field(default=None)
    
    @staticmethod
    def NULL(position: Position) -> 'Object':
        return Object('NULL', Type('nil'), position)
    
    @staticmethod
    def STRINGBUF(buf_free: Free, pos: Position) -> 'Object':
        return Object(buf_free.object_name, Type('string'), pos, free=buf_free)
    
    def __str__(self) -> str:
        return self.code

@dataclass(**kwargs)
class Field:
    name: str
    type: Type
    default: Object | None = field(default=None)
    public: bool = field(default=True)

@dataclass(**kwargs)
class Class:
    name: str
    type: Type
    defined_at: Position
    bases: list['EnvItem'] = field(default_factory=list)
    fields: list[Field] = field(default_factory=list)
    members: ClassMembers = field(default_factory=ClassMembers)
    free_members: list[Free] = field(default_factory=list)

@dataclass(**kwargs)
class EnvItem:
    name: str
    type: Type
    defined_at: Position
    func: Any = field(default=None)
    reserved: bool = field(default=False)
    free: Free | None = field(default=None)
    is_const: bool = field(default=False)
    class_: Class | None = field(default=None)
    added_by_preprocessor: bool = field(default=False)

@dataclass(**kwargs)
class TempVar:
    name: str
    type: Type
    created_at: Position
    free: Free | None = field(default=None)
    
    def __str__(self) -> str:
        return self.name
    
    def OBJECT(self) -> Object:
        return Object(self.name, self.type, self.created_at, free=self.free)
    
    def REFERENCE(self) -> Object:
        return Object(f'&({self.name})', self.type, self.created_at, free=self.free)
