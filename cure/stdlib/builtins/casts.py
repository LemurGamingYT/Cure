from llvmlite import ir as lir

from cure.ir import Param, Position, TypeManager, FunctionFlags
from cure.lib import function, Lib, DefinitionContext
from cure.codegen_utils import (
    create_string_constant, create_ternary, create_static_buffer, cast_value
)


class casts(Lib):
    def init_lib(self):
        self.INT_BUF_SIZE = 16
        self.FLOAT_BUF_SIZE = 64

    @function(
        [Param(Position.zero(), 'x', TypeManager.get('int'))],
        TypeManager.get('string'), flags=FunctionFlags(method=True)
    )
    def int_to_string(self, ctx: DefinitionContext):
        buf_size = lir.Constant(lir.IntType(64), self.INT_BUF_SIZE)

        snprintf = ctx.c_registry.get('snprintf')

        x = ctx.param('x').value
        buf = create_static_buffer(ctx.module, lir.IntType(8), self.INT_BUF_SIZE)
        fmt_ptr = create_string_constant(ctx.module, r'%d')
        ctx.builder.call(snprintf, [buf, buf_size, fmt_ptr, x])
        return ctx.call('string_new', [
            buf, cast_value(ctx.builder, buf_size, TypeManager.get('int').type)
        ])
    
    @function(
        [Param(Position.zero(), 'x', TypeManager.get('float'))],
        TypeManager.get('string'), flags=FunctionFlags(method=True)
    )
    def float_to_string(self, ctx: DefinitionContext):
        buf_size = lir.Constant(lir.IntType(64), self.FLOAT_BUF_SIZE)

        snprintf = ctx.c_registry.get('snprintf')

        x = cast_value(ctx.builder, ctx.param('x').value, lir.DoubleType())
        buf = create_static_buffer(ctx.module, lir.IntType(8), self.FLOAT_BUF_SIZE)
        fmt_ptr = create_string_constant(ctx.module, r'%f')
        ctx.builder.call(snprintf, [buf, buf_size, fmt_ptr, x])
        return ctx.call('string_new', [
            buf, cast_value(ctx.builder, buf_size, TypeManager.get('int').type)
        ])
    
    @function(
        [Param(Position.zero(), 'x', TypeManager.get('string'))],
        TypeManager.get('string'), flags=FunctionFlags(method=True)
    )
    def string_to_string(self, ctx: DefinitionContext):
        return ctx.param('x').value
    
    @function(
        [Param(Position.zero(), 'x', TypeManager.get('bool'))],
        TypeManager.get('string'), flags=FunctionFlags(method=True)
    )
    def bool_to_string(self, ctx: DefinitionContext):
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
        [Param(Position.zero(), 'x', TypeManager.get('nil'))],
        TypeManager.get('string'), flags=FunctionFlags(method=True)
    )
    def nil_to_string(self, ctx: DefinitionContext):
        return ctx.call('string_new', [
            create_string_constant(ctx.module, 'nil'),
            lir.Constant(TypeManager.get('int').type, 3)
        ])
    

    @function(
        [Param(Position.zero(), 'x', TypeManager.get('int'))],
        TypeManager.get('float')
    )
    def int_to_float(self, ctx: DefinitionContext):
        x = ctx.param('x').value
        return cast_value(ctx.builder, x, TypeManager.get('float').type)
    
    @function(
        [Param(Position.zero(), 'x', TypeManager.get('float'))],
        TypeManager.get('float')
    )
    def float_to_int(self, ctx: DefinitionContext):
        x = ctx.param('x').value
        return cast_value(ctx.builder, x, TypeManager.get('int').type)
