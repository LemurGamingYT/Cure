from codegen.objects import Object, Position, Type, TempVar, Param
from codegen.c_manager import c_dec


class Pointer:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""typedef struct {
    void* data;
} Pointer;
""")
        
        codegen.c_manager.init_class(self, 'Pointer', Type('Pointer'))
        codegen.type_checker.add_type('Pointer')
        
        @c_dec(param_types=(Param('ptr', Type('Pointer')),), is_method=True, add_to_class=self)
        def _Pointer_to_string(codegen, call_position: Position, ptr: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position,
                '"0x%p"', f'({ptr}).data'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(param_types=(Param('size', Type('int')),), can_user_call=True, add_to_class=self)
        def _allocate(codegen, call_position: Position, size: Object) -> Object:
            ptr: TempVar = codegen.create_temp_var(Type('Pointer'), call_position)
            codegen.prepend_code(f'Pointer {ptr} = {{ .data = malloc({size}) }};')
            return ptr.OBJECT()
        
        
        @c_dec(
            param_types=(Param('size', Type('int')),), is_method=True, is_static=True,
            add_to_class=self
        )
        def _Pointer_new(codegen, call_position: Position, size: Object) -> Object:
            return _allocate(codegen, call_position, size)
        
        @c_dec(
            param_types=(Param('ptr', Type('Pointer')), Param('size', Type('int'))),
            is_method=True, add_to_class=self
        )
        def _Pointer_reallocate(codegen, _: Position,
                                pointer: Object, size: Object) -> Object:
            ptr = f'({pointer})'
            codegen.prepend_code(f"""{ptr}.data = realloc({ptr}.data, {size});
{codegen.c_manager.buf_check(f'{ptr}.data')}
""")
            
            return pointer
        
        @c_dec(param_types=(Param('ptr', Type('Pointer')),), is_method=True, add_to_class=self)
        def _Pointer_free(codegen, call_position: Position, ptr: Object) -> Object:
            codegen.prepend_code(f'free(({ptr}).data);')
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('ptr', Type('Pointer')), Param('data', Type('any'))),
            is_method=True, add_to_class=self
        )
        def _Pointer_write(codegen, call_position: Position, pointer: Object, data: Object) -> Object:
            data_var = codegen.create_temp_var('string', call_position)
            codegen.prepend_code(f"""{data.type.c_type} {data_var} = {data};
memcpy(({pointer}).data, (void*)(&{data_var}), sizeof({data_var}));
""")
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('ptr', Type('Pointer')),),
            is_method=True, add_to_class=self, generic_params=('T',), return_type=Type('{T}')
        )
        def _Pointer_read(_, call_position: Position, pointer: Object, *, T: Type) -> Object:
            return Object(f'(*({T}*)({pointer}).data)', T, call_position)
