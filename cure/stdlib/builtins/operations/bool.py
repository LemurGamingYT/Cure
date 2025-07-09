from cure.lib import function, Lib, DefinitionContext
from cure.ir import Param, Position


class boolOperations(Lib):
    def init_lib(self):
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('bool'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('bool'), 'b')
        ], self.scope.type_map.get('bool'))
        def bool_eq_bool(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.icmp_signed('==', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('bool'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('bool'), 'b')
        ], self.scope.type_map.get('bool'))
        def bool_neq_bool(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.icmp_signed('!=', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('bool'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('bool'), 'b')
        ], self.scope.type_map.get('bool'))
        def bool_and_bool(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.and_(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('bool'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('bool'), 'b')
        ], self.scope.type_map.get('bool'))
        def bool_or_bool(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.or_(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('bool'), 'a')
        ], self.scope.type_map.get('bool'))
        def not_bool(ctx: DefinitionContext):
            a = ctx.param_value('a')
            return ctx.builder.not_(a)
