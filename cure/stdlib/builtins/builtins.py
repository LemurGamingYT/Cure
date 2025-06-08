from llvmlite import ir as lir

from cure.codegen_utils import NULL, get_struct_field_value
from cure.stdlib.builtins.operations import operations
from cure.lib import function, Lib, DefinitionContext
from cure.stdlib.builtins.string import string
from cure.stdlib.builtins.casts import casts
from cure import ir


class builtins(Lib):
    def init_lib(self):
        self.add_lib(casts)
        self.add_lib(string)
        self.add_lib(operations)

    @function([ir.Param(ir.Position.zero(), 'message', ir.Type.string())])
    @staticmethod
    def error(ctx: DefinitionContext):
        exit = ctx.c_registry.get('exit')
        puts = ctx.c_registry.get('puts')

        message = ctx.param('message').value
        ctx.builder.call(puts, [get_struct_field_value(ctx.builder, message, 0)])
        ctx.builder.call(exit, [lir.Constant(ir.Type.int().type, 1)])
        ctx.builder.ret(NULL())

    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.any())])
    @staticmethod
    def print(ctx: DefinitionContext):
        puts = ctx.c_registry.get('puts')

        x = ctx.param('x')
        x_str = ctx.call(f'{x.type}_to_string', [x.value])
        ctx.builder.call(puts, [get_struct_field_value(ctx.builder, x_str, 0)])
        ctx.builder.ret(NULL())
    
    @function([
        ir.Param(ir.Position.zero(), 'condition', ir.Type.bool()),
        ir.Param(ir.Position.zero(), 'fail_message', ir.Type.string())
    ])
    @staticmethod
    def assert_(ctx: DefinitionContext):
        condition = ctx.param('condition').value
        with ctx.builder.if_then(ctx.builder.not_(condition)):
            fail_message = ctx.param('fail_message').value
            ctx.call('error', [fail_message])
            ctx.builder.ret(NULL())
        
        ctx.builder.ret(NULL())
