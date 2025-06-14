from llvmlite import ir as lir

from cure.lib import function, overload, Lib, DefinitionContext
from cure.codegen_utils import create_string_constant
from cure.target import Target
from cure import ir


class System(Lib):
    @function(ret_type=ir.TypeManager.get('string'), flags=ir.FunctionFlags(static=True, property=True))
    @staticmethod
    def System_os(ctx: DefinitionContext):
        target = ctx.scope.target
        os_name = 'unknown'
        if target == Target.Windows:
            os_name = 'windows'
        elif target == Target.Linux:
            os_name = 'linux'
        
        os_str = create_string_constant(ctx.module, os_name)
        return ctx.call('string_new', [
            os_str, lir.Constant(ir.TypeManager.get('int').type, len(os_name))
        ])
    
    @function([ir.Param(ir.Position.zero(), 'exit_code', ir.TypeManager.get('int'))],
              flags=ir.FunctionFlags(static=True, method=True))
    @staticmethod
    def System_exit(ctx: DefinitionContext):
        exit_code = ctx.param('exit_code').value

        exit = ctx.c_registry.get('exit')

        ctx.builder.call(exit, [exit_code])
    
    @overload(System_exit)
    @staticmethod
    def System_exit_fine(ctx: DefinitionContext):
        return ctx.call('System_exit', [lir.Constant(ir.TypeManager.get('int').type, 0)])
