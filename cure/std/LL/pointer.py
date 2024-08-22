from cure.objects import Object, Position, Type
from cure.c_manager import c_dec


class Pointer:
    def __init__(self, compiler) -> None:
        compiler.valid_types.append('Pointer')
        
        compiler.add_toplevel_code("""typedef struct {
    void* data;
} Pointer;
""")
    
    @c_dec()
    def _Pointer_type(self, _, call_position: Position) -> Object:
        return Object('"Pointer"', Type('string'), call_position)
    
    @c_dec(param_types=('Pointer',))
    def _Pointer_to_string(self, compiler, call_position: Position, pointer: Object) -> Object:
        ptr = f'({pointer.code})'
        code, buf_free = compiler.c_manager.fmt_length(
            compiler, call_position,
            '%p', ptr
        )
        
        compiler.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    
    
    @c_dec(param_types=('int',), can_user_call=True)
    def _allocate(self, compiler, call_position: Position, size: Object) -> Object:
        ptr = compiler.create_temp_var(Type('Pointer'), call_position)
        compiler.prepend_code(f"""Pointer {ptr};
{ptr}.data = malloc({size.code});
""")
        
        return Object(ptr, Type('Pointer'), call_position)
    
    
    @c_dec(param_types=('int',), is_method=True, is_static=True)
    def _Pointer_new(self, compiler, call_position: Position, size: Object) -> Object:
        return self._allocate(compiler, call_position, size)
    
    @c_dec(param_types=('Pointer', 'int'), is_method=True)
    def _Pointer_reallocate(self, compiler, call_position: Position,
                            pointer: Object, size: Object) -> Object:
        ptr = f'({pointer.code})'
        compiler.prepend_code(f"""{ptr}.data = realloc({ptr}.data, {size.code});
{compiler.c_manager.buf_check(f'{ptr}.data')}
""")
        return Object(pointer.code, Type('Pointer'), call_position)
    
    @c_dec(param_types=('Pointer',), is_method=True)
    def _Pointer_free(self, compiler, call_position: Position, pointer: Object) -> Object:
        compiler.prepend_code(f'free(({pointer.code}).data);')
        return Object('NULL', Type('nil'), call_position)
    
    @c_dec(param_types=('Pointer', 'any'), is_method=True)
    def _Pointer_write(self, compiler, call_position: Position,
                       pointer: Object, data: Object) -> Object:
        data_var = compiler.create_temp_var('string', call_position)
        compiler.prepend_code(f"""{data.type.c_type} {data_var} = {data.code};
memcpy(({pointer.code}).data, (void*)(&{data_var}), sizeof({data_var}));
""")
        return Object('NULL', Type('nil'), call_position)
    
    @c_dec(param_types=('Pointer', 'type'), is_method=True)
    def _Pointer_read(self, _, call_position: Position,
                      pointer: Object, as_type: Object) -> Object:
        return Object(
            f'(*({as_type.code}*)({pointer.code}).data)',
            Type(as_type.code), call_position
        )
