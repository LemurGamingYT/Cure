from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Any
from logging import info, debug

from llvmlite import ir as lir

from cure.codegen_utils import create_string_constant
from cure.c_registry import CRegistry
from cure import ir


def run_function(
    pos: ir.Position, builder: lir.IRBuilder, module: lir.Module,
    scope: ir.Scope, name: str, args: list['CallArgument'] | None = None
):
    if args is None:
        args = []
    
    symbol = scope.symbol_table.get(name)
    if symbol is None:
        return pos.comptime_error(f'no function named {name}', scope.src)
    
    func = symbol.value
    if not isinstance(func, ir.Function):
        return pos.comptime_error(f'invalid callable {name}', scope.src)
    
    assert all(isinstance(arg, CallArgument) for arg in args)
    return func(pos, scope, args, module, builder)


def function(self: Any, params: list[ir.Param] | None = None, ret_type: ir.Type | None = None,
             flags: ir.FunctionFlags | None = None, name: str | None = None):
    if params is None:
        params = []
    
    if ret_type is None:
        ret_type = ir.TypeManager.get('nil')
    
    if flags is None:
        flags = ir.FunctionFlags()
    
    def decorator(func):
        nonlocal name

        name = name or func.__name__
        func.function = True
        func.name = name
        func.params = params
        func.ret_type = ret_type
        func.flags = flags
        func.overloads = []

        if self is not None:
            setattr(self, name, func)
            debug(f'Added {name} to {self}')
        
        return func
    
    return decorator

def overload(overload_of: Callable, params: list[ir.Param] | None = None,
             ret_type: ir.Type | None = None, name: str | None = None):
    if params is None:
        params = []
    
    if ret_type is None:
        ret_type = ir.TypeManager.get('nil')
    
    def decorator(func):
        nonlocal name
        
        name = name or func.__name__

        func.function = True
        func.name = name
        func.params = params
        func.ret_type = ret_type
        func.flags = overload_of.flags
        func.overload_of = overload_of

        return func
    
    return decorator

def getattrs(instance):
    attrs = {}
    for k in dir(instance):
        v = getattr(instance, k)
        if k.startswith('_') or not callable(v) or not getattr(v, 'function', False):
            continue

        attrs[k] = v
    
    return attrs

def add_instance(self, instance):
    attrs = list(getattrs(instance).values())
    debug(f'Adding {attrs} (from instance {instance}) to {self}')

    for v in getattrs(instance).values():
        if isinstance(self, Class):
            name = f'{self.type}_{v.name}'
        else:
            name = v.name
        
        if (overload_of := getattr(v, 'overload_of', None)) is not None:
            overload_of.overloads.append(ir.Function(
                ir.Position.zero(), name, v.params, v.ret_type, v, v.flags
            ))
        else:
            self.scope.symbol_table.add(ir.Symbol(name, ir.TypeManager.get('function'), ir.Function(
                ir.Position.zero(), name, v.params, v.ret_type, v, v.flags, v.overloads
            )))

        info(f'Added {name} from {self._name}')


# TODO: maybe combine ParamPointer and CallArgument?
@dataclass
class ParamPointer:
    value: lir.Value
    type: ir.Type

# TODO: I don't like this ;-;
@dataclass
class CallArgument:
    value: lir.Value
    type: ir.Type

@dataclass
class DefinitionContext:
    pos: ir.Position
    scope: ir.Scope
    module: lir.Module
    builder: lir.IRBuilder
    c_registry: CRegistry
    params: list[ir.Param]
    ret_type: ir.Type

    def param(self, name: str) -> ParamPointer:
        for param in self.params:
            if param.name != name:
                continue

            symbol = self.scope.symbol_table.get(name)
            if symbol is None:
                return self.pos.comptime_error(f'invalid param {name}', self.scope.src)
            
            value = symbol.value
            if isinstance(symbol.value, lir.PointerType):
                value = self.builder.load(value, symbol.name)
            
            return ParamPointer(value, symbol.type)

        return self.pos.comptime_error(f'unknown param {name}', self.scope.src)
    
    def param_value(self, name: str) -> lir.Value:
        return self.param(name).value
    
    def call(self, name: str, args: list[CallArgument] | None = None):
        return run_function(self.pos, self.builder, self.module, self.scope, name, args)
    
    def error(self, message: str):
        err_msg = create_string_constant(self.module, message)
        err_string_struct = self.call('string_new', [
            CallArgument(err_msg, ir.TypeManager.get('pointer')),
            CallArgument(lir.Constant(lir.IntType(32), len(message)), ir.TypeManager.get('int'))
        ])

        self.call('error', [CallArgument(err_string_struct, ir.TypeManager.get('string'))])
        self.builder.unreachable()

class Lib(ABC):
    def __init__(self, scope: ir.Scope):
        self.scope = scope
        self._name = type(self).__name__

        self.init_lib()
        add_instance(self, self)
    
    def init_lib(self):
        pass

    def add_lib(self, cls: type['Lib']):
        instance = cls(self.scope)
        add_instance(self, instance)

        info(f'merged {self._name} and {instance._name} (Lib)')
    
    def add_class(self, cls: type['Class']):
        instance = cls(self.scope)
        add_instance(self, instance)

        info(f'merged {self._name} and {instance._name} (Class)')

@dataclass
class ClassField:
    name: str
    type: ir.Type

class Class(ABC):
    @abstractmethod
    def fields(self) -> list[ClassField]:
        ...

    def __init__(self, scope: ir.Scope, *generic_types: ir.Type):
        self.generic_types = generic_types
        self.scope = scope

        self._class_name = type(self).__name__
        if not hasattr(self, '_name'):
            self._name = self._class_name + ''.join(f'_{type}' for type in generic_types)

        if not ir.TypeManager.exists(self._name):
            ir.TypeManager.add(self._name, self._create_struct())
        
        if not hasattr(self, 'type'):
            self.type = ir.TypeManager.get(self._name)

        self.init_class()
        add_instance(self, self)
    
    def _create_struct(self):
        struct_type = lir.global_context.get_identified_type(self._name)
        if struct_type.is_opaque:
            struct_type.set_body(*[field.type.type for field in self.fields()])
        
        return struct_type
    
    def init_class(self):
        ...
