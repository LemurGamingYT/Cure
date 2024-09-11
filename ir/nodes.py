from dataclasses import dataclass, field
from typing import NoReturn, Union
from sys import exit as sys_exit
from pathlib import Path
from abc import ABC

from colorama import init, Fore, Style
init()


kwargs = {'slots': True, 'unsafe_hash': True}

@dataclass(**kwargs)
class Position:
    line: int
    column: int
    src: str = field(repr=False)
    
    def _line(self) -> str:
        return self.src.splitlines()[self.line - 1]
        # lines[1] = f'{Style.BRIGHT}{lines[1]}{Style.RESET_ALL}'
        # return '\n'.join(lines) + '\n'
    
    def error_here(self, msg: str) -> NoReturn:
        print(self._line())
        print(f'{Style.BRIGHT}{Fore.RED}{" " * self.column}^\n{msg}{Style.RESET_ALL}')
        sys_exit(1)
    
    def warn_here(self, msg: str) -> None:
        print(self._line())
        print(f'{Style.BRIGHT}{Fore.YELLOW}{msg}{Style.RESET_ALL}')
    
    def info_here(self, msg: str) -> None:
        print(self._line())
        print(f'{Style.BRIGHT}{Fore.CYAN}{msg}{Style.RESET_ALL}')

@dataclass(**kwargs)
class Node(ABC):
    pos: Position

@dataclass(**kwargs)
class Program(Node):
    nodes: list[Node] = field(default_factory=list)
    file: Path | None = field(default=None)

@dataclass(**kwargs)
class Body(Node):
    nodes: list[Node] = field(default_factory=list)

@dataclass(**kwargs)
class TypeNode(Node):
    name: str
    array_type: Union['TypeNode', None] = field(default=None)
    dict_types: tuple['TypeNode', 'TypeNode'] | None = field(default=None)

@dataclass(**kwargs)
class ParamNode(Node):
    name: str
    type: TypeNode
    ref: bool = field(default=False)
    default: Node | None = field(default=None)

@dataclass(**kwargs)
class ArgNode(Node):
    expr: Node
    keyword: str | None = field(default=None)

@dataclass(**kwargs)
class Call(Node):
    name: str
    args: list[ArgNode] = field(default_factory=list)

@dataclass(**kwargs)
class FunctionMod(Call):
    pass

@dataclass(**kwargs)
class Return(Node):
    expr: Node

@dataclass(**kwargs)
class Continue(Node):
    pass

@dataclass(**kwargs)
class Break(Node):
    pass

@dataclass(**kwargs)
class Foreach(Node):
    loop_name: str
    expr: Node
    body: Body

@dataclass(**kwargs)
class While(Node):
    expr: Node
    body: Body

@dataclass(**kwargs)
class If(Node):
    expr: Node
    body: Body
    else_body: Body | None = field(default=None)
    elseifs: list[tuple[Node, Body]] = field(default_factory=list)

@dataclass(**kwargs)
class Use(Node):
    path: str

@dataclass(**kwargs)
class VarDecl(Node):
    name: str
    value: Node
    op: str | None = field(default=None)
    type: TypeNode | None = field(default=None)
    is_const: bool = field(default=False)

@dataclass(**kwargs)
class FuncDecl(Node):
    name: str
    body: Body
    params: list[ParamNode] = field(default_factory=list)
    return_type: TypeNode | None = field(default=None)
    modifications: list[Call] = field(default_factory=list)

@dataclass(**kwargs)
class Value(Node):
    value: str
    type: str

@dataclass(**kwargs)
class Identifier(Node):
    name: str

@dataclass(**kwargs)
class Nil(Node):
    pass

@dataclass(**kwargs)
class Array(Node):
    type: TypeNode
    elements: list[ArgNode] = field(default_factory=list)

@dataclass(**kwargs)
class Dict(Node):
    key_type: TypeNode
    value_type: TypeNode
    elements: dict[Node, Node] = field(default_factory=dict)

@dataclass(**kwargs)
class Brackets(Node):
    expr: Node

@dataclass(**kwargs)
class BinOp(Node):
    left: Node
    op: str
    right: Node

@dataclass(**kwargs)
class UOp(Node):
    value: Node
    op: str

@dataclass(**kwargs)
class Attribute(Node):
    obj: Node
    attr: str
    args: list[ArgNode] | None = field(default=None)

@dataclass(**kwargs)
class New(Node):
    name: Identifier
    args: list[ArgNode] = field(default_factory=list)

@dataclass(**kwargs)
class Ternary(Node):
    cond: Node
    if_true: Node
    if_false: Node

@dataclass(**kwargs)
class Index(Node):
    obj: Node
    index: Node

@dataclass(**kwargs)
class DollarString(Node):
    nodes: list[Node] = field(default_factory=list)

@dataclass(**kwargs)
class Cast(Node):
    obj: Node
    type: TypeNode

@dataclass(**kwargs)
class ArrayComprehension(Node):
    expr: Node
    loop_name: str
    iterable: Node

@dataclass(**kwargs)
class Enum(Node):
    name: Identifier
    members: list[Identifier] = field(default_factory=list)

@dataclass(**kwargs)
class ClassProperty(Node):
    name: str
    value: Node
    type: TypeNode

@dataclass(**kwargs)
class ClassMethod(FuncDecl):
    pass

ClassMembers = list[ClassProperty | ClassMethod]

@dataclass(**kwargs)
class Class(Node):
    name: str
    members: ClassMembers = field(default_factory=ClassMembers)
