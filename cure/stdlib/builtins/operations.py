from llvmlite import ir as lir

from cure.lib import function, Lib, DefinitionContext
from cure import ir
from cure.codegen_utils import (
    create_string_constant, create_struct_value, get_struct_field_value, cast_value
)


class operations(Lib):
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('int')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('int'))
    @staticmethod
    def int_add_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.add(a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('float')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('float'))
    ], ir.TypeManager.get('float'))
    @staticmethod
    def float_add_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fadd(a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('string')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('string'))
    ], ir.TypeManager.get('string'))
    @staticmethod
    def string_add_string(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        memcpy = ctx.c_registry.get('memcpy')
        malloc = ctx.c_registry.get('malloc')

        a_len = get_struct_field_value(ctx.builder, a, 1)
        b_len = get_struct_field_value(ctx.builder, b, 1)
        total_length = ctx.builder.add(a_len, b_len)
        ptr = ctx.builder.call(malloc, [ctx.builder.add(
            total_length, lir.Constant(lir.IntType(64), 1)
        )])

        a_buf = get_struct_field_value(ctx.builder, a, 0)
        b_buf = get_struct_field_value(ctx.builder, b, 0)
        ctx.builder.call(memcpy, [ptr, a_buf, a_len])

        ptr_offset = ctx.builder.gep(ptr, [a_len])
        ctx.builder.call(memcpy, [ptr_offset, b_buf, b_len])

        null_pos = ctx.builder.gep(ptr, [total_length])
        null_byte = lir.Constant(lir.IntType(8), 0)
        ctx.builder.store(null_byte, null_pos)
        
        return ctx.call('string_new', [ptr, cast_value(ctx.builder, total_length, ir.TypeManager.get('int').type)])
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('int')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('int'))
    @staticmethod
    def int_sub_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.sub(a, b)

    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('float')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('float'))
    ], ir.TypeManager.get('float'))
    @staticmethod
    def float_sub_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fsub(a, b)

    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('int')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('int'))
    @staticmethod
    def int_mul_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.mul(a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('float')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('float'))
    ], ir.TypeManager.get('float'))
    @staticmethod
    def float_mul_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fmul(a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('int')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('int'))
    @staticmethod
    def int_div_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        zero = lir.Constant(ir.TypeManager.get('int').type, 0)
        div_by_zero = ctx.builder.icmp_signed('==', b, zero)
        
        with ctx.builder.if_then(div_by_zero):
            err_str = 'division by zero'
            err_msg = create_string_constant(ctx.module, err_str)
            err_string_struct = create_struct_value(ctx.builder, ir.TypeManager.get('string').type, [
                err_msg, lir.Constant(lir.IntType(64), len(err_str))
            ])
            ctx.call('error', [err_string_struct])
            ctx.builder.ret(zero)
        
        return ctx.builder.sdiv(a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('float')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('float'))
    ], ir.TypeManager.get('float'))
    @staticmethod
    def float_div_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        zero = lir.Constant(ir.TypeManager.get('float').type, 0.0)
        div_by_zero = ctx.builder.fcmp_ordered('==', b, zero)
        
        with ctx.builder.if_then(div_by_zero):
            err_str = 'division by zero'
            err_msg = create_string_constant(ctx.module, err_str)
            err_string_struct = create_struct_value(ctx.builder, ir.TypeManager.get('string').type, [
                err_msg, lir.Constant(lir.IntType(64), len(err_str))
            ])
            ctx.call('error', [err_string_struct])
            ctx.builder.ret(zero)
        
        return ctx.builder.fdiv(a, b)

    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('int')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('int'))
    @staticmethod
    def int_mod_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        zero = lir.Constant(ir.TypeManager.get('int').type, 0)
        div_by_zero = ctx.builder.icmp_signed('==', b, zero)
        
        with ctx.builder.if_then(div_by_zero):
            err_str = 'modulo by zero'
            err_msg = create_string_constant(ctx.module, err_str)
            err_string_struct = create_struct_value(ctx.builder, ir.TypeManager.get('string').type, [
                err_msg, lir.Constant(lir.IntType(64), len(err_str))
            ])
            ctx.call('error', [err_string_struct])
            ctx.builder.ret(zero)
        
        return ctx.builder.srem(a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('float')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('float'))
    ], ir.TypeManager.get('float'))
    @staticmethod
    def float_mod_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        zero = lir.Constant(ir.TypeManager.get('float').type, 0.0)
        div_by_zero = ctx.builder.fcmp_ordered('==', b, zero)
        
        with ctx.builder.if_then(div_by_zero):
            err_str = 'modulo by zero'
            err_msg = create_string_constant(ctx.module, err_str)
            err_string_struct = create_struct_value(ctx.builder, ir.TypeManager.get('string').type, [
                err_msg, lir.Constant(lir.IntType(64), len(err_str))
            ])
            ctx.call('error', [err_string_struct])
        
        return ctx.builder.frem(a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('int')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def int_eq_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('==', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('float')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('float'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def float_eq_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fcmp_ordered('==', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('string')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('string'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def string_eq_string(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        
        memcmp = ctx.c_registry.get('memcmp')

        a_len = get_struct_field_value(ctx.builder, a, 1)
        b_len = get_struct_field_value(ctx.builder, b, 1)
        with ctx.builder.if_then(ctx.builder.icmp_signed('!=', a_len, b_len)):
            ctx.builder.ret(lir.Constant(ir.TypeManager.get('bool').type, 0))
        
        a_ptr = get_struct_field_value(ctx.builder, a, 0)
        b_ptr = get_struct_field_value(ctx.builder, b, 0)
        return ctx.builder.icmp_signed(
            '==',
            ctx.builder.call(memcmp, [a_ptr, b_ptr, a_len]),
            lir.Constant(ir.TypeManager.get('bool').type, 0)
        )
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('bool')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('bool'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def bool_eq_bool(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('==', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('int')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def int_neq_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('!=', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('float')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('float'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def float_neq_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fcmp_ordered('!=', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('string')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('string'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def string_neq_string(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        
        memcmp = ctx.c_registry.get('memcmp')

        a_len = get_struct_field_value(ctx.builder, a, 1)
        b_len = get_struct_field_value(ctx.builder, b, 1)
        with ctx.builder.if_then(ctx.builder.icmp_signed('==', a_len, b_len)):
            ctx.builder.ret(lir.Constant(ir.TypeManager.get('bool').type, 0))
        
        a_ptr = get_struct_field_value(ctx.builder, a, 0)
        b_ptr = get_struct_field_value(ctx.builder, b, 0)
        return ctx.builder.icmp_signed(
            '!=',
            ctx.builder.call(memcmp, [a_ptr, b_ptr, a_len]),
            lir.Constant(ir.TypeManager.get('bool').type, 0)
        )
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('bool')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('bool'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def bool_neq_bool(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('!=', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('int')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def int_lt_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('<', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('float')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('float'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def float_lt_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fcmp_ordered('<', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('int')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def int_gt_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('>', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('float')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('float'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def float_gt_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fcmp_ordered('>', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('int')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def int_lte_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('<=', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('float')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('float'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def float_lte_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fcmp_ordered('<=', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('int')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def int_gte_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('>=', a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('float')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('float'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def float_gte_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fcmp_ordered('>=', a, b)

    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('bool')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('bool'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def bool_and_bool(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.and_(a, b)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('bool')),
        ir.Param(ir.Position.zero(), 'b', ir.TypeManager.get('bool'))
    ], ir.TypeManager.get('bool'))
    @staticmethod
    def bool_or_bool(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.or_(a, b)
    
    @function([ir.Param(ir.Position.zero(), 'a', ir.TypeManager.get('bool'))], ir.TypeManager.get('bool'))
    @staticmethod
    def not_bool(ctx: DefinitionContext):
        a = ctx.param('a').value
        return ctx.builder.not_(a)
