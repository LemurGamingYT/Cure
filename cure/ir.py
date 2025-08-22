from dataclasses import dataclass, field, fields
from sys import exit as sys_exit, stderr
from tempfile import NamedTemporaryFile
from logging import debug, info, error
from abc import ABC, abstractmethod
from typing import Union, Any, cast
from pathlib import Path

from colorama import Fore, Style

from cure.target import Target


# a list of all reserved keywords in C++ that are not in this language
RESERVED_CPP_KEYWORDS = {'alignas', 'alignof', 'and', 'and_eq', 'asm', 'atomic_cancel',
                         'atomic_commit', 'atomic_noexcept', 'auto', 'bitand', 'bitor', 'bool',
                         'break', 'case', 'catch', 'char', 'char8_t', 'char16_t', 'char32_t',
                         'char32_t', 'compl', 'concept', 'const', 'consteval', 'constexpr',
                         'constinit', 'const_cast', 'continue', 'contract_assert', 'co_await',
                         'co_return', 'co_yield', 'decltype', 'default', 'delete', 'do', 'double',
                         'dynamic_cast', 'enum', 'explicit', 'export', 'extern', 'false', 'friend',
                         'goto', 'inline', 'long', 'mutable', 'namespace', 'noexcept', 'not',
                         'not_eq', 'nullptr', 'operator', 'or', 'or_eq', 'private', 'protected',
                         'public', 'reflexpr', 'register', 'reinterpret_cast', 'requires',
                         'return', 'short', 'signed', 'sizeof', 'static_assert', 'static_cast',
                         'struct', 'switch', 'synchronized', 'template', 'this', 'thread_local',
                         'throw', 'try', 'typedef', 'typeid', 'typename', 'union', 'unsigned',
                         'using', 'virtual', 'void', 'volatile', 'wchar_t', 'xor', 'xor_eq'}
STDLIB_PATH = Path(__file__).parent / 'stdlib'
op_map = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'div', '%': 'mod', '==': 'eq', '!=': 'neq',
          '<': 'lt', '>': 'gt', '<=': 'lte', '>=': 'gte', '&&': 'and', '||': 'or', '!': 'not'}

@dataclass
class Dependency:
    path: Path
    type: str

@dataclass
class Position:
    line: int
    column: int

    def comptime_error(self, scope: 'Scope', message: str):
        src = scope.src
        if self.line > len(src.splitlines()):
            self.line = len(src.splitlines())
        
        print(src.splitlines()[self.line - 1], file=stderr)
        print(' ' * self.column + '^', file=stderr)
        print(f'{Style.BRIGHT}{Fore.RED}error: {message}{Style.RESET_ALL}', file=stderr)
        error(message)
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

@dataclass
class SymbolTable:
    symbols: dict[str, Symbol] = field(default_factory=dict)

    def add(self, symbol: Symbol, name: str | None = None):
        self.symbols[name or symbol.name] = symbol
    
    def get(self, name: str):
        return self.symbols.get(name)
    
    def has(self, name: str):
        return name in self.symbols
    
    def remove(self, name: str):
        if self.has(name):
            self.symbols.pop(name)
            return True
        
        return False
    
    def merge(self, other: 'SymbolTable'):
        self.symbols.update(other.symbols)
    
    def clone(self):
        return SymbolTable(self.symbols.copy())

@dataclass
class TypeMap:
    types: dict[str, 'Type'] = field(default_factory=dict)
    
    def add(self, type: 'Type'):
        self.types[type.type] = type
    
    def get(self, display: str):
        return self.types.get(display)
    
    def has(self, display: str):
        return display in self.types
    
    def remove(self, display: str):
        if self.has(display):
            self.types.pop(display)
            return True
        
        return False
    
    def merge(self, other: 'TypeMap'):
        self.types.update(other.types)
    
    def clone(self):
        return TypeMap(self.types.copy())

@dataclass
class Scope:
    file: Path
    parent: Union['Scope', None] = None
    symbol_table: SymbolTable = field(default_factory=SymbolTable)
    type_map: TypeMap = field(default_factory=TypeMap)
    children: list['Scope'] = field(default_factory=list)
    dependencies: list[Dependency] = field(default_factory=list)
    prepended_nodes: list['Node'] = field(default_factory=list)
    target: Target = Target.get_current()
    in_loop: bool = False
    
    @property
    def unique_name(self):
        self._unique_name_idx += 1
        return f'_{self._unique_name_idx}'

    def __post_init__(self):
        self.src = self.file.read_text()
        if self.parent is not None:
            self._unique_name_idx = self.parent._unique_name_idx + 1

            self.symbol_table = self.parent.symbol_table.clone()
            self.type_map = self.parent.type_map.clone()

            self.in_loop = self.parent.in_loop
        else:
            self._unique_name_idx = -1
            
            self.type_map.add(PrimitiveType(Position.zero(), 'int'))
            self.type_map.add(PrimitiveType(Position.zero(), 'float'))
            self.type_map.add(ClassType(Position.zero(), 'string'))
            self.type_map.add(PrimitiveType(Position.zero(), 'bool'))
            self.type_map.add(PrimitiveType(Position.zero(), 'nil'))

            self.type_map.add(PrimitiveType(Position.zero(), 'any'))
            self.type_map.add(PrimitiveType(Position.zero(), 'function'))

            self.type_map.add(PrimitiveType(Position.zero(), 'Math'))
            self.type_map.add(PrimitiveType(Position.zero(), 'System'))
            self.type_map.add(PrimitiveType(Position.zero(), 'Random'))
    
    def use(self, pos: Position, name: str):
        file = Path(name).resolve()
        debug(f'Using {name} at Path {file}')
        if file.exists():
            self.use_local(file)
            return
        
        stdlib_path = STDLIB_PATH / name
        debug(f'{file} doesn\'t exist, checking if {name} is part of the standard library at '\
              f'{stdlib_path}')
        if not stdlib_path.is_dir():
            pos.comptime_error(self, f'unknown library \'{name}\'')
        
        for header in stdlib_path.glob('*.hpp'):
            debug(f'Found header file {header}, relative path = {header.relative_to(STDLIB_PATH)}')
            self.dependencies.append(Dependency(header.relative_to(STDLIB_PATH), 'hpp'))
        
        for cfile in stdlib_path.glob('*.cpp'):
            debug(f'Found source file {cfile}')
            self.dependencies.append(Dependency(cfile, 'src'))
        
        for cure in stdlib_path.glob('*.cure'):
            debug(f'Found cure file {cure}')
            self.use_local(cure)
        
        if (deps := stdlib_path / 'dependencies.txt').exists():
            self.read_dependencies(deps)
    
    def read_dependencies(self, file: Path):
        lines = file.read_text().splitlines()
        for line in lines:
            if line.startswith('#'):
                continue
            elif line.startswith('sources = '):
                line = line.removeprefix('sources = ')
                for source in line.split(','):
                    self.dependencies.append(Dependency(file.parent / Path(source.strip()), 'src'))
            elif line.startswith('include_dirs = '):
                line = line.removeprefix('include_dirs = ')
                for directory in line.split(','):
                    self.dependencies.append(Dependency(
                        file.parent / Path(directory.strip()), 'hpp_dir'
                    ))
            elif line.startswith('deps = '):
                line = line.removeprefix('deps = ')
                for dependency in line.split(','):
                    self.dependencies.append(Dependency(file.parent / Path(dependency.strip()), 'dep'))
            elif line.startswith('libs = '):
                line = line.removeprefix('libs = ')
                for library in line.split(','):
                    self.dependencies.append(Dependency(Path(library.strip()), 'lib'))
    
    def use_local(self, file: Path):
        from cure import compile_to_str

        info(f'{file} is a local file')
        scope = Scope(file)
        code = compile_to_str(scope)
        debug(f'Compiled {file} to string')
        if not file.stem.endswith('_wrapper'): # wrapper files do not need .hpp files generated
            header_file = file.with_suffix('.hpp').with_stem(f'{file.stem}_header')
            header_file.write_text(f"""#pragma once
{code}""")
            
            self.dependencies.append(Dependency(header_file, 'hpp'))
            info(f'Compiled {file} to header file {header_file}')
        else:
            info(f'{file} is a wrapper file, no .hpp file generated')
        
        self.merge(scope)
    
    def merge(self, other: 'Scope'):
        self.symbol_table.merge(other.symbol_table)
        self.type_map.merge(other.type_map)
        self.dependencies.extend(other.dependencies)

    def make_child(self) -> 'Scope':
        child = Scope(file=self.file, parent=self)
        self.children.append(child)
        return child
    
    def define_class(self, pos: Position, name: str, generic_types: list['Type']):
        symbol = self.symbol_table.get(name)
        if symbol is None:
            pos.comptime_error(self, f'No class named \'{name}\'')
        
        return cast(Class, symbol.value).define(self, generic_types)


@dataclass(unsafe_hash=True)
class Node(ABC):
    pos: Position = field(compare=False, repr=False, hash=False)
    type: 'Type'

    @property
    def children(self):
        children = []
        for f in fields(self):
            child = getattr(self, f.name)
            if isinstance(child, list):
                for c in child:
                    if isinstance(c, Node):
                        children.append(c)
            elif isinstance(child, Node):
                children.append(child)
        
        return children

    @abstractmethod
    def codegen(self, scope: Scope) -> str:
        ...
    
    def analyse(self, scope: Scope) -> 'Node':
        return self

@dataclass(unsafe_hash=True)
class Program(Node):
    nodes: list[Node] = field(default_factory=list)

    def codegen(self, scope):
        code = '\n'.join(f'{node.codegen(scope)};' for node in self.nodes)
        includes = '\n'.join(
            f'#include "{dep.path.as_posix()}"' for dep in scope.dependencies
            if dep.type == 'hpp'
        )

        return f"""{includes}

{code}
"""
    
    def analyse(self, scope):
        return Program(self.pos, self.type.analyse(scope), [node.analyse(scope) for node in self.nodes])

@dataclass(unsafe_hash=True)
class Type(Node):
    type: str # type: ignore

    def object_type(self, scope: Scope):
        """The type that will be used in mangled function names and to access methods and properties
in the symbol table. Defaults to the C++ type name (by calling `.codegen`)."""

        return self.codegen(scope)

    def __str__(self):
        return self.type

    def codegen(self, _):
        return self.type

    def analyse(self, scope: Scope):
        typ = scope.type_map.get(self.type)
        if typ is None:
            self.pos.comptime_error(scope, f'unknown type \'{self.type}\'')
        
        return typ

@dataclass(unsafe_hash=True)
class PrimitiveType(Type):
    pass

@dataclass(unsafe_hash=True)
class ArrayType(Type):
    element_type: Type

    def codegen(self, scope):
        return f'array<{self.element_type.codegen(scope)}>'
    
    def analyse(self, scope):
        elem_type = self.element_type.analyse(scope)
        array_cls = scope.define_class(self.pos, 'array', [elem_type])
        return array_cls.type

@dataclass(unsafe_hash=True)
class ClassType(Type):
    generic_types: list[Type] = field(default_factory=list)

    def codegen(self, scope):
        if self.generic_types:
            generic_types_str = ', '.join(typ.codegen(scope) for typ in self.generic_types)
            return f'{self.type}<{generic_types_str}>'
    
        return self.type
    
    def analyse(self, scope):
        return ClassType(self.pos, self.type, [typ.analyse(scope) for typ in self.generic_types])

@dataclass(unsafe_hash=True)
class ReferenceType(Type):
    type: str # type: ignore
    inner: Type

    def __eq__(self, other):
        if not isinstance(other, Type):
            return False
        
        return self.inner == other

    def object_type(self, scope):
        return self.inner.object_type(scope)

    def codegen(self, scope):
        return f'{self.inner.codegen(scope)}&'
    
    def analyse(self, scope):
        return ReferenceType(
            self.pos, self.type if self.type.endswith('&') else f'{self.type}&',
            self.inner.analyse(scope)
        )

@dataclass(unsafe_hash=True)
class FunctionType(Type):
    return_type: Type
    param_types: list[Type] = field(default_factory=list)

    @staticmethod
    def new(pos: Position, return_type: Type, param_types: list[Type]):
        param_types_str = ', '.join(str(t) for t in param_types)
        return FunctionType(
            pos, f'({param_types_str}) -> {return_type}',
            return_type, param_types
        )

    def __eq__(self, other):
        if not isinstance(other, FunctionType):
            return False
        
        return self.return_type == other.return_type and self.param_types == other.param_types

    def object_type(self, _):
        return 'function'

    def codegen(self, scope):
        param_types_str = ', '.join(typ.codegen(scope) for typ in self.param_types)
        return f'std::function<{self.return_type.codegen(scope)}({param_types_str})>'
    
    def analyse(self, scope):
        param_types = [typ.analyse(scope) for typ in self.param_types]
        return_type = self.return_type.analyse(scope)
        return FunctionType.new(self.pos, return_type, param_types)

@dataclass(unsafe_hash=True)
class GenericType(Type):
    real_type: Type | None = None

    def __eq__(self, other):
        if not isinstance(other, GenericType):
            return False
        
        if self.real_type is None:
            return self.type == other.type
        
        return self.real_type == other.real_type
    
    def codegen(self, scope):
        if self.real_type is not None:
            return self.real_type.codegen(scope)
        
        return self.type
    
    def analyse(self, scope):
        return GenericType(
            self.pos, self.type,
            self.real_type.analyse(scope) if self.real_type is not None else None
        )

@dataclass
class Arg(Node):
    value: Node
    label: str | None = None

    def codegen(self, scope):
        return self.value.codegen(scope)
    
    def analyse(self, scope):
        value = self.value.analyse(scope)
        return Arg(self.pos, value.type, value, self.label)

@dataclass(unsafe_hash=True)
class Param(Node):
    name: str
    is_mutable: bool = False
    default: Node | None = None

    def codegen(self, scope):
        # default parameters are handled in function calls
        typ = self.type.codegen(scope)
        # if self.default is not None:
        #     return f'{typ} {self.name} /* = {self.default.codegen(scope)} */'
        
        return f'{typ} {self.name}'
    
    def analyse(self, scope):
        return Param(
            self.pos, self.type.analyse(scope), self.name, self.is_mutable,
            self.default.analyse(scope) if self.default is not None else None
        )

@dataclass(unsafe_hash=True)
class Body(Node):
    nodes: list[Node] = field(default_factory=list)

    def codegen(self, scope):
        return '\n'.join(f'{node.codegen(scope)};' for node in self.nodes)
    
    def analyse(self, scope):
        nodes = []
        for node in self.nodes:
            node = node.analyse(scope)
            if scope.prepended_nodes:
                nodes.extend(scope.prepended_nodes)
                scope.prepended_nodes.clear()
            
            nodes.append(node)
        
        return Body(self.pos, self.type.analyse(scope), nodes)

@dataclass(unsafe_hash=True)
class Return(Node):
    value: Node

    def codegen(self, scope):
        return f'return {self.value.codegen(scope)}'
    
    def analyse(self, scope):
        value = self.value.analyse(scope)
        return Return(self.pos, value.type, value)

@dataclass(kw_only=True, unsafe_hash=True)
class FunctionFlags:
    static: bool = False
    property: bool = False
    method: bool = False
    public: bool = False
    internal: bool = False

@dataclass(unsafe_hash=True)
class Function(Node):
    name: str
    ret_type: Type
    params: list[Param] = field(default_factory=list)
    body: Body | None = field(default=None)
    overloads: list['Function'] = field(default_factory=list)
    flags: FunctionFlags = field(default_factory=FunctionFlags)
    generic_names: list[str] = field(default_factory=list)
    extend_type: Type | None = None

    def codegen(self, scope):
        if self.body is None:
            return ''
        
        body = self.body.codegen(scope)
        if self.name == 'main':
            if len(self.params) != 0:
                self.pos.comptime_error(scope, 'main function cannot have parameters')
            
            if self.ret_type.type != 'int':
                self.pos.comptime_error(scope, 'main function must return int')
            
            params_str = 'int argc, char* argv[]'
            body = f"""cure_init(argc, argv);
{body}"""
        else:
            params_str = ', '.join(param.codegen(scope) for param in self.params)\
                if len(self.params) > 0 else 'void'
        
        signature = f'{self.ret_type.codegen(scope)} {self.name}({params_str})'
        return f"""{signature} {{
{body}
}}"""
    
    def analyse(self, scope):
        extend_type = self.extend_type.analyse(scope) if self.extend_type is not None else None
        name = self.name
        if name in op_map:
            op_name = op_map[name]
            if len(self.params) == 2:
                name = f'{self.params[0].type.object_type(scope)}_{op_name}_'\
                    f'{self.params[1].type.object_type(scope)}'
            elif len(self.params) == 1:
                name = f'{op_name}_{self.params[0].type.object_type(scope)}'
            
            debug(f'Function name is an operator {self.name}, mangled name = {name}')
        
        if extend_type is not None:
            name = f'{extend_type.object_type(scope)}_{name}'

            debug(f'Function {self.name} extends type {extend_type}, mangled name = {name}')
        
        _name = name
        if name in RESERVED_CPP_KEYWORDS:
            self.pos.comptime_error(
                scope, f'\'{name}\' is a reserved name, it cannot be used as a function name'
            )
        
        for generic_name in self.generic_names:
            scope.type_map.add(PrimitiveType(self.pos, generic_name))

        func = Function(
            self.pos, self.type.analyse(scope), name, self.ret_type.analyse(scope),
            [param.analyse(scope) for param in self.params], self.body,
            [overload.analyse(scope) for overload in self.overloads],
            self.flags, self.generic_names, extend_type
        )
        
        if (symbol := scope.symbol_table.get(func.name)) is not None:
            base_func = symbol.value
            if not isinstance(base_func, Function):
                self.pos.comptime_error(scope, f'base of overload is not a function \'{func.name}\'')
            
            base_func.overloads.append(func)
        else:
            scope.symbol_table.add(Symbol(func.name, FunctionType.new(
                func.pos, func.ret_type, [param.type for param in func.params]
            ), func), _name)
        
        if func.body is not None:
            body_scope = scope.make_child()
            for param in func.params:
                body_scope.symbol_table.add(Symbol(param.name, param.type, param, param.is_mutable))
            
            func.body = func.body.analyse(body_scope)

            if func.ret_type == scope.type_map.get('nil'):
                func.body.nodes.append(Return(
                    self.pos, scope.type_map.get('nil'),
                    Nil(self.pos, scope.type_map.get('nil'))
                ))
        
        for generic_name in self.generic_names:
            scope.type_map.remove(generic_name)
        
        return func

@dataclass(unsafe_hash=True)
class Variable(Node):
    name: str
    value: Node
    is_mutable: bool = False
    op: str | None = None

    def codegen(self, scope):
        return f'{self.type.codegen(scope)} {self.name} = {self.value.codegen(scope)}'
    
    def analyse(self, scope):
        name = self.name
        if name in RESERVED_CPP_KEYWORDS:
            self.pos.comptime_error(
                scope, f'\'{name}\' is a reserved name, it cannot be used as a variable name'
            )

        value = self.value.analyse(scope)
        if scope.symbol_table.has(self.name):
            return Assignment(self.pos, value.type, self.name, value, self.op).analyse(scope)

        scope.symbol_table.add(Symbol(name, value.type, value, self.is_mutable), self.name)
        return Variable(self.pos, value.type, name, value, self.is_mutable, self.op)

@dataclass(unsafe_hash=True)
class Assignment(Node):
    name: str
    value: Node
    op: str | None = None

    def codegen(self, scope):
        return f'{self.name} = {self.value.codegen(scope)}'
    
    def analyse(self, scope):
        symbol = cast(Symbol, scope.symbol_table.get(self.name))
        if not symbol.is_mutable:
            self.pos.comptime_error(scope, f'\'{self.name}\' is immutable')
        
        value = self.value
        if self.op is not None:
            value = Operation(
                self.pos, scope.type_map.get('any'), self.op, Id(self.pos, symbol.type, symbol.name),
                value
            ).analyse(scope)

        return Assignment(self.pos, value.type, symbol.name, value, self.op)

@dataclass(unsafe_hash=True)
class Class(Node):
    name: str
    members: list[Node] = field(default_factory=list)
    generic_names: list[str] = field(default_factory=list)
    is_internal: bool = False

    def codegen(self, _):
        return ''
    
    def analyse(self, scope):
        scope.type_map.add(ClassType(self.pos, self.name))
        typ = scope.type_map.get(self.name)
        scope.symbol_table.add(Symbol(self.name, typ, self))
        if not self.generic_names:
            self.define(scope, [])
        
        return Class(self.pos, typ, self.members, self.generic_names)
    
    def replace_type(self, scope: Scope, typ: Type, cls_type: Type, **generics: Type):
        out_type = None
        if typ.type == 'self':
            out_type = cls_type
        elif typ.type not in generics:
            out_type = typ
        else:
            info(f'Replacing return type with generic type {generics[typ.type]}')
            out_type = generics[typ.type]
        
        for f in fields(out_type):
            child = getattr(out_type, f.name)
            if isinstance(child, Type):
                setattr(out_type, f.name, self.replace_type(scope, child, cls_type, **generics))
            elif isinstance(child, list):
                for i, item in enumerate(child):
                    if not isinstance(item, Type):
                        continue

                    child[i] = self.replace_type(scope, item, cls_type, **generics)
        
        return out_type.analyse(scope)
    
    def define_method(self, member: Function, scope: Scope, cls_type: Type, typ: Type,
                      **generics: Type):
        debug(f'Adding class member {member.name}')

        flags = FunctionFlags()
        flags.internal = self.is_internal or member.flags.internal
        flags.method = member.flags.method
        flags.property = member.flags.property
        flags.public = member.flags.public
        flags.static = member.flags.static

        needs_self_param = not flags.static and not flags.internal
        debug(f'Member needs self parameter = {needs_self_param}')
        debug(f'Member is internal = {flags.internal}')

        params = []
        if needs_self_param and len(member.params) > 0 and member.params[0].type != typ:
            params.append(Param(self.pos, cls_type, 'self', True))
            info(f'Added self parameter to {member.name}\'s parameters')
        
        for generic_name in member.generic_names:
            scope.type_map.add(GenericType(self.pos, generic_name))
        
        ret_type = self.replace_type(scope, member.ret_type, cls_type, **generics)
        params.extend(Param(
            self.pos, self.replace_type(scope, param.type, cls_type, **generics),
            param.name, param.is_mutable
        ) for param in member.params)

        for generic_name in member.generic_names:
            scope.type_map.remove(generic_name)

        name = member.name
        if member.name in op_map:
            op_name = op_map[name]
            if len(params) == 2:
                name = f'{params[0].type.object_type(scope)}_{op_name}_'\
                    f'{params[1].type.object_type(scope)}'
            elif len(params) == 1:
                name = f'{op_name}_{params[0].type.object_type(scope)}'
        else:
            name = f'{cls_type.object_type(scope)}_{member.name}'
        
        debug(f'Creating method with name {name}')
        method = Function(
            self.pos, member.type, name, ret_type, params, member.body,
            member.overloads, flags, member.generic_names
        )

        scope.symbol_table.add(Symbol(name, scope.type_map.get('function'), method))

        method.name = member.name
        return method
    
    def define(self, scope: Scope, generic_types: list['Type']):
        info(f'Defining class {self.name}')

        generics = {}
        for generic_name, generic_type in zip(self.generic_names, generic_types):
            generics[generic_name] = generic_type
            info(f'Added generic type {generic_name} = {str(generic_type)}')
        
        info(f'Generics = {generics}')

        typ = scope.type_map.get(self.name)
        if self.generic_names:
            generics_display_str = ', '.join(str(t) for t in generics.values())
            cls_display_str = f'{self.name}<{generics_display_str}>'
            cls_type: Type
            if self.name == 'array':
                cls_display_str = f'{generics_display_str}[]'

                cls_type = ArrayType(self.pos, cls_display_str, generics['T'])
            # elif self.name == 'string':
            #     cls_type = PrimitiveType(self.pos, 'string')
            else:
                cls_type = ClassType(self.pos, cls_display_str, list(generics.values()))

            debug(f'Created generic class type {cls_type} (Type = {cls_type.codegen(scope)})')
            if scope.type_map.has(str(cls_type)):
                info('Generic class already defined')
                return Class(self.pos, cls_type, self.name, self.members, self.generic_names,
                             self.is_internal)
            
            scope.type_map.add(cls_type)
        else:
            cls_type = typ

        members: list[Node] = []
        for member in self.members:
            if isinstance(member, Function):
                # add class generic types here because the method could override them
                # for generic_name in generics:
                #     scope.type_map.add(PrimitiveType(self.pos, generic_name))

                # copy the member so we're not modifying the original
                members.append(self.define_method(member, scope, cls_type, typ, **generics))

                # for generic_name in generics:
                #     scope.type_map.remove(generic_name)
            else:
                raise NotImplementedError(f'Class {self.name} does not support member {member}')
        
        return Class(self.pos, cls_type, self.name, members, self.generic_names, self.is_internal)

@dataclass(unsafe_hash=True)
class Elseif(Node):
    cond: Node
    body: Body

    def codegen(self, scope):
        return f""" else if ({self.cond.codegen(scope)}) {{
{self.body.codegen(scope)}
}}"""
    
    def analyse(self, scope):
        body_scope = scope.make_child()
        return Elseif(self.pos, self.type, self.cond.analyse(scope), self.body.analyse(body_scope))

@dataclass(unsafe_hash=True)
class If(Node):
    cond: Node
    body: Body
    else_body: Body | None = field(default=None)
    elseifs: list[Elseif] = field(default_factory=list)

    def codegen(self, scope):
        cond, body = self.cond.codegen(scope), self.body.codegen(scope)
        else_body = f' else {{\n{self.else_body.codegen(scope)}\n}}'\
            if self.else_body is not None else ''
        elseifs = ''.join(elseif.codegen(scope) for elseif in self.elseifs)
        return f"""if ({cond}) {{
{body}
}}{elseifs}{else_body}
"""
    
    def analyse(self, scope):
        cond = self.cond.analyse(scope)
        if cond.type != scope.type_map.get('bool'):
            self.pos.comptime_error(scope, 'condition must be a boolean')
        
        body_scope = scope.make_child()
        else_scope = scope.make_child()
        return If(
            self.pos, self.type, cond, self.body.analyse(body_scope),
            self.else_body.analyse(else_scope) if self.else_body is not None else None,
            [elseif.analyse(scope) for elseif in self.elseifs]
        )

@dataclass(unsafe_hash=True)
class While(Node):
    cond: Node
    body: Body

    def codegen(self, scope):
        return f"""while ({self.cond.codegen(scope)}) {{
{self.body.codegen(scope)}
}}"""
    
    def analyse(self, scope):
        cond = self.cond.analyse(scope)
        if cond.type != scope.type_map.get('bool'):
            self.pos.comptime_error(scope, 'condition must be a boolean')
        
        body_scope = scope.make_child()
        body_scope.in_loop = True
        return While(self.pos, self.type.analyse(scope), cond, self.body.analyse(body_scope))

@dataclass(unsafe_hash=True)
class Break(Node):
    def codegen(self, _):
        return 'break'
    
    def analyse(self, scope):
        if not scope.in_loop:
            self.pos.comptime_error(scope, 'break can only be used inside a loop')
        
        return self

@dataclass(unsafe_hash=True)
class Continue(Node):
    def codegen(self, _):
        return 'continue'
    
    def analyse(self, scope):
        if not scope.in_loop:
            self.pos.comptime_error(scope, 'continue can only be used inside a loop')
        
        return self

@dataclass(unsafe_hash=True)
class Use(Node):
    path: str

    def codegen(self, _):
        return f'// use {self.path}'
    
    def analyse(self, scope):
        scope.use(self.pos, self.path)
        return self

@dataclass(unsafe_hash=True)
class Int(Node):
    value: int

    def codegen(self, _):
        return str(self.value)
    
    def analyse(self, scope):
        return Int(self.pos, self.type.analyse(scope), self.value)

@dataclass(unsafe_hash=True)
class Float(Node):
    value: float

    def codegen(self, _):
        return f'{self.value}f'
    
    def analyse(self, scope):
        return Float(self.pos, self.type.analyse(scope), self.value)

@dataclass(unsafe_hash=True)
class String(Node):
    value: str

    def codegen(self, _):
        return f'string("{self.value}")'
    
    def analyse(self, scope):
        return String(self.pos, self.type.analyse(scope), self.value)

# TODO: add support for String interpolation
@dataclass(unsafe_hash=True)
class FormattedString(Node):
    value: str

    def codegen(self, _):
        return f'string("{self.value}")'
    
    def analyse(self, scope):
        src = ''
        in_bracket = False
        nodes = []
        for char in self.value:
            if char == '{':
                in_bracket = True
            elif char == '}':
                in_bracket = False
                nodes.extend(self.compile(src))
                src = ''
            elif in_bracket:
                src += char
        
        return
    
    def compile(self, src: str):
        with NamedTemporaryFile() as f:
            from cure import parse

            f.write(src.encode('utf-8'))

            scope = Scope(Path(f.name))
            program = parse(scope)
            return program.analyse(scope).nodes

@dataclass(unsafe_hash=True)
class Bool(Node):
    value: bool

    def codegen(self, _):
        return str(self.value).lower()
    
    def analyse(self, scope):
        return Bool(self.pos, self.type.analyse(scope), self.value)

@dataclass(unsafe_hash=True)
class Nil(Node):
    def codegen(self, _):
        return 'nil()'
    
    def analyse(self, scope):
        return Nil(self.pos, self.type.analyse(scope))

@dataclass(unsafe_hash=True)
class Id(Node):
    name: str

    def codegen(self, _):
        return self.name
    
    def analyse(self, scope):
        symbol = scope.symbol_table.get(self.name)
        typ = scope.type_map.get(self.name)
        if symbol is None and typ is None:
            self.pos.comptime_error(scope, f'undefined name \'{self.name}\'')
        
        if typ is not None:
            return Id(self.pos, typ, self.name)
        
        return Id(self.pos, symbol.type, symbol.name)

@dataclass(unsafe_hash=True)
class Call(Node):
    callee: Id
    args: list[Arg] = field(default_factory=list)

    def codegen(self, scope):
        args_str = ', '.join(arg.codegen(scope) for arg in self.args)
        return f'{self.callee.codegen(scope)}({args_str})'
    
    def analyse(self, scope):
        self.callee.analyse(scope)

        # don't need to check if the symbol exists, already done in Id.analyse
        symbol = cast(Symbol, scope.symbol_table.get(self.callee.name))
        func = symbol.value
        if not isinstance(func, Function) and not isinstance(func.type, FunctionType):
            self.pos.comptime_error(scope, f'invalid function \'{self.callee.name}\'')

        args = [arg.analyse(scope) for arg in self.args]
        arg_types = [arg.type for arg in args]
        if isinstance(func.type, FunctionType):
            info(f'Calling function type {func.type}')

            if not self.check_params(func.type.param_types, arg_types):
                arg_types_str = ', '.join(str(t) for t in arg_types)
                self.pos.comptime_error(
                    scope, f'cannot call function type with argument types {arg_types_str}'
                )
            
            return Call(self.pos, func.type.return_type, self.callee, args)

        info(f'Calling function {symbol.name} with {len(args)} arguments')

        functions = [func] + func.overloads
        functions_str = ', '.join(
            '(' + ', '.join(str(param.type) for param in func.params) + ')'
            for func in functions
        )
        debug(f'Possible function signatures = [{functions_str}]')

        call_func = None
        for func in functions:
            func_args = self.build_args(args, func.params)
            if func_args is None:
                continue

            are_params_valid = self.check_params(
                [param.type for param in func.params], [arg.type for arg in func_args],
                func.generic_names
            )
            if not are_params_valid:
                continue
            
            if call_func is not None:
                self.pos.comptime_error(
                    scope, 'ambiguous function call (multiple overloads with the same signature)'
                )
            
            call_func = (func, func_args)
        
        if call_func is None:
            arg_types_str = ', '.join(str(t) for t in arg_types)
            error(f"""Arg Type Display = {', '.join(str(t) for t in arg_types)}
Arg C++ Type = {', '.join(t.codegen(scope) for t in arg_types)}
Arg Object Type = {', '.join(t.object_type(scope) for t in arg_types)}""")
            return self.pos.comptime_error(scope, f'no matching overload with types [{arg_types_str}]')
        
        call_func, args = call_func
        for arg, param in zip(args, call_func.params):
            if isinstance(param.type, ReferenceType) and not isinstance(arg, Id):
                arg.pos.comptime_error(scope, 'cannot pass values to reference types')
        
        debug(f'Found valid callable function {call_func.name}')
        return Call(
            self.pos, call_func.ret_type,
            Id(self.pos, call_func.type, call_func.name),
            args
        )
    
    def index_param_name(self, params: list[Param], name: str):
        for i, param in enumerate(params):
            if param.name == name:
                return i
    
    def build_args(self, args: list[Arg], params: list[Param]):
        # no ideas why these two if statements break everything if you remove them
        if len(params) == 0 and len(args) > 0:
            return None
        elif len(params) == 0:
            return args

        debug(f'Building arguments with {len(params)} parameters')
        new_args: list[Arg | None] = [None] * len(params)
        for i, arg in enumerate(args):
            if arg.label is not None:
                debug(f'Argument {i} has label \'{arg.label}\'')
                param_index = self.index_param_name(params, arg.label)
                if param_index is None:
                    return None
                
                debug(f'Found parameter at index {param_index}')
                new_args[param_index] = arg
            else:
                debug(f'Argument {i} has no label, assuming positional argument')
                try:
                    new_args[i] = arg
                except IndexError:
                    debug(f'Argument {i} is out of range')
                    return None
        
        for i, param in enumerate(params):
            if new_args[i] is not None:
                continue
            
            if param.default is None:
                return None # missing non-optional parameter

            debug(f'Parameter {i} has no argument, using default value')
            new_args[i] = Arg(self.pos, param.type, param.default)
        
        if any(arg is None for arg in new_args):
            return None
        
        return new_args
    
    def check_params(self, param_types: list[Type], arg_types: list[Type],
                     generic_names: list[str] | None = None):
        if generic_names is None:
            generic_names = []
        
        for param_type, arg_type in zip(param_types, arg_types):
            if param_type == arg_type or param_type.type == 'any' or param_type.type in generic_names:
                continue

            debug(f"""Type mismatch with Param Type {param_type} and Arg Type {arg_type}
Param Type = {param_type!r}
Arg Type = {arg_type!r}""")
            return False
        
        return True

@dataclass(unsafe_hash=True)
class Cast(Node):
    object: Node

    def codegen(self, scope):
        return f'static_cast<{self.type.object_type(scope)}>({self.object.codegen(scope)})'
    
    def analyse(self, scope):
        object = self.object.analyse(scope)
        if object.type == self.type:
            return object
        
        callee = f'{object.type.object_type(scope)}_to_{self.type.object_type(scope)}'
        symbol = scope.symbol_table.get(callee)

        debug(f"""Analysing Cast node
Type Display = {object.type}
C++ Type = {object.type.codegen(scope)}
Object Type = {object.type.object_type(scope)}
Callee = {callee}
Callee Symbol = {symbol}""")
        if symbol is None:
            self.pos.comptime_error(
                scope, f'cannot cast type \'{object.type}\' to type \'{self.type}\''
            )
        
        return Call(
            self.pos, self.type, Id(self.pos, scope.type_map.get('function'), callee),
            [Arg(object.pos, object.type, object)]
        ).analyse(scope)

@dataclass(unsafe_hash=True)
class Operation(Node):
    op: str
    left: Node
    right: Node | None

    def codegen(self, scope):
        left = self.left.codegen(scope)
        if self.right is None:
            return f'{self.op}{left}'
        
        right = self.right.codegen(scope)
        return f'{left} {self.op} {right}'
    
    def analyse(self, scope):
        left = self.left.analyse(scope)
        op_name = op_map[self.op]

        debug(f"""Analysing Operation node
Left Type Display = {left.type}
Left C++ Type = {left.type.codegen(scope)}
Left Object Type = {left.type.object_type(scope)}""")
        if self.right is None:
            right = None
            callee = f'{op_name}_{left.type.object_type(scope)}'
            error_message = f'cannot perform operation \'{self.op}\' on type \'{left.type}\''
            args = [Arg(left.pos, left.type, left)]
        else:
            right = self.right.analyse(scope)
            debug(f"""Right Type Display = {right.type}
Right C++ Type = {right.type.codegen(scope)}
Right Object Type = {right.type.object_type(scope)}
""")
            
            callee = f'{left.type.object_type(scope)}_{op_name}_{right.type.object_type(scope)}'
            error_message = f'cannot perform operation \'{self.op}\' on type \'{left.type}\' and '\
                f'\'{right.type}\''
            args = [Arg(left.pos, left.type, left), Arg(right.pos, right.type, right)]
        
        symbol = scope.symbol_table.get(callee)
        debug(f"""Callee = {callee}
Callee Symbol = {symbol}""")
        if symbol is None:
            self.pos.comptime_error(scope, error_message)
        
        func = symbol.value
        if not isinstance(func, Function):
            self.pos.comptime_error(scope, f'invalid function \'{callee}\'')
        
        if func.flags.internal:
            return Operation(self.pos, func.ret_type, self.op, left, right)
        
        return Call(
            self.pos, self.type, Id(self.pos, scope.type_map.get('function'), callee), args
        ).analyse(scope)

@dataclass(unsafe_hash=True)
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
            self.pos.comptime_error(scope, 'condition must be a boolean')
        
        if true.type != false.type:
            self.pos.comptime_error(scope, 'both branches must be the same type')

        return Ternary(self.pos, self.type.analyse(scope), cond, true, false)

@dataclass(unsafe_hash=True)
class Bracketed(Node):
    value: Node

    def codegen(self, scope):
        return f'({self.value.codegen(scope)})'
    
    def analyse(self, scope):
        value = self.value.analyse(scope)
        return Bracketed(self.pos, value.type, value)

@dataclass(unsafe_hash=True)
class Attribute(Node):
    object: Node
    attr: str
    args: list[Node] | None = None

    def codegen(self, scope):
        object = self.object.codegen(scope)
        if self.args is None:
            return f'{object}.{self.attr}'
        
        args_str = ', '.join(arg.codegen(scope) for arg in self.args)
        return f'{object}.{self.attr}({args_str})'
    
    def analyse(self, scope):
        object = self.object.analyse(scope)
        args = [Arg(object.pos, object.type, object)] + (
            [arg.analyse(scope) for arg in self.args]
            if self.args else []
        )
        callee = f'{object.type.object_type(scope)}_{self.attr}'
        symbol = scope.symbol_table.get(callee)

        debug(f"""Analysing Attribute node
Type Display = {object.type}
C++ Type = {object.type.codegen(scope)}
Object Type = {object.type.object_type(scope)}
Attr = {self.attr}
Callee = {callee}
Symbol = {symbol}""")
        if symbol is None:
            self.pos.comptime_error(
                scope, f'unknown attribute \'{self.attr}\' on type \'{object.type}\''
            )
        
        func = symbol.value
        if not isinstance(func, Function):
            self.pos.comptime_error(scope, f'attribute \'{self.attr}\' is not a function')
        
        if func.flags.static or func.flags.internal:
            args = args[1:]
        
        # is_call_a_property = self.args is None
        # if is_call_a_property and func.flags.method:
        #     self.pos.comptime_error(scope, f'\'{self.attr}\' is a method, not a property')
        # elif not is_call_a_property and func.flags.property:
        #     self.pos.comptime_error(scope, f'\'{self.attr}\' is a property, not a method')
        
        res = Call(
            self.pos, self.type, Id(self.pos, scope.type_map.get('function'), callee), args
        ).analyse(scope)

        if not func.flags.internal:
            return res
        
        if self.attr == 'new':
            return New(self.pos, res.type, res.type, args)
        
        attr = Attribute(self.pos, res.type, object, self.attr, args)
        if res.type == scope.type_map.get('nil'):
            return attr
        
        # because they're internal, there's a chance that they could not return the right type
        # e.g. string length in C++ returns size_type but should return an int
        return Cast(self.pos, res.type, attr)

@dataclass(unsafe_hash=True)
class New(Node):
    new_type: Type
    args: list[Node] = field(default_factory=list)

    def codegen(self, scope):
        args_str = ', '.join(arg.codegen(scope) for arg in self.args)
        return f'{self.new_type.codegen(scope)}{{{args_str}}}'

    def analyse(self, scope):
        new_type = self.new_type.analyse(scope)
        return Attribute(
            self.pos, new_type, Id(self.pos, new_type, str(new_type)), 'new', self.args
        ).analyse(scope)

@dataclass(unsafe_hash=True)
class NewArray(Node):
    element_type: Type
    size: Node | None = None

    def codegen(self, scope):
        return f'array<{self.element_type.codegen(scope)}>()'
    
    def analyse(self, scope):
        typ = self.element_type.analyse(scope)
        array_cls = scope.define_class(self.pos, 'array', [typ])
        return NewArray(self.pos, array_cls.type, typ, self.size)

@dataclass(unsafe_hash=True)
class ArrayInit(Node):
    elements: list[Node] = field(default_factory=list)

    def codegen(self, scope):
        elements_str = ', '.join(element.codegen(scope) for element in self.elements)
        return f'array<{self.elements[0].type.codegen(scope)}>{{{elements_str}}}'
    
    def analyse(self, scope):
        if len(self.elements) == 0:
            self.pos.comptime_error(scope, 'cannot initialize empty array')
        
        elements = [element.analyse(scope) for element in self.elements]
        elem_type = elements[0].type
        for elem in elements[1:]:
            if elem.type == elem_type:
                continue

            self.pos.comptime_error(scope, 'array initialization type mismatch')
        
        array_cls = scope.define_class(self.pos, 'array', [elem_type])
        return ArrayInit(self.pos, array_cls.type, elements)

@dataclass(unsafe_hash=True)
class ForRange(Node):
    name: str
    start: Node
    end: Node
    body: Body

    def codegen(self, scope):
        start = self.start.codegen(scope)
        end = self.end.codegen(scope)
        body = self.body.codegen(scope)
        return f"""for (auto {self.name} = {start}; {self.name} < {end}; {self.name}++) {{
{body}
}}"""
    
    def analyse(self, scope):
        start = self.start.analyse(scope)
        end = self.end.analyse(scope)
        name = self.name

        if start.type != end.type:
            self.pos.comptime_error(scope, 'range type mismatch')
        
        if start.type not in (scope.type_map.get('int'), scope.type_map.get('float')):
            self.pos.comptime_error(scope, f'invalid start type for range loop \'{start.type}\'')
        
        if end.type not in (scope.type_map.get('int'), scope.type_map.get('float')):
            self.pos.comptime_error(scope, f'invalid end type for range loop \'{end.type}\'')
        
        if scope.symbol_table.has(name):
            self.pos.comptime_error(scope, f'\'{name}\' is already defined')
        
        body_scope = scope.make_child()
        body_scope.symbol_table.add(Symbol(name, start.type, self))
        body_scope.in_loop = True

        body = self.body.analyse(body_scope)
        return ForRange(self.pos, self.type, name, start, end, body)
