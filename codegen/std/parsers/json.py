from codegen.objects import Object, Position, Type, Free, Arg, TempVar
from codegen.c_manager import c_dec, INCLUDES


CJSON_PATH = (INCLUDES / 'cJSON').absolute()


class json:
    def __init__(self, codegen) -> None:
        codegen.c_manager.include(f'"{(CJSON_PATH / 'cJSON.h').as_posix()}"', codegen)
        codegen.extra_compile_args.append((CJSON_PATH / 'cJSON.c').as_posix())
        codegen.valid_types.append('JSONParser')
        codegen.add_toplevel_code("""#ifndef CURE_PARSERS_H
typedef struct {
    cJSON* json;
} JSONParser;
#endif
""")
    
        @c_dec(add_to_class=self, is_method=True, is_static=True)
        def _JSONParser_type(_, call_position: Position) -> Object:
            return Object('"JSONParser"', Type('string'), call_position)
        
        @c_dec(param_types=('JSONParser',), add_to_class=self, is_method=True)
        def _JSONParser_to_string(_, call_position: Position, jp: Object) -> Object:
            return Object(f'(cJSON_Print(({jp}).json))', Type('string'), call_position)

        
        @c_dec(param_types=('JSONParser',), is_property=True, add_to_class=self)
        def _JSONParser_get_string(_, call_position: Position, jp: Object) -> Object:
            return Object(f'(cJSON_Print(({jp}).json))', Type('string'), call_position)
        
        @c_dec(param_types=('JSONParser', 'string'), is_method=True, add_to_class=self)
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
        
        @c_dec(param_types=('JSONParser', 'string'), is_method=True, add_to_class=self)
        def _JSONParser_read_int(codegen, call_position: Position, jp: Object,
                                 key: Object) -> Object:
            value: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""cJSON* {value} = cJSON_GetObjectItemCaseSensitive(
    ({jp}).json, {key}
);
if (!cJSON_IsNumber({value})) {{
    {codegen.c_manager.err('Key is not a number')}
}}
""")

            return Object(f'({value}->valueint)', Type('int'), call_position)
        
        @c_dec(param_types=('JSONParser', 'string'), is_method=True, add_to_class=self)
        def _JSONParser_read_bool(codegen, call_position: Position, jp: Object,
                                  key: Object) -> Object:
            value: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""cJSON* {value} = cJSON_GetObjectItemCaseSensitive(
    ({jp}).json, {key}
);
if (!cJSON_IsBool({value})) {{
    {codegen.c_manager.err('Key is not a bool')}
}}
""")

            return Object(f'({value}->valuebool)', Type('bool'), call_position)
        
        @c_dec(param_types=('JSONParser', 'string', 'string'), is_method=True, add_to_class=self)
        def _JSONParser_write_string(codegen, call_position: Position, jp: Object,
                                     key: Object, value: Object) -> Object:
            codegen.prepend_code(f'cJSON_AddStringToObject(({jp}).json, {key}, {value});')
            return Object.NULL(call_position)
        
        @c_dec(param_types=('JSONParser', 'string', 'int'), is_method=True, add_to_class=self)
        def _JSONParser_write_int(codegen, call_position: Position, jp: Object,
                                  key: Object, value: Object) -> Object:
            codegen.prepend_code(f'cJSON_AddNumberToObject(({jp}).json, {key}, {value});')
            return Object.NULL(call_position)
        
        @c_dec(param_types=('JSONParser', 'string', 'float'), is_method=True, add_to_class=self)
        def _JSONParser_write_float(codegen, call_position: Position, jp: Object,
                                     key: Object, value: Object) -> Object:
            codegen.prepend_code(f'cJSON_AddNumberToObject(({jp}).json, {key}, {value});')
            return Object.NULL(call_position)
        
        @c_dec(param_types=('JSONParser', 'string', 'bool'), is_method=True, add_to_class=self)
        def _JSONParser_write_bool(codegen, call_position: Position, jp: Object,
                                   key: Object, value: Object) -> Object:
            codegen.prepend_code(f'cJSON_AddBoolToObject(({jp}).json, {key}, {value});')
            return Object.NULL(call_position)
        
        @c_dec(param_types=('JSONParser', 'string'), is_method=True, add_to_class=self)
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
            param_types=('string',), is_method=True, is_static=True,
            add_to_class=self, overloads={
                (('File',), 'JSONParser'): _JSONParser_new2,
                ((), 'JSONParser'): _JSONParser_new3
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
