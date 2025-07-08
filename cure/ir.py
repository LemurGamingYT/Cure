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

    @property
    def names(self):
        return list(self.symbols.keys())

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
        
        # try again without being a pointer
        if llvm_type.is_pointer:
            llvm_type = llvm_type.pointee
            res = TypeManager.from_llvm(llvm_type)

            # if it returns a non-None result, convert it back into a pointer
            if res is not None:
                return res.as_pointer()

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

            TypeManager.add('int', lir.IntType(32))
            TypeManager.add('float', lir.FloatType())
            TypeManager.add('string', string_type)
            TypeManager.add('bool', lir.IntType(1))
            TypeManager.add('nil', lir.IntType(8).as_pointer())
            TypeManager.add('any', lir.IntType(8).as_pointer())
            TypeManager.add('pointer', lir.IntType(8).as_pointer())
            TypeManager.add('function', lir.IntType(8).as_pointer())
            TypeManager.add('Ref', Ref_type)
            TypeManager.add('any_function', lir.FunctionType(
                lir.IntType(8).as_pointer(),
                [lir.IntType(8).as_pointer()]
            ).as_pointer())

            TypeManager.add('Math', lir.IntType(8).as_pointer())

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
    
    def needs_memory_management(self):
        if not isinstance(self.type, (lir.LiteralStructType, lir.IdentifiedStructType)):
            return False

        if not any(elem == TypeManager.get('Ref').type.as_pointer() for elem in self.type.elements):
            return False

        return True

    def as_pointer(self):
        return Type(self.pos, f'{self.display}*', self.type.as_pointer())
    
    def reference(self):
        return Type(self.pos, f'{self.display}&', self.type.as_pointer(), self)

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
        return Type(Position.zero(), f'{self.element_type}[]', lir.LiteralStructType([
            self.element_type.type.as_pointer(),
            TypeManager.get('int').type, TypeManager.get('int').type,
            TypeManager.get('Ref').type.as_pointer()
        ]))

@dataclass
class Param(Node):
    name: str
    type: Type
    is_mutable: bool = False

@dataclass
class Body(Node):
    nodes: list[Node] = field(default_factory=list)

@dataclass
class Variable(Node):
    name: str
    value: Union[Node, None] = None
    is_mutable: bool = False
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
    
    
    def compile(
        self, pos: Position, module: lir.Module, scope: Scope, arg_types: list[Type]
    ):
        from cure.lib import DefinitionContext

        c_registry = module.c_registry

        params = []
        generic_types = []
        for arg_type, param in zip(arg_types, self.params):
            if param.type == TypeManager.get('any'):
                params.append(Param(param.pos, param.name, arg_type, param.is_mutable))
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
        elif self.ret_type == TypeManager.get('nil') and not body_builder.block.is_terminated:
            body_builder.ret(NULL())

        info(f'Compiled {callee}')
        return ir_func
    
    @staticmethod
    def _check_params(param_types: list[Type], arg_types: list[Type]):
        # check if the parameter types list and argument types list match in length
        if len(param_types) != len(arg_types):
            return False
        
        # loop through each parameter and argument types
        for param_type, arg_type in zip(param_types, arg_types):
            # for each parameter, check the following:
            # - if the parameter is an any type, if so, immediately allow the parameter
            any_type = TypeManager.get('any')
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
        if self._check_params([param.type for param in self.params], arg_types):
            func = self
        else:
            # for each overload, call _check_params, if none match, produce an error
            for overload in self.overloads:
                if not self._check_params([param.type for param in overload.params], arg_types):
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
            return Call(pos, self.name, args, func.ret_type)

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
