from logging import debug
from typing import cast

from llvmlite import ir as lir

from cure.codegen_utils import set_struct_field, get_struct_ptr_field, NULL, get_type_size, cast_value
from cure.ir import Param, Position, FunctionFlags, Type
from cure.lib import function, Class, DefinitionContext


class Ref(Class):
    def fields(self):
        return []

    def init_class(self):
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('pointer'), 'data'),
            Param(Position.zero(), self.scope.type_map.get('any_function'), 'destroy_fn')
        ], self.scope.type_map.get('Ref').as_pointer(), flags=FunctionFlags(static=True, method=True))
        def new(ctx: DefinitionContext):
            malloc = ctx.c_registry.get('malloc')

            data = ctx.param_value('data')
            destroy_fn = ctx.param_value('destroy_fn')

            ref_type = cast(Type, self.scope.type_map.get('Ref'))
            struct_size = get_type_size(ctx.builder, ref_type.type)

            ptr = cast_value(
                ctx.builder,
                ctx.builder.call(malloc, [struct_size]), 
                ref_type.type.as_pointer()
            )

            debug('Allocating Ref pointer')

            destroy_fn = lir.Constant.bitcast(destroy_fn, lir.FunctionType(
                lir.IntType(8).as_pointer(), [lir.IntType(8).as_pointer()]
            ).as_pointer())
            
            set_struct_field(ctx.builder, ptr, 0, data)
            set_struct_field(ctx.builder, ptr, 1, destroy_fn)
            set_struct_field(ctx.builder, ptr, 2, lir.Constant(lir.IntType(64), 1))

            return ptr
        
        @function(self, [Param(Position.zero(), self.scope.type_map.get('Ref').as_pointer(), 'self')],
                flags=FunctionFlags(method=True))
        def inc(ctx: DefinitionContext):
            self = ctx.param_value('self')

            ref_count_ptr = get_struct_ptr_field(ctx.builder, self, 2)
            debug(f'Incrementing Ref pointer {self}')

            ref_count = ctx.builder.load(ref_count_ptr)
            one = lir.Constant(lir.IntType(64), 1)
            new_count = ctx.builder.add(ref_count, one)
            ctx.builder.store(new_count, ref_count_ptr)
        
        @function(self, [Param(Position.zero(), self.scope.type_map.get('Ref').as_pointer(), 'self')],
                flags=FunctionFlags(method=True))
        def dec(ctx: DefinitionContext):
            self = ctx.param_value('self')

            ref_count_ptr = get_struct_ptr_field(ctx.builder, self, 2)
            ref_count = ctx.builder.load(ref_count_ptr)
            one = lir.Constant(lir.IntType(64), 1)
            new_count = ctx.builder.sub(ref_count, one)
            ctx.builder.store(new_count, ref_count_ptr)
            debug('Decrementing Ref pointer')

            zero = lir.Constant(lir.IntType(64), 0)
            with ctx.builder.if_then(ctx.builder.icmp_signed('==', new_count, zero)):
                free = ctx.c_registry.get('free')

                data_ptr_ptr = get_struct_ptr_field(ctx.builder, self, 0)
                data_ptr = ctx.builder.load(data_ptr_ptr)
                
                destroy_fn_ptr = get_struct_ptr_field(ctx.builder, self, 1)
                destroy_fn = ctx.builder.load(destroy_fn_ptr)
                
                func_ptr_type = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer()
                ]).as_pointer()
                null_func_ptr = lir.Constant(func_ptr_type, None)
                
                with ctx.builder.if_else(ctx.builder.icmp_signed('!=', destroy_fn, null_func_ptr))\
                    as (then, else_):
                    with then:
                        ctx.builder.call(destroy_fn, [data_ptr])
                    
                    with else_:
                        ctx.builder.call(free, [data_ptr])
                
                ctx.builder.store(NULL(), data_ptr_ptr)
                ctx.builder.call(free, [cast_value(ctx.builder, self, lir.IntType(8).as_pointer())])
