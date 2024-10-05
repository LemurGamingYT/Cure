from codegen.objects import Object, Position, Free, Type, TempVar, Param
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec, INCLUDES


class serialization:
    def __init__(self, codegen) -> None:
        codegen.add_type('Serialization')
        codegen.extra_compile_args.append(INCLUDES / 'binn/binn.c')
        codegen.c_manager.include(f'"{INCLUDES / "binn/binn.h"}"', codegen)
        codegen.c_manager.reserve((
            'BINN_H', 'BINN_VERSION', 'TRUE', 'FALSE', 'BOOL', 'APIENTRY', 'BINN_PRIVATE', 'INLINE',
            'ALWAYS_INLINE', 'int64', 'uint64', 'INT64_FORMAT', 'UINT64_FORMAT', 'INT64_HEX_FORMAT',
            'INVALID_BINN', 'BINN_STORAGE_NOBYTES', 'BINN_STORAGE_BYTE', 'BINN_STORAGE_WORD',
            'BINN_STORAGE_DWORD', 'BINN_STORAGE_QWORD', 'BINN_STORAGE_STRING', 'BINN_STORAGE_BLOB',
            'BINN_STORAGE_CONTAINER', 'BINN_STORAGE_VIRTUAL', 'BINN_STORAGE_MIN', 'BINN_STORAGE_MAX',
            'BINN_STORAGE_MASK', 'BINN_STORAGE_MASK16', 'BINN_STORAGE_HAS_MORE', 'BINN_TYPE_MASK',
            'BINN_TYPE_MASK16', 'BINN_MAX_VALUE_MASK', 'BINN_LIST', 'BINN_MAP', 'BINN_OBJECT',
            'BINN_NULL', 'BINN_TRUE', 'BINN_FALSE', 'BINN_UINT8', 'BINN_INT8', 'BINN_UINT16',
            'BINN_INT16', 'BINN_UINT32', 'BINN_INT32', 'BINN_UINT64', 'BINN_INT64', 'BINN_SCHAR',
            'BINN_UCHAR', 'BINN_STRING', 'BINN_DATETIME', 'BINN_DATE', 'BINN_TIME', 'BINN_DECIMAL',
            'BINN_CURRENCYSTR', 'BINN_SINGLE_STR', 'BINN_DOUBLE_STR', 'BINN_FLOAT32', 'BINN_FLOAT64',
            'BINN_FLOAT', 'BINN_SINGLE', 'BINN_DOUBLE', 'BINN_CURRENCY', 'BINN_BLOB', 'BINN_BOOL',
            'BINN_EXTENDED', 'BINN_HTML', 'BINN_XML', 'BINN_JSON', 'BINN_JAVASCRIPT', 'BINN_CSS',
            'BINN_JPEG', 'BINN_GIF', 'BINN_PNG', 'BINN_BMP', 'BINN_FAMILY_NONE', 'BINN_FAMILY_NULL',
            'BINN_FAMILY_INT', 'BINN_FAMILY_FLOAT', 'BINN_FAMILY_STRING', 'BINN_FAMILY_BLOB',
            'BINN_FAMILY_BINN', 'BINN_FAMILY_BOOL', 'BINN_SIGNED_INT', 'BINN_UNSIGNED_INT',
            'binn_mem_free', 'BINN_STATIC', 'BINN_TRANSIENT', 'binn_struct', 'binn', 'binn_version',
            'binn_set_alloc_functions', 'binn_create_type', 'binn_get_type_info',
            'binn_get_write_storage', 'binn_get_read_storage', 'binn_is_container', 'binn_new',
            'binn_list', 'binn_map', 'binn_object', 'binn_create', 'binn_create_list',
            'binn_create_map', 'binn_create_object', 'binn_copy', 'binn_list_add_new',
            'binn_map_set_new', 'binn_object_set_new', 'binn_list_add', 'binn_map_set',
            'binn_object_set', 'binn_free', 'binn_release', 'binn_value', 'binn_int8', 'binn_int16',
            'binn_int32', 'binn_int64', 'binn_uint8', 'binn_uint16', 'binn_uint32', 'binn_uint64',
            'binn_float', 'binn_double', 'binn_bool', 'binn_null', 'binn_string', 'binn_blob'
            # TODO: Finish this
        ))
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
            
            return serializer
        
        @c_dec(is_method=True, is_static=True, overloads={
            OverloadKey(
                Type('Serialization'), (Param('file', Type('string')),)
            ): OverloadValue(Serialization_from_string_file)
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
