from math import pi, e

from llvmlite import ir as lir

from cure.lib import function, overload, Class, DefinitionContext
from cure.ir import TypeManager, FunctionFlags, Param, Position
from cure.codegen_utils import cast_value


class Math(Class):
    def fields(self):
        return []

    @function(ret_type=TypeManager.get('float'), flags=FunctionFlags(static=True, property=True))
    def pi(self, ctx: DefinitionContext):
        return lir.Constant(ctx.ret_type.type, float(pi))
    
    @function(ret_type=TypeManager.get('float'), flags=FunctionFlags(static=True, property=True))
    def e(self, ctx: DefinitionContext):
        return lir.Constant(ctx.ret_type.type, float(e))
    
    
    @function(
        [Param(Position.zero(), 'arg', TypeManager.get('float'))],
        TypeManager.get('float'), flags=FunctionFlags(static=True, method=True)
    )
    def sin(self, ctx: DefinitionContext):
        arg = ctx.param('arg').value

        sinf = ctx.c_registry.get('sinf')
        return ctx.builder.call(sinf, [arg])
    
    @overload(sin, [
        Param(Position.zero(), 'arg', TypeManager.get('int'))
    ], TypeManager.get('float'))
    def sin_int(self, ctx: DefinitionContext):
        arg = ctx.param('arg').value

        sinf = ctx.c_registry.get('sinf')
        return ctx.builder.call(sinf, [cast_value(ctx.builder, arg, TypeManager.get('float').type)])
    

    @function(
        [Param(Position.zero(), 'arg', TypeManager.get('float'))],
        TypeManager.get('float'), flags=FunctionFlags(static=True, method=True)
    )
    def cos(self, ctx: DefinitionContext):
        arg = ctx.param('arg').value

        cosf = ctx.c_registry.get('cosf')
        return ctx.builder.call(cosf, [arg])
    
    @overload(cos, [
        Param(Position.zero(), 'arg', TypeManager.get('int'))
    ], TypeManager.get('float'))
    def cos_int(self, ctx: DefinitionContext):
        arg = ctx.param('arg').value

        cosf = ctx.c_registry.get('cosf')
        return ctx.builder.call(cosf, [cast_value(ctx.builder, arg, TypeManager.get('float').type)])
    

    @function(
        [Param(Position.zero(), 'arg', TypeManager.get('float'))],
        TypeManager.get('float'), flags=FunctionFlags(static=True, method=True)
    )
    def tan(self, ctx: DefinitionContext):
        arg = ctx.param('arg').value

        tanf = ctx.c_registry.get('tanf')
        return ctx.builder.call(tanf, [arg])
    
    @overload(tan, [
        Param(Position.zero(), 'arg', TypeManager.get('int'))
    ], TypeManager.get('float'))
    def tan_int(self, ctx: DefinitionContext):
        arg = ctx.param('arg').value

        tanf = ctx.c_registry.get('tanf')
        return ctx.builder.call(tanf, [cast_value(ctx.builder, arg, TypeManager.get('float').type)])
    

    @function([Param(Position.zero(), 'arg', TypeManager.get('float'))],
              TypeManager.get('int'), flags=FunctionFlags(static=True, method=True))
    def floor(self, ctx: DefinitionContext):
        arg = ctx.param('arg').value

        floorf = ctx.c_registry.get('floorf')
        return cast_value(ctx.builder, ctx.builder.call(floorf, [arg]), TypeManager.get('int').type)

    @function([Param(Position.zero(), 'arg', TypeManager.get('float'))],
              TypeManager.get('int'), flags=FunctionFlags(static=True, method=True))
    def ceil(self, ctx: DefinitionContext):
        arg = ctx.param('arg').value

        ceilf = ctx.c_registry.get('ceilf')
        return cast_value(ctx.builder, ctx.builder.call(ceilf, [arg]), TypeManager.get('int').type)
    
    @function([Param(Position.zero(), 'arg', TypeManager.get('float'))],
              TypeManager.get('int'), flags=FunctionFlags(static=True, method=True))
    def sqrt(self, ctx: DefinitionContext):
        arg = ctx.param('arg').value

        sqrtf = ctx.c_registry.get('sqrtf')
        return cast_value(ctx.builder, ctx.builder.call(sqrtf, [arg]), TypeManager.get('int').type)
    
    @function([
        Param(Position.zero(), 'base', TypeManager.get('float')),
        Param(Position.zero(), 'exponent', TypeManager.get('float'))
    ], TypeManager.get('float'), flags=FunctionFlags(static=True, method=True))
    def pow(self, ctx: DefinitionContext):
        base = ctx.param('base').value
        exponent = ctx.param('exponent').value

        powf = ctx.c_registry.get('powf')
        return ctx.builder.call(powf, [base, exponent])
    
    @overload(pow, [
        Param(Position.zero(), 'base', TypeManager.get('int')),
        Param(Position.zero(), 'exponent', TypeManager.get('int'))
    ], TypeManager.get('int'))
    def pow_int(self, ctx: DefinitionContext):
        base = ctx.param('base').value
        exponent = ctx.param('exponent').value

        powf = ctx.c_registry.get('powf')
        return cast_value(ctx.builder, ctx.builder.call(powf, [
            cast_value(ctx.builder, base, lir.FloatType()),
            cast_value(ctx.builder, exponent, lir.FloatType())
        ]), TypeManager.get('int').type)
