from dataclasses import dataclass, field
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
    dependencies: list[Path] = field(default_factory=list)
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
            self.dependencies.append(header.relative_to(STDLIB_PATH))
        
        for cfile in stdlib_path.glob('*.cpp'):
            debug(f'Found source file {cfile}')
            self.dependencies.append(cfile)
        
        for cure in stdlib_path.glob('*.cure'):
            debug(f'Found cure file {cure}')
            self.use_local(cure)
    
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
            
            self.dependencies.append(header_file)
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


@dataclass
class Node(ABC):
    pos: Position = field(compare=False, repr=False, hash=False)
    type: 'Type'

    @abstractmethod
    def codegen(self, scope: Scope) -> str:
        ...
    
    def analyse(self, scope: Scope) -> 'Node':
        return self

@dataclass
class Program(Node):
    nodes: list[Node] = field(default_factory=list)

    def codegen(self, scope):
        code = '\n'.join(node.codegen(scope) for node in self.nodes)
        includes = '\n'.join(
            f'#include "{path.as_posix()}"' for path in scope.dependencies
            if path.suffix == '.hpp'
        )

        return f"""{includes}

{code}
"""
    
    def analyse(self, scope):
        return Program(self.pos, self.type.analyse(scope), [node.analyse(scope) for node in self.nodes])

@dataclass
class Type(Node):
    type: str # type: ignore

    def __str__(self):
        return self.type

    def codegen(self, _):
        return self.type

    def analyse(self, scope: Scope):
        typ = scope.type_map.get(self.type)
        if typ is None:
            self.pos.comptime_error(scope, f'unknown type \'{self.type}\'')
        
        return typ

@dataclass
class PrimitiveType(Type):
    pass

@dataclass
class ArrayType(Type):
    element_type: Type

    def codegen(self, scope):
        return f'array<{self.element_type.codegen(scope)}>'
    
    def analyse(self, scope):
        elem_type = self.element_type.analyse(scope)
        array_cls = scope.define_class(self.pos, 'array', [elem_type])
        return array_cls.type

@dataclass
class ClassType(Type):
    generic_types: list[Type] = field(default_factory=list)

    def codegen(self, scope):
        if self.generic_types:
            generic_types_str = ', '.join(typ.codegen(scope) for typ in self.generic_types)
            return f'{self.type}<{generic_types_str}>'
    
        return self.type
    
    def analyse(self, scope):
        return ClassType(self.pos, self.type, [typ.analyse(scope) for typ in self.generic_types])

@dataclass
class ReferenceType(Type):
    type: str # type: ignore
    inner: Type

    def __eq__(self, other):
        if not isinstance(other, Type):
            return False
        
        return self.inner == other

    def codegen(self, scope):
        return f'{self.inner.codegen(scope)}&'
    
    def analyse(self, scope):
        return ReferenceType(
            self.pos, self.type if self.type.endswith('&') else f'{self.type}&',
            self.inner.analyse(scope)
        )

@dataclass
class Param(Node):
    name: str
    is_mutable: bool = False
    default: Node | None = None

    def codegen(self, scope):
        if self.default is not None:
            return f'{self.type.codegen(scope)} {self.name} = {self.default.codegen(scope)}'
        
        return f'{self.type.codegen(scope)} {self.name}'
    
    def analyse(self, scope):
        return Param(
            self.pos, self.type.analyse(scope), self.name, self.is_mutable,
            self.default.analyse(scope) if self.default is not None else None
        )

@dataclass
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

@dataclass
class Return(Node):
    value: Node

    def codegen(self, scope):
        return f'return {self.value.codegen(scope)}'
    
    def analyse(self, scope):
        value = self.value.analyse(scope)
        return Return(self.pos, value.type, value)

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
    ret_type: Type
    params: list[Param] = field(default_factory=list)
    body: Body | None = field(default=None)
    overloads: list['Function'] = field(default_factory=list)
    flags: FunctionFlags = field(default_factory=FunctionFlags)
    generic_names: list[str] = field(default_factory=list)
    extend_type: Type | None = None

    def codegen(self, scope):
        params_str = ', '.join(param.codegen(scope) for param in self.params) if len(self.params) > 0\
            else 'void'
        signature = f'{self.ret_type.codegen(scope)} {self.name}({params_str})'
        if self.body is None:
            return ''

        return f"""{signature} {{
{self.body.codegen(scope)}
}}"""
    
    def analyse(self, scope):
        extend_type = self.extend_type.analyse(scope) if self.extend_type is not None else None
        name = self.name
        if extend_type is not None:
            name = f'{extend_type.codegen(scope)}_{name}'

            debug(f'Function {self.name} extends type {extend_type}, mangled name = {name}')
        
        _name = name
        if name in RESERVED_CPP_KEYWORDS:
            name = f'_{name}'
        
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
            scope.symbol_table.add(Symbol(func.name, func.type, func), _name)
        
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
    
    
    def __call__(self, pos: Position, scope: Scope, args: list[Node]):
        info(f'Calling function {self.name} with {len(args)} arguments')

        functions = [cast(Function, self)] + self.overloads
        functions_str = ', '.join(func.name for func in functions)
        debug(f'Possible functions = [{functions_str}]')

        call_func = None
        for func in functions:
            if len(func.params) != len(args):
                continue

            valid_params = True
            for param, arg in zip(func.params, args):
                info(f'Checking Param Type {param.type} and Arg Type {arg.type}')
                if param.type == arg.type or param.type.type in func.generic_names or\
                        param.type.type == 'any':
                    continue

                debug(f"""Type mismatch with Param Type {param.type} and Arg Type {arg.type}
Param Type Display = {str(param.type)}
Param C++ Type = {param.type.codegen(scope)}
Param Type = {param.type!r}
Arg Type Display = {str(arg.type)}
Arg C++ Type = {arg.type.codegen(scope)}
Arg Type = {arg.type!r}""")
                valid_params = False
                break
            
            if not valid_params:
                continue
            
            call_func = func
            break

            # TODO: handle ambiguous function calls
            # if call_func is not None:
            #     self.pos.comptime_error(
            #         scope, 'ambiguous function call (multiple overloads with the same signature)'
            #     )
        
        if call_func is None:
            arg_types_str = ', '.join(str(arg.type) for arg in args)
            error(f"""no matching overloads with types [{arg_types_str}]
Self Param Type Display = {', '.join(str(param.type) for param in self.params)}
Self Param C++ Type = {', '.join(param.type.codegen(scope) for param in self.params)}
Arg Type Display = {', '.join(str(arg.type) for arg in args)}
Arg C++ Type = {', '.join(arg.type.codegen(scope) for arg in args)}""")
            return pos.comptime_error(scope, f'no matching overload with types [{arg_types_str}]')
        
        for arg, param in zip(args, call_func.params):
            if isinstance(param.type, ReferenceType) and not isinstance(arg, Id):
                arg.pos.comptime_error(scope, 'cannot pass values to reference types')
        
        debug(f'Found valid callable function {call_func.name}')
        return Call(
            pos, call_func.ret_type,
            Id(pos, call_func.type, call_func.name),
            args
        )

@dataclass
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
            name = f'_{name}'

        value = self.value.analyse(scope)
        if scope.symbol_table.has(self.name):
            return Assignment(self.pos, value.type, self.name, value, self.op).analyse(scope)

        scope.symbol_table.add(Symbol(name, value.type, value, self.is_mutable), self.name)
        return Variable(self.pos, value.type, name, value, self.is_mutable, self.op)

@dataclass
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

@dataclass
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
    
    def replace_type(self, typ: Type, **generics: Type):
        if typ.type not in generics:
            return typ
        
        info(f'Replacing return type with generic type {generics[typ.type]}')
        return generics[typ.type]
    
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
        
        ret_type = self.replace_type(member.ret_type, **generics)
        params.extend(Param(
            self.pos, self.replace_type(param.type, **generics), param.name, param.is_mutable
        ) for param in member.params)

        name = f'{cls_type}_{member.name}'
        debug(f'Creating method with name {name}')
        method = Function(
            self.pos, member.type, name, ret_type, params, member.body,
            member.overloads, # TODO: method overloads
            flags, member.generic_names
        )

        method.analyse(scope)

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
            # TODO: check if this generic class has already been defined
            # if scope.type_map.has(str(cls_type)):
            #     info('Generic class already defined')
            #     return Class(self.pos, cls_type, self.name, self.members, self.generic_names,
            #                  self.is_internal)
            
            scope.type_map.add(cls_type)
        else:
            cls_type = typ

        members: list[Node] = []
        for member in self.members:
            if isinstance(member, Function):
                # copy the member so we're not modifying the original
                members.append(self.define_method(member, scope, cls_type, typ, **generics))
            else:
                raise NotImplementedError(f'Class {self.name} does not support member {member}')
        
        return Class(self.pos, cls_type, self.name, members, self.generic_names, self.is_internal)

@dataclass
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

@dataclass
class If(Node):
    cond: Node
    body: Body
    else_body: Body | None = field(default=None)
    elseifs: list[Elseif] = field(default_factory=list)

    def codegen(self, scope):
        cond, body = self.cond.codegen(scope), self.body.codegen(scope)
        else_body = f' else {self.else_body.codegen(scope)}' if self.else_body is not None else ''
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

@dataclass
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

@dataclass
class Break(Node):
    def codegen(self, _):
        return 'break'
    
    def analyse(self, scope):
        if not scope.in_loop:
            self.pos.comptime_error(scope, 'break can only be used inside a loop')
        
        return self

@dataclass
class Continue(Node):
    def codegen(self, _):
        return 'continue'
    
    def analyse(self, scope):
        if not scope.in_loop:
            self.pos.comptime_error(scope, 'continue can only be used inside a loop')
        
        return self

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

@dataclass
class Float(Node):
    value: float

    def codegen(self, _):
        return f'{self.value}f'

@dataclass
class String(Node):
    value: str

    def codegen(self, _):
        return f'string("{self.value}")'

# TODO: add support for String interpolation
@dataclass
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

@dataclass
class Bool(Node):
    value: bool

    def codegen(self, _):
        return str(self.value).lower()

@dataclass
class Nil(Node):
    def codegen(self, _):
        return 'nil()'

@dataclass
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

@dataclass
class Call(Node):
    callee: Id
    args: list[Node] = field(default_factory=list)

    def codegen(self, scope):
        args_str = ', '.join(arg.codegen(scope) for arg in self.args)
        return f'{self.callee.codegen(scope)}({args_str})'
    
    def analyse(self, scope):
        self.callee.analyse(scope)

        # don't need to check if the symbol exists, already done in Id.analyse
        symbol = cast(Symbol, scope.symbol_table.get(self.callee.name))
        func = symbol.value
        if not isinstance(func, Function):
            self.pos.comptime_error(scope, f'invalid function \'{self.callee.name}\'')

        args = [arg.analyse(scope) for arg in self.args]
        return func(self.pos, scope, args)

@dataclass
class Cast(Node):
    object: Node

    def codegen(self, scope):
        return f'static_cast<{self.type.codegen(scope)}>({self.object.codegen(scope)})'
    
    def analyse(self, scope):
        object = self.object.analyse(scope)
        if object.type == self.type:
            return object
        
        callee = f'{object.type}_to_{self.type}'
        symbol = scope.symbol_table.get(callee)

        debug(f"""Analysing Cast node
Object Type Display = {object.type}
Object C++ Type = {object.type.codegen(scope)}
Callee = {callee}
Callee Symbol = {symbol}""")
        if symbol is None:
            self.pos.comptime_error(
                scope, f'cannot cast type \'{object.type}\' to type \'{self.type}\''
            )
        
        return Call(
            self.pos, self.type, Id(self.pos, scope.type_map.get('function'), callee),
            [object]
        ).analyse(scope)

@dataclass
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
Left C++ Type = {left.type.codegen(scope)}""")
        if self.right is None:
            callee = f'{op_name}_{left.type}'
            error_message = f'cannot perform operation \'{self.op}\' on type \'{left.type}\''
            args = [left]
        else:
            right = self.right.analyse(scope)
            debug(f"""Right Type Display = {right.type}
Right Object Type = {right.type.codegen(scope)}
""")
            
            callee = f'{left.type}_{op_name}_{right.type}'
            error_message = f'cannot perform operation \'{self.op}\' on type \'{left.type}\' and '\
                f'\'{right.type}\''
            args = [left, right]
        
        symbol = scope.symbol_table.get(callee)
        debug(f"""Callee = {callee}
Callee Symbol = {symbol}""")
        if symbol is None:
            self.pos.comptime_error(scope, error_message)
        
        return Call(
            self.pos, self.type, Id(self.pos, scope.type_map.get('function'), callee), args
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
            self.pos.comptime_error(scope, 'condition must be a boolean')
        
        if true.type != false.type:
            self.pos.comptime_error(scope, 'both branches must be the same type')

        return Ternary(self.pos, self.type.analyse(scope), cond, true, false)

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
        object = self.object.codegen(scope)
        if self.args is None:
            return f'{object}.{self.attr}'
        
        args_str = ', '.join(arg.codegen(scope) for arg in self.args)
        return f'{object}.{self.attr}({args_str})'
    
    def analyse(self, scope):
        object = self.object.analyse(scope)
        args = [object] + ([arg.analyse(scope) for arg in self.args] if self.args else [])
        callee = f'{object.type}_{self.attr}'
        symbol = scope.symbol_table.get(callee)

        debug(f"""Analysing Attribute node
Object Type Display = {object.type}
Object C++ Type = {object.type.codegen(scope)}
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

@dataclass
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

@dataclass
class NewArray(Node):
    element_type: Type
    size: Node | None = None

    def codegen(self, scope):
        return f'array<{self.element_type.codegen(scope)}>()'
    
    def analyse(self, scope):
        typ = self.element_type.analyse(scope)
        array_cls = scope.define_class(self.pos, 'array', [typ])
        return NewArray(self.pos, array_cls.type, typ, self.size)

@dataclass
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

@dataclass
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
        
        # TODO: allow more range types
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
