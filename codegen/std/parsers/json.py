from codegen.objects import Object, Position, Type, Free, Arg, TempVar, Param
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec, INCLUDES


CJSON_PATH = (INCLUDES / 'cJSON').absolute()


class json:
    def __init__(self, codegen) -> None:
        codegen.c_manager.include(f'"{(CJSON_PATH / 'cJSON.h').as_posix()}"', codegen)
        codegen.extra_compile_args.append((CJSON_PATH / 'cJSON.c').as_posix())
        codegen.c_manager.reserve((
            'JSONParser', 'CCJSON_CDECL', 'CJSON_STDCALL', 'CJSON_HIDE_SYMBOLS',
            'CJSON_IMPORT_SYMBOLS', 'CJSON_EXPORT_SYMBOLS', 'CJSON_PUBLIC', 'CJSON_API_VISIBILITY',
            'CJSON_VERSION_MAJOR', 'CJSON_VERSION_MINOR', 'CJSON_VERSION_PATCH', 'cJSON_Invalid',
            'cJSON_False', 'cJSON_True', 'cJSON_NULL', 'cJSON_Value', 'cJSON_Number', 'cJSON_String',
            'cJSON_Array', 'cJSON_Object', 'cJSON_Parse', 'cJSON_Raw', 'cJSON_IsReference',
            'cJSON_IsReference', 'cJSON_StringIsConst', 'cJSON', 'cJSON_Hooks', 'cJSON_bool',
            'CJSON_NESTING_LIMIT', 'cJSON_Version', 'cJSON_InitHooks', 'cJSON_ParseWithLength',
            'cJSON_ParseWithOpts', 'cJSON_ParseWithLengthOpts', 'cJSON_Print', 'cJSON_PrintUnformatted',
            'cJSON_PrintBuffered', 'cJSON_PrintPreallocated', 'cJSON_Delete', 'cJSON_GetArraySize',
            'cJSON_GetArrayItem', 'cJSON_GetObjectItem', 'cJSON_GetObjectItemCaseSensitive',
            'cJSON_HasObjectItem', 'cJSON_GetErrorPtr', 'cJSON_GetStringValue', 'cJSON_GetNumberValue',
            'cJSON_IsInvalid', 'cJSON_IsFalse', 'cJSON_IsTrue', 'cJSON_IsNull', 'cJSON_IsBool'
            'cJSON_IsNumber', 'cJSON_IsString', 'cJSON_IsArray', 'cJSON_IsObject', 'cJSON_IsRaw',
            'cJSON_CreateNull', 'cJSON_CreateTrue', 'cJSON_CreateFalse', 'cJSON_CreateBool',
            'cJSON_CreateNumber', 'cJSON_CreateString', 'cJSON_CreateArray', 'cJSON_CreateObject',
            'cJSON_CreateRaw', 'cJSON_CreateStringReference', 'cJSON_CreateObjectReference',
            'cJSON_CreateArrayReference', 'cJSON_CreateIntArray', 'cJSON_CreateFloatArray',
            'cJSON_CreateDoubleArray', 'cJSON_CreateStringArray', 'cJSON_AddItemToArray',
            'cJSON_AddItemToObject', 'cJSON_AddItemToObjectCS', 'cJSON_AddItemReferenceToArray',
            'cJSON_AddItemReferenceToObject', 'cJSON_DetachItemViaPointer',
            'cJSON_DetachItemFromArray', 'cJSON_DeleteItemFromArray', 'cJSON_DetachItemFromObject',
            'cJSON_DetachItemFromObjectCaseSensitive', 'cJSON_DeleteItemFromObject',
            'cJSON_DeleteItemFromObjectCaseSensitive', 'cJSON_InsertItemInArray',
            'cJSON_ReplaceItemViaPointer', 'cJSON_ReplaceItemInArray', 'cJSON_ReplaceItemInObject',
            'cJSON_ReplaceItemInObjectCaseSensitive', 'cJSON_Duplicate', 'cJSON_Compare',
            'cJSON_Minify', 'cJSON_AddNullToObject', 'cJSON_AddTrueToObject', 'cJSON_AddFalseToObject',
            'cJSON_AddBoolToObject', 'cJSON_AddNumberToObject', 'cJSON_AddStringToObject',
            'cJSON_AddRawToObject', 'cJSON_AddObjectToObject', 'cJSON_AddArrayToObject',
            'cJSON_SetIntValue', 'cJSON_SetNumberHelper', 'cJSON_SetNumberValue',
            'cJSON_SetValuestring', 'cJSON_SetBoolValue', 'cJSON_ArrayForEach', 'cJSON_malloc',
            'cJSON_free', 'cJSON__h'
        ))
        codegen.add_toplevel_code("""#ifndef CURE_PARSERS_H
typedef struct {
    cJSON* json;
} JSONParser;
#endif
""")
    
        @c_dec(add_to_class=self, is_method=True, is_static=True)
        def _JSONParser_type(_, call_position: Position) -> Object:
            return Object('"JSONParser"', Type('string'), call_position)
        
        @c_dec(param_types=(Param('json', Type('JSONParser')),), add_to_class=self, is_method=True)
        def _JSONParser_to_string(_, call_position: Position, jp: Object) -> Object:
            return Object(f'(cJSON_Print(({jp}).json))', Type('string'), call_position)

        
        @c_dec(param_types=(Param('json', Type('JSONParser')),), is_property=True, add_to_class=self)
        def _JSONParser_get_string(codegen, call_position: Position, jp: Object) -> Object:
            return _JSONParser_to_string(codegen, call_position, jp)
        
        @c_dec(
            param_types=(Param('json', Type('JSONParser')), Param('key', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _JSONParser_read_string(codegen, call_position: Position, jp: Object,
                                    key: Object) -> Object:
            value: TempVar = codegen.create_temp_var(Type('JsonObject', 'cJSON*'), call_position)
            codegen.prepend_code(f"""cJSON* {value} = cJSON_GetObjectItemCaseSensitive(
    ({jp}).json, {key}
);
if (!cJSON_IsString({value}) || {value}->valuestring == NULL) {{
    {codegen.c_manager.err('Key is not a string')}
}}
""")
            
            return Object(f'({value}->valuestring)', Type('string'), call_position)
        
        @c_dec(
            param_types=(Param('json', Type('JSONParser')), Param('key', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _JSONParser_read_int(codegen, call_position: Position, jp: Object, key: Object) -> Object:
            value: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""cJSON* {value} = cJSON_GetObjectItemCaseSensitive(
    ({jp}).json, {key}
);
if (!cJSON_IsNumber({value})) {{
    {codegen.c_manager.err('Key is not a number')}
}}
""")

            return Object(f'({value}->valueint)', Type('int'), call_position)
        
        @c_dec(
            param_types=(Param('json', Type('JSONParser')), Param('key', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _JSONParser_read_bool(codegen, call_position: Position, jp: Object, key: Object) -> Object:
            value: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""cJSON* {value} = cJSON_GetObjectItemCaseSensitive(
    ({jp}).json, {key}
);
if (!cJSON_IsBool({value})) {{
    {codegen.c_manager.err('Key is not a bool')}
}}
""")

            return Object(f'({value}->valuebool)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(
                Param('json', Type('JSONParser')), Param('key', Type('string')),
                Param('value', Type('string'))
            ), is_method=True, add_to_class=self
        )
        def _JSONParser_write_string(codegen, call_position: Position, jp: Object,
                                     key: Object, value: Object) -> Object:
            codegen.prepend_code(f'cJSON_AddStringToObject(({jp}).json, {key}, {value});')
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(
                Param('json', Type('JSONParser')), Param('key', Type('string')),
                Param('value', Type('int'))
            ), is_method=True, add_to_class=self
        )
        def _JSONParser_write_int(codegen, call_position: Position, jp: Object,
                                  key: Object, value: Object) -> Object:
            codegen.prepend_code(f'cJSON_AddNumberToObject(({jp}).json, {key}, {value});')
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(
                Param('json', Type('JSONParser')), Param('key', Type('string')),
                Param('value', Type('float'))
            ), is_method=True, add_to_class=self
        )
        def _JSONParser_write_float(codegen, call_position: Position, jp: Object,
                                     key: Object, value: Object) -> Object:
            codegen.prepend_code(f'cJSON_AddNumberToObject(({jp}).json, {key}, {value});')
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(
                Param('json', Type('JSONParser')), Param('key', Type('string')),
                Param('value', Type('bool'))
            ), is_method=True, add_to_class=self
        )
        def _JSONParser_write_bool(codegen, call_position: Position, jp: Object,
                                   key: Object, value: Object) -> Object:
            codegen.prepend_code(f'cJSON_AddBoolToObject(({jp}).json, {key}, {value});')
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('json', Type('JSONParser')), Param('filename', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _JSONParser_to_file(codegen, call_position: Position, jp: Object,
                                filename: Object) -> Object:
            fp: TempVar = codegen.create_temp_var(Type('FILE*'), call_position)
            codegen.prepend_code(f"""FILE* {fp} = fopen({filename}, "w");
if ({fp} == NULL) {{
    {codegen.c_manager.err('Failed to open file for writing JSON')}
}}

fprintf({fp}, "%s", cJSON_Print(({jp}).json));
""")
            
            return Object.NULL(call_position)
        
        def _JSONParser_new3(codegen, call_position: Position) -> Object:
            jp_free = Free(free_name='cJSON_Delete')
            jp: TempVar = codegen.create_temp_var(Type('JSONParser'), call_position, free=jp_free)
            jp_free.object_name = f'{jp}.json'
            
            codegen.prepend_code(f'JSONParser {jp} = {{ .json = cJSON_CreateObject() }};')
            return jp.OBJECT()
        
        def _JSONParser_new2(codegen, call_position: Position, file: Object) -> Object:
            return _JSONParser_new(
                codegen, call_position,
                codegen.call('File_contents', [Arg(file)], call_position)
            )
        
        @c_dec(
            param_types=(Param('code', Type('string')),), is_method=True, is_static=True,
            add_to_class=self, overloads={
                OverloadKey(
                    Type('JSONParser'), (Param('file', Type('File')),)
                ): OverloadValue(_JSONParser_new2),
                OverloadKey(Type('JSONParser'), ()): OverloadValue(_JSONParser_new3)
            }
        )
        def _JSONParser_new(codegen, call_position: Position, code: Object) -> Object:
            jp_free = Free(free_name='cJSON_Delete')
            jp: TempVar = codegen.create_temp_var(Type('JSONParser'), call_position, free=jp_free)
            jp_free.object_name = f'{jp}.json'
            
            eptr: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""JSONParser {jp};
{jp}.json = cJSON_Parse({code});
if ({jp}.json == NULL) {{
    const char* {eptr} = cJSON_GetErrorPtr();
    if ({eptr} != NULL) {{
        {codegen.c_manager.err('JSON parsing error: %s', str(eptr))}
    }}
    
    {codegen.c_manager.err('JSON parsing error')}
}}
""")
            
            return jp.OBJECT()
