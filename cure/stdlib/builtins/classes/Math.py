from math import pi as pi_value, e as e_value
from typing import cast

from llvmlite import ir as lir

from cure.lib import function, overload, Class, DefinitionContext
from cure.ir import FunctionFlags, Param, Position, Type
from cure.codegen_utils import cast_value


class Math(Class):
    def fields(self):
        return []
    
    def init_class(self):
        @function(self, ret_type=self.scope.type_map.get('float'),
                  flags=FunctionFlags(static=True, property=True))
        def pi(ctx: DefinitionContext):
            return lir.Constant(ctx.ret_type.type, float(pi_value))
        
        @function(self, ret_type=self.scope.type_map.get('float'),
                  flags=FunctionFlags(static=True, property=True))
        def e(ctx: DefinitionContext):
            return lir.Constant(ctx.ret_type.type, float(e_value))
        

        @function(self, [Param(Position.zero(), self.scope.type_map.get('float'), 'arg')],
                self.scope.type_map.get('int'), flags=FunctionFlags(static=True, method=True))
        def floor(ctx: DefinitionContext):
            arg = ctx.param_value('arg')

            floorf = ctx.c_registry.get('floorf')
            return cast_value(
                ctx.builder, ctx.builder.call(floorf, [arg]),
                cast(Type, self.scope.type_map.get('int')).type
            )

        @function(self, [Param(Position.zero(), self.scope.type_map.get('float'), 'arg')],
                self.scope.type_map.get('int'), flags=FunctionFlags(static=True, method=True))
        def ceil(ctx: DefinitionContext):
            arg = ctx.param_value('arg')

            ceilf = ctx.c_registry.get('ceilf')
            return cast_value(
                ctx.builder, ctx.builder.call(ceilf, [arg]),
                cast(Type, self.scope.type_map.get('int')).type
            )
        
        @function(self, [Param(Position.zero(), self.scope.type_map.get('float'), 'arg')],
                self.scope.type_map.get('float'), flags=FunctionFlags(static=True, method=True))
        def sqrt(ctx: DefinitionContext):
            arg = ctx.param_value('arg')

            sqrtf = ctx.c_registry.get('sqrtf')
            return ctx.builder.call(sqrtf, [arg])

        @overload(sqrt, [Param(Position.zero(), self.scope.type_map.get('int'), 'arg')],
                self.scope.type_map.get('int'))
        def sqrt_int(ctx: DefinitionContext):
            arg = ctx.param_value('arg')

            sqrtf = ctx.c_registry.get('sqrtf')
            return cast_value(
                ctx.builder, ctx.builder.call(sqrtf, [
                    cast_value(ctx.builder, arg, cast(Type, self.scope.type_map.get('float')).type)
                ]), cast(Type, self.scope.type_map.get('int')).type
            )
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('float'), 'base'),
            Param(Position.zero(), self.scope.type_map.get('float'), 'exponent')
        ], self.scope.type_map.get('float'), flags=FunctionFlags(static=True, method=True))
        def pow(ctx: DefinitionContext):
            base = ctx.param_value('base')
            exponent = ctx.param_value('exponent')

            powf = ctx.c_registry.get('powf')
            return ctx.builder.call(powf, [base, exponent])
        
        @overload(pow, [
            Param(Position.zero(), self.scope.type_map.get('int'), 'base'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'exponent')
        ], self.scope.type_map.get('int'))
        def pow_int(ctx: DefinitionContext):
            base = ctx.param_value('base')
            exponent = ctx.param_value('exponent')

            powf = ctx.c_registry.get('powf')
            return cast_value(ctx.builder, ctx.builder.call(powf, [
                cast_value(ctx.builder, base, lir.FloatType()),
                cast_value(ctx.builder, exponent, lir.FloatType())
            ]), cast(Type, self.scope.type_map.get('int')).type)
