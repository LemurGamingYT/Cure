from llvmlite import ir as lir

from cure.lib import function, overload, Lib, DefinitionContext
from cure.stdlib.builtins.operations import operations
from cure.stdlib.builtins.testing import testing
from cure.stdlib.builtins.string import string
from cure.stdlib.builtins.System import System
from cure.stdlib.builtins.casts import casts
from cure.stdlib.builtins.Math import Math
from cure.stdlib.builtins.ref import Ref
from cure import ir
from cure.codegen_utils import (
    get_struct_field_value, create_static_buffer, NULL_BYTE, cast_value, create_string_constant
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
    
    @function(ret_type=ir.TypeManager.get('string'), flags=ir.FunctionFlags(public=True))
    @staticmethod
    def input(ctx: DefinitionContext):
        acrt_iob_func = ctx.c_registry.get('__acrt_iob_func')
        strlen = ctx.c_registry.get('strlen')
        fgets = ctx.c_registry.get('fgets')

        INPUT_BUF_SIZE = 256

        buf = create_static_buffer(ctx.module, lir.IntType(8), INPUT_BUF_SIZE)
        size_const = lir.Constant(lir.IntType(32), INPUT_BUF_SIZE)
        stdin = ctx.builder.call(acrt_iob_func, [lir.Constant(lir.IntType(32), 0)])
        ctx.builder.call(fgets, [buf, size_const, stdin])

        input_len = ctx.builder.call(strlen, [buf])
        len_minus_one = ctx.builder.sub(input_len, lir.Constant(lir.IntType(64), 1))
        last_char_ptr = ctx.builder.gep(buf, [len_minus_one])
        last_char = ctx.builder.load(last_char_ptr)
        newline_char = lir.Constant(lir.IntType(8), ord('\n'))
        is_newline = ctx.builder.icmp_signed('==', last_char, newline_char)
        with ctx.builder.if_then(is_newline):
            ctx.builder.store(NULL_BYTE(), last_char_ptr)
            input_len = ctx.builder.sub(input_len, lir.Constant(lir.IntType(64), 1))

        return ctx.call('string_new', [
            buf, cast_value(ctx.builder, input_len, ir.TypeManager.get('int').type)
        ])
    
    @overload(input, [ir.Param(ir.Position.zero(), 'prompt', ir.TypeManager.get('string'))],
              ir.TypeManager.get('string'))
    @staticmethod
    def input_prompt(ctx: DefinitionContext):
        prompt = ctx.param('prompt').value

        printf = ctx.c_registry.get('printf')

        fmt = create_string_constant(ctx.module, '%s')
        prompt_ptr = get_struct_field_value(ctx.builder, prompt, 0)
        ctx.builder.call(printf, [fmt, prompt_ptr])
        return ctx.call('input')
