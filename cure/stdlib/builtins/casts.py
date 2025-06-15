from llvmlite import ir as lir

from cure.lib import function, Lib, DefinitionContext
from cure import ir
from cure.codegen_utils import (
    create_string_constant, create_ternary, create_static_buffer, cast_value
)


class casts(Lib):
    @function(
        [ir.Param(ir.Position.zero(), 'x', ir.TypeManager.get('int'))],
        ir.TypeManager.get('string'), flags=ir.FunctionFlags(method=True)
    )
    @staticmethod
    def int_to_string(ctx: DefinitionContext):
        BUF_SIZE = 16
        buf_size = lir.Constant(lir.IntType(64), BUF_SIZE)

        snprintf = ctx.c_registry.get('snprintf')

        x = ctx.param('x').value
        buf = create_static_buffer(ctx.module, lir.IntType(8), BUF_SIZE)
        fmt_ptr = create_string_constant(ctx.module, r'%d')
        ctx.builder.call(snprintf, [buf, buf_size, fmt_ptr, x])
        return ctx.call('string_new', [
            buf, cast_value(ctx.builder, buf_size, ir.TypeManager.get('int').type)
        ])
    
    @function(
        [ir.Param(ir.Position.zero(), 'x', ir.TypeManager.get('float'))],
        ir.TypeManager.get('float'), flags=ir.FunctionFlags(method=True)
    )
    @staticmethod
    def float_to_string(ctx: DefinitionContext):
        BUF_SIZE = 64
        buf_size = lir.Constant(lir.IntType(64), BUF_SIZE)

        snprintf = ctx.c_registry.get('snprintf')

        x = cast_value(ctx.builder, ctx.param('x').value, lir.DoubleType())
        buf = create_static_buffer(ctx.module, lir.IntType(8), BUF_SIZE)
        fmt_ptr = create_string_constant(ctx.module, r'%f')
        ctx.builder.call(snprintf, [buf, buf_size, fmt_ptr, x])
        return ctx.call('string_new', [
            buf, cast_value(ctx.builder, buf_size, ir.TypeManager.get('int').type)
        ])
    
    @function(
        [ir.Param(ir.Position.zero(), 'x', ir.TypeManager.get('string'))],
        ir.TypeManager.get('string'), flags=ir.FunctionFlags(method=True)
    )
    @staticmethod
    def string_to_string(ctx: DefinitionContext):
        return ctx.param('x').value
    
    @function(
        [ir.Param(ir.Position.zero(), 'x', ir.TypeManager.get('bool'))],
        ir.TypeManager.get('string'), flags=ir.FunctionFlags(method=True)
    )
    @staticmethod
    def bool_to_string(ctx: DefinitionContext):
        x = ctx.param('x').value
        ptr = create_ternary(
            ctx.builder, x,
            create_string_constant(ctx.module, 'true'), create_string_constant(ctx.module, 'false')
        )

        length = create_ternary(
            ctx.builder, x, lir.Constant(lir.IntType(32), 4), lir.Constant(lir.IntType(32), 5)
        )

        return ctx.call('string_new', [ptr, length])
    
    @function(
        [ir.Param(ir.Position.zero(), 'x', ir.TypeManager.get('nil'))],
        ir.TypeManager.get('string'), flags=ir.FunctionFlags(method=True)
    )
    @staticmethod
    def nil_to_string(ctx: DefinitionContext):
        return ctx.call('string_new', [
            create_string_constant(ctx.module, 'nil'),
            lir.Constant(ir.TypeManager.get('int').type, 3)
        ])
    

    @function(
        [ir.Param(ir.Position.zero(), 'x', ir.TypeManager.get('int'))],
        ir.TypeManager.get('float')
    )
    @staticmethod
    def int_to_float(ctx: DefinitionContext):
        x = ctx.param('x').value
        return cast_value(ctx.builder, x, ir.TypeManager.get('float').type)
    
    @function(
        [ir.Param(ir.Position.zero(), 'x', ir.TypeManager.get('float'))],
        ir.TypeManager.get('float')
    )
    @staticmethod
    def float_to_int(ctx: DefinitionContext):
        x = ctx.param('x').value
        return cast_value(ctx.builder, x, ir.TypeManager.get('int').type)
