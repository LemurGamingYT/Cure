from llvmlite import ir as lir

from cure.codegen_utils import float_zero
from cure.lib import function, Lib, DefinitionContext
from cure.ir import Param, Position, TypeManager


class floatOperations(Lib):
    def init_lib(self):
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('float')),
            Param(Position.zero(), 'b', TypeManager.get('float'))
        ], TypeManager.get('float'))
        def float_add_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fadd(a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('float')),
            Param(Position.zero(), 'b', TypeManager.get('float'))
        ], TypeManager.get('float'))
        def float_sub_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fsub(a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('float')),
            Param(Position.zero(), 'b', TypeManager.get('float'))
        ], TypeManager.get('float'))
        def float_mul_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fmul(a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('float')),
            Param(Position.zero(), 'b', TypeManager.get('float'))
        ], TypeManager.get('float'))
        def float_div_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')

            div_by_zero = ctx.builder.fcmp_ordered('==', b, float_zero())
            
            with ctx.builder.if_then(div_by_zero):
                ctx.error('division by zero')
            
            return ctx.builder.fdiv(a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('float')),
            Param(Position.zero(), 'b', TypeManager.get('float'))
        ], TypeManager.get('float'))
        def float_mod_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')

            zero = lir.Constant(TypeManager.get('float').type, 0.0)
            div_by_zero = ctx.builder.fcmp_ordered('==', b, zero)
            
            with ctx.builder.if_then(div_by_zero):
                ctx.error('modulo by zero')
            
            return ctx.builder.frem(a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('float')),
            Param(Position.zero(), 'b', TypeManager.get('float'))
        ], TypeManager.get('bool'))
        def float_eq_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fcmp_ordered('==', a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('float')),
            Param(Position.zero(), 'b', TypeManager.get('float'))
        ], TypeManager.get('bool'))
        def float_neq_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fcmp_ordered('!=', a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('float')),
            Param(Position.zero(), 'b', TypeManager.get('float'))
        ], TypeManager.get('bool'))
        def float_lt_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fcmp_ordered('<', a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('float')),
            Param(Position.zero(), 'b', TypeManager.get('float'))
        ], TypeManager.get('bool'))
        def float_gt_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fcmp_ordered('>', a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('float')),
            Param(Position.zero(), 'b', TypeManager.get('float'))
        ], TypeManager.get('bool'))
        def float_lte_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fcmp_ordered('<=', a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('float')),
            Param(Position.zero(), 'b', TypeManager.get('float'))
        ], TypeManager.get('bool'))
        def float_gte_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fcmp_ordered('>=', a, b)
