from typing import Union, Callable, TypeAlias, Any, cast
from dataclasses import dataclass, field
from importlib import import_module
from sys import exit as sys_exit
from logging import error, info
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
        # raise NotImplementedError
        sys_exit(1)

@dataclass
class Symbol:
    name: str
    type: 'Type'
    value: Any
    is_mutable: bool = False

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
class TypeMap:
    types: dict[str, 'Type'] = field(default_factory=dict)

    def __iter__(self):
        return iter(self.types.values())

    def add(self, display: str, llvm_type: lir.Type):
        self.types[display] = Type(Position.zero(), llvm_type, display)

    def get(self, name: str) -> Union['Type', None]:
        return self.types.get(name)
    
    def has(self, name: str):
        return name in self.types
    
    def remove(self, name: str):
        if self.has(name):
            self.types.pop(name)
    
    def clone(self):
        return TypeMap(self.types.copy())
    
    def merge(self, other: 'TypeMap'):
        self.types.update(other.types)

@dataclass
class Scope:
    file: Path
    parent: Union['Scope', None] = None
    symbol_table: SymbolTable = field(default_factory=SymbolTable)
    type_map: TypeMap = field(default_factory=TypeMap)
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
            self.type_map = self.parent.type_map.clone()
        else:
            self.src = self.file.read_text('utf-8')

            Ref_type = lir.global_context.get_identified_type('Ref')
            Ref_type.set_body(
                lir.IntType(8).as_pointer(), # void*
                lir.FunctionType(
                    lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()]
                ).as_pointer(), # nil (*destroy)(void*)
                lir.IntType(64), # size_t
            )

            string_type = lir.global_context.get_identified_type('string')
            string_type.set_body(
                lir.IntType(8).as_pointer(), # ptr
                lir.IntType(64), # length
                Ref_type.as_pointer() # ref
            )

            self.type_map.add('int', lir.IntType(32))
            self.type_map.add('float', lir.FloatType())
            self.type_map.add('string', string_type)
            self.type_map.add('bool', lir.IntType(1))
            self.type_map.add('nil', lir.IntType(8).as_pointer())
            self.type_map.add('any', lir.IntType(8).as_pointer())
            self.type_map.add('pointer', lir.IntType(8).as_pointer())
            self.type_map.add('function', lir.IntType(8).as_pointer())
            self.type_map.add('Ref', Ref_type)
            self.type_map.add('any_function', lir.FunctionType(
                lir.IntType(8).as_pointer(),
                [lir.IntType(8).as_pointer()]
            ).as_pointer())

            self.type_map.add('Math', lir.IntType(8).as_pointer())

            info('Added types')

            self.use('builtins', Position.zero())

    def clone(self):
        return Scope(self.file, self)
    
    def merge(self, other: 'Scope'):
        self.dependencies.extend(other.dependencies)
        self.symbol_table.merge(other.symbol_table)
        self.type_map.merge(other.type_map)
    
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
    type: 'Type'
    
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
    
    def clone(self):
        return copy(self)

@dataclass
class Type(Node):
    type: lir.Type
    display: str
    ref_target: Union['Type', None] = None

    @property
    def is_pointer(self):
        return isinstance(self.type, lir.PointerType) and self.display.endswith('*')
    
    @property
    def is_reference(self):
        return isinstance(self.type, lir.PointerType) and self.display.endswith('&')
    
    def __str__(self):
        return self.display
    
    def __repr__(self):
        return self.display
    
    def needs_memory_management(self, scope: Scope):
        if not isinstance(self.type, (lir.LiteralStructType, lir.IdentifiedStructType)):
            return False

        Ref = cast(Type, scope.type_map.get('Ref'))
        if not any(elem == Ref.type.as_pointer() for elem in self.type.elements):
            return False

        return True

    def as_pointer(self):
        return Type(self.pos, self.type.as_pointer(), f'{self.display}*')
    
    def reference(self):
        return Type(self.pos, self.type.as_pointer(), f'{self.display}&', self)

@dataclass
class Program(Node):
    nodes: list[Node] = field(default_factory=list)

@dataclass
class Int(Node):
    value: int

@dataclass
class Float(Node):
    value: float

@dataclass
class String(Node):
    value: str

@dataclass
class Bool(Node):
    value: bool

@dataclass
class Nil(Node):
    ...

@dataclass
class StringLiteral(Node):
    value: str

@dataclass
class Id(Node):
    name: str

@dataclass
class BinaryOp(Node):
    left: Node
    op: str
    right: Node

@dataclass
class UnaryOp(Node):
    op: str
    expr: Node

@dataclass
class Call(Node):
    callee: str
    args: list[Node] = field(default_factory=list)

@dataclass
class Attribute(Node):
    obj: Node
    attr: str
    args: Union[list[Node], None] = None # default to property call

@dataclass
class Cast(Node):
    obj: Node

@dataclass
class Ternary(Node):
    condition: Node
    true: Node
    false: Node

@dataclass
class NewArray(Node):
    element_type: Type
    capacity: Node

@dataclass
class Param(Node):
    name: str
    is_mutable: bool = False

@dataclass
class Body(Node):
    nodes: list[Node] = field(default_factory=list)

@dataclass
class Variable(Node):
    name: str
    value: Union[Node, None] = None
    is_mutable: bool = False

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
    body: BodyType = None
    flags: FunctionFlags = field(default_factory=FunctionFlags)
    overloads: list['Function'] = field(default_factory=list)

    @property
    def ret_type(self):
        return self.type
    
    
    def compile(
        self, pos: Position, module: lir.Module, scope: Scope, arg_types: list[Type]
    ):
        from cure.lib import DefinitionContext

        c_registry = module.c_registry

        params = []
        generic_types = []
        for arg_type, param in zip(arg_types, self.params):
            if param.type == scope.type_map.get('any'):
                params.append(Param(param.pos, arg_type, param.name, param.is_mutable))
                generic_types.append(arg_type)
            else:
                params.append(param)

        callee = f'{self.name}{"".join(f"_{generic_type}" for generic_type in generic_types)}'
        if callee in module.globals:
            return module.get_global(callee)

        param_types = [param.type.type for param in params]
        ir_func = lir.Function(module, lir.FunctionType(self.ret_type.type, param_types),
                                callee)
        body_builder = lir.IRBuilder(ir_func.append_basic_block())
        def_scope = scope.clone()
        ctx = DefinitionContext(pos, def_scope, module, body_builder, c_registry,
                                params, self.ret_type)
        for i, (ir_type, param) in enumerate(zip(arg_types, params)):
            value = ir_func.args[i]
            if param.is_mutable:
                value = store_in_pointer(body_builder, ir_type.type, value, f'{param.name}_ptr')
            
            def_scope.symbol_table.add(Symbol(param.name, ir_type, value))
        
        info(f'Added parameters to scope: {params}')
        info(f'Compiling {callee}')
        info(f'Current function signature: {ir_func}')
        if self.body is not None and callable(self.body):
            result = self.body(ctx)

        # utility and ease of use if statements
        if result is not None:
            body_builder.ret(result)
        elif self.ret_type == scope.type_map.get('nil') and not body_builder.block.is_terminated:
            body_builder.ret(NULL())

        info(f'Compiled {callee}')
        return ir_func
    
    @staticmethod
    def _check_params(scope: Scope, param_types: list[Type], arg_types: list[Type]):
        # check if the parameter types list and argument types list match in length
        if len(param_types) != len(arg_types):
            return False
        
        # loop through each parameter and argument types
        for param_type, arg_type in zip(param_types, arg_types):
            # for each parameter, check the following:
            # - if the parameter is an any type, if so, immediately allow the parameter
            any_type = scope.type_map.get('any')
            if param_type == any_type:
                continue
            
            # - if the parameter is a reference type, if so, remove the reference and carry on
            if param_type.is_reference:
                param_type = cast(Type, param_type.ref_target)

            # - if the parameter type matches the argument type
            if arg_type != param_type:
                return False
        
        return True
    
    def __call__(
        self, pos: Position, scope: Scope, args: list[Any],
        module: lir.Module | None = None, builder: lir.IRBuilder | None = None
    ):
        arg_types = [arg.type for arg in args]

        # check if the main function matches the argument types
        if self._check_params(scope, [param.type for param in self.params], arg_types):
            func = self
        else:
            # for each overload, call _check_params, if none match, produce an error
            for overload in self.overloads:
                if not self._check_params(scope, [param.type for param in overload.params], arg_types):
                    continue

                func = overload
                break
            else:
                arg_types_str = ', '.join(map(str, arg_types))
                error(
                    f'no matching overloads for argument types [{arg_types_str}]'\
                        f' for function call to {self.name}'
                )

                info(f'Args: {args}')
                info(f'Argument types {arg_types}')
                info(f'Parameter Types: [{", ".join(str(param.type) for param in self.params)}]')
                info(f'Num Overloads: {len(self.overloads)}')
                if self.overloads:
                    info(f'Overload Names: [{", ".join(overload.name for overload in self.overloads)}]')

                pos.comptime_error(
                    f'no matching overloads [{arg_types_str}]', scope.src
                )
        
        # if the module and builder is given, then it's a code generation call and the _compile
        # function should be used
        if module is not None and builder is not None:
            info(f'Code generation call to {func.name}')
            ir_func = func.compile(pos, module, scope, arg_types)
            call_args = [arg.value for arg in args]
            return builder.call(ir_func, call_args)
        # otherwise, the call is an IR call, return the Call node
        else:
            info(f'IR call to {func.name}')
            return Call(pos, func.ret_type, self.name, args)

@dataclass
class Return(Node):
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
