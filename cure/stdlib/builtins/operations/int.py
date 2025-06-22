from llvmlite import ir as lir

from cure.codegen_utils import create_string_constant, zero
from cure.lib import function, Lib, DefinitionContext
from cure.ir import Param, Position, TypeManager


class intOperations(Lib):
    @function([
        Param(Position.zero(), 'a', TypeManager.get('int')),
        Param(Position.zero(), 'b', TypeManager.get('int'))
    ], TypeManager.get('int'))
    @staticmethod
    def int_add_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.add(a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('int')),
        Param(Position.zero(), 'b', TypeManager.get('int'))
    ], TypeManager.get('int'))
    @staticmethod
    def int_sub_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.sub(a, b)

    @function([
        Param(Position.zero(), 'a', TypeManager.get('int')),
        Param(Position.zero(), 'b', TypeManager.get('int'))
    ], TypeManager.get('int'))
    @staticmethod
    def int_mul_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.mul(a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('int')),
        Param(Position.zero(), 'b', TypeManager.get('int'))
    ], TypeManager.get('int'))
    @staticmethod
    def int_div_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        div_by_zero = ctx.builder.icmp_signed('==', b, zero(32))
        
        with ctx.builder.if_then(div_by_zero):
            ctx.error('division by zero')
        
        return ctx.builder.sdiv(a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('int')),
        Param(Position.zero(), 'b', TypeManager.get('int'))
    ], TypeManager.get('int'))
    @staticmethod
    def int_mod_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        div_by_zero = ctx.builder.icmp_signed('==', b, zero(32))
        
        with ctx.builder.if_then(div_by_zero):
            err_str = 'modulo by zero'
            err_msg = create_string_constant(ctx.module, err_str)
            err_string_struct = ctx.call('string_new', [
                err_msg, lir.Constant(lir.IntType(64), len(err_str))
            ])

            ctx.call('error', [err_string_struct])
            ctx.builder.ret(zero(32))
        
        return ctx.builder.srem(a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('int')),
        Param(Position.zero(), 'b', TypeManager.get('int'))
    ], TypeManager.get('bool'))
    @staticmethod
    def int_eq_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('==', a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('int')),
        Param(Position.zero(), 'b', TypeManager.get('int'))
    ], TypeManager.get('bool'))
    @staticmethod
    def int_neq_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('!=', a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('int')),
        Param(Position.zero(), 'b', TypeManager.get('int'))
    ], TypeManager.get('bool'))
    @staticmethod
    def int_lt_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('<', a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('int')),
        Param(Position.zero(), 'b', TypeManager.get('int'))
    ], TypeManager.get('bool'))
    @staticmethod
    def int_gt_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('>', a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('int')),
        Param(Position.zero(), 'b', TypeManager.get('int'))
    ], TypeManager.get('bool'))
    @staticmethod
    def int_lte_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('<=', a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('int')),
        Param(Position.zero(), 'b', TypeManager.get('int'))
    ], TypeManager.get('bool'))
    @staticmethod
    def int_gte_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.icmp_signed('>=', a, b)
