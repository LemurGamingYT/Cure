from llvmlite import ir as lir

from cure.codegen_utils import get_struct_field_value, create_struct_value
from cure.lib import function, Lib, DefinitionContext
from cure import ir


class string(Lib):
    @function([
        ir.Param(ir.Position.zero(), 'literal', ir.Type.string_literal()),
        ir.Param(ir.Position.zero(), 'length', ir.Type.int())
    ], ir.Type.string())
    @staticmethod
    def string_new(ctx: DefinitionContext):
        literal = ctx.param('literal').value
        length = ctx.builder.zext(ctx.param('length').value, lir.IntType(64))
        string_type = ir.Type.string().type

        malloc = ctx.c_registry.get('malloc')
        memcpy = ctx.c_registry.get('memcpy')

        # +1 for null terminator
        one = lir.Constant(lir.IntType(64), 1)
        tot_length = ctx.builder.add(length, one)
        data_ptr = ctx.builder.bitcast(
            ctx.builder.call(malloc, [tot_length]),
            lir.IntType(8).as_pointer()
        )
        ctx.builder.call(memcpy, [data_ptr, literal, length])

        null_byte = lir.Constant(lir.IntType(8), 0)
        null_ptr = ctx.builder.gep(data_ptr, [length])
        ctx.builder.store(null_byte, null_ptr)

        struct = create_struct_value(ctx.builder, string_type, [data_ptr, length])
        ctx.builder.ret(struct)


    @function([ir.Param(ir.Position.zero(), 's', ir.Type.string())], ir.Type.int())
    @staticmethod
    def string_length(ctx: DefinitionContext):
        s = ctx.param('s').value
        length = get_struct_field_value(ctx.builder, s, 1)
        length_i32 = ctx.builder.trunc(length, ir.Type.int().type)
        ctx.builder.ret(length_i32)
