from math import pi as pi_value, e as e_value

from llvmlite import ir as lir

from cure.lib import function, overload, Class, DefinitionContext
from cure.ir import TypeManager, FunctionFlags, Param, Position
from cure.codegen_utils import cast_value


class Math(Class):
    def fields(self):
        return []
    
    def init_class(self):
        @function(self, ret_type=TypeManager.get('float'),
                  flags=FunctionFlags(static=True, property=True))
        def pi(ctx: DefinitionContext):
            return lir.Constant(ctx.ret_type.type, float(pi_value))
        
        @function(self, ret_type=TypeManager.get('float'),
                  flags=FunctionFlags(static=True, property=True))
        def e(ctx: DefinitionContext):
            return lir.Constant(ctx.ret_type.type, float(e_value))
        

        @function(self, [Param(Position.zero(), 'arg', TypeManager.get('float'))],
                TypeManager.get('int'), flags=FunctionFlags(static=True, method=True))
        def floor(ctx: DefinitionContext):
            arg = ctx.param_value('arg')

            floorf = ctx.c_registry.get('floorf')
            return cast_value(ctx.builder, ctx.builder.call(floorf, [arg]), TypeManager.get('int').type)

        @function(self, [Param(Position.zero(), 'arg', TypeManager.get('float'))],
                TypeManager.get('int'), flags=FunctionFlags(static=True, method=True))
        def ceil(ctx: DefinitionContext):
            arg = ctx.param_value('arg')

            ceilf = ctx.c_registry.get('ceilf')
            return cast_value(ctx.builder, ctx.builder.call(ceilf, [arg]), TypeManager.get('int').type)
        
        @function(self, [Param(Position.zero(), 'arg', TypeManager.get('float'))],
                TypeManager.get('float'), flags=FunctionFlags(static=True, method=True))
        def sqrt(ctx: DefinitionContext):
            arg = ctx.param_value('arg')

            sqrtf = ctx.c_registry.get('sqrtf')
            return ctx.builder.call(sqrtf, [arg])

        @overload(sqrt, [Param(Position.zero(), 'arg', TypeManager.get('int'))],
                TypeManager.get('int'))
        def sqrt_int(ctx: DefinitionContext):
            arg = ctx.param_value('arg')

            sqrtf = ctx.c_registry.get('sqrtf')
            return cast_value(
                ctx.builder,
                ctx.builder.call(sqrtf, [cast_value(ctx.builder, arg, TypeManager.get('float').type)]),
                TypeManager.get('int').type
            )
        
        @function(self, [
            Param(Position.zero(), 'base', TypeManager.get('float')),
            Param(Position.zero(), 'exponent', TypeManager.get('float'))
        ], TypeManager.get('float'), flags=FunctionFlags(static=True, method=True))
        def pow(ctx: DefinitionContext):
            base = ctx.param_value('base')
            exponent = ctx.param_value('exponent')

            powf = ctx.c_registry.get('powf')
            return ctx.builder.call(powf, [base, exponent])
        
        @overload(pow, [
            Param(Position.zero(), 'base', TypeManager.get('int')),
            Param(Position.zero(), 'exponent', TypeManager.get('int'))
        ], TypeManager.get('int'))
        def pow_int(ctx: DefinitionContext):
            base = ctx.param_value('base')
            exponent = ctx.param_value('exponent')

            powf = ctx.c_registry.get('powf')
            return cast_value(ctx.builder, ctx.builder.call(powf, [
                cast_value(ctx.builder, base, lir.FloatType()),
                cast_value(ctx.builder, exponent, lir.FloatType())
            ]), TypeManager.get('int').type)
