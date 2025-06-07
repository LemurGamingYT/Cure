from dataclasses import dataclass
from functools import wraps
from abc import ABC

from llvmlite import ir as lir

from cure.passes.code_generation import CRegistry
from cure import ir
from cure.codegen_utils import (
    create_struct_value, create_string_constant, NULL, get_struct_field_value, get_or_add_global
)


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
                return module.get_global(name)
            
            if func.generic:
                name += module.get_unique_name()
            
            ir_args = [param.type.type for param in params]
            ir_func = lir.Function(module, lir.FunctionType(ret_type.type, ir_args), name)
            builder = lir.IRBuilder(ir_func.append_basic_block())
            def_scope = scope.clone()
            ctx = DefinitionContext(ir.Position.zero(), def_scope, module, builder, c_registry, params)
            for i, param in enumerate(params):
                def_scope.symbol_table.add(ir.Symbol(
                    param.name, param.type, ParamPointer(ir_func.args[i], param.type)
                ))
            
            func(ctx)
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
    
    def __add_instance(self, instance):
        for k, v in getattrs(instance).items():
            self.scope.symbol_table.add(ir.Symbol(k, ir.Type.function(), v))

class builtins(Lib):
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.int())
    @staticmethod
    def int_add_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        intrinsic_name = f'llvm.sadd.with.overflow.{ir.Type.int().type}'
        res_type = lir.LiteralStructType([ir.Type.int().type, lir.IntType(1)])
        intrinsic = get_or_add_global(ctx.module, intrinsic_name, lir.Function(
            ctx.module, lir.FunctionType(res_type, [lir.IntType(32), lir.IntType(32)]),
            intrinsic_name
        ))
        struct = ctx.builder.call(intrinsic, [a, b])
        res = get_struct_field_value(ctx.builder, struct, 0)
        overflow = get_struct_field_value(ctx.builder, struct, 1)

        overflow_block = ctx.builder.function.append_basic_block('overflow')
        success_block = ctx.builder.function.append_basic_block()
        ctx.builder.cbranch(overflow, overflow_block, success_block)

        ctx.builder.position_at_end(overflow_block)
        err_str = 'integer overflow'
        err_msg = create_string_constant(ctx.module, err_str)
        err_string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [
            err_msg, lir.Constant(lir.IntType(64), len(err_str))
        ])
        ctx.call('error', [err_string_struct])
        ctx.builder.ret(lir.Constant(lir.IntType(32), 0))

        ctx.builder.position_at_end(success_block)
        ctx.builder.ret(res)

    @function([ir.Param(ir.Position.zero(), 'message', ir.Type.string())])
    @staticmethod
    def error(ctx: DefinitionContext):
        exit = ctx.c_registry.get('exit')
        puts = ctx.c_registry.get('puts')

        message = ctx.param('message')
        ctx.builder.call(puts, [get_struct_field_value(ctx.builder, message.value, 0)])
        ctx.builder.call(exit, [lir.Constant(ir.Type.int().type, 1)])
        ctx.builder.ret(NULL())

    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.any())])
    @staticmethod
    def print(ctx: DefinitionContext):
        puts = ctx.c_registry.get('puts')

        x = ctx.param('x')
        x_str = ctx.call(f'{x.type}_to_string', [x.value])
        ctx.builder.call(puts, [get_struct_field_value(ctx.builder, x_str, 0)])
        ctx.builder.ret(NULL())

    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.int())], ir.Type.string())
    @staticmethod
    def int_to_string(ctx: DefinitionContext):
        BUF_SIZE = 16
        buf_size = lir.Constant(lir.IntType(64), BUF_SIZE)

        snprintf = ctx.c_registry.get('snprintf')

        x = ctx.param('x')
        buf_type = lir.ArrayType(lir.IntType(8), BUF_SIZE)
        buf = lir.GlobalVariable(ctx.module, buf_type, ctx.module.get_unique_name())
        buf.initializer = lir.Constant(buf_type, None)
        buf.linkage = 'internal'

        zero = lir.Constant(lir.IntType(32), 0)
        buf_ptr = lir.Constant.gep(buf, [zero, zero])

        fmt_ptr = create_string_constant(ctx.module, r'%d')
        ctx.builder.call(snprintf, [buf_ptr, buf_size, fmt_ptr, x.value])

        string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [buf_ptr, buf_size])
        ctx.builder.ret(string_struct)
    
    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.float())], ir.Type.string())
    @staticmethod
    def float_to_string(ctx: DefinitionContext):
        BUF_SIZE = 64
        buf_size = lir.Constant(lir.IntType(64), BUF_SIZE)

        snprintf = ctx.c_registry.get('snprintf')

        x = ctx.param('x')
        buf_type = lir.ArrayType(lir.IntType(8), BUF_SIZE)
        buf = lir.GlobalVariable(ctx.module, buf_type, ctx.module.get_unique_name())
        buf.initializer = lir.Constant(buf_type, None)
        buf.linkage = 'internal'

        zero = lir.Constant(lir.IntType(32), 0)
        buf_ptr = lir.Constant.gep(buf, [zero, zero])

        fmt_ptr = create_string_constant(ctx.module, r'%f')
        ctx.builder.call(snprintf, [buf_ptr, buf_size, fmt_ptr, x.value])

        string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [buf_ptr, buf_size])
        ctx.builder.ret(string_struct)
    
    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.string())], ir.Type.string())
    @staticmethod
    def string_to_string(ctx: DefinitionContext):
        x = ctx.param('x')
        ctx.builder.ret(x.value)
