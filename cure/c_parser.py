from logging import debug, warning
from dataclasses import dataclass
from typing import Any, TypeAlias
from pathlib import Path

from cure.ir import Function, FunctionFlags, Param, Class, Symbol, Scope, Position


CommentFlags: TypeAlias = dict[str, Any]

@dataclass
class State:
    i: int
    lines: list[str]
    src: str
    scope: Scope

    @property
    def line(self):
        return self.lines[self.i].strip()
    
    def inc(self):
        self.i += 1
    
    def dec(self):
        self.i -= 1


def is_comment(line: str):
    return line.startswith('//') or (line.startswith('/*') and line.endswith('*/'))

def parse_comment_flags(line: str) -> CommentFlags:
    if line.startswith('//'):
        line = line.removeprefix('//')
    elif line.startswith('/*') and line.endswith('*/'):
        line = line.removeprefix('/*').removesuffix('*/')

    line = line.strip()
    if not line.startswith('[') and not line.endswith(']'):
        return {}
    
    splitted = line[1:-1].split(', ')
    flags: dict[str, Any] = {}
    for flag in splitted:
        if '=' not in flag:
            flags[flag] = True
            continue

        k, v = flag.strip().split('=')
        k, v = k.strip(), v.strip()
        flags[k] = v
    
    return flags

def parse_type(type_str: str, state: State):
    is_reference = False
    if type_str.endswith('*'):
        type_str = type_str[:-1]
        is_reference = True
    
    if '#' in type_str:
        type_str = type_str.replace('##', '') # it's a generic type, C generic types use '##'
    
    type = state.scope.type_map.get(type_str)
    if type is None:
        return
    
    if is_reference:
        type = type.as_reference()
    
    return type

def get_name(state: State):
    line = state.line
    if line.startswith('#define'):
        # name(T)\ -> [name, 'T)\'] -> name
        name = line.split()[1].split('(')[0]
        debug(f'Generic function name: {name}')
    else:
        # type name(params) -> name
        name = line.split()[1].split('(')[0]
        debug(f'Function name: {name}')
    
    return name

def get_generic_params(state: State):
    line = state.line
    if not line.startswith('#define'):
        return []
    
    # #define name(T)\ -> name(T)\ -> ['name', 'T)\'] -> T)\ -> ['T', '\'] -> ['T']
    generic_params = line.removeprefix('#define ').split('(')[1].split(')')[0].split(', ')
    debug(f'Generic params: {generic_params}')

    return generic_params

def get_return_type(state: State):
    line = state.line
    splitted = line.split()
    ret_type = parse_type(splitted[0], state)
    if ret_type is None:
        return

    debug(f'Function return type: {ret_type} ({splitted[0]})')
    return ret_type

def get_parameters(state: State):
    line = state.line

    # type name(params) -> params
    params_list = line.strip().split('(')[1].split(')')[0].split(', ')
    if params_list == ['void']:
        params = []
    else:
        params = [
            Param(Position.zero(), parse_type(param.split()[0], state), param.split()[1])
            for param in params_list
        ]
    
    if any(param.type is None for param in params):
        return
    
    debug(f'Function parameters: {params} ({params_list})')
    return params

def add_overload(state: State, overload_of: str | None, func: Function):
    if overload_of is None:
        return False
    
    symbol = state.scope.symbol_table.get(overload_of)
    if symbol is None:
        return False

    overload = symbol.value
    if not isinstance(overload, Function):
        return False

    overload.overloads.append(func)
    return True

def parse_function(state: State, comment_flags: CommentFlags):
    line = state.line
    debug(f'Parsing function line {line}')

    name = get_name(state)
    generic_params = get_generic_params(state)
    if line.startswith('#define'):
        state.inc()
        line = state.line
        debug(f'Parsing generic function line {line}')

    for param in generic_params:
        state.scope.type_map.add(param)
    
    ret_type = get_return_type(state)
    if ret_type is None:
        warning(f'C function {name} will not be added: invalid return type {line.split()[0]}')
        return

    params = get_parameters(state)
    if params is None:
        warning(f'C function {name} will not be added: one or more invalid parameter types')
        return

    for param in generic_params:
        state.scope.type_map.remove(param)
    
    overload_of = comment_flags.pop('overload_of', None)
    
    func_flags = FunctionFlags()
    for k, v in comment_flags.items():
        setattr(func_flags, k, v)
    
    func = Function(
        Position.zero(), ret_type, name, params,
        flags=func_flags, generic_params=generic_params
    )

    if add_overload(state, overload_of, func):
        debug(f'Added overload to {name}: {overload_of}')
    elif overload_of is not None:
        warning(f'no function named {overload_of}, expected as the base function of {name}')

    state.scope.symbol_table.add(Symbol(name, state.scope.type_map.get('function'), func))
    debug(f'Added {name} to scope from C code')
    return func

def parse_method(state: State, comment_flags: CommentFlags, class_name: str,
                 class_generics: list[str] | None = None):
    if class_generics is None:
        class_generics = []

    line = state.line
    debug(f'Parsing method line {line}')

    name = get_name(state).replace('##', '').removeprefix(class_name)
    for param in class_generics:
        state.scope.type_map.add(param)
    
    ret_type = get_return_type(state)
    if ret_type is None:
        warning(f'C function {name} will not be added: invalid return type {line.split()[0]}')
        return

    params = get_parameters(state)
    if params is None:
        warning(f'C function {name} will not be added: one or more invalid parameter types')
        return

    for param in class_generics:
        state.scope.type_map.remove(param)
    
    # TODO: add method overloading
    
    func_flags = FunctionFlags()
    for k, v in comment_flags.items():
        setattr(func_flags, k, v)
    
    func = Function(Position.zero(), ret_type, name, params, flags=func_flags)
    state.scope.symbol_table.add(Symbol(name, state.scope.type_map.get('function'), func))
    debug(f'Added method {name} to scope from C code')
    return func

def parse_class(state: State):
    # TODO: implement normal class parsing (this function only supports C generic classes)
    name = get_name(state)
    generic_params = get_generic_params(state)

    state.inc()

    # display_generic_str = ', '.join(generic_params)
    type_generic_str = ''.join(map(lambda t: f'_{t}', generic_params))
    cls_type = state.scope.type_map.add(f'{name}{type_generic_str}')
    cls = Class(Position.zero(), cls_type, cls_type.display, generic_params=generic_params)

    while not state.line.startswith('}'):
        state.inc()
    
    cls_name = state.line.split()[1].rstrip(';\\')
    state.scope.type_map.add(cls_name.replace('##', ''))

    state.inc()
    while (line := state.line).endswith('\\'):
        line = line[:-1] # get rid of '\'
        if line.startswith('/*'):
            flags = parse_comment_flags(line)
            state.inc()
            func = parse_method(state, flags, cls_name, generic_params)
            if func:
                cls.members.append(func)
                debug(f'Added new method {func.name} to class {cls.name}')

        state.inc()
    
    state.scope.symbol_table.add(Symbol(cls.name, cls_type, cls))
    debug(f'Added class {cls.name} to scope from C code')
    return cls


def parse_symbols(header: Path, scope: Scope):
    src = header.read_text('utf-8')
    state = State(0, src.splitlines(), src, scope)
    while state.i < len(state.lines):
        line = state.line
        if is_comment(line):
            debug(f'Parsing line {line}')

            comment_flags = parse_comment_flags(line)

            state.inc()
            if 'class' not in comment_flags:
                parse_function(state, comment_flags)
            else:
                parse_class(state)
        
        state.inc()
