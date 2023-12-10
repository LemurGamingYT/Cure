from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Int:
    value: int
    
    type = 'int'
    
    def as_c(self) -> str:
        return str(self.value)


@dataclass(unsafe_hash=True)
class Float:
    value: float
    
    type = 'float'
    
    def as_c(self) -> str:
        return str(self.value)


@dataclass(unsafe_hash=True)
class String:
    value: str
    
    type = 'string'
    
    def as_c(self) -> str:
        return f'"{self.value}"'


@dataclass(unsafe_hash=True)
class Bool:
    value: bool
    
    type = 'bool'
    
    def as_c(self) -> str:
        return 'true' if self.value else 'false'


@dataclass(unsafe_hash=True)
class Nil:
    type = 'nil'
    
    def as_c(self) -> str:
        return 'null'


@dataclass(unsafe_hash=True)
class Id:
    name: str
    
    type = 'nil'
    
    def as_c(self) -> str:
        return self.name
