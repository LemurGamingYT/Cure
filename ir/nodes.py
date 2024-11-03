from dataclasses import dataclass, field
from typing import NoReturn, Union
from sys import exit as sys_exit
from pathlib import Path
from abc import ABC

from colorama import init, Fore, Style
from colorama.ansi import AnsiFore
init()


kwargs = {'slots': True, 'unsafe_hash': True}

@dataclass(**kwargs)
class Position:
    line: int
    column: int
    src: str = field(repr=False)
    
    def not_supported_err(self, symbol_name: str) -> NoReturn:
        """Error message for when a symbol is not supported.

        Args:
            symbol_name (str): The symbol name. If this is a function, it should end with `()` to
            indicate that it is a function.
        """
        
        self.error_here(f'{symbol_name} is not supported on current target')
    
    def get_print_content(self, color: AnsiFore, msg: str) -> str:
        return f'{self.get_src()}\n{Style.BRIGHT}{color}{" " * self.column}^\n{msg}{Style.RESET_ALL}'
    
    def get_src(self) -> str:
        return self.src.splitlines()[self.line - 1]
    
    def error_here(self, msg: str) -> NoReturn:
        print(self.get_print_content(Fore.RED, msg))
        sys_exit(1)
    
    def warn_here(self, msg: str) -> None:
        print(self.get_print_content(Fore.YELLOW, msg))
    
    def info_here(self, msg: str) -> None:
        print(self.get_print_content(Fore.CYAN, msg))

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
    is_optional: bool = field(default=False)
    func_type: Union['FuncType', None] = field(default=None)
    tuple_types: list['TypeNode'] | None = field(default=None)

@dataclass(**kwargs)
class FuncType(Node):
    return_type: TypeNode
    params: list['TypeNode'] = field(default_factory=list)

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
    callee: Node
    args: list[ArgNode] = field(default_factory=list)
    generic_args: list[TypeNode] = field(default_factory=list)

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
class Extern(Node):
    name: str

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
    generic_params: list[str] = field(default_factory=list)
    extend_type: TypeNode | None = field(default=None)

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
    type: TypeNode | None
    elements: list[ArgNode] = field(default_factory=list)

@dataclass(**kwargs)
class Dict(Node):
    key_type: TypeNode | None
    value_type: TypeNode | None
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
    generic_args: list[TypeNode] = field(default_factory=list)

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
    type: TypeNode
    value: Node | None = field(default=None)
    public: bool = field(default=True)

@dataclass(**kwargs)
class ClassMethod(FuncDecl):
    is_public: bool = field(default=True)
    is_static: bool = field(default=False)
    is_overriding: bool = field(default=False)

ClassMembers = list[ClassProperty | ClassMethod]

@dataclass(**kwargs)
class Class(Node):
    name: str
    members: ClassMembers = field(default_factory=ClassMembers)
    bases: list[str] = field(default_factory=list)

@dataclass(**kwargs)
class AttrAssign(Node):
    obj: Node
    attr_chain: list[str]
    value: Node
    op: str | None = field(default=None)

@dataclass(**kwargs)
class LiteralCode(Node):
    code: str
    type: TypeNode

@dataclass(**kwargs)
class AnonymousFunc(Node):
    body: Body
    params: list[ParamNode] = field(default_factory=list)
    return_type: TypeNode | None = field(default=None)

@dataclass(**kwargs)
class CreateTuple(Node):
    elements: list[Node] = field(default_factory=list)

@dataclass(**kwargs)
class RangeFor(Node):
    loop_name: str
    start: Node
    end: Node
    body: Body

@dataclass(**kwargs)
class Test(Node):
    name: str
    body: Body
