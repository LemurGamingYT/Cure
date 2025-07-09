from typing import cast

from llvmlite import ir as lir

from cure.lib import function, Lib, DefinitionContext, CallArgument
from cure.ir import Param, Position, Type, FunctionFlags
from cure.codegen_utils import (
    create_string_constant, create_ternary, create_static_buffer, cast_value
)


class casts(Lib):
    def init_lib(self):
        self.INT_BUF_SIZE = 16
        self.FLOAT_BUF_SIZE = 64

        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('int'), 'x')],
            self.scope.type_map.get('string'), flags=FunctionFlags(method=True)
        )
        def int_to_string(ctx: DefinitionContext):
            buf_size = lir.Constant(lir.IntType(64), self.INT_BUF_SIZE)

            snprintf = ctx.c_registry.get('snprintf')

            x = ctx.param_value('x')

            buf = create_static_buffer(ctx.module, lir.IntType(8), self.INT_BUF_SIZE)
            fmt_ptr = create_string_constant(ctx.module, r'%d')
            ctx.builder.call(snprintf, [buf, buf_size, fmt_ptr, x])

            buf_size_i32 = cast_value(
                ctx.builder, buf_size, cast(Type, self.scope.type_map.get('int')).type
            )

            return ctx.call('string_new', [
                CallArgument(buf, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(buf_size_i32, cast(Type, self.scope.type_map.get('int')))
            ])
        
        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('float'), 'x')],
            self.scope.type_map.get('string'), flags=FunctionFlags(method=True)
        )
        def float_to_string(ctx: DefinitionContext):
            buf_size = lir.Constant(lir.IntType(64), self.FLOAT_BUF_SIZE)

            snprintf = ctx.c_registry.get('snprintf')

            x = cast_value(ctx.builder, ctx.param_value('x'), lir.DoubleType())
            buf = create_static_buffer(ctx.module, lir.IntType(8), self.FLOAT_BUF_SIZE)
            fmt_ptr = create_string_constant(ctx.module, r'%f')
            ctx.builder.call(snprintf, [buf, buf_size, fmt_ptr, x])
            
            buf_size_i32 = cast_value(
                ctx.builder, buf_size, cast(Type, self.scope.type_map.get('int')).type
            )

            return ctx.call('string_new', [
                CallArgument(buf, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(buf_size_i32, cast(Type, self.scope.type_map.get('int')))
            ])
        
        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('string'), 'x')],
            self.scope.type_map.get('string'), flags=FunctionFlags(method=True),
        )
        def string_to_string(ctx: DefinitionContext):
            return ctx.param_value('x')
        
        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('bool'), 'x')],
            self.scope.type_map.get('string'), flags=FunctionFlags(method=True)
        )
        def bool_to_string(ctx: DefinitionContext):
            x = ctx.param_value('x')

            ptr = create_ternary(
                ctx.builder, x,
                create_string_constant(ctx.module, 'true'), create_string_constant(ctx.module, 'false')
            )

            length = create_ternary(
                ctx.builder, x, lir.Constant(lir.IntType(32), 4), lir.Constant(lir.IntType(32), 5)
            )

            return ctx.call('string_new', [
                CallArgument(ptr, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(length, cast(Type, self.scope.type_map.get('int')))
            ])
        
        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('nil'), 'x')],
            self.scope.type_map.get('string'), flags=FunctionFlags(method=True)
        )
        def nil_to_string(ctx: DefinitionContext):
            return ctx.call('string_new', [
                CallArgument(create_string_constant(ctx.module, 'nil'),
                             cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(lir.Constant(cast(Type, self.scope.type_map.get('int')).type, 3),
                             cast(Type, self.scope.type_map.get('int')))
            ])
        

        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('int'), 'x')],
            self.scope.type_map.get('float')
        )
        def int_to_float(ctx: DefinitionContext):
            x = ctx.param_value('x')
            return cast_value(ctx.builder, x, cast(Type, self.scope.type_map.get('float')).type)
        
        @function(
            self,
            [Param(Position.zero(), self.scope.type_map.get('float'), 'x')],
            self.scope.type_map.get('float')
        )
        def float_to_int(ctx: DefinitionContext):
            x = ctx.param_value('x')
            return cast_value(ctx.builder, x, cast(Type, self.scope.type_map.get('int')).type)
