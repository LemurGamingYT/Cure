from codegen.objects import Object, Position, Type, TempVar, Param, Stringable
from codegen.c_manager import c_dec


class Pointer:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""typedef struct {
    void* data;
    bool is_freed;
} Pointer;
""")
        
        codegen.c_manager.init_class(self, 'Pointer', Type('Pointer'))
        codegen.type_checker.add_type('Pointer')
        
        def check_pointer(codegen, pointer: Stringable) -> None:
            codegen.prepend_code(f"""if (({pointer}).is_freed || ({pointer}).data == NULL) {{
    {codegen.c_manager.err('Pointer has been freed')}
}}
""")
        
        @c_dec(params=(Param('ptr', Type('Pointer')),), is_method=True, add_to_class=self)
        def _Pointer_to_string(codegen, call_position: Position, ptr: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position,
                '"0x%p"', f'({ptr}).data'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(params=(Param('size_bytes', Type('int')),), can_user_call=True, add_to_class=self)
        def _allocate(codegen, call_position: Position, size_bytes: Object) -> Object:
            ptr: TempVar = codegen.create_temp_var(Type('Pointer'), call_position)
            codegen.prepend_code(f"""Pointer {ptr} = {{
    .data = malloc({size_bytes}), .is_freed = false
}};
""")
            return ptr.OBJECT()
        
        
        @c_dec(
            params=(Param('size_bytes', Type('int')),), is_method=True, is_static=True,
            add_to_class=self
        )
        def _Pointer_new(codegen, call_position: Position, size_bytes: Object) -> Object:
            return _allocate(codegen, call_position, size_bytes)
        
        @c_dec(
            params=(Param('size', Type('int')),), is_method=True, is_static=True,
            add_to_class=self
        )
        def _Pointer_zero(codegen, call_position: Position, size: Object) -> Object:
            ptr = _Pointer_new(codegen, call_position, size)
            codegen.prepend_code(f'memset(({ptr}).data, 0, {size});')
            return ptr
        
        @c_dec(
            params=(Param('ptr', Type('Pointer')), Param('size', Type('int'))),
            is_method=True, add_to_class=self
        )
        def _Pointer_reallocate(codegen, _: Position,
                                pointer: Object, size: Object) -> Object:
            check_pointer(codegen, pointer)
            codegen.prepend_code(f"""({pointer}).data = realloc(({pointer}).data, {size});
{codegen.c_manager.buf_check(f'({pointer}).data')}
""")
            
            return pointer
        
        @c_dec(params=(Param('ptr', Type('Pointer')),), is_method=True, add_to_class=self)
        def _Pointer_free(codegen, call_position: Position, pointer: Object) -> Object:
            check_pointer(codegen, pointer)
            codegen.prepend_code(f"""free(({pointer}).data);
({pointer}).is_freed = true;
""")
            return Object.NULL(call_position)
        
        @c_dec(
            params=(Param('ptr', Type('Pointer')), Param('data', Type('any'))),
            is_method=True, add_to_class=self
        )
        def _Pointer_write(codegen, call_position: Position, pointer: Object, data: Object) -> Object:
            check_pointer(codegen, pointer)
            data_var = codegen.create_temp_var('string', call_position)
            codegen.prepend_code(f"""{data.type.c_type} {data_var} = {data};
memcpy(({pointer}).data, &{data_var}, sizeof({data_var}));
""")
            return Object.NULL(call_position)
        
        @c_dec(
            params=(Param('ptr', Type('Pointer')),),
            is_method=True, add_to_class=self, generic_params=('T',), return_type=Type('{T}')
        )
        def _Pointer_read(codegen, call_position: Position, pointer: Object, *, T: Type) -> Object:
            check_pointer(codegen, pointer)
            return Object(f'(*({T}*)({pointer}).data)', T, call_position)
        
        @c_dec(
            params=(Param('ptr', Type('Pointer')), Param('src', Type('any')),),
            is_method=True, add_to_class=self
        )
        def _Pointer_copy(codegen, call_position: Position, pointer: Object, src: Object) -> Object:
            check_pointer(codegen, pointer)
            src_var: TempVar = codegen.create_temp_var(Type('any'), call_position)
            codegen.prepend_code(f"""{src.type.c_type} {src_var} = {src};
memcpy(({pointer}).data, &{src_var}, sizeof({src_var}));
""")
            return Object.NULL(call_position)
        
        @c_dec(
            params=(Param('ptr', Type('Pointer')), Param('value', Type('any')),
                    Param('size', Type('int')),),
            is_method=True, add_to_class=self
        )
        def _Pointer_set(codegen, call_position: Position, pointer: Object, value: Object,
                         size: Object) -> Object:
            check_pointer(codegen, pointer)
            codegen.prepend_code(f'memset(({pointer}).data, {value}, {size});')
            return Object.NULL(call_position)
        
        @c_dec(
            params=(Param('ptr', Type('Pointer')), Param('offset', Type('int'))),
            is_method=True, add_to_class=self
        )
        def _Pointer_offset(codegen, call_position: Position, pointer: Object,
                            offset: Object) -> Object:
            check_pointer(codegen, pointer)
            codegen.prepend_code(f'((char*)({pointer}).data) += {offset};')
            return Object.NULL(call_position)
        
        @c_dec(
            params=(Param('ptr', Type('Pointer')), Param('other', Type('Pointer'))),
            is_method=True, add_to_class=self
        )
        def _Pointer_swap(codegen, call_position: Position, pointer: Object, other: Object) -> Object:
            check_pointer(codegen, pointer)
            check_pointer(codegen, other)
            other_data = other.attr('data')
            pointer_data = pointer.attr('data')
            codegen.prepend_code(f"""memcpy({pointer_data}, {other_data}, sizeof({pointer_data}));
memcpy({other_data}, {pointer_data}, sizeof({pointer_data}));
memcpy({pointer_data}, {other_data}, sizeof({pointer_data}));
""")
            
            return Object.NULL(call_position)
