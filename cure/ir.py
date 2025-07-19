from dataclasses import dataclass, field, fields
from typing import Union, Any, cast
from abc import ABC, abstractmethod
from logging import debug, error
from sys import exit as sys_exit
from pathlib import Path

from colorama import Fore, Style

from cure.cstdlib_headers import ALLOWED_HEADERS


STDLIB_PATH = Path(__file__).parent / 'stdlib'
op_map = {
    '+': 'add', '-': 'sub', '*': 'mul', '/': 'div', '%': 'mod', '==': 'eq', '!=': 'neq', '>': 'gt',
    '<': 'lt', '>=': 'gte', '<=': 'lte', '&&': 'and', '||': 'or', '!': 'not'
}


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def increment_reference(pos: 'Position', scope: 'Scope', child: 'Id'):
    ref = Attribute(pos, scope.type_map.get('Ref'), child, 'ref')
    return Call(
        pos, scope.type_map.get('nil'),
        Id(pos, scope.type_map.get('function'), 'Ref_inc'),
        [ref]
    )

def destroy(pos: 'Position', scope: 'Scope', id: 'Id'):
    destructor_function = id.type.destructor(scope)
    if destructor_function is None:
        return

    func = destructor_function.value
    if not isinstance(func, Function):
        pos.comptime_error(scope, f'invalid destructor for type \'{id.type}\'')

    return Call(
        pos, func.type, Id(pos, scope.type_map.get('function'), func.name),
        [Ref(pos, id.type, id)]
    )


@dataclass
class Position:
    line: int
    column: int

    def comptime_error(self, scope: 'Scope', message: str):
        src = scope.src
        print(src.splitlines()[self.line - 1])
        print(' ' * self.column + '^')
        print(f'{Style.BRIGHT}{Fore.RED}error: {message}{Style.RESET_ALL}')
        error(message)
        # raise NotImplementedError
        sys_exit(1)
    
    @staticmethod
    def zero():
        return Position(0, 0)

@dataclass
class Symbol:
    name: str
    type: 'Type'
    value: Any
    is_mutable: bool = False

    def as_id(self, pos: Position):
        return Id(pos, self.type, self.name)

@dataclass
class SymbolTable:
    symbols: dict[str, Symbol] = field(default_factory=dict)
    local_symbols: dict[str, Symbol] = field(default_factory=dict)

    def get(self, name: str):
        return self.symbols.get(name)
    
    def has(self, name: str):
        return self.get(name) is not None
    
    def add(self, symbol: Symbol, name: str | None = None):
        self.symbols[name or symbol.name] = symbol
        self.local_symbols[name or symbol.name] = symbol
    
    def remove(self, name: str):
        if name in self.symbols:
            self.symbols.pop(name)
            return True
        
        return False
    
    def clone(self):
        return SymbolTable(self.symbols.copy())

@dataclass
class TypeMap:
    types: dict[str, 'Type'] = field(default_factory=dict)

    @staticmethod
    def new_type(display: str, type: str | None = None, is_reference: bool = False,
                 is_external: bool = False):
        return Type(Position.zero(), type or display, display, is_reference, is_external)

    def get(self, display: str):
        return self.types.get(display)
    
    def has(self, display: str):
        return self.get(display) is not None
    
    def add(self, display: str, type: str | None = None):
        typ = self.new_type(display, type)
        self.types[display] = typ
        return typ
    
    def remove(self, display: str):
        if display in self.types:
            self.types.pop(display)
            return True
        
        return False
    
    def clone(self):
        return TypeMap(self.types.copy())

@dataclass
class Scope:
    file: Path
    parent: Union['Scope', None] = None
    symbol_table: SymbolTable = field(default_factory=SymbolTable)
    type_map: TypeMap = field(default_factory=TypeMap)
    dependencies: list[Path] = field(default_factory=list)
    global_nodes: list['Node'] = field(default_factory=list)
    prepended_nodes: list['Node'] = field(default_factory=list)
    
    @property
    def unique_name(self):
        self._unique_name_idx += 1
        return f'_{self._unique_name_idx}'
    
    @property
    def toplevel(self):
        scope = self
        while scope.parent is not None:
            scope = scope.parent
        
        return scope

    def __post_init__(self):
        self.src = self.file.read_text()
        if self.parent is not None:
            self._unique_name_idx = self.parent._unique_name_idx + 1

            self.symbol_table = self.parent.symbol_table.clone()
            self.type_map = self.parent.type_map.clone()

            self.global_nodes = self.parent.global_nodes
        else:
            self._unique_name_idx = -1 # names start at 0
            
            self.type_map.add('int')
            self.type_map.add('float')
            self.type_map.add('string')
            self.type_map.add('bool')
            self.type_map.add('nil')

            self.type_map.add('any')
            self.type_map.add('function')

            self.type_map.add('Math')
    
    def use(self, pos: Position, name: str):
        if name in ALLOWED_HEADERS:
            self.dependencies.append(Path(name))
            return

        file = Path(name).resolve()
        if file.exists():
            self.use_local(file)
            return
        
        stdlib_file = STDLIB_PATH / name
        if stdlib_file.is_file():
            self.use_local(stdlib_file)
        elif stdlib_file.is_dir():
            for header in stdlib_file.glob('*.h'):
                header_scope = Scope(header)
                # TODO: check if parse_symbols is needed
                # parse_symbols(header, header_scope)

                self.merge(header_scope)
                self.dependencies.append(header.relative_to(STDLIB_PATH))
            
            for cfile in stdlib_file.glob('*.c'):
                self.dependencies.append(cfile)
            
            for cure in stdlib_file.glob('*.cure'):
                self.use_local(cure)
        else:
            pos.comptime_error(self, f'unknown library \'{name}\'')
    
    def use_local(self, path: Path):
        from cure import compile_to_str

        header_scope = Scope(path)
        debug(f'Compiling local file {path}')
        code = compile_to_str(header_scope)

        # wrapper files are for the analysis and memory passes only, they don't need to be included
        # in the resulting C file
        if not path.stem.endswith('_wrapper'):
            header_path = path.with_suffix('.h')
            header_path.write_text(f'#pragma once\n{code}')

            self.dependencies.append(header_path.absolute())
        else:
            debug(f'Using wrapper file {path}')
        
        self.merge(header_scope)
        debug(f'Compiled local file {path}')
    
    def merge(self, other: 'Scope'):
        self.symbol_table.symbols.update(other.symbol_table.symbols)
        self.type_map.types.update(other.type_map.types)

    def make_child(self) -> 'Scope':
        child = Scope(self.file, parent=self)
        # self.children.append(child)
        return child


@dataclass
class Node(ABC):
    pos: Position
    type: 'Type'

    def children(self, recursive: bool = False) -> list['Node']:
        def _children(node: Node):
            children_list = []
            for f in fields(node):
                k = f.name
                if k in ('pos', 'type'):
                    continue

                v = getattr(node, k)
                if isinstance(v, Node):
                    children_list.append(v)

                    if recursive:
                        children_list.extend(_children(v))
                elif is_iterable(v):
                    for child in v:
                        if not isinstance(child, Node):
                            continue

                        children_list.append(child)

                        if recursive:
                            children_list.extend(_children(child))
            
            return children_list
        
        return _children(self)

    def as_var(self, scope: Scope):
        name = scope.unique_name
        var = Variable(self.pos, self.type, name, self)
        scope.symbol_table.add(Symbol(name, self.type, self, var.is_mutable))

        id = Id(self.pos, self.type, name)
        return var, id
    
    def extract(self, scope: Scope):
        """Extracts the node out into a variable IF needed"""
        if self.type.destructor(scope) is None:
            return self
        
        var, id = self.as_var(scope)
        scope.prepended_nodes.append(var)
        return id


    @abstractmethod
    def codegen(self, scope: Scope) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def analyse(self, scope: Scope) -> 'Node':
        raise NotImplementedError

@dataclass
class Program(Node):
    nodes: list[Node] = field(default_factory=list)

    def codegen(self, scope):
        code = '\n'.join(map(lambda node: node.codegen(scope), self.nodes))
        includes_str = '\n'.join(map(
            lambda header: f'#include "{header.as_posix()}"',
            filter(lambda dep: dep.suffix == '.h', scope.dependencies)
        ))
        debug(f'Added includes: {includes_str}')

        global_nodes_str = '\n'.join(map(lambda node: node.codegen(scope), scope.global_nodes))
        debug(f'Added global nodes: {global_nodes_str}')
        return f"""{includes_str}

{global_nodes_str}

{code}"""
    
    def analyse(self, scope):
        return Program(
            self.pos, self.type.analyse(scope),
            [node.analyse(scope) for node in self.nodes]
        )

@dataclass
class Type(Node):
    type: str # type: ignore
    display: str
    is_reference: bool = field(compare=False, default=False)
    is_external: bool = field(compare=False, default=False)

    def __post_init__(self):
        self.ref_target = None

    def codegen(self, _):
        return self.type

    def analyse(self, scope):
        if self.is_reference:
            return self.ref_target.analyse(scope).as_reference()

        if not scope.type_map.has(self.display):
            self.pos.comptime_error(scope, f'unknown type \'{self.display}\'')
        
        return self
    
    def __eq__(self, other):
        if not isinstance(other, Type):
            return False
        
        if self.is_reference:
            return self.ref_target == other.ref_target
        elif other.is_reference:
            return self == other.ref_target
        else:
            return self.display == other.display
    
    def __str__(self):
        return self.display
    
    def __repr__(self):
        return str(self.type)
    
    def destructor(self, scope: Scope):
        return scope.symbol_table.get(f'{self.type}_destroy')
    
    def as_reference(self):
        typ = Type(self.pos, self.type + '*', self.display + '&', True)
        typ.ref_target = self
        return typ

@dataclass
class Param(Node):
    name: str
    is_mutable: bool = False

    def codegen(self, scope):
        return f'{self.type.codegen(scope)} {self.name}'
    
    def analyse(self, scope):
        return Param(self.pos, self.type.analyse(scope), self.name)

@dataclass
class Body(Node):
    nodes: list[Node] = field(default_factory=list)

    def codegen(self, scope):
        body_str = '\n'.join(map(lambda node: f'{node.codegen(scope)};', self.nodes))
        return f"""{{
{body_str}
}}"""
    
    def analyse(self, scope):
        nodes = []
        has_returned = False
        for node in self.nodes:
            node = node.analyse(scope)
            if scope.prepended_nodes:
                nodes.extend(scope.prepended_nodes)
                scope.prepended_nodes.clear()
            
            if isinstance(node, Return):
                has_returned = True
            
            nodes.append(node)
        
        if not has_returned:
            nodes.extend(self.destruct_symbols(self.pos, scope))
        
        return Body(self.pos, self.type.analyse(scope), nodes)
    

    @staticmethod
    def destruct_symbols(pos: Position, scope: Scope) -> list['Call']:
        destructors = []
        for symbol in scope.symbol_table.local_symbols.values():
            if isinstance(symbol.value, Param):
                continue

            call = destroy(pos, scope, symbol.as_id(pos))
            if call is None:
                continue

            destructors.append(call)
        
        return destructors

@dataclass
class Return(Node):
    value: Node

    def codegen(self, scope):
        return f'return {self.value.codegen(scope)}'
    
    def analyse(self, scope):
        value = self.value.analyse(scope)
        for child in [value] + value.children(True):
            if child.type.destructor(scope) is None:
                continue

            if not isinstance(child, Id):
                continue

            scope.prepended_nodes.append(increment_reference(self.pos, scope, child))
        
        scope.prepended_nodes.extend(Body.destruct_symbols(self.pos, scope))
        return Return(self.pos, value.type, value)

@dataclass
class Variable(Node):
    name: str
    value: Node
    is_mutable: bool = False
    op: str | None = None

    def codegen(self, scope):
        return f'{self.type.codegen(scope)} {self.name} = {self.value.codegen(scope)}'
    
    def analyse(self, scope):
        value = self.value.analyse(scope)
        for child in [value] + value.children(True):
            if child.type.destructor(scope) is None:
                continue

            if not isinstance(child, Id):
                continue
            
            scope.prepended_nodes.append(increment_reference(child.pos, scope, child))

        if (symbol := scope.symbol_table.get(self.name)) is not None:
            if not symbol.is_mutable:
                self.pos.comptime_error(scope, f'\'{self.name}\' is immutable')
            
            return Assignment(self.pos, value.type, self.name, value, self.op)
        
        if self.op is not None:
            self.pos.comptime_error(scope, f'\'{self.name}\' is not defined')
        
        scope.symbol_table.add(Symbol(self.name, value.type, value, self.is_mutable))
        return Variable(self.pos, value.type, self.name, value, self.is_mutable, self.op)

@dataclass
class Assignment(Node):
    name: str
    value: Node
    op: str | None = None

    def codegen(self, scope):
        return f'{self.name} = {self.value.codegen(scope)}'
    
    def analyse(self, scope):
        value = self.value
        if self.op is not None:
            value = Operation(
                self.pos, value.type, self.op,
                Id(value.pos, value.type, self.name), value
            ).analyse(scope)
        
        symbol = cast(Symbol, scope.symbol_table.get(self.name))
        symbol.value = value
        return Assignment(self.pos, value.type, self.name, value, self.op)

@dataclass(kw_only=True)
class FunctionFlags:
    static: bool = False
    property: bool = False
    method: bool = False
    public: bool = False
    internal: bool = False

@dataclass
class Function(Node):
    name: str
    params: list[Param] = field(default_factory=list)
    body: Body | None = field(default=None)
    overloads: list['Function'] = field(default_factory=list)
    flags: FunctionFlags = field(default_factory=FunctionFlags)
    generic_params: list[str] = field(default_factory=list)
    extend_type: Type | None = None

    def __post_init__(self):
        self._generics = []

    def codegen(self, scope):
        if self.body is None:
            return ''
        
        if self.params:
            params_str = ', '.join(map(lambda param: param.codegen(scope), self.params))
        else:
            params_str = 'void'
        
        return f'{self.type.codegen(scope)} {self.name}({params_str}) {self.body.codegen(scope)}\n'
    
    def analyse(self, scope):
        for param in self.generic_params:
            scope.type_map.add(param)

        type = self.type.analyse(scope)
        params = [param.analyse(scope) for param in self.params]
        body = self.body

        extend_type = self.extend_type.analyse(scope) if self.extend_type is not None else None
        extend_type_str = f'{extend_type}_' if extend_type is not None else ''
        name = f'{extend_type_str}{self.name}'
        func = Function(
            self.pos, self.type.analyse(scope), name, params, body,
            [overload.analyse(scope) for overload in self.overloads],
            self.flags, self.generic_params, extend_type
        )

        if func.name in scope.symbol_table.symbols:
            base = cast(Symbol, scope.symbol_table.get(func.name))
            func.name = f'{func.name}{scope.unique_name}'
            cast(Function, base.value).overloads.append(func)
        else:
            scope.symbol_table.add(Symbol(func.name, scope.type_map.get('function'), func))
        
        if body is not None:
            body_scope = scope.make_child()
            for param in params:
                body_scope.symbol_table.add(Symbol(param.name, param.type, param, param.is_mutable))
            
            body = body.analyse(body_scope)

            if type == body_scope.type_map.get('nil'):
                body.nodes.append(Return(body.pos, type, Nil(body.pos, type)))
        
        func.body = body
        for param in self.generic_params:
            scope.type_map.remove(param)

        return func
    
    
    def __call__(self, pos: Position, scope: Scope, args: list[Node]):
        func = self.find_matching_overload(scope, args)
        if func is None:
            arg_types_str = ', '.join(map(lambda arg: arg.type.display, args))
            pos.comptime_error(scope, f'no matching overloads with argument types [{arg_types_str}]')
        
        debug(f'Found valid function: {func.name}')
        if func.generic_params:
            debug('Function is generic')

            generic_list = []
            for param, arg in zip(func.params, args):
                if param.type.display not in func.generic_params:
                    continue

                generic_list.append(arg.type)

            debug(f'Generic list: {generic_list}')
            
            generic_list_str = ''.join(f'_{type}' for type in generic_list)
            callee_name = f'{func.name}{generic_list_str}'
            debug(f'Created new name for function: {callee_name}')
            if tuple(generic_list) not in self._generics:
                scope.global_nodes.append(Call(
                    pos, func.type, Id(pos, scope.type_map.get('function'), func.name),
                    [cast(Node, typ) for typ in generic_list]
                ))

                self._generics.append(tuple(generic_list))
                debug('Created new call for generic function')
        else:
            callee_name = func.name
        
        new_args: list[Node] = []
        for arg, param in zip(args, func.params):
            if param.type.is_reference:
                new_args.append(Ref(arg.pos, arg.type.as_reference(), arg))
            else:
                new_args.append(arg)
        
        return Call(pos, func.type, Id(pos, scope.type_map.get('function'), callee_name), new_args)
    
    def match_params(self, scope: Scope, func: 'Function', args: list[Node]) -> bool:
        params = func.params
        if len(params) != len(args):
            return False
        
        for arg, param in zip(args, params):
            if param.type.display in func.generic_params:
                debug(f'Generic type found {param.type.display}')
                continue

            if param.type == scope.type_map.get('any'):
                continue

            if param.type.is_reference:
                arg.type = arg.type.as_reference()

            if arg.type != param.type:
                debug(f'{arg.type} does not match {param.type}')
                return False
        
        return True

    def find_matching_overload(self, scope: Scope, args: list[Node]):
        if self.match_params(scope, self, args):
            return cast(Function, self)
        
        for overload in self.overloads:
            if not self.match_params(scope, overload, args):
                continue

            # TODO: check for ambiguous function calls (calls that match more than one overload)
            return overload

@dataclass
class Class(Node):
    name: str
    members: list[Function] = field(default_factory=list)
    bases: list[str] = field(default_factory=list)
    generic_params: list[str] = field(default_factory=list)

    def codegen(self, scope):
        if self.generic_params:
            return ''

        methods = [member for member in self.members if isinstance(member, Function)]

        code = []
        for method in methods:
            code.append(method.codegen(scope))
        
        return '\n'.join(code)
    
    def analyse(self, scope):
        scope.symbol_table.add(Symbol(self.name, self.type, self))
        scope.type_map.add(self.name)

        if self.generic_params:
            return self
        
        # if there are no generic parameters, we can define the class now
        return self.define(scope, {})
    
    def define(self, scope: Scope, generics: dict[str, Type]):
        type_name = self.name
        if self.generic_params:
            type_name += ''.join(f'_{str(g)}' for g in generics.values())
        
        if self.generic_params and scope.type_map.has(type_name):
            # already defined
            return self
        
        original_type = scope.type_map.get(self.name)
        typ = scope.type_map.add(type_name)
        members = []
        for member in self.members:
            member.name = f'{typ}_{member.name}'
            member_type = member.type
            if member_type.is_reference:
                member_type = member_type.ref_target
            
            if original_type == member_type:
                member.type = typ.as_reference() if member.type.is_reference else typ
            elif member_type.display in self.generic_params:
                member.type = generics[member_type.display].as_reference() if\
                    member.type.is_reference else generics[member_type.display]

            if not member.flags.static:
                member.params.insert(0, Param(self.pos, typ.as_reference(), 'self'))
            
            for i, param in enumerate(member.params):
                param_type = param.type
                if param_type.is_reference:
                    param_type = param_type.ref_target

                if param_type == original_type:
                    member.params[i].type = typ.as_reference() if param.type.is_reference else typ
                elif param_type.display in self.generic_params:
                    member.params[i].type = generics[param.type.display].as_reference() if\
                        param.type.is_reference else generics[param.type.display]
            
            members.append(member.analyse(scope))
            debug(f'Defined method {member.name}')
        
        if self.generic_params:
            scope.global_nodes.append(Call(
                self.pos, scope.type_map.get('any'),
                Id(self.pos, scope.type_map.get('function'), 'array'),
                list(generics.values())
            ))
        
        return Class(self.pos, typ, self.name, members, self.bases, self.generic_params)

@dataclass
class Elseif(Node):
    cond: Node
    body: Body

    def codegen(self, scope):
        return f' else if ({self.cond.codegen(scope)}) {self.body.codegen(scope)}'
    
    def analyse(self, scope):
        return Elseif(
            self.pos, self.type.analyse(scope), self.cond.analyse(scope), self.body.analyse(scope)
        )

@dataclass
class If(Node):
    cond: Node
    body: Body
    else_body: Body | None = field(default=None)
    elseifs: list[Elseif] = field(default_factory=list)

    def codegen(self, scope):
        cond = self.cond.codegen(scope)
        body = self.body.codegen(scope)
        else_body = f' else {self.else_body.codegen(scope)}' if self.else_body is not None else ''
        elseifs = '\n'.join(elseif.codegen(scope) for elseif in self.elseifs)
        return f'if ({cond}) {body}{elseifs}{else_body}'
    
    def analyse(self, scope):
        return If(
            self.pos, self.type.analyse(scope), self.cond.analyse(scope), self.body.analyse(scope),
            self.else_body.analyse(scope) if self.else_body is not None else self.else_body,
            [elseif.analyse(scope) for elseif in self.elseifs]
        )

@dataclass
class While(Node):
    cond: Node
    body: Body

    def codegen(self, scope):
        return f'while ({self.cond.codegen(scope)}) {self.body.codegen(scope)}'
    
    def analyse(self, scope):
        return While(
            self.pos, self.type.analyse(scope),
            self.cond.analyse(scope), self.body.analyse(scope)
        )

@dataclass
class Break(Node):
    def codegen(self, _):
        return 'break'
    
    def analyse(self, scope):
        return Break(self.pos, self.type.analyse(scope))

@dataclass
class Continue(Node):
    def codegen(self, _):
        return 'continue'
    
    def analyse(self, scope):
        return Continue(self.pos, self.type.analyse(scope))

@dataclass
class Use(Node):
    path: str

    def codegen(self, _):
        return f'// use {self.path}'
    
    def analyse(self, scope):
        scope.use(self.pos, self.path)
        return self

@dataclass
class Int(Node):
    value: int

    def codegen(self, _):
        return str(self.value)
    
    def analyse(self, _):
        # TODO: check if the integer value is too large (or small) for a 32 bit integer
        # calculated using: 2^(31) - 1
        return self

@dataclass
class Float(Node):
    value: float

    def codegen(self, _):
        return str(self.value)
    
    def analyse(self, _):
        # TODO: check if the float value is too large (or small) for a float
        return self

@dataclass
class String(Node):
    value: str

    def codegen(self, _):
        return f'string_new((u8*)"{self.value}", {len(self.value)})'
    
    def analyse(self, _):
        # TODO: check if length exceeds 64 bit unsigned integer limit
        # calculated using: 2^64 - 1

        return self

@dataclass
class Bool(Node):
    value: bool

    def codegen(self, _):
        return str(self.value).lower()
    
    def analyse(self, _):
        return self

@dataclass
class Nil(Node):
    def codegen(self, _):
        return 'NIL'
    
    def analyse(self, _):
        return self

@dataclass
class Id(Node):
    name: str

    def codegen(self, _):
        return self.name
    
    def analyse(self, scope):
        symbol = scope.symbol_table.get(self.name)
        type = scope.type_map.get(self.name)
        if symbol is None and type is None:
            self.pos.comptime_error(scope, f'unknown object \'{self.name}\'')
        
        if symbol is not None:
            return Id(self.pos, symbol.type, symbol.name)
        
        return Id(self.pos, type, self.name)

@dataclass
class Call(Node):
    callee: Id
    args: list[Node] = field(default_factory=list)

    def codegen(self, scope):
        args_str = ', '.join(map(lambda node: node.codegen(scope), self.args))
        return f'{self.callee.codegen(scope)}({args_str})'
    
    def analyse(self, scope):
        callee_name = self.callee.name
        symbol = scope.symbol_table.get(callee_name)
        if symbol is None:
            self.pos.comptime_error(scope, f'unknown function \'{callee_name}\'')
        
        func = symbol.value
        if not isinstance(func, Function):
            self.pos.comptime_error(scope, f'\'{callee_name}\' is not a function')
        
        args = [arg.analyse(scope) for arg in self.args]
        return func(self.pos, scope, args)

@dataclass
class Cast(Node):
    value: Node

    def codegen(self, scope):
        return f'({self.type.codegen(scope)})({self.value.codegen(scope)})'
    
    def analyse(self, scope):
        value = self.value.analyse(scope)
        result_type = self.type.analyse(scope)
        callee_name = f'{value.type}_to_{result_type}'
        symbol = scope.symbol_table.get(callee_name)
        if symbol is None:
            self.pos.comptime_error(scope, f'cannot cast \'{value.type}\' to type \'{result_type}\'')
        
        return Call(
            self.pos, result_type, Id(self.pos, scope.type_map.get('function'), callee_name),
            [value]
        ).analyse(scope)

@dataclass
class New(Node):
    new_type: Type
    args: list[Node] = field(default_factory=list)

    def codegen(self, scope):
        return super().codegen(scope)
    
    def analyse(self, scope):
        callee_name = f'{self.new_type}_new'
        symbol = scope.symbol_table.get(callee_name)
        if symbol is None:
            self.pos.comptime_error(scope, f'type \'{self.new_type}\' cannot be created')
        
        return Call(
            self.pos, self.type, Id(self.pos, scope.type_map.get('function'), callee_name),
            self.args
        ).analyse(scope)

@dataclass
class Operation(Node):
    op: str
    left: Node
    right: Node | None

    def codegen(self, scope):
        if self.right is None:
            return f'{self.op}{self.left.codegen(scope)}'
        
        return f'{self.left.codegen(scope)} {self.op} {self.right.codegen(scope)}'
    
    def analyse(self, scope):
        op_name = op_map[self.op]
        left = self.left.analyse(scope)
        if self.right is None:
            callee_name = f'{op_name}_{left.type}'
            args = [left]
            error_message = f'invalid operation \'{self.op}\' on type \'{left.type}\''
        else:
            right = self.right.analyse(scope)
            callee_name = f'{left.type}_{op_name}_{right.type}'
            args = [left, right]
            error_message = f'invalid operation \'{self.op}\' between types \'{left.type}\' and '\
                 f'\'{right.type}\''
        
        symbol = scope.symbol_table.get(callee_name)
        if symbol is None:
            self.pos.comptime_error(scope, error_message)
        
        return Call(
            self.pos, self.type, Id(self.pos, scope.type_map.get('function'), callee_name), args
        ).analyse(scope)

@dataclass
class Ternary(Node):
    cond: Node
    true: Node
    false: Node

    def codegen(self, scope):
        return f'{self.cond.codegen(scope)} ? {self.true.codegen(scope)} : {self.false.codegen(scope)}'
    
    def analyse(self, scope):
        cond = self.cond.analyse(scope)
        true = self.true.analyse(scope)
        false = self.false.analyse(scope)

        if cond.type != scope.type_map.get('bool'):
            self.pos.comptime_error(scope, 'condition type is not a boolean')

        if true.type != false.type:
            self.pos.comptime_error(scope, 'true and false ternary value types don\'t match')
        
        return Ternary(self.pos, true.type, cond, true, false)

@dataclass
class Bracketed(Node):
    value: Node

    def codegen(self, scope):
        return f'({self.value.codegen(scope)})'
    
    def analyse(self, scope):
        value = self.value.analyse(scope)
        return Bracketed(self.pos, value.type, value)

@dataclass
class Attribute(Node):
    object: Node
    attr: str
    args: list[Node] | None = None

    def codegen(self, scope):
        if self.args is None:
            return f'{self.object.codegen(scope)}.{self.attr}'
        
        args_str = ', '.join(arg.codegen(scope) for arg in self.args)
        return f'{self.object.codegen(scope)}.{self.attr}({args_str})'
    
    def analyse(self, scope):
        object = self.object.analyse(scope)
        attr = self.attr

        callee_name = f'{object.type}_{attr}'
        symbol = scope.symbol_table.get(callee_name)
        args = [object] + ([arg.analyse(scope) for arg in self.args] if self.args is not None else [])
        if symbol is None or not isinstance(symbol.value, Function):
            self.pos.comptime_error(scope, f'unknown attribute \'{attr}\' on type \'{object.type}\'')

        func = symbol.value
        if func.flags.static:
            args = args[1:]
        
        return Call(
            self.pos, self.type, Id(self.pos, scope.type_map.get('function'), symbol.name), args
        ).analyse(scope)

@dataclass
class NewArray(Node):
    element_type: Type
    size: int | None = None

    def codegen(self, _):
        raise NotImplementedError
    
    def analyse(self, scope):
        array_symbol = scope.symbol_table.get('array')
        array_cls = cast(Class, array_symbol.value).define(scope, {'T': self.element_type})

        return Call(
            self.pos, scope.type_map.get('any'),
            Id(self.pos, scope.type_map.get('function'), f'{array_cls.type}_new'),
            [Int(self.pos, scope.type_map.get('int'), 10)]
        ).analyse(scope)

@dataclass
class ArrayInit(Node):
    elements: list[Node] = field(default_factory=list)

    def codegen(self, _):
        raise NotImplementedError
    
    def analyse(self, scope):
        elements = [elem.analyse(scope) for elem in self.elements]
        if len(elements) == 0:
            self.pos.comptime_error(scope, 'cannot initialize empty array')
        
        array_type = elements[0].type
        name = scope.unique_name

        array_symbol = scope.symbol_table.get('array')
        array_cls = cast(Class, array_symbol.value).define(scope, {'T': array_type})

        scope.prepended_nodes.append(Variable(
            self.pos, array_cls.type, name, Call(
            self.pos, array_cls.type,
            Id(self.pos, scope.type_map.get('function'), f'{array_cls.type}_new'),
            [Int(self.pos, scope.type_map.get('int'), len(elements))]
        )).analyse(scope))

        for elem in elements:
            if elem.type != array_type:
                self.pos.comptime_error(
                    scope, 'cannot initialize array with elements of incompatible types'
                )
            
            scope.prepended_nodes.append(Call(
                self.pos, array_cls.type,
                Id(self.pos, scope.type_map.get('function'), f'{array_cls.type}_add'),
                [Id(self.pos, array_cls.type, name), elem]
            ).analyse(scope))
        
        return Id(self.pos, array_cls.type, name)

@dataclass
class Ref(Node):
    object: Node

    def codegen(self, scope):
        return f'&{self.object.codegen(scope)}'
    
    def analyse(self, scope):
        object = self.object.analyse(scope)
        return Ref(self.pos, object.type, object)

@dataclass
class Unsafe(Node):
    body: Body

    def codegen(self, scope):
        body = self.body.codegen(scope)[2:-2] # remove the leading and trailing '{' and '}'
        return f'// unsafe\n{body}\n// safe'
    
    def analyse(self, _):
        return self

@dataclass
class Noop(Node):
    def codegen(self, _):
        return ''
    
    def analyse(self, _):
        return self
