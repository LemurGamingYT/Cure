from llvmlite import ir as lir

from cure.codegen_utils import cast_value, get_struct_value_field, zero
from cure.lib import function, Lib, DefinitionContext
from cure.ir import Param, Position, TypeManager


class stringOperations(Lib):
    def init_lib(self):
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('string')),
            Param(Position.zero(), 'b', TypeManager.get('string'))
        ], TypeManager.get('string'))
        def string_add_string(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')

            memcpy = ctx.c_registry.get('memcpy')
            malloc = ctx.c_registry.get('malloc')

            a_len = get_struct_value_field(ctx.builder, a, 1)
            b_len = get_struct_value_field(ctx.builder, b, 1)
            total_length = ctx.builder.add(a_len, b_len)
            ptr = ctx.builder.call(malloc, [ctx.builder.add(
                total_length, lir.Constant(lir.IntType(64), 1)
            )])

            a_buf = get_struct_value_field(ctx.builder, a, 0)
            b_buf = get_struct_value_field(ctx.builder, b, 0)
            ctx.builder.call(memcpy, [ptr, a_buf, a_len])

            ptr_offset = ctx.builder.gep(ptr, [a_len])
            ctx.builder.call(memcpy, [ptr_offset, b_buf, b_len])

            null_pos = ctx.builder.gep(ptr, [total_length])
            null_byte = lir.Constant(lir.IntType(8), 0)
            ctx.builder.store(null_byte, null_pos)
            
            return ctx.call('string_new', [
                ptr, cast_value(ctx.builder, total_length, TypeManager.get('int').type)
            ])
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('string')),
            Param(Position.zero(), 'b', TypeManager.get('string'))
        ], TypeManager.get('bool'))
        def string_eq_string(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            
            memcmp = ctx.c_registry.get('memcmp')

            a_len = get_struct_value_field(ctx.builder, a, 1)
            b_len = get_struct_value_field(ctx.builder, b, 1)
            with ctx.builder.if_then(ctx.builder.icmp_signed('!=', a_len, b_len)):
                ctx.builder.ret(zero(1))
            
            a_ptr = get_struct_value_field(ctx.builder, a, 0)
            b_ptr = get_struct_value_field(ctx.builder, b, 0)
            return ctx.builder.icmp_signed(
                '==',
                ctx.builder.call(memcmp, [a_ptr, b_ptr, a_len]),
                zero(1)
            )
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('string')),
            Param(Position.zero(), 'b', TypeManager.get('string'))
        ], TypeManager.get('bool'))
        def string_neq_string(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            
            memcmp = ctx.c_registry.get('memcmp')

            a_len = get_struct_value_field(ctx.builder, a, 1)
            b_len = get_struct_value_field(ctx.builder, b, 1)
            with ctx.builder.if_then(ctx.builder.icmp_signed('==', a_len, b_len)):
                ctx.builder.ret(zero(1))
            
            a_ptr = get_struct_value_field(ctx.builder, a, 0)
            b_ptr = get_struct_value_field(ctx.builder, b, 0)
            return ctx.builder.icmp_signed(
                '!=',
                ctx.builder.call(memcmp, [a_ptr, b_ptr, a_len]),
                zero(1)
            )
