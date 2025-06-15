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

    @function([ir.Param(ir.Position.zero(), 'x', ir.Type.string())],
              flags=ir.FunctionFlags(public=True))
    @staticmethod
    def print_literal(ctx: DefinitionContext):
        printf = ctx.c_registry.get('printf')

        x = ctx.param('x').value
        ctx.builder.call(printf, [get_struct_field_value(ctx.builder, x, 0)])
    
    # @function([ir.Param(ir.Position.zero(), 'prompt', ir.Type.string())], ir.Type.string(),
    #           flags=ir.FunctionFlags(public=True))
    # @staticmethod
    # def input(ctx: DefinitionContext):
    #     INPUT_BUF_SIZE = 256

    #     prompt = ctx.param('prompt').value

    #     acrt_iob_func = ctx.c_registry.get('__acrt_iob_func')
    #     strlen = ctx.c_registry.get('strlen')
    #     fgets = ctx.c_registry.get('fgets')
    #     puts = ctx.c_registry.get('puts')

    #     buf = create_static_buffer(ctx.module, lir.IntType(8), INPUT_BUF_SIZE)
    #     fmt = create_string_constant(ctx.module, '%s')

    #     prompt_ptr = get_struct_field_value(ctx.builder, prompt, 0)
    #     ctx.builder.call(puts, [fmt, prompt_ptr])

    #     stdin = ctx.builder.call(acrt_iob_func, [lir.Constant(lir.IntType(32), 0)])
    #     ctx.builder.call(fgets, [buf, lir.Constant(lir.IntType(32), INPUT_BUF_SIZE), stdin])
    #     length = ctx.builder.call(strlen, [buf])
    #     buf_length_ptr = ctx.builder.gep(buf, [lir.Constant(lir.IntType(32), 0), length])
    #     ctx.builder.store(NULL_BYTE(), buf_length_ptr)
    #     return ctx.call('string_new', [
    #         buf, cast_value(ctx.builder, length, ir.Type.int().type)
    #     ])