from llvmlite import ir as lir

from cure.ir import Scope, TypeManager, Type, Position, Param, FunctionFlags
from cure.lib import function, Class, ClassField, DefinitionContext
from cure.codegen_utils import (
    cast_value, zero, create_struct_value, get_type_size, get_struct_field_ptr
)


class array(Class):
    def fields(self):
        return [
            ClassField('elements', self.T.as_pointer()),
            ClassField('length', TypeManager.get('int')),
            ClassField('capacity', TypeManager.get('int')),
            ClassField('ref', TypeManager.get('Ref').as_pointer())
        ]
    
    def __init__(self, scope: Scope, *generic_types: Type):
        self.T = generic_types[0]

        self._name = f'array_{self.T}'
        TypeManager.add(f'{self.T}[]', self._create_struct())
        self.type = TypeManager.get(f'{self.T}[]')

        super().__init__(scope, *generic_types)

    def init_class(self):
        @function(self, [Param(Position.zero(), 'capacity', TypeManager.get('int'))],
                  self.type, flags=FunctionFlags(method=True))
        def new(ctx: DefinitionContext):
            capacity = ctx.param_value('capacity')

            malloc = ctx.c_registry.get('malloc')

            capacity_i64 = cast_value(ctx.builder, capacity, lir.IntType(64))
            alloc_size = ctx.builder.mul(capacity_i64, get_type_size(ctx.builder, self.T.type))
            raw_ptr = ctx.builder.call(malloc, [alloc_size])
            data_ptr = cast_value(ctx.builder, raw_ptr, self.T.type.as_pointer())

            length = zero(TypeManager.get('int').type.width)

            func_ptr_type = lir.FunctionType(
                lir.IntType(8).as_pointer(), [lir.IntType(8).as_pointer()]
            ).as_pointer()
            null_func_ptr = lir.Constant(func_ptr_type, None)
            
            ref = ctx.call('Ref_new', [raw_ptr, null_func_ptr])
            return create_struct_value(ctx.builder, self.type.type, [data_ptr, length, capacity, ref])
        
        @function(self, [
            Param(Position.zero(), 'arr', self.type.reference()),
            Param(Position.zero(), 'elem', self.T)
        ], flags=FunctionFlags(method=True))
        def add(ctx: DefinitionContext):
            arr = ctx.param_value('arr')
            elem = ctx.param_value('elem')

            elements_ptr = get_struct_field_ptr(ctx.builder, arr, 0)
            elements = ctx.builder.load(elements_ptr)

            length_ptr = get_struct_field_ptr(ctx.builder, arr, 1)
            length = ctx.builder.load(length_ptr)

            capacity_ptr = get_struct_field_ptr(ctx.builder, arr, 2)
            capacity = ctx.builder.load(capacity_ptr)

            with ctx.builder.if_then(ctx.builder.icmp_signed('>=', length, capacity)):
                ctx.error('array length exceeded capacity')

            elements_ptr = ctx.builder.gep(elements, [length])
            ctx.builder.store(elem, elements_ptr)

            one = lir.Constant(length.type, 1)
            new_length = ctx.builder.add(length, one)

            length_ptr = get_struct_field_ptr(ctx.builder, arr, 1)
            ctx.builder.store(new_length, length_ptr)

        @function(self, [
            Param(Position.zero(), 'arr', self.type),
            Param(Position.zero(), 'index', TypeManager.get('int'))
        ], self.T, flags=FunctionFlags(method=True))
        def get(ctx: DefinitionContext):
            arr = ctx.param_value('arr')
            index = ctx.param_value('index')

            elements = get_struct_field_ptr(ctx.builder, arr, 0)
            length = get_struct_field_ptr(ctx.builder, arr, 1)
            capacity = get_struct_field_ptr(ctx.builder, arr, 2)
            with ctx.builder.if_then(ctx.builder.icmp_signed('>=', length, capacity)):
                ctx.error('array index out of bounds')
            
            elements_ptr = ctx.builder.gep(elements, [index])
            return ctx.builder.load(elements_ptr)
