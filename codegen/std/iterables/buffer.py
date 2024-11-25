from codegen.objects import Object, Position, Type, Param, TempVar
# from codegen.function_manager import OverloadKey, OverloadValue
from codegen.array_manager import get_index
from codegen.c_manager import c_dec


class buffer:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        codegen.type_checker.add_type('Buffer')
        
        @c_dec(
            params=(Param('size', Type('int')),),
            add_to_class=self, is_method=True, is_static=True, generic_params=('T',),
            return_type=Type('Buffer[{T}]')
        )
        def _Buffer_new(codegen, call_position: Position, size: Object, *, T: Type) -> Object:
            if not codegen.is_number_constant(size):
                call_position.error_here('Buffer size must be a constant integer size')
            
            buf_type = self.define_buffer_type(T, size)
            return codegen.call(f'{buf_type.c_type}_make', [], call_position)
    
    def define_buffer_type(self, type: Type, size: Object) -> Type:
        buf_type = Type(f'{str(type).title()}Buffer[{size}]', f'{type.c_type}_buffer{size}')
        if self.codegen.type_checker.is_valid_type(buf_type):
            return buf_type
        
        self.codegen.add_toplevel_code(f"""typedef struct {{
    {type.c_type} elements[{size}];
    size_t length;
}} {buf_type.c_type};
""")
        
        c_manager = self.codegen.c_manager
        
        c_manager.init_class(self, str(buf_type), buf_type)
        c_manager.wrap_struct_properties('buf', buf_type, [
            Param('length', Type('int'))
        ])
        
        @c_dec(add_to_class=c_manager, func_name_override=f'{buf_type.c_type}_make')
        def make_buf(codegen, call_position: Position) -> Object:
            buf: TempVar = codegen.create_temp_var(buf_type, call_position)
            codegen.prepend_code(f"""{buf_type.c_type} {buf} = {{ .elements = {{ 0 }} }};
""")
            
            return buf.OBJECT()
        
        @c_dec(
            params=(Param('buf', buf_type),), is_method=True,
            func_name_override=f'{buf_type.c_type}_to_string', add_to_class=c_manager,
        )
        def to_string(codegen, call_position: Position, buf: Object) -> Object:
            builder: Object = codegen.c_manager._StringBuilder_new(codegen, call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('"Buffer("', Type('string'), call_position)
)};
for (size_t {i} = 0; {i} < ({buf}).length; {i}++) {{
""")
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, codegen.c_manager._to_string(
        codegen, call_position, Object(f'({buf}).elements[{i}]', type, call_position)
    )
)};

if ({i} < ({buf}).length - 1) {{
""")
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('", "', Type('string'), call_position)
)};
}}
}}
""")
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('")"', Type('string'), call_position)
)};
""")
            
            return codegen.c_manager._StringBuilder_str(codegen, call_position, builder)
        
        @c_dec(
            params=(Param('buf', buf_type),), is_property=True,
            func_name_override=f'{buf_type.c_type}_size', add_to_class=c_manager
        )
        def size_(_, call_position: Position, _buf: Object) -> Object:
            return Object(f'{size}', Type('int'), call_position)
        
        @c_dec(
            params=(Param('buf', buf_type), Param('i', Type('int')),),
            is_method=True, func_name_override=f'{buf_type.c_type}_get', add_to_class=c_manager
        )
        def get(codegen, call_position: Position, buf: Object, i: Object) -> Object:
            code, idx = get_index(codegen, call_position, i, f'({buf}).length')
            
            codegen.prepend_code(code)
            return Object(f'({buf}).elements[{idx}]', type, call_position)

        # TODO: reimplement buffer insert
        
        @c_dec(
            params=(Param('buf', buf_type), Param('value', type)),
            is_method=True, func_name_override=f'{buf_type.c_type}_add', add_to_class=c_manager,
            # overloads={
            #     OverloadKey(Type('nil'),
            #         (Param('buf', buf_type), Param('i', Type('int')), Param('value', type)),
            #     ): OverloadValue(insert)
            # }
        )
        def add(codegen, call_position: Position, buf: Object, value: Object) -> Object:
            codegen.prepend_code(f"""if (({buf}).length >= {size}) {{
    {codegen.c_manager.err('Buffer overflow')}
}}
""")

            codegen.prepend_code(f"""({buf}).elements[({buf}).length++] = {value};
""")

            return Object.NULL(call_position)
        
        self.codegen.type_checker.add_type(buf_type)
        return buf_type
