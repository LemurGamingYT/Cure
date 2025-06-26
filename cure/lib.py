from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import debug, info
from typing import Callable

from llvmlite import ir as lir

from cure.codegen_utils import NULL, store_in_pointer, create_string_constant
from cure.c_registry import CRegistry
from cure import ir


def compile_function(func, module: lir.Module, scope: ir.Scope, arg_types: list[ir.Type]):
    info(f'Compiling {func.name}')

    c_registry = module.c_registry

    if len(arg_types) != len(func.params):
        ir.Position.zero().comptime_error(
            f'unmatched number of args and params in function call to {func.name}',
            scope.src
        )

    generic_types = []
    callee_params = []
    for i, (arg_type, param) in enumerate(zip(arg_types, func.params)):
        if param.type == ir.TypeManager.get('any'):
            callee_params.append(ir.Param(param.pos, param.name, arg_type))
            generic_types.append(arg_type)
        else:
            callee_params.append(ir.Param(param.pos, param.name, param.type))
    
    callee = func.name
    if len(generic_types) > 0:
        callee += ''.join(map(lambda x: f'_{x}', generic_types))
        debug(f'Generic function name: {callee}')
    
    if callee in module.globals:
        debug(f'{callee} is compiled, using it again')
        return module.get_global(callee)
    
    ir_args = [param.type.type for param in callee_params]
    ir_func = lir.Function(module, lir.FunctionType(func.ret_type.type, ir_args), callee)
    builder = lir.IRBuilder(ir_func.append_basic_block())
    def_scope = scope.clone()
    ctx = DefinitionContext(
        ir.Position.zero(), def_scope, module, builder, c_registry, callee_params,
        func.ret_type
    )

    info('Created definition context')

    for i, param in enumerate(callee_params):
        def_scope.symbol_table.add(ir.Symbol(param.name, param.type, store_in_pointer(
            ctx.builder, param.type.type, ir_func.args[i], f'param_{param.name}_ptr'
        )))
    
    info(f'Compiling {callee}')
    result = func(ctx)

    # utility and ease of use if statements
    if result is not None:
        ctx.builder.ret(result)
    elif func.ret_type == ir.TypeManager.get('nil') and not ctx.builder.block.is_terminated:
        ctx.builder.ret(NULL())

    info(f'Compiled {callee}')
    return ir_func

def run_function(
    pos: ir.Position, builder: lir.IRBuilder, module: lir.Module,
    scope: ir.Scope, name: str, args: list[lir.Value] | None = None
):
    if args is None:
        args = []
    
    symbol = scope.symbol_table.get(name)
    if symbol is None:
        return pos.comptime_error(f'no function named {name}', scope.src)
    
    func = symbol.value
    if not isinstance(func, ir.Function):
        return pos.comptime_error(f'invalid callable {name}', scope.src)
    
    return func(pos, scope, args, module, builder)

def py_func_to_ir_func(func):
    pass


def function(params: list[ir.Param] | None = None, ret_type: ir.Type | None = None,
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
        if k.startswith('_'):
            continue

        v = getattr(instance, k)
        if not callable(v):
            continue

        if not getattr(v, 'function', False):
            continue

        attrs[k] = v
    
    return attrs

def add_instance(self, instance):
    for v in getattrs(instance).values():
        if isinstance(self, Class):
            name = f'{self._name}_{v.name}'
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


@dataclass
class ParamPointer:
    value: lir.Value
    ptr: lir.Value
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
            
            return ParamPointer(
                self.builder.load(symbol.value, symbol.name), symbol.value, symbol.type
            )

        return self.pos.comptime_error(f'unknown param {name}', self.scope.src)
    
    def create_function(self, name: str) -> lir.Function | None:
        symbol = self.scope.symbol_table.get(name)
        if symbol is None:
            self.pos.comptime_error(f'no function named {name}', self.scope.src)
            return None
        
        func = symbol.value
        if callable(func):
            arg_types = [param.type for param in func.params]
            return func(self.module, self.scope, arg_types)
        
        return func
    
    def call(self, name: str, args: list[lir.Value] | None = None):
        return run_function(self.pos, self.builder, self.module, self.scope, name, args)
    
    def error(self, message: str):
        err_msg = create_string_constant(self.module, message)
        err_string_struct = self.call('string_new', [
            err_msg, lir.Constant(lir.IntType(32), len(message))
        ])

        self.call('error', [err_string_struct])
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

    def __init__(self, scope: ir.Scope):
        self.scope = scope
        self._name = type(self).__name__

        if not ir.TypeManager.exists(self._name):
            field_types = [field.type for field in self.fields()]
            ir.TypeManager.add(self._name, lir.LiteralStructType(field_types))

        self.init_class()
        add_instance(self, self)
    
    def init_class(self):
        ...
