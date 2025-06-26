from llvmlite import ir as lir

from cure.stdlib.builtins.operations.string import stringOperations
from cure.stdlib.builtins.operations.float import floatOperations
from cure.ir import Param, Position, TypeManager, FunctionFlags
from cure.lib import function, overload, Lib, DefinitionContext
from cure.stdlib.builtins.operations.bool import boolOperations
from cure.stdlib.builtins.operations.int import intOperations
from cure.stdlib.builtins.classes.string import string
from cure.stdlib.builtins.classes.Math import Math
from cure.stdlib.builtins.classes.Ref import Ref
from cure.stdlib.builtins.casts import casts
from cure.codegen_utils import (
    get_struct_field_value, create_static_buffer, NULL_BYTE, cast_value, create_string_constant,
    index_of_type, get_struct_field_ptr
)


class builtins(Lib):
    def init_lib(self):
        self.add_lib(Ref)
        self.add_lib(Math)
        self.add_lib(casts)
        self.add_lib(string)
        self.add_lib(intOperations)
        self.add_lib(boolOperations)
        self.add_lib(floatOperations)
        self.add_lib(stringOperations)

    @function([Param(Position.zero(), 'message', TypeManager.get('string'))],
              flags=FunctionFlags(public=True))
    def error(self, ctx: DefinitionContext):
        exit = ctx.c_registry.get('exit')
        puts = ctx.c_registry.get('puts')

        message = ctx.param('message').value
        ctx.builder.call(puts, [get_struct_field_value(ctx.builder, message, 0)])
        ctx.builder.call(exit, [lir.Constant(TypeManager.get('int').type, 1)])

    @function([Param(Position.zero(), 'x', TypeManager.get('any'))],
              flags=FunctionFlags(public=True))
    def print(self, ctx: DefinitionContext):
        puts = ctx.c_registry.get('puts')

        x = ctx.param('x')
        x_str = ctx.call(f'{x.type}_to_string', [x.value])
        ctx.builder.call(puts, [get_struct_field_value(ctx.builder, x_str, 0)])

        # manually free the string (because the CodeGeneration's memory management does not apply here)
        ref_index = index_of_type(x_str.type, TypeManager.get('Ref').type.as_pointer())
        ref = ctx.builder.load(get_struct_field_ptr(ctx.builder, x_str, ref_index)) if\
            isinstance(x_str.type, lir.PointerType) else\
            get_struct_field_value(ctx.builder, x_str, ref_index)
        ctx.call('Ref_dec', [ref])

    @function([Param(Position.zero(), 'x', TypeManager.get('string'))],
              flags=FunctionFlags(public=True))
    def print_literal(self, ctx: DefinitionContext):
        printf = ctx.c_registry.get('printf')

        x = ctx.param('x').value
        ctx.builder.call(printf, [get_struct_field_value(ctx.builder, x, 0)])
    
    @function(ret_type=TypeManager.get('string'), flags=FunctionFlags(public=True))
    def input(self, ctx: DefinitionContext):
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
            buf, cast_value(ctx.builder, input_len, TypeManager.get('int').type)
        ])
    
    @overload(input, [Param(Position.zero(), 'prompt', TypeManager.get('string'))],
              TypeManager.get('string'))
    def input_prompt(self, ctx: DefinitionContext):
        prompt = ctx.param('prompt').value

        printf = ctx.c_registry.get('printf')

        fmt = create_string_constant(ctx.module, '%s')
        prompt_ptr = get_struct_field_value(ctx.builder, prompt, 0)
        ctx.builder.call(printf, [fmt, prompt_ptr])
        return ctx.call('input')
