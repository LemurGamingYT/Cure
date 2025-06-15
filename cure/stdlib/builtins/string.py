from llvmlite import ir as lir

from cure.codegen_utils import get_struct_field_value, create_struct_value, cast_value, NULL_BYTE
from cure.lib import function, Lib, DefinitionContext
from cure import ir


class string(Lib):
    @function([
        ir.Param(ir.Position.zero(), 'literal', ir.TypeManager.get('pointer')),
        ir.Param(ir.Position.zero(), 'length', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('string'), flags=ir.FunctionFlags(method=True))
    @staticmethod
    def string_new(ctx: DefinitionContext):
        literal = ctx.param('literal').value
        length = cast_value(ctx.builder, ctx.param('length').value, lir.IntType(64))
        string_type = ir.TypeManager.get('string').type

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

        null_ptr = ctx.builder.gep(data_ptr, [length])
        ctx.builder.store(NULL_BYTE(), null_ptr)

        func_ptr_type = lir.FunctionType(
            lir.IntType(8).as_pointer(), [lir.IntType(8).as_pointer()]
        ).as_pointer()
        null_func_ptr = lir.Constant(func_ptr_type, None)
        
        ref = ctx.call('Ref_new', [data_ptr, null_func_ptr])
        return create_struct_value(ctx.builder, string_type, [data_ptr, length, ref])


    @function([ir.Param(ir.Position.zero(), 's', ir.TypeManager.get('string'))], ir.TypeManager.get('int'),
              flags=ir.FunctionFlags(method=True))
    @staticmethod
    def string_length(ctx: DefinitionContext):
        s = ctx.param('s').value
        length = get_struct_field_value(ctx.builder, s, 1)
        return cast_value(ctx.builder, length, ir.TypeManager.get('int').type)
