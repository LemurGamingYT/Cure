from cure.lib import function, Lib, DefinitionContext
from cure.ir import Param, Position, TypeManager


class boolOperations(Lib):
    def init_lib(self):
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('bool')),
            Param(Position.zero(), 'b', TypeManager.get('bool'))
        ], TypeManager.get('bool'))
        def bool_eq_bool(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.icmp_signed('==', a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('bool')),
            Param(Position.zero(), 'b', TypeManager.get('bool'))
        ], TypeManager.get('bool'))
        def bool_neq_bool(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.icmp_signed('!=', a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('bool')),
            Param(Position.zero(), 'b', TypeManager.get('bool'))
        ], TypeManager.get('bool'))
        def bool_and_bool(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.and_(a, b)
        
        @function(self, [
            Param(Position.zero(), 'a', TypeManager.get('bool')),
            Param(Position.zero(), 'b', TypeManager.get('bool'))
        ], TypeManager.get('bool'))
        def bool_or_bool(ctx: DefinitionContext):
            a = ctx.param('a').value
            b = ctx.param('b').value
            return ctx.builder.or_(a, b)
        
        @function(self, [Param(Position.zero(), 'a', TypeManager.get('bool'))], TypeManager.get('bool'))
        def not_bool(ctx: DefinitionContext):
            a = ctx.param('a').value
            return ctx.builder.not_(a)
