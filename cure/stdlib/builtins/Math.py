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
