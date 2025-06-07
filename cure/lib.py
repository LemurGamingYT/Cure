from dataclasses import dataclass
from logging import debug, info
from functools import wraps
from abc import ABC

from llvmlite import ir as lir

from cure.passes.code_generation import CRegistry
from cure import ir


def function(params: list[ir.Param] | None = None, ret_type: ir.Type | None = None):
    if params is None:
        params = []
    
    if ret_type is None:
        ret_type = ir.Type.nil()
    
    def decorator(func):
        name = func.__name__

        setattr(func, 'function', True)
        setattr(func, 'name', name)
        setattr(func, 'params', params)
        setattr(func, 'ret_type', ret_type)
        setattr(func, 'generic', any(param.type == ir.Type.any() for param in params))

        @wraps(func)
        def wrapper(*args):
            nonlocal name

            _, module, scope, arg_types = args
            c_registry = module.c_registry

            for i, (arg_type, param) in enumerate(zip(arg_types, params)):
                if param.type != ir.Type.any():
                    continue

                params[i] = ir.Param(param.pos, param.name, arg_type)
            
            if name in module.globals:
                debug(f'{name} is compiled, using it again')
                return module.get_global(name)
            
            if func.generic:
                unique_part = module.get_unique_name()
                debug(f'{name} is generic, adding {unique_part}')
                name += unique_part
            
            ir_args = [param.type.type for param in params]
            ir_func = lir.Function(module, lir.FunctionType(ret_type.type, ir_args), name)
            builder = lir.IRBuilder(ir_func.append_basic_block())
            def_scope = scope.clone()
            ctx = DefinitionContext(ir.Position.zero(), def_scope, module, builder, c_registry, params)
            info('Created definition context')

            for i, param in enumerate(params):
                def_scope.symbol_table.add(ir.Symbol(
                    param.name, param.type, ParamPointer(ir_func.args[i], param.type)
                ))
            
            info(f'Compiling {name}')
            func(ctx)
            info(f'Compiled {name}')
            return ir_func
        
        return wrapper
    
    return decorator

def getattrs(instance):
    attrs = {}
    for k in dir(instance):
        if k.startswith('_'):
            continue

        v = getattr(instance, k)
        if not getattr(v, 'function', False):
            continue

        attrs[k] = v
    
    return attrs


@dataclass
class ParamPointer:
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

    def param(self, name: str):
        for param in self.params:
            if param.name == name:
                symbol = self.scope.symbol_table.get(name)
                if symbol is None:
                    self.pos.comptime_error(f'invalid param {name}', self.scope.src)
                    return
                
                return symbol.value

        self.pos.comptime_error(f'unknown param {name}', self.scope.src)
    
    def call(self, name: str, args: list[lir.Value] | None = None):
        if args is None:
            args = []
        
        symbol = self.scope.symbol_table.get(name)
        if symbol is None:
            self.pos.comptime_error(f'no function named {name}', self.scope.src)
            return
        
        func = symbol.value
        if isinstance(func, lir.Function):
            return self.builder.call(func, args)
        elif callable(func):
            ir_func = func(self.module, self.scope, args)
            return self.builder.call(ir_func, args)

class Lib(ABC):
    def __init__(self, scope: ir.Scope):
        self.scope = scope

        self.__add_instance(self)
        self.init_lib()
    
    def init_lib(self):
        pass

    def add_lib(self, cls: type['Lib']):
        instance = cls(self.scope)
        self.__add_instance(instance)
    
    def __add_instance(self, instance):
        for k, v in getattrs(instance).items():
            self.scope.symbol_table.add(ir.Symbol(k, ir.Type.function(), v))
