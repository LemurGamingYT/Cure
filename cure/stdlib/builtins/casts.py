from llvmlite import ir as lir

from cure.lib import function, Lib, DefinitionContext
from cure import ir
from cure.codegen_utils import (
    create_struct_value, create_string_constant, create_ternary, create_static_buffer
)


class casts(Lib):
    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.int())], ir.Type.string())
    @staticmethod
    def int_to_string(ctx: DefinitionContext):
        BUF_SIZE = 16
        buf_size = lir.Constant(lir.IntType(64), BUF_SIZE)

        snprintf = ctx.c_registry.get('snprintf')

        x = ctx.param('x').value
        buf = create_static_buffer(ctx.module, lir.IntType(8), BUF_SIZE)
        fmt_ptr = create_string_constant(ctx.module, r'%d')
        ctx.builder.call(snprintf, [buf, buf_size, fmt_ptr, x])

        string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [buf, buf_size])
        ctx.builder.ret(string_struct)
    
    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.float())], ir.Type.string())
    @staticmethod
    def float_to_string(ctx: DefinitionContext):
        BUF_SIZE = 64
        buf_size = lir.Constant(lir.IntType(64), BUF_SIZE)

        snprintf = ctx.c_registry.get('snprintf')

        x = ctx.builder.fpext(ctx.param('x').value, lir.DoubleType())
        buf = create_static_buffer(ctx.module, lir.IntType(8), BUF_SIZE)
        fmt_ptr = create_string_constant(ctx.module, r'%f')
        ctx.builder.call(snprintf, [buf, buf_size, fmt_ptr, x])

        string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [buf, buf_size])
        ctx.builder.ret(string_struct)
    
    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.string())], ir.Type.string())
    @staticmethod
    def string_to_string(ctx: DefinitionContext):
        x = ctx.param('x')
        ctx.builder.ret(x.value)
    
    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.bool())], ir.Type.string())
    @staticmethod
    def bool_to_string(ctx: DefinitionContext):
        x = ctx.param('x').value
        ptr = create_ternary(
            ctx.builder, x,
            create_string_constant(ctx.module, 'true'), create_string_constant(ctx.module, 'false')
        )

        length = create_ternary(
            ctx.builder, x, lir.Constant(lir.IntType(64), 4), lir.Constant(lir.IntType(64), 5)
        )

        ctx.builder.ret(create_struct_value(ctx.builder, ir.Type.string().type, [ptr, length]))
    
    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.nil())], ir.Type.string())
    @staticmethod
    def nil_to_string(ctx: DefinitionContext):
        ctx.builder.ret(create_struct_value(ctx.builder, ir.Type.string().type, [
            create_string_constant(ctx.module, 'nil'),
            lir.Constant(lir.IntType(64), 3)
        ]))
    

    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.int())], ir.Type.float())
    @staticmethod
    def int_to_float(ctx: DefinitionContext):
        x = ctx.param('x').value
        ctx.builder.ret(ctx.builder.sitofp(x, ir.Type.float().type))
    
    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.float())], ir.Type.int())
    @staticmethod
    def float_to_int(ctx: DefinitionContext):
        x = ctx.param('x').value
        ctx.builder.ret(ctx.builder.fptosi(x, ir.Type.int().type))
