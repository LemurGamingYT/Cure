from cure.lib import function, Lib, DefinitionContext
from cure.codegen_utils import get_struct_field_value
from cure import ir


class string(Lib):
    @function([ir.Param(ir.Position.zero(), 's', ir.Type.string())], ir.Type.int())
    @staticmethod
    def string_length(ctx: DefinitionContext):
        s = ctx.param('s').value
        length = get_struct_field_value(ctx.builder, s, 1)
        length_i32 = ctx.builder.trunc(length, ir.Type.int().type)
        ctx.builder.ret(length_i32)
