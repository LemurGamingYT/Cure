from math import pi, e

from llvmlite import ir as lir

from cure.lib import function, overload, Lib, DefinitionContext
from cure.codegen_utils import cast_value
from cure import ir


class Math(Lib):
    @function(ret_type=ir.TypeManager.get('float'), flags=ir.FunctionFlags(static=True, property=True))
    @staticmethod
    def Math_pi(ctx: DefinitionContext):
        return lir.Constant(ctx.ret_type.type, pi)
    
    @function(ret_type=ir.TypeManager.get('float'), flags=ir.FunctionFlags(static=True, property=True))
    @staticmethod
    def Math_e(ctx: DefinitionContext):
        return lir.Constant(ctx.ret_type.type, e)
    
    
    @function(
        [ir.Param(ir.Position.zero(), 'arg', ir.TypeManager.get('float'))],
        ir.TypeManager.get('float'), flags=ir.FunctionFlags(static=True, method=True)
    )
    @staticmethod
    def Math_sin(ctx: DefinitionContext):
        arg = ctx.param('arg').value

        sinf = ctx.c_registry.get('sinf')
        return ctx.builder.call(sinf, [arg])
    
    @overload(Math_sin, [
        ir.Param(ir.Position.zero(), 'arg', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('float'))
    @staticmethod
    def Math_sin_int(ctx: DefinitionContext):
        arg = ctx.param('arg').value

        sinf = ctx.c_registry.get('sinf')
        return ctx.builder.call(sinf, [cast_value(ctx.builder, arg, ir.TypeManager.get('float').type)])
    

    @function(
        [ir.Param(ir.Position.zero(), 'arg', ir.TypeManager.get('float'))],
        ir.TypeManager.get('float'), flags=ir.FunctionFlags(static=True, method=True)
    )
    @staticmethod
    def Math_cos(ctx: DefinitionContext):
        arg = ctx.param('arg').value

        cosf = ctx.c_registry.get('cosf')
        return ctx.builder.call(cosf, [arg])
    
    @overload(Math_cos, [
        ir.Param(ir.Position.zero(), 'arg', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('float'))
    @staticmethod
    def Math_cos_int(ctx: DefinitionContext):
        arg = ctx.param('arg').value

        cosf = ctx.c_registry.get('cosf')
        return ctx.builder.call(cosf, [cast_value(ctx.builder, arg, ir.TypeManager.get('float').type)])
    

    @function(
        [ir.Param(ir.Position.zero(), 'arg', ir.TypeManager.get('float'))],
        ir.TypeManager.get('float'), flags=ir.FunctionFlags(static=True, method=True)
    )
    @staticmethod
    def Math_tan(ctx: DefinitionContext):
        arg = ctx.param('arg').value

        tanf = ctx.c_registry.get('tanf')
        return ctx.builder.call(tanf, [arg])
    
    @overload(Math_tan, [
        ir.Param(ir.Position.zero(), 'arg', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('float'))
    @staticmethod
    def Math_tan_int(ctx: DefinitionContext):
        arg = ctx.param('arg').value

        tanf = ctx.c_registry.get('tanf')
        return ctx.builder.call(tanf, [cast_value(ctx.builder, arg, ir.TypeManager.get('float').type)])
    

    @function([ir.Param(ir.Position.zero(), 'arg', ir.TypeManager.get('float'))],
              ir.TypeManager.get('int'), flags=ir.FunctionFlags(static=True, method=True))
    @staticmethod
    def Math_floor(ctx: DefinitionContext):
        arg = ctx.param('arg').value

        floorf = ctx.c_registry.get('floorf')
        return ctx.builder.call(floorf, [arg])

    @function([ir.Param(ir.Position.zero(), 'arg', ir.TypeManager.get('float'))],
              ir.TypeManager.get('int'), flags=ir.FunctionFlags(static=True, method=True))
    @staticmethod
    def Math_ceil(ctx: DefinitionContext):
        arg = ctx.param('arg').value

        ceilf = ctx.c_registry.get('ceilf')
        return ctx.builder.call(ceilf, [arg])
    
    @function([ir.Param(ir.Position.zero(), 'arg', ir.TypeManager.get('float'))],
              ir.TypeManager.get('int'), flags=ir.FunctionFlags(static=True, method=True))
    @staticmethod
    def Math_sqrt(ctx: DefinitionContext):
        arg = ctx.param('arg').value

        sqrtf = ctx.c_registry.get('sqrtf')
        return ctx.builder.call(sqrtf, [arg])
    
    @function([
        ir.Param(ir.Position.zero(), 'base', ir.TypeManager.get('float')),
        ir.Param(ir.Position.zero(), 'exponent', ir.TypeManager.get('float'))
    ], ir.TypeManager.get('float'), flags=ir.FunctionFlags(static=True, method=True))
    @staticmethod
    def Math_pow(ctx: DefinitionContext):
        base = ctx.param('base').value
        exponent = ctx.param('exponent').value

        powf = ctx.c_registry.get('powf')
        return ctx.builder.call(powf, [base, exponent])
    
    @overload(Math_pow, [
        ir.Param(ir.Position.zero(), 'base', ir.TypeManager.get('int')),
        ir.Param(ir.Position.zero(), 'exponent', ir.TypeManager.get('int'))
    ], ir.TypeManager.get('int'))
    @staticmethod
    def Math_pow_int(ctx: DefinitionContext):
        base = ctx.param('base').value
        exponent = ctx.param('exponent').value

        powf = ctx.c_registry.get('powf')
        return cast_value(ctx.builder, ctx.builder.call(powf, [
            cast_value(ctx.builder, base, lir.FloatType()),
            cast_value(ctx.builder, exponent, lir.FloatType())
        ]), ir.TypeManager.get('int').type)
