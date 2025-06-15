from llvmlite import ir as lir

from cure.stdlib.builtins.operations import operations
from cure.lib import function, Lib, DefinitionContext
from cure.stdlib.builtins.testing import testing
from cure.stdlib.builtins.string import string
from cure.stdlib.builtins.System import System
from cure.stdlib.builtins.casts import casts
from cure.stdlib.builtins.Math import Math
from cure.stdlib.builtins.ref import Ref
from cure import ir
from cure.codegen_utils import (
    get_struct_field_value#, create_static_buffer, cast_value, NULL_BYTE
)


class builtins(Lib):
    def init_lib(self):
        self.add_lib(Ref)
        self.add_lib(Math)
        self.add_lib(casts)
        self.add_lib(System)
        self.add_lib(string)
        self.add_lib(testing)
        self.add_lib(operations)

    @function([ir.Param(ir.Position.zero(), 'message', ir.TypeManager.get('string'))],
              flags=ir.FunctionFlags(public=True))
    @staticmethod
    def error(ctx: DefinitionContext):
        exit = ctx.c_registry.get('exit')
        puts = ctx.c_registry.get('puts')

        message = ctx.param('message').value
        ctx.builder.call(puts, [get_struct_field_value(ctx.builder, message, 0)])
        ctx.builder.call(exit, [lir.Constant(ir.TypeManager.get('int').type, 1)])

    @function([ir.Param(ir.Position.zero(), 'x', ir.TypeManager.get('any'))],
              flags=ir.FunctionFlags(public=True))
    @staticmethod
    def print(ctx: DefinitionContext):
        puts = ctx.c_registry.get('puts')

        x = ctx.param('x')
        x_str = ctx.call(f'{x.type}_to_string', [x.value])
        ctx.builder.call(puts, [get_struct_field_value(ctx.builder, x_str, 0)])

    @function([ir.Param(ir.Position.zero(), 'x', ir.TypeManager.get('string'))],
              flags=ir.FunctionFlags(public=True))
    @staticmethod
    def print_literal(ctx: DefinitionContext):
        printf = ctx.c_registry.get('printf')

        x = ctx.param('x').value
        ctx.builder.call(printf, [get_struct_field_value(ctx.builder, x, 0)])
