from llvmlite import ir as lir

from cure.lib import function, Lib, DefinitionContext
from cure import ir
from cure.codegen_utils import (
    create_string_constant, create_struct_value, get_struct_field_value, cast_value
)


class operations(Lib):
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.int())
    @staticmethod
    def int_add_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        ctx.builder.ret(ctx.builder.add(a, b))
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.float()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.float())
    ], ir.Type.float())
    @staticmethod
    def float_add_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        ctx.builder.ret(ctx.builder.fadd(a, b))
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.string()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.string())
    ], ir.Type.string())
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
        
        res = ctx.call('string_new', [ptr, cast_value(ctx.builder, total_length, ir.Type.int().type)])
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.int())
    @staticmethod
    def int_sub_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        ctx.builder.ret(ctx.builder.sub(a, b))

    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.float()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.float())
    ], ir.Type.float())
    @staticmethod
    def float_sub_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        ctx.builder.ret(ctx.builder.fsub(a, b))

    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.int())
    @staticmethod
    def int_mul_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        ctx.builder.ret(ctx.builder.mul(a, b))
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.float()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.float())
    ], ir.Type.float())
    @staticmethod
    def float_mul_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        ctx.builder.ret(ctx.builder.fmul(a, b))
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.int())
    @staticmethod
    def int_div_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        zero = lir.Constant(ir.Type.int().type, 0)
        div_by_zero = ctx.builder.icmp_signed('==', b, zero)
        
        with ctx.builder.if_then(div_by_zero):
            err_str = 'division by zero'
            err_msg = create_string_constant(ctx.module, err_str)
            err_string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [
                err_msg, lir.Constant(lir.IntType(64), len(err_str))
            ])
            ctx.call('error', [err_string_struct])
            ctx.builder.ret(zero)
        
        res = ctx.builder.sdiv(a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.float()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.float())
    ], ir.Type.float())
    @staticmethod
    def float_div_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        zero = lir.Constant(ir.Type.float().type, 0.0)
        div_by_zero = ctx.builder.fcmp_ordered('==', b, zero)
        
        with ctx.builder.if_then(div_by_zero):
            err_str = 'division by zero'
            err_msg = create_string_constant(ctx.module, err_str)
            err_string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [
                err_msg, lir.Constant(lir.IntType(64), len(err_str))
            ])
            ctx.call('error', [err_string_struct])
            ctx.builder.ret(zero)
        
        res = ctx.builder.fdiv(a, b)
        ctx.builder.ret(res)

    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.int())
    @staticmethod
    def int_mod_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        zero = lir.Constant(ir.Type.int().type, 0)
        div_by_zero = ctx.builder.icmp_signed('==', b, zero)
        
        with ctx.builder.if_then(div_by_zero):
            err_str = 'modulo by zero'
            err_msg = create_string_constant(ctx.module, err_str)
            err_string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [
                err_msg, lir.Constant(lir.IntType(64), len(err_str))
            ])
            ctx.call('error', [err_string_struct])
            ctx.builder.ret(zero)
        
        res = ctx.builder.srem(a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.float()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.float())
    ], ir.Type.float())
    @staticmethod
    def float_mod_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        zero = lir.Constant(ir.Type.float().type, 0.0)
        div_by_zero = ctx.builder.fcmp_ordered('==', b, zero)
        
        with ctx.builder.if_then(div_by_zero):
            err_str = 'modulo by zero'
            err_msg = create_string_constant(ctx.module, err_str)
            err_string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [
                err_msg, lir.Constant(lir.IntType(64), len(err_str))
            ])
            ctx.call('error', [err_string_struct])
            ctx.builder.ret(zero)
        
        res = ctx.builder.fdiv(a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.bool())
    @staticmethod
    def int_eq_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.icmp_signed('==', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.float()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.float())
    ], ir.Type.bool())
    @staticmethod
    def float_eq_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.fcmp_ordered('==', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.bool()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.bool())
    ], ir.Type.bool())
    @staticmethod
    def bool_eq_bool(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.icmp_signed('==', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.bool())
    @staticmethod
    def int_neq_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.icmp_signed('!=', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.float()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.float())
    ], ir.Type.bool())
    @staticmethod
    def float_neq_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.fcmp_ordered('!=', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.bool()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.bool())
    ], ir.Type.bool())
    @staticmethod
    def bool_neq_bool(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.icmp_signed('!=', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.bool())
    @staticmethod
    def int_lt_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.icmp_signed('<', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.float()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.float())
    ], ir.Type.bool())
    @staticmethod
    def float_lt_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.fcmp_ordered('<', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.bool())
    @staticmethod
    def int_gt_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.icmp_signed('>', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.float()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.float())
    ], ir.Type.bool())
    @staticmethod
    def float_gt_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.fcmp_ordered('>', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.bool())
    @staticmethod
    def int_lte_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.icmp_signed('<=', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.float()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.float())
    ], ir.Type.bool())
    @staticmethod
    def float_lte_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.fcmp_ordered('<=', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.bool())
    @staticmethod
    def int_gte_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.icmp_signed('>=', a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.float()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.float())
    ], ir.Type.bool())
    @staticmethod
    def float_gte_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.fcmp_ordered('>=', a, b)
        ctx.builder.ret(res)

    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.bool()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.bool())
    ], ir.Type.bool())
    @staticmethod
    def bool_and_bool(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.and_(a, b)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.bool()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.bool())
    ], ir.Type.bool())
    @staticmethod
    def bool_or_bool(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        res = ctx.builder.or_(a, b)
        ctx.builder.ret(res)
    
    @function([ir.Param(ir.Position.zero(), 'a', ir.Type.bool())], ir.Type.bool())
    @staticmethod
    def not_bool(ctx: DefinitionContext):
        a = ctx.param('a').value
        res = ctx.builder.not_(a)
        ctx.builder.ret(res)
