from llvmlite import ir as lir

from cure.codegen_utils import create_struct_value, create_string_constant
from cure.lib import function, Lib, DefinitionContext
from cure import ir


class casts(Lib):
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
