from llvmlite import ir as lir

from cure.codegen_utils import create_string_constant, float_zero
from cure.lib import function, Lib, DefinitionContext
from cure.ir import Param, Position, TypeManager


class floatOperations(Lib):
    @function([
        Param(Position.zero(), 'a', TypeManager.get('float')),
        Param(Position.zero(), 'b', TypeManager.get('float'))
    ], TypeManager.get('float'))
    @staticmethod
    def float_add_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fadd(a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('float')),
        Param(Position.zero(), 'b', TypeManager.get('float'))
    ], TypeManager.get('float'))
    @staticmethod
    def float_sub_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fsub(a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('float')),
        Param(Position.zero(), 'b', TypeManager.get('float'))
    ], TypeManager.get('float'))
    @staticmethod
    def float_mul_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fmul(a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('float')),
        Param(Position.zero(), 'b', TypeManager.get('float'))
    ], TypeManager.get('float'))
    @staticmethod
    def float_div_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        div_by_zero = ctx.builder.fcmp_ordered('==', b, float_zero())
        
        with ctx.builder.if_then(div_by_zero):
            ctx.error('division by zero')
        
        return ctx.builder.fdiv(a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('float')),
        Param(Position.zero(), 'b', TypeManager.get('float'))
    ], TypeManager.get('float'))
    @staticmethod
    def float_mod_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        zero = lir.Constant(TypeManager.get('float').type, 0.0)
        div_by_zero = ctx.builder.fcmp_ordered('==', b, zero)
        
        with ctx.builder.if_then(div_by_zero):
            err_str = 'modulo by zero'
            err_msg = create_string_constant(ctx.module, err_str)
            err_string_struct = ctx.call('string_new', [
                err_msg, lir.Constant(lir.IntType(64), len(err_str))
            ])

            ctx.call('error', [err_string_struct])
        
        return ctx.builder.frem(a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('float')),
        Param(Position.zero(), 'b', TypeManager.get('float'))
    ], TypeManager.get('bool'))
    @staticmethod
    def float_eq_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fcmp_ordered('==', a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('float')),
        Param(Position.zero(), 'b', TypeManager.get('float'))
    ], TypeManager.get('bool'))
    @staticmethod
    def float_neq_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fcmp_ordered('!=', a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('float')),
        Param(Position.zero(), 'b', TypeManager.get('float'))
    ], TypeManager.get('bool'))
    @staticmethod
    def float_lt_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fcmp_ordered('<', a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('float')),
        Param(Position.zero(), 'b', TypeManager.get('float'))
    ], TypeManager.get('bool'))
    @staticmethod
    def float_gt_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fcmp_ordered('>', a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('float')),
        Param(Position.zero(), 'b', TypeManager.get('float'))
    ], TypeManager.get('bool'))
    @staticmethod
    def float_lte_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fcmp_ordered('<=', a, b)
    
    @function([
        Param(Position.zero(), 'a', TypeManager.get('float')),
        Param(Position.zero(), 'b', TypeManager.get('float'))
    ], TypeManager.get('bool'))
    @staticmethod
    def float_gte_float(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        return ctx.builder.fcmp_ordered('>=', a, b)
