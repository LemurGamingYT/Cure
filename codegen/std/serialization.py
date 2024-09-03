from codegen.objects import Object, Position, Free, Type
from codegen.c_manager import c_dec, INCLUDES


class serialization:
    def __init__(self, codegen) -> None:
        codegen.valid_types.append('Serialization')
        codegen.extra_compile_args.append(INCLUDES / 'binn/binn.c')
        codegen.c_manager.include(f'"{INCLUDES / "binn/binn.h"}"', codegen)
        
        codegen.add_toplevel_code("""#ifndef CURE_SERIALIZATION_H
typedef struct {
    binn* b;
} Serialization;
#define CURE_SERIALIZATION_H
#endif
""")
        
        def Serialization_from_file(codegen, call_position: Position,
                                    filename: Object) -> Object:
            size = codegen.create_temp_var(Type('long'), call_position)
            buf_free = Free()
            buffer = codegen.create_temp_var(Type('any', 'void*'), call_position, free=buf_free)
            f = codegen.create_temp_var(Type('FILE*'), call_position)
            obj_free = Free(free_name='binn_free')
            obj = codegen.create_temp_var(Type('Serialization'), call_position, free=obj_free)
            obj_free.object_name = f'({obj}).b'
            codegen.prepend_code(f"""Serialization {obj} = {{ .b = NULL }};
void* {buffer} = NULL;

FILE* {f} = fopen({filename.code}, "rb");
if ({f} == NULL) {{
    {codegen.c_manager.err('Failed to open file for reading')}
}}

fseek({f}, 0, SEEK_END);
long {size} = ftell({f});
fseek({f}, 0, SEEK_SET);
{buffer} = malloc({size});
{codegen.c_manager.buf_check(buffer)}
fread({buffer}, 1, {size}, {f});
{obj}.b = binn_open({buffer});
fclose({f});
""")
            
            return Object(obj, Type('Serialization'), call_position, free=obj_free)
        
        @c_dec(param_types=(), is_method=True, is_static=True, overloads={
            (('string',), 'Serialization'): Serialization_from_file
        }, add_to_class=self)
        def _Serialization_new(codegen, call_position: Position) -> Object:
            obj_free = Free(free_name='binn_free')
            obj = codegen.create_temp_var(Type('Serialization'), call_position, free=obj_free)
            obj_free.object_name = f'({obj}).b'
            
            codegen.prepend_code(f'Serialization {obj} = {{ .b = binn_object() }};')
            return Object(obj, Type('Serialization'), call_position, free=obj_free)
    
    @c_dec(is_method=True, is_static=True)
    def _Serialization_type(self, _, call_position: Position) -> Object:
        return Object('"Serialization"', Type('string'), call_position)

    @c_dec(param_types=('Serialization',), is_method=True)
    def _Serialization_to_string(self, _, call_position: Position, _obj: Object) -> Object:
        return Object('"class \'Serialization\'"', Type('string'), call_position)
    
    @c_dec(param_types=('Serialization', 'string'), is_method=True)
    def _Serialization_to_file(self, codegen, call_position: Position, obj: Object,
                               filename: Object) -> Object:
        buffer = codegen.create_temp_var(Type('any', 'void*'), call_position)
        size = codegen.create_temp_var(Type('int'), call_position)
        f = codegen.create_temp_var(Type('FILE*'), call_position)
        codegen.prepend_code(f"""void* {buffer} = binn_ptr(({obj.code}).b);
int {size} = binn_size({buffer});
FILE* {f} = fopen({filename.code}, "wb");
if ({f} == NULL) {{
    {codegen.c_manager.err('Failed to open file for writing')}
}}

fwrite({buffer}, 1, {size}, {f});
fclose({f});
""")
        
        return Object.NULL(call_position)
    
    
    @c_dec(param_types=('Serialization', 'string', 'int'), is_method=True)
    def _Serialization_write_int(self, _, call_position: Position, obj: Object, key: Object,
                                 value: Object) -> Object:
        return Object(
            f'((bool)binn_object_set_int32(({obj.code}).b, {key.code}, {value.code}))',
            Type('bool'), call_position
        )
    
    @c_dec(param_types=('Serialization', 'string'), is_method=True)
    def _Serialization_read_int(self, codegen, call_position: Position, obj: Object,
                                key: Object) -> Object:
        value = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""int {value};
binn_object_get_int32(({obj.code}).b, {key.code}, &{value});
""")
        return Object(value, Type('int'), call_position)
    
    @c_dec(param_types=('Serialization', 'string', 'float'), is_method=True)
    def _Serialization_write_float(self, _, call_position: Position, obj: Object, key: Object,
                                   value: Object) -> Object:
        return Object(
            f'((bool)binn_object_set_float(({obj.code}).b, {key.code}, {value.code}))',
            Type('bool'), call_position
        )
    
    @c_dec(param_types=('Serialization', 'string'), is_method=True)
    def _Serialization_read_float(self, codegen, call_position: Position, obj: Object,
                                  key: Object) -> Object:
        value = codegen.create_temp_var(Type('float'), call_position)
        codegen.prepend_code(f"""float {value};
binn_object_get_float(({obj.code}).b, {key.code}, &{value});
""")
        return Object(value, Type('float'), call_position)
    
    @c_dec(param_types=('Serialization', 'string', 'string'), is_method=True)
    def _Serialization_write_string(self, _, call_position: Position, obj: Object, key: Object,
                                    value: Object) -> Object:
        return Object(
            f'((bool)binn_object_set_str(({obj.code}).b, {key.code}, {value.code}))',
            Type('bool'), call_position
        )
    
    @c_dec(param_types=('Serialization', 'string'), is_method=True)
    def _Serialization_read_string(self, codegen, call_position: Position, obj: Object,
                                   key: Object) -> Object:
        value = codegen.create_temp_var(Type('string'), call_position)
        codegen.prepend_code(f"""string {value};
binn_object_get_str(({obj.code}).b, {key.code}, &{value});
""")
        return Object(value, Type('string'), call_position)
    
    @c_dec(param_types=('Serialization', 'string', 'bool'), is_method=True)
    def _Serialization_write_bool(self, _, call_position: Position, obj: Object, key: Object,
                                  value: Object) -> Object:
        return Object(
            f'((bool)binn_object_set_bool(({obj.code}).b, {key.code}, {value.code}))',
            Type('bool'), call_position
        )
    
    @c_dec(param_types=('Serialization', 'string'), is_method=True)
    def _Serialization_read_bool(self, codegen, call_position: Position, obj: Object,
                                 key: Object) -> Object:
        value = codegen.create_temp_var(Type('bool'), call_position)
        codegen.prepend_code(f"""bool {value};
binn_object_get_bool(({obj.code}).b, {key.code}, &{value});
""")
        return Object(value, Type('bool'), call_position)
    
    @c_dec(param_types=('Serialization', 'string'), is_method=True)
    def _Serialization_write_nil(self, _, call_position: Position, obj: Object,
                                 key: Object) -> Object:
        return Object(
            f'((bool)binn_object_set_null(({obj.code}).b, {key.code}))',
            Type('bool'), call_position
        )
    
    @c_dec(param_types=('Serialization', 'string'), is_method=True)
    def _Serialization_read_nil(self, _, call_position: Position, obj: Object,
                                key: Object) -> Object:
        return Object(
            f'((bool)binn_object_get_null(({obj.code}).b, {key.code}))',
            Type('nil'), call_position
        )
