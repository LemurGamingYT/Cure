from llvmlite import ir as lir

from cure.stdlib.builtins.operations import operations
from cure.codegen_utils import get_struct_field_value
from cure.lib import function, Lib, DefinitionContext
from cure.stdlib.builtins.testing import testing
from cure.stdlib.builtins.string import string
from cure.stdlib.builtins.casts import casts
from cure.stdlib.builtins.ref import Ref
from cure import ir


class builtins(Lib):
    def init_lib(self):
        self.add_lib(Ref)
        self.add_lib(casts)
        self.add_lib(string)
        self.add_lib(testing)
        self.add_lib(operations)

    @function([ir.Param(ir.Position.zero(), 'message', ir.Type.string())],
              flags=ir.FunctionFlags(public=True))
    @staticmethod
    def error(ctx: DefinitionContext):
        exit = ctx.c_registry.get('exit')
        puts = ctx.c_registry.get('puts')

        message = ctx.param('message').value
        ctx.builder.call(puts, [get_struct_field_value(ctx.builder, message, 0)])
        ctx.builder.call(exit, [lir.Constant(ir.Type.int().type, 1)])

    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.any())],
              flags=ir.FunctionFlags(public=True))
    @staticmethod
    def print(ctx: DefinitionContext):
        puts = ctx.c_registry.get('puts')

        x = ctx.param('x')
        x_str = ctx.call(f'{x.type}_to_string', [x.value])
        ctx.builder.call(puts, [get_struct_field_value(ctx.builder, x_str, 0)])
