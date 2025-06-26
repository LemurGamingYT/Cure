from typing import Union, Callable, TypeAlias, Any
from dataclasses import dataclass, field
from logging import error, debug, info
from importlib import import_module
from pathlib import Path
from copy import copy
from abc import ABC

from colorama import Fore, Style
from llvmlite import ir as lir

from cure.codegen_utils import store_in_pointer, NULL
from cure.target import Target


STDLIB_PATH = Path(__file__).parent.absolute() / 'stdlib'
BodyType: TypeAlias = Union['Body', Callable, None]
op_map = {
    '+': 'add', '-': 'sub', '*': 'mul', '/': 'div', '%': 'mod', '==': 'eq', '!=': 'neq', '>': 'gt',
    '<': 'lt', '>=': 'gte', '<=': 'lte', '&&': 'and', '||': 'or', '!': 'not'
}


def params_match(func, arg_types: list['Type']):
    params = func.params
    param_types = [param.type for param in params]
    any_type = TypeManager.get('any')
    if all(isinstance(arg_type, lir.Type) for arg_type in arg_types):
        param_types = [param.type for param in param_types]

        any_type = any_type.type
    
    if len(arg_types) > len(param_types):
        return False
    elif len(arg_types) < len(param_types):
        return False
    
    for arg_type, param_type in zip(arg_types, param_types):
        if param_type == arg_type or param_type == any_type:
            continue

        return False
    
    return True

def match_to_overloads(func, arg_types: list['Type']):
    for overload in getattr(func, 'overloads', []):
        if not params_match(overload, arg_types):
            continue

        # TODO: check for ambiguous function call (function types match multiple overloads)
        return overload
    
    if not params_match(func, arg_types):
        return None
    
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
        print(' ' * self.column + '^')
        print(f'{Style.BRIGHT}{Fore.RED}error: {msg}{Style.RESET_ALL}')
        error(msg)
        # sys_exit(1)
        raise NotImplementedError

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

class TypeManager:
    type_map: dict[str, lir.Type] = {}

    @staticmethod
    def create_function_type(ret_type: 'Type', param_types: list['Type']):
        param_types_str = ', '.join(map(str, param_types))
        return Type(
            Position.zero(),
            f'({param_types_str}) -> {ret_type}',
            lir.FunctionType(ret_type.type, [param.type for param in param_types])
        )
    
    @staticmethod
    def from_llvm(llvm_type: lir.Type):
        for k, v in TypeManager.type_map.items():
            if v != llvm_type:
                continue

            return TypeManager.get(k)

    @staticmethod
    def get(name: str) -> Any:
        llvm_type = TypeManager.type_map.get(name)
        if llvm_type is None:
            return None
        
        return Type(Position.zero(), name, llvm_type)
    
    @staticmethod
    def exists(name: str):
        return name in TypeManager.type_map
    
    @staticmethod
    def add(name: str, llvm_type: lir.Type):
        if name in TypeManager.type_map:
            return
        
        TypeManager.type_map[name] = llvm_type
    
    @staticmethod
    def set(name: str, llvm_type: lir.Type):
        TypeManager.type_map[name] = llvm_type

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

            TypeManager.add('nil', lir.IntType(8).as_pointer())
            TypeManager.add('any', lir.IntType(8).as_pointer())
            TypeManager.add('Ref', lir.LiteralStructType([
                lir.IntType(8).as_pointer(), # void*
                lir.FunctionType(
                    lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()]
                ).as_pointer(), # nil (*destroy)(void*)
                lir.IntType(64), # size_t
            ]))

            TypeManager.add('int', lir.IntType(32))
            TypeManager.add('float', lir.FloatType())
            TypeManager.add('string', lir.LiteralStructType([
                lir.IntType(8).as_pointer(), # ptr
                lir.IntType(64), # length
                TypeManager.get('Ref').type.as_pointer() # ref
            ]))
            TypeManager.add('array', lir.LiteralStructType([
                lir.IntType(8).as_pointer(), # elements
                lir.IntType(64), # length
                lir.IntType(64), # capacity
                lir.IntType(64), # element_size
                TypeManager.get('Ref').type.as_pointer() # ref
            ]))
            TypeManager.add('bool', lir.IntType(1))
            TypeManager.add('pointer', lir.IntType(8).as_pointer())
            TypeManager.add('function', lir.IntType(8).as_pointer())

            TypeManager.add('Math', lir.IntType(8).as_pointer())
            TypeManager.add('System', lir.IntType(8).as_pointer())

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
        return getattr(self, 'type', TypeManager.get('nil'))
    
    def clone(self):
        return copy(self)

@dataclass
class Type(Node):
    display: str
    type: lir.Type
    
    def __str__(self):
        return self.display
    
    def __repr__(self):
        return self.display
    
    def needs_memory_management(self):
        if not isinstance(self.type, lir.LiteralStructType):
            return False

        if not any(elem == TypeManager.get('Ref').type.as_pointer() for elem in self.type.elements):
            return False

        return True

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
        return TypeManager.get('int')

@dataclass
class Float(Node):
    value: float

    @property
    def type(self) -> 'Type':
        return TypeManager.get('float')

@dataclass
class String(Node):
    value: str

    @property
    def type(self) -> 'Type':
        return TypeManager.get('string')

@dataclass
class Bool(Node):
    value: bool

    @property
    def type(self) -> 'Type':
        return TypeManager.get('bool')

@dataclass
class Nil(Node):
    @property
    def type(self) -> 'Type':
        return TypeManager.get('nil')

@dataclass
class StringLiteral(Node):
    value: str
    
    @property
    def type(self) -> 'Type':
        return TypeManager.get('pointer')

@dataclass
class Id(Node):
    name: str
    type: Type = field(default_factory=lambda: TypeManager.get('any'))

@dataclass
class BinaryOp(Node):
    left: Node
    op: str
    right: Node
    type: Type = field(default_factory=lambda: TypeManager.get('any'))

@dataclass
class UnaryOp(Node):
    op: str
    expr: Node
    type: Type = field(default_factory=lambda: TypeManager.get('any'))

@dataclass
class Call(Node):
    callee: str
    args: list[Node] = field(default_factory=list)
    type: Type = field(default_factory=lambda: TypeManager.get('any'))

@dataclass
class Attribute(Node):
    obj: Node
    attr: str
    args: Union[list[Node], None] = None # default to property call
    type: Type = field(default_factory=lambda: TypeManager.get('any'))

@dataclass
class Cast(Node):
    obj: Node
    type: Type

@dataclass
class Ternary(Node):
    condition: Node
    true: Node
    false: Node

    @property
    def type(self):
        return self.true.get_type()

@dataclass
class NewArray(Node):
    element_type: Type
    capacity: Node = field(default_factory=lambda: Int(Position.zero(), 10))

    @property
    def type(self):
        return TypeManager.get(f'array_{self.element_type}')

@dataclass
class Param(Node):
    name: str
    type: Type

@dataclass
class Body(Node):
    nodes: list[Node] = field(default_factory=list)

@dataclass
class Variable(Node):
    name: str
    value: Union[Node, None] = None
    is_const: bool = False
    type: Type = field(default_factory=lambda: TypeManager.get('nil'))

@dataclass
class Assignment(Node):
    name: str
    value: Node

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
    type: Type = field(default_factory=lambda: TypeManager.get('nil'))
    body: BodyType = None
    flags: FunctionFlags = field(default_factory=FunctionFlags)
    overloads: list['Function'] = field(default_factory=list)

    @property
    def ret_type(self):
        return self.type
    
    
    def __call__(
        self, pos: Position, scope: Scope, args: list[Any],
        module: lir.Module | None = None, builder: lir.IRBuilder | None = None
    ):
        arg_types = [arg.type for arg in args]
        func = match_to_overloads(self, arg_types)
        if func is None:
            pos.comptime_error(
                f'no matching overload in call to {self.name}',
                scope.src
            )
        
        callee = func.name
        generic_types = []
        callee_params = []
        symbol_types = []
        for i, (arg, param) in enumerate(zip(args, func.params)):
            any_type = TypeManager.get('any')
            arg_type = arg.type
            param_type = param.type
            if isinstance(arg_type, lir.Type):
                param_type = param_type.type
                any_type = any_type.type

            if param_type == any_type:
                if isinstance(arg_type, lir.Type):
                    symbol_types.append(TypeManager.from_llvm(arg_type))
                else:
                    symbol_types.append(arg_type)
                
                callee_params.append(Param(param.pos, param.name, arg_type))
                generic_types.append(arg_type)
            else:
                if arg_type != param_type:
                    pos.comptime_error(
                        'type mismatch in function call', scope.src
                    )
                
                symbol_types.append(param.type)
                callee_params.append(Param(param.pos, param.name, param_type))
        
        param_types = [param.type for param in callee_params]
        if generic_types:
            callee += ''.join(map(lambda x: f'_{x}', generic_types))
            debug(f'Generic function name: {callee}')
        
        if module is not None and builder is not None:
            c_registry = module.c_registry
            
            if callee in module.globals:
                debug(f'{callee} is compiled, using it again')
                ir_func = module.get_global(callee)
            else:
                from cure.lib import DefinitionContext

                ir_func = lir.Function(module, lir.FunctionType(func.ret_type.type, param_types),
                                       callee)
                body_builder = lir.IRBuilder(ir_func.append_basic_block())
                def_scope = scope.clone()
                ctx = DefinitionContext(pos, def_scope, module, body_builder, c_registry,
                                        callee_params, func.ret_type)
                for i, (param_type, symbol_type, param) in enumerate(
                    zip(param_types, symbol_types, callee_params)
                ):
                    def_scope.symbol_table.add(Symbol(param.name, symbol_type, store_in_pointer(
                        body_builder, param_type, ir_func.args[i], f'param_{param.name}_ptr'
                    )))
                
                info(f'Compiling {callee}')
                if func.body is not None and callable(func.body):
                    result = func.body(ctx)

                # utility and ease of use if statements
                if result is not None:
                    body_builder.ret(result)
                elif func.ret_type == TypeManager.get('nil') and not body_builder.block.is_terminated:
                    body_builder.ret(NULL())

                info(f'Compiled {callee}')
            
            return builder.call(ir_func, args)
        elif module is None and builder is None:
            return Call(pos, self.name, args, func.ret_type)

@dataclass
class Method(Function):
    pass

@dataclass
class Property(Variable):
    pass

@dataclass
class Class(Node):
    name: str
    generic_types: list[str] = field(default_factory=list)
    members: list[Method | Property] = field(default_factory=list)

@dataclass
class Return(Node):
    value: Node

    @property
    def type(self):
        return self.value.get_type()

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
