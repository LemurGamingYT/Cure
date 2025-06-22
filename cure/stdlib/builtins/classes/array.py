from llvmlite import ir as lir

from cure.codegen_utils import get_struct_field_value, cast_value, create_struct_value, zero, NULL
from cure.ir import Param, Position, TypeManager, FunctionFlags
from cure.lib import function, Class, DefinitionContext


class array(Class):
    def fields(self):
        return []
    
    @function([
        Param(Position.zero(), 'capacity', TypeManager.get('int')),
        Param(Position.zero(), 'element_size', TypeManager.get('int'))
    ], TypeManager.get('array'), flags=FunctionFlags(method=True))
    @staticmethod
    def array_new(ctx: DefinitionContext):
        malloc = ctx.c_registry.get('malloc')

        capacity = ctx.param('capacity').value
        element_size = ctx.param('element_size').value

        total_size = ctx.builder.mul(capacity, element_size)
        data_ptr = ctx.builder.call(malloc, [cast_value(ctx.builder, total_size, lir.IntType(64))])

        func_ptr_type = lir.FunctionType(
            lir.IntType(8).as_pointer(), [lir.IntType(8).as_pointer()]
        ).as_pointer()

        ref = ctx.call('Ref_new', [data_ptr, NULL(func_ptr_type)])
        array_type = TypeManager.get('array').type
        return create_struct_value(ctx.builder, array_type, [
            data_ptr, zero(64),
            cast_value(ctx.builder, capacity, lir.IntType(64)),
            cast_value(ctx.builder, element_size, lir.IntType(64)),
            ref
        ])
    
    @function([
        Param(Position.zero(), 'arr', TypeManager.get('array')),
        Param(Position.zero(), 'index', TypeManager.get('int'))
    ], TypeManager.get('any'), flags=FunctionFlags(method=True))
    @staticmethod
    def array_get(ctx: DefinitionContext):
        arr = ctx.param('arr').value
        index = ctx.param('index').value

        data_ptr = get_struct_field_value(ctx.builder, arr, 0)
        length = get_struct_field_value(ctx.builder, arr, 1)
        element_size = get_struct_field_value(ctx.builder, arr, 3)

        idx_64 = cast_value(ctx.builder, index, lir.IntType(64))
        with ctx.builder.icmp_signed('>=', idx_64, length):
            ctx.error('index out of bounds')
        
        offset = ctx.builder.mul(idx_64, element_size)
        return ctx.builder.gep(data_ptr, [offset])

    @function([
        Param(Position.zero(), 'arr', TypeManager.get('array')),
        Param(Position.zero(), 'value', TypeManager.get('any'))
    ], flags=FunctionFlags(method=True))
    @staticmethod
    def array_add(ctx: DefinitionContext):
        arr = ctx.param('arr').value
        value = ctx.param('value').value

        realloc = ctx.c_registry.get('realloc')
        memcpy = ctx.c_registry.get('memcpy')

        data_ptr = get_struct_field_value(ctx.builder, arr, 0)
        length = get_struct_field_value(ctx.builder, arr, 1)
        capacity = get_struct_field_value(ctx.builder, arr, 2)
        element_size = get_struct_field_value(ctx.builder, arr, 3)
        with ctx.builder.if_then(ctx.builder.icmp_signed('>=', length, capacity)):
            new_capacity = ctx.builder.mul(capacity, lir.Constant(lir.IntType(64), 2))
            new_size = ctx.builder.mul(new_capacity, element_size)
            new_data = ctx.builder.call(realloc, [data_ptr, new_size])
            arr = ctx.builder.insert_value(arr, new_data, 0)
            arr = ctx.builder.insert_value(arr, new_capacity, 2)
            data_ptr = new_data
        
        offset = ctx.builder.mul(length, element_size)
        element_ptr = ctx.builder.gep(data_ptr, [offset])
        ctx.builder.call(memcpy, [element_ptr, value, element_size])

        new_length = ctx.builder.add(length, lir.Constant(lir.IntType(64), 1))
        arr = ctx.builder.insert_value(arr, new_length, 1)
