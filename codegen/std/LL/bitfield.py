from codegen.objects import Object, Type, Position, Param, TempVar, Free
from codegen.c_manager import c_dec


BITS_PER_WORD = 32


class BitField:
    def __init__(self, codegen) -> None:
        codegen.add_type('BitField')
        codegen.add_toplevel_code("""#ifndef CURE_LL_H
typedef struct {
    unsigned int *bits;
    size_t num_of_bits;
} BitField;
#endif
""")
        
        codegen.c_manager.wrap_struct_properties('field', Type('BitField'), [
            Param('num_of_bits', Type('int'))
        ])
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _BitField_type(_, call_position: Position) -> Object:
            return Object('"BitField"', Type('string'), call_position)
        
        @c_dec(param_types=(Param('field', Type('BitField')),), is_method=True, add_to_class=self)
        def _BitField_to_string(codegen, call_position: Position, field: Object) -> Object:
            builder: Object = codegen.c_manager._StringBuilder_new(codegen, call_position)
            i: TempVar = codegen.create_temp_var(Type('size_t'), call_position)
            word_index = f'{i} / {BITS_PER_WORD}'
            bit_index = f'{i} % {BITS_PER_WORD}'
            codegen.prepend_code(f"""for (size_t {i} = 0; {i} < ({field}).num_of_bits; {i}++) {{
""")
            codegen.c_manager._StringBuilder_add(
                codegen, call_position, builder, Object(
                    f'({field}).bits[{word_index}] & (1U << {bit_index}) ? "1" : "0"',
                    Type('string'), call_position
                )
            )
            codegen.prepend_code('}')
            
            return codegen.c_manager._StringBuilder_str(codegen, call_position, builder)
        
        
        @c_dec(
            param_types=(Param('a', Type('BitField')), Param('b', Type('BitField'))),
            add_to_class=self
        )
        def _BitField_and_BitField(codegen, call_position: Position, a: Object, b: Object) -> Object:
            res: Object = _BitField_new(
                codegen, call_position,
                Object(f'({a}).num_of_bits', Type('int'), call_position)
            )
            i: TempVar = codegen.create_temp_var(Type('size_t'), call_position)
            num_words = f'(({a}).num_of_bits + {BITS_PER_WORD} - 1) / {BITS_PER_WORD}'
            
            codegen.prepend_code(f"""if (({a}).num_of_bits != ({b}).num_of_bits) {{
    {codegen.c_manager.err('BitField sizes do not match')}
}}

for (size_t {i} = 0; {i} < {num_words}; {i}++) {{
    {res}.bits[{i}] = ({a}).bits[{i}] & ({b}).bits[{i}];
}}
""")
            
            return res
        
        @c_dec(
            param_types=(Param('a', Type('BitField')), Param('b', Type('BitField'))),
            add_to_class=self
        )
        def _BitField_or_BitField(codegen, call_position: Position, a: Object, b: Object) -> Object:
            res: Object = _BitField_new(
                codegen, call_position,
                Object(f'({a}).num_of_bits', Type('int'), call_position)
            )
            i: TempVar = codegen.create_temp_var(Type('size_t'), call_position)
            num_words = f'(({a}).num_of_bits + {BITS_PER_WORD} - 1) / {BITS_PER_WORD}'
            
            codegen.prepend_code(f"""if (({a}).num_of_bits != ({b}).num_of_bits) {{
    {codegen.c_manager.err('BitField sizes do not match')}
}}

for (size_t {i} = 0; {i} < {num_words}; {i}++) {{
    {res}.bits[{i}] = ({a}).bits[{i}] | ({b}).bits[{i}];
}}
""")
            
            return res
        
        
        @c_dec(
            param_types=(Param('field', Type('BitField')), Param('index', Type('int')),),
            is_method=True, add_to_class=self
        )
        def _BitField_get(codegen, call_position: Position, field: Object, index: Object) -> Object:
            word_index = f'({index}) / {BITS_PER_WORD}'
            bit_index = f'({index}) % {BITS_PER_WORD}'
            codegen.prepend_code(f"""if (({index}) >= ({field}).num_of_bits) {{
    {codegen.c_manager.err('Index out of bounds')}
}}
""")
            
            return Object(
                f'(bool)(({field}).bits[{word_index}] & (1U << {bit_index}))',
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(
                Param('field', Type('BitField')), Param('index', Type('int')),
                Param('value', Type('bool'))
            ), is_method=True, add_to_class=self
        )
        def _BitField_set(codegen, call_position: Position, field: Object, index: Object,
                          value: Object) -> Object:
            word_index = f'({index}) / {BITS_PER_WORD}'
            bit_index = f'({index}) % {BITS_PER_WORD}'
            codegen.prepend_code(f"""if (({index}) >= ({field}).num_of_bits) {{
    {codegen.c_manager.err('Index out of bounds')}
}}

if ({value}) {{
    ({field}).bits[{word_index}] |= (1U << {bit_index});
}} else {{
    ({field}).bits[{word_index}] &= ~(1U << {bit_index});
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('size', Type('int')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _BitField_new(codegen, call_position: Position, size: Object) -> Object:
            field_free = Free()
            field: TempVar = codegen.create_temp_var(Type('BitField'), call_position, free=field_free)
            field_free.object_name = f'{field}.bits'
            codegen.prepend_code(f"""BitField {field} = {{
    .num_of_bits = {size},
    .bits = calloc(({size} + {BITS_PER_WORD} - 1) / {BITS_PER_WORD}, sizeof(unsigned int))
}};
""")
            
            return field.OBJECT()
