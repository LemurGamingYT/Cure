from math import pi, e

from llvmlite import ir as lir

from cure.lib import function, Lib, DefinitionContext
from cure import ir


class Math(Lib):
    @function(ret_type=ir.Type.float(), flags=ir.FunctionFlags(static=True, property=True))
    @staticmethod
    def Math_pi(ctx: DefinitionContext):
        return lir.Constant(ctx.ret_type.type, pi)
    
    @function(ret_type=ir.Type.float(), flags=ir.FunctionFlags(static=True, property=True))
    @staticmethod
    def Math_e(ctx: DefinitionContext):
        return lir.Constant(ctx.ret_type.type, e)
    
    @function([ir.Param(ir.Position.zero(), 'arg', ir.Type.float())], ir.Type.float(),
              flags=ir.FunctionFlags(static=True, method=True))
    @staticmethod
    def Math_sin(ctx: DefinitionContext):
        arg = ctx.param('arg').value

        sinf = ctx.c_registry.get('sinf')
        return ctx.builder.call(sinf, [arg])
    
    @function([ir.Param(ir.Position.zero(), 'arg', ir.Type.float())], ir.Type.float(),
              flags=ir.FunctionFlags(static=True, method=True))
    @staticmethod
    def Math_cos(ctx: DefinitionContext):
        arg = ctx.param('arg').value

        cosf = ctx.c_registry.get('cosf')
        return ctx.builder.call(cosf, [arg])
    
    @function([ir.Param(ir.Position.zero(), 'arg', ir.Type.float())], ir.Type.float(),
              flags=ir.FunctionFlags(static=True, method=True))
    @staticmethod
    def Math_tan(ctx: DefinitionContext):
        arg = ctx.param('arg').value

        tanf = ctx.c_registry.get('tanf')
        return ctx.builder.call(tanf, [arg])
