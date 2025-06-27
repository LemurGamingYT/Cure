from cure.codegen_utils import zero
from cure.lib import function, Lib, DefinitionContext
from cure.ir import Param, Position, TypeManager


class intOperations(Lib):
    def init_lib(self):
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('int')),
            Param(Position.zero(), 'b', TypeManager.get('int'))
        ], TypeManager.get('int'))
        def int_add_int(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.add(a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('int')),
            Param(Position.zero(), 'b', TypeManager.get('int'))
        ], TypeManager.get('int'))
        def int_sub_int(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.sub(a, b)

        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('int')),
            Param(Position.zero(), 'b', TypeManager.get('int'))
        ], TypeManager.get('int'))
        def int_mul_int(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.mul(a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('int')),
            Param(Position.zero(), 'b', TypeManager.get('int'))
        ], TypeManager.get('int'))
        def int_div_int(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value

            div_by_zero = ctx.builder.icmp_signed('==', b, zero(32))
            
            with ctx.builder.if_then(div_by_zero):
                ctx.error('division by zero')
            
            return ctx.builder.sdiv(a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('int')),
            Param(Position.zero(), 'b', TypeManager.get('int'))
        ], TypeManager.get('int'))
        def int_mod_int(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value

            div_by_zero = ctx.builder.icmp_signed('==', b, zero(32))
            
            with ctx.builder.if_then(div_by_zero):
                ctx.error('modulo by zero')
            
            return ctx.builder.srem(a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('int')),
            Param(Position.zero(), 'b', TypeManager.get('int'))
        ], TypeManager.get('bool'))
        def int_eq_int(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.icmp_signed('==', a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('int')),
            Param(Position.zero(), 'b', TypeManager.get('int'))
        ], TypeManager.get('bool'))
        def int_neq_int(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.icmp_signed('!=', a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('int')),
            Param(Position.zero(), 'b', TypeManager.get('int'))
        ], TypeManager.get('bool'))
        def int_lt_int(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.icmp_signed('<', a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('int')),
            Param(Position.zero(), 'b', TypeManager.get('int'))
        ], TypeManager.get('bool'))
        def int_gt_int(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.icmp_signed('>', a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('int')),
            Param(Position.zero(), 'b', TypeManager.get('int'))
        ], TypeManager.get('bool'))
        def int_lte_int(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.icmp_signed('<=', a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('int')),
            Param(Position.zero(), 'b', TypeManager.get('int'))
        ], TypeManager.get('bool'))
        def int_gte_int(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.icmp_signed('>=', a, b)
