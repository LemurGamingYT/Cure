from typing import cast

from llvmlite import ir as lir

from cure.lib import function, Class, DefinitionContext, CallArgument
from cure.ir import Param, Position, Type, FunctionFlags
from cure.codegen_utils import (
    get_struct_value_field, create_struct_value, cast_value, NULL_BYTE, zero#, get_struct_ptr_field,
    #get_struct_ptr_field_value
)


class string(Class):
    def fields(self):
        return []

    def init_class(self):
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('pointer'), 'literal'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'length')
        ], self.scope.type_map.get('string'), flags=FunctionFlags(method=True))
        def new(ctx: DefinitionContext):
            literal = ctx.param_value('literal')

            length = cast_value(ctx.builder, ctx.param_value('length'), lir.IntType(64))
            string_type = cast(Type, self.scope.type_map.get('string')).type

            malloc = ctx.c_registry.get('malloc')
            memcpy = ctx.c_registry.get('memcpy')

            # +1 for null terminator
            one = lir.Constant(lir.IntType(64), 1)
            tot_length = ctx.builder.add(length, one)
            data_ptr = ctx.builder.bitcast(
                ctx.builder.call(malloc, [tot_length]),
                lir.IntType(8).as_pointer()
            )
            ctx.builder.call(memcpy, [data_ptr, literal, length])

            null_ptr = ctx.builder.gep(data_ptr, [length])
            ctx.builder.store(NULL_BYTE(), null_ptr)

            func_ptr_type = lir.FunctionType(
                lir.IntType(8).as_pointer(), [lir.IntType(8).as_pointer()]
            ).as_pointer()
            null_func_ptr = lir.Constant(func_ptr_type, None)
            
            ref = ctx.call('Ref_new', [
                CallArgument(data_ptr, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(null_func_ptr, cast(Type, self.scope.type_map.get('any_function')))
            ])

            return create_struct_value(ctx.builder, string_type, [data_ptr, length, ref])


        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('string'), 's')],
            self.scope.type_map.get('int'), flags=FunctionFlags(property=True)
        )
        def length(ctx: DefinitionContext):
            s = ctx.param_value('s')

            length = get_struct_value_field(ctx.builder, s, 1)
            return cast_value(ctx.builder, length, cast(Type, self.scope.type_map.get('int')).type)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string'), 's'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'index')
        ], self.scope.type_map.get('string'), flags=FunctionFlags(method=True))
        def get(ctx: DefinitionContext):
            s = ctx.param_value('s')
            index = ctx.param_value('index')

            length = get_struct_value_field(ctx.builder, s, 1)
            length_i32 = cast_value(ctx.builder, length, lir.IntType(32))
            with ctx.builder.if_then(ctx.builder.icmp_signed('>', index, length_i32)):
                ctx.error('string index out of bounds')
            
            with ctx.builder.if_then(ctx.builder.icmp_signed('<', index, zero(32))):
                index = ctx.builder.add(length_i32, index)

            ptr = get_struct_value_field(ctx.builder, s, 0)
            index_ptr = ctx.builder.gep(ptr, [index])
            return ctx.call('string_new', [
                CallArgument(index_ptr, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(lir.Constant(lir.IntType(32), 1),
                             cast(Type, self.scope.type_map.get('int')))
            ])
        
        # @function(self, [
        #     Param(Position.zero(), self.scope.type_map.get('string').reference(), 's'),
        #     Param(Position.zero(), self.scope.type_map.get('int'), 'index'),
        #     Param(Position.zero(), self.scope.type_map.get('string'), 'value')
        # ], flags=FunctionFlags(method=True))
        # def set(ctx: DefinitionContext):
        #     s = ctx.param_value('s')
        #     index = ctx.param_value('index')
        #     value = ctx.param_value('value')

        #     length = get_struct_ptr_field_value(ctx.builder, s, 1)
        #     length_i32 = cast_value(ctx.builder, length, lir.IntType(32))
        #     with ctx.builder.if_then(ctx.builder.icmp_signed('>', index, length_i32)):
        #         ctx.error('string index out of bounds')
            
        #     with ctx.builder.if_then(ctx.builder.icmp_signed('<', index, zero(32))):
        #         index = ctx.builder.add(length_i32, index)
            
        #     ptr = get_struct_ptr_field(ctx.builder, s, 0)
        #     index_ptr = ctx.builder.gep(ptr, [index])

        #     value_ptr = get_struct_value_field(ctx.builder, value, 0)
        #     ctx.builder.store(value_ptr, index_ptr)
