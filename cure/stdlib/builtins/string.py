from llvmlite import ir as lir

from cure.lib import function, Lib, DefinitionContext
from cure import ir
from cure.codegen_utils import (
    get_struct_field_value, create_struct_value, get_struct_field_ptr, cast_value, NULL_BYTE
)


class string(Lib):
    @function([
        ir.Param(ir.Position.zero(), 'literal', ir.Type.string_literal()),
        ir.Param(ir.Position.zero(), 'length', ir.Type.int())
    ], ir.Type.string(), flags=ir.FunctionFlags(static=True, method=True))
    @staticmethod
    def string_new(ctx: DefinitionContext):
        literal = ctx.param('literal').value
        length = cast_value(ctx.builder, ctx.param('length').value, lir.IntType(64))
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

        null_ptr = ctx.builder.gep(data_ptr, [length])
        ctx.builder.store(NULL_BYTE(), null_ptr)

        func_ptr_type = lir.FunctionType(
            lir.IntType(8).as_pointer(), [lir.IntType(8).as_pointer()]
        ).as_pointer()
        null_func_ptr = lir.Constant(func_ptr_type, None)
        
        ref = ctx.call('Ref_new', [data_ptr, null_func_ptr])
        return create_struct_value(ctx.builder, string_type, [data_ptr, length, ref])
    
    @function([ir.Param(ir.Position.zero(), 's', ir.Type.string().as_pointer())])
    @staticmethod
    def string_destroy(ctx: DefinitionContext):
        s = ctx.param('s').value

        ref_ptr = get_struct_field_ptr(ctx.builder, s, 2)
        ref = ctx.builder.load(ref_ptr)
        
        ctx.call('Ref_dec', [ref])


    @function([ir.Param(ir.Position.zero(), 's', ir.Type.string())], ir.Type.int(),
              flags=ir.FunctionFlags(method=True))
    @staticmethod
    def string_length(ctx: DefinitionContext):
        s = ctx.param('s').value
        length = get_struct_field_value(ctx.builder, s, 1)
        return cast_value(ctx.builder, length, ir.Type.int().type)
