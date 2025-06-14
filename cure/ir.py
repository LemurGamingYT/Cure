from typing import Union, Callable, TypeAlias, Any
from dataclasses import dataclass, field
from importlib import import_module
from sys import exit as sys_exit
from logging import error
from pathlib import Path
from copy import copy
from abc import ABC

from colorama import Fore, Style
from llvmlite import ir as lir

from cure.target import Target


STDLIB_PATH = Path(__file__).parent.absolute() / 'stdlib'
BodyType: TypeAlias = Union['Body', Callable, None]
op_map = {
    '+': 'add', '-': 'sub', '*': 'mul', '/': 'div', '%': 'mod', '==': 'eq', '!=': 'neq', '>': 'gt',
    '<': 'lt', '>=': 'gte', '<=': 'lte', '&&': 'and', '||': 'or', '!': 'not'
}


def params_match(func, arg_types: list['Type']):
    params = func.params
    if len(arg_types) > len(params):
        return False
    elif len(arg_types) < len(params):
        return False

    for arg_type, param in zip(arg_types, params):
        param_type = param.type
        if param_type == arg_type or param_type == Type.any():
            continue

        return False
    
    return True

def match_to_overloads(func, arg_types: list['Type']):
    for overload in getattr(func, 'overloads', []):
        if not params_match(overload, arg_types):
            continue

        # TODO: check for ambiguous function call (function types match multiple overloads)
        return overload
    
    return func


@dataclass
class Position:
    line: int
    column: int

    @staticmethod
    def zero():
        return Position(0, 0)

    def comptime_error(self, msg: str, src: str):
        print(src.splitlines()[self.line - 1])
        print(' ' * (self.column - 1) + '^')
        print(f'{Style.BRIGHT}{Fore.RED}error: {msg}{Style.RESET_ALL}')
        error(msg)
        raise Exception
        sys_exit(1)

@dataclass
class Symbol:
    name: str
    type: 'Type'
    value: Any

@dataclass
class SymbolTable:
    symbols: dict[str, Symbol] = field(default_factory=dict)

    def __iter__(self):
        return iter(self.symbols.values())

    def add(self, symbol: Symbol, name: Union[str, None] = None):
        self.symbols[name or symbol.name] = symbol

    def get(self, name: str) -> Union[Symbol, None]:
        return self.symbols.get(name)
    
    def has(self, name: str):
        return name in self.symbols
    
    def remove(self, name: str):
        if self.has(name):
            self.symbols.pop(name)
    
    def clone(self):
        return SymbolTable(self.symbols.copy())
    
    def merge(self, other: 'SymbolTable'):
        self.symbols.update(other.symbols)

@dataclass
class Scope:
    file: Path
    parent: Union['Scope', None] = None
    symbol_table: SymbolTable = field(default_factory=SymbolTable)
    dependencies: list[Path] = field(default_factory=list)
    target: Target = field(default_factory=lambda: Target.get_current())
    
    @property
    def is_toplevel(self):
        return self.parent is None

    def __post_init__(self):
        if self.parent is not None:
            self.src = self.parent.src
            self.dependencies = self.parent.dependencies

            self.symbol_table = self.parent.symbol_table.clone()
        else:
            self.src = self.file.read_text('utf-8')

            self.use('builtins', Position.zero())

    def clone(self):
        return Scope(self.file, self)
    
    def merge(self, other: 'Scope'):
        self.dependencies.extend(other.dependencies)
        self.symbol_table.merge(other.symbol_table)
    
    def use(self, name: str, pos: Position):
        if name in self.dependencies:
            return
        
        path = STDLIB_PATH / name
        if self.file.parent == path:
            # TODO: currently, this is for stopping recursion error of using the builtins library
            # it should error if used in a non-stdlib file
            return
        
        if not path.exists():
            pos.comptime_error(f'unknown library {name}', self.src)
        
        if (file := path / f'{name}.py').is_file():
            if file.stem == '__init__':
                module = import_module(f'cure.stdlib.{name}')
            else:
                module = import_module(f'cure.stdlib.{name}.{name}')
            
            getattr(module, name)(self)

        # TODO: use [name].ptl file

        self.dependencies.append(path)


@dataclass
class Node(ABC):
    pos: Position
    
    @property
    def children(self):
        children = []
        for attr in dir(self):
            if attr.startswith('_') or attr == 'children':
                continue

            value = getattr(self, attr)
            if isinstance(value, Node):
                children.append(value)
            elif isinstance(value, (list, tuple, set)):
                for elem in children:
                    if not isinstance(elem, Node):
                        continue

                    children.append(elem)
        
        return children

    def get_type(self) -> 'Type':
        return getattr(self, 'type', Type.nil())
    
    def clone(self):
        return copy(self)

@dataclass
class Type(Node):
    display: str
    type: lir.Type

    @staticmethod
    def int():
        return Type(Position.zero(), 'int', lir.IntType(32))
    
    @staticmethod
    def float():
        return Type(Position.zero(), 'float', lir.FloatType())
    
    @staticmethod
    def string():
        return Type(
            Position.zero(), 'string',
            lir.LiteralStructType([
                lir.IntType(8).as_pointer(), # char*
                lir.IntType(64), # size_t
                Type.Ref().type.as_pointer() # Ref*
            ])
        )
    
    @staticmethod
    def string_literal():
        return Type(Position.zero(), 'string_literal', lir.IntType(8).as_pointer())
    
    @staticmethod
    def bool():
        return Type(Position.zero(), 'bool', lir.IntType(1))
    
    @staticmethod
    def nil():
        return Type(Position.zero(), 'nil', lir.IntType(8).as_pointer())
    
    @staticmethod
    def any():
        return Type(Position.zero(), 'any', lir.IntType(8).as_pointer())
    
    @staticmethod
    def function():
        return Type(Position.zero(), 'function', lir.IntType(8).as_pointer())


    @staticmethod
    def pointer():
        return Type(Position.zero(), 'pointer', lir.IntType(8).as_pointer())

    @staticmethod
    def Ref():
        return Type(Position.zero(), 'Ref', lir.LiteralStructType([
            lir.IntType(8).as_pointer(), # void*
            lir.FunctionType(Type.nil().type, [Type.any().type]).as_pointer(), # nil (*destroy)(void*)
            lir.IntType(64), # size_t
        ]))


    @staticmethod
    def get_from_llvm(type: lir.Type):
        if isinstance(type, lir.IntType):
            if type.width == 1:
                return Type.bool()
            elif type.width == 32:
                return Type.int()
        elif isinstance(type, lir.FloatType):
            return Type.float()
        elif isinstance(type, lir.LiteralStructType):
            if len(type.elements) == 2 and isinstance(type.elements[0], lir.PointerType) and\
                isinstance(type.elements[1], lir.IntType):
                return Type.string()
        elif isinstance(type, lir.PointerType):
            return Type.nil()
        
        raise TypeError(f'cannot convert to cure type {type}')
    
    @staticmethod
    def get(name: str):
        type = getattr(Type, name, Type(Position.zero(), name, name))
        if isinstance(type, Type):
            return type
        
        return type()
    
    @staticmethod
    def exists(name: str):
        type = getattr(Type, name, None)
        if type is None:
            return
        
        return type()
    
    def __str__(self):
        return self.display
    
    def __repr__(self):
        return self.display
    
    def needs_free(self, scope: Scope):
        return self.destroy_method(scope) is not None
    
    def destroy_method(self, scope: Scope):
        symbol = scope.symbol_table.get(f'{self}_destroy')
        if symbol is None or symbol.type != Type.function():
            return
        
        return symbol

    def as_pointer(self):
        return Type(self.pos, f'{self.display}&', self.type.as_pointer())

@dataclass
class Program(Node):
    nodes: list[Node] = field(default_factory=list)

@dataclass
class Int(Node):
    value: int

    @property
    def type(self) -> 'Type':
        return Type.int()

@dataclass
class Float(Node):
    value: float

    @property
    def type(self) -> 'Type':
        return Type.float()

@dataclass
class String(Node):
    value: str

    @property
    def type(self) -> 'Type':
        return Type.string()

@dataclass
class Bool(Node):
    value: bool

    @property
    def type(self) -> 'Type':
        return Type.bool()

@dataclass
class Nil(Node):
    @property
    def type(self) -> 'Type':
        return Type.nil()

@dataclass
class StringLiteral(Node):
    value: str
    
    @property
    def type(self) -> 'Type':
        return Type.string_literal()

@dataclass
class Id(Node):
    name: str
    type: Type = field(default_factory=lambda: Type.any())

@dataclass
class BinaryOp(Node):
    left: Node
    op: str
    right: Node
    type: Type = field(default_factory=lambda: Type.any())

@dataclass
class UnaryOp(Node):
    op: str
    expr: Node
    type: Type = field(default_factory=lambda: Type.any())

@dataclass
class Call(Node):
    callee: str
    args: list[Node] = field(default_factory=list)
    type: Type = field(default_factory=lambda: Type.any())

@dataclass
class Attribute(Node):
    obj: Node
    attr: str
    args: Union[list[Node], None] = None # default to property call
    type: Type = field(default_factory=lambda: Type.any())

@dataclass
class Param(Node):
    name: str
    type: Type

@dataclass
class Body(Node):
    nodes: list[Node] = field(default_factory=list)

@dataclass(kw_only=True)
class FunctionFlags:
    static: bool = False
    extern: bool = False
    public: bool = False
    property: bool = False
    method: bool = False

@dataclass
class Function(Node):
    name: str
    params: list[Param] = field(default_factory=list)
    type: Type = field(default_factory=lambda: Type.nil())
    body: BodyType = None
    flags: FunctionFlags = field(default_factory=FunctionFlags)
    overloads: list['Function'] = field(default_factory=list)

    @property
    def ret_type(self):
        return self.type

@dataclass
class Return(Node):
    value: Node

    @property
    def type(self):
        return self.value.get_type()

@dataclass
class Variable(Node):
    name: str
    value: Union[Node, None] = None
    type: Type = field(default_factory=lambda: Type.any())

@dataclass
class Assignment(Node):
    name: str
    value: Node

@dataclass
class Comment(Node):
    text: str

@dataclass
class Elif(Node):
    condition: Node
    body: Body

@dataclass
class If(Node):
    condition: Node
    body: Body
    else_body: Union[Body, None] = None
    elseifs: list[Elif] = field(default_factory=list)

@dataclass
class While(Node):
    condition: Node
    body: Body


@dataclass
class Ref(Node):
    name: str
    type: Type
