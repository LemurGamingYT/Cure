from codegen.objects import Object, Position, Free, Type, TempVar, Param
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
        
        def Serialization_from_string_file(codegen, call_position: Position,
                                    filename: Object) -> Object:
            size: TempVar = codegen.create_temp_var(Type('int64', 'long'), call_position)
            buf_free = Free()
            buffer: TempVar = codegen.create_temp_var(Type('any', 'void*'), call_position,
                                                      free=buf_free)
            f: TempVar = codegen.create_temp_var(Type('FilePointer', 'FILE*'), call_position)
            serializer = _Serialization_new(codegen, call_position)
            codegen.prepend_code(f"""void* {buffer} = NULL;
FILE* {f} = fopen({filename}, "rb");
if ({f} == NULL) {{
    {codegen.c_manager.err('Failed to open file for reading')}
}}

fseek({f}, 0, SEEK_END);
long {size} = ftell({f});
fseek({f}, 0, SEEK_SET);
{buffer} = malloc({size});
{codegen.c_manager.buf_check(buffer)}
fread({buffer}, 1, {size}, {f});
{serializer}.b = binn_open({buffer});
fclose({f});
""")
            
            return serializer.OBJECT()
        
        @c_dec(is_method=True, is_static=True, overloads={
            ((Param('file', Type('string')),), Type('Serialization')): Serialization_from_string_file
        }, add_to_class=self)
        def _Serialization_new(codegen, call_position: Position) -> Object:
            obj_free = Free(free_name='binn_free')
            obj: TempVar = codegen.create_temp_var(Type('Serialization'), call_position, free=obj_free)
            obj_free.object_name = f'({obj}).b'
            
            codegen.prepend_code(f'Serialization {obj} = {{ .b = binn_object() }};')
            return obj.OBJECT()
    
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Serialization_type(_, call_position: Position) -> Object:
            return Object('"Serialization"', Type('string'), call_position)

        @c_dec(param_types=(Param('sz', Type('Serialization')),), is_method=True, add_to_class=self)
        def _Serialization_to_string(_, call_position: Position, _obj: Object) -> Object:
            return Object('"class \'Serialization\'"', Type('string'), call_position)
        
        @c_dec(
            param_types=(Param('sz', Type('Serialization')), Param('filename', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _Serialization_to_file(codegen, call_position: Position, obj: Object,
                                filename: Object) -> Object:
            buffer: TempVar = codegen.create_temp_var(Type('any', 'void*'), call_position)
            size: TempVar = codegen.create_temp_var(Type('int'), call_position)
            f: TempVar = codegen.create_temp_var(Type('FilePointer', 'FILE*'), call_position)
            codegen.prepend_code(f"""void* {buffer} = binn_ptr(({obj}).b);
int {size} = binn_size({buffer});
FILE* {f} = fopen({filename}, "wb");
if ({f} == NULL) {{
    {codegen.c_manager.err('Failed to open file for writing')}
}}

fwrite({buffer}, 1, {size}, {f});
fclose({f});
""")
            
            return Object.NULL(call_position)
        
        
        @c_dec(
            param_types=(
                Param('sz', Type('Serialization')), Param('key', Type('string')),
                Param('value', Type('int'))
            ), is_method=True, add_to_class=self
        )
        def _Serialization_write_int(_, call_position: Position, obj: Object, key: Object,
                                    value: Object) -> Object:
            return Object(
                f'((bool)binn_object_set_int32(({obj}).b, {key}, {value}))',
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(Param('sz', Type('Serialization')), Param('key', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _Serialization_read_int(codegen, call_position: Position, obj: Object,
                                    key: Object) -> Object:
            value: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {value};
binn_object_get_int32(({obj}).b, {key}, &{value});
""")
            return value.OBJECT()
        
        @c_dec(
            param_types=(
                Param('sz', Type('Serialization')), Param('key', Type('string')),
                Param('value', Type('float'))
            ), is_method=True, add_to_class=self
        )
        def _Serialization_write_float(_, call_position: Position, obj: Object, key: Object,
                                        value: Object) -> Object:
            return Object(
                f'((bool)binn_object_set_float(({obj}).b, {key}, {value}))',
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(Param('sz', Type('Serialization')), Param('key', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _Serialization_read_float(codegen, call_position: Position, obj: Object,
                                    key: Object) -> Object:
            value: TempVar = codegen.create_temp_var(Type('float'), call_position)
            codegen.prepend_code(f"""float {value};
binn_object_get_float(({obj}).b, {key}, &{value});
""")
            return value.OBJECT()
        
        @c_dec(
            param_types=(
                Param('sz', Type('Serialization')), Param('key', Type('string')),
                Param('value', Type('string'))
            ), is_method=True, add_to_class=self
        )
        def _Serialization_write_string(_, call_position: Position, obj: Object, key: Object,
                                        value: Object) -> Object:
            return Object(
                f'((bool)binn_object_set_str(({obj}).b, {key}, {value}))',
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(Param('sz', Type('Serialization')), Param('key', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _Serialization_read_string(codegen, call_position: Position, obj: Object,
                                        key: Object) -> Object:
            value: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""string {value};
binn_object_get_str(({obj}).b, {key}, &{value});
""")
            return value.OBJECT()
        
        @c_dec(
            param_types=(
                Param('sz', Type('Serialization')), Param('key', Type('string')),
                Param('value', Type('bool'))
            ), is_method=True, add_to_class=self
        )
        def _Serialization_write_bool(_, call_position: Position, obj: Object, key: Object,
                                        value: Object) -> Object:
            return Object(
                f'((bool)binn_object_set_bool(({obj}).b, {key}, {value}))',
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(Param('sz', Type('Serialization')), Param('key', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _Serialization_read_bool(codegen, call_position: Position, obj: Object,
                                        key: Object) -> Object:
            value: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {value};
binn_object_get_bool(({obj}).b, {key}, &{value});
""")
            return value.OBJECT()
        
        @c_dec(
            param_types=(Param('sz', Type('Serialization')), Param('key', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _Serialization_write_nil(_, call_position: Position, obj: Object,
                                        key: Object) -> Object:
            return Object(
                f'((bool)binn_object_set_null(({obj}).b, {key}))',
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(Param('sz', Type('Serialization')), Param('key', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _Serialization_read_nil(_, call_position: Position, obj: Object,
                                    key: Object) -> Object:
            return Object(
                f'((bool)binn_object_get_null(({obj}).b, {key}))',
                Type('nil'), call_position
            )
