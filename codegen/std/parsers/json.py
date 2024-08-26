from pathlib import Path

from codegen.objects import Object, Position, Type, Free
from codegen.c_manager import c_dec


CJSON_PATH = (Path(__file__).parent.parent.parent.parent / 'include/cJSON/cJSON.h').absolute()


class json:
    def __init__(self, compiler) -> None:
        compiler.c_manager.include(f'"{CJSON_PATH.as_posix()}"', compiler)
        compiler.extra_compile_args.append((CJSON_PATH.parent / 'cJSON.c').as_posix())
        compiler.valid_types.append('JSONParser')
        compiler.add_toplevel_code("""typedef struct {
    string code;
    cJSON* json;
} JSONParser;
""")
    
        @c_dec(add_to_class=self)
        def _JSONParser_type(_, call_position: Position) -> Object:
            return Object('"JSONParser"', Type('string'), call_position)
        
        @c_dec(param_types=('JSONParser',), add_to_class=self)
        def _JSONParser_to_string(_, call_position: Position, _jp: Object) -> Object:
            return Object('"class \'JSONParser\'"', Type('string'), call_position)

        
        @c_dec(param_types=('JSONParser',), is_property=True, add_to_class=self)
        def _JSONParser_json_content(_, call_position: Position, jp: Object) -> Object:
            return Object(f'(({jp.code}).code)', Type('string'), call_position)
        
        @c_dec(param_types=('JSONParser', 'string'), is_method=True, add_to_class=self)
        def _JSONParser_read_string(compiler, call_position: Position, jp: Object,
                                    key: Object) -> Object:
            value = compiler.create_temp_var(Type('JsonObject', 'cJSON*'), call_position)
            compiler.prepend_code(f"""cJSON* {value} = cJSON_GetObjectItemCaseSensitive(
    ({jp.code}).json, {key.code}
);
if (!cJSON_IsString({value}) || {value}->valuestring == NULL) {{
    {compiler.c_manager.err('Key is not a string')}
}}
""")
            
            return Object(f'({value}->valuestring)', Type('string'), call_position)
        
        @c_dec(param_types=('JSONParser', 'string'), is_method=True, add_to_class=self)
        def _JSONParser_read_int(compiler, call_position: Position, jp: Object,
                                 key: Object) -> Object:
            value = compiler.create_temp_var(Type('int'), call_position)
            compiler.prepend_code(f"""cJSON* {value} = cJSON_GetObjectItemCaseSensitive(
    ({jp.code}).json, {key.code}
);
if (!cJSON_IsNumber({value})) {{
    {compiler.c_manager.err('Key is not a number')}
}}
""")

            return Object(f'({value}->valueint)', Type('int'), call_position)
        
        def _JSONParser_new2(compiler, call_position: Position, file: Object) -> Object:
            jp_free = Free(free_name='cJSON_Delete')
            jp = compiler.create_temp_var(Type('JSONParser'), call_position, free=jp_free)
            jp_free.object_name = f'{jp}.json'
            
            contents = compiler.create_temp_var(Type('string'), call_position)
            
            eptr = compiler.create_temp_var(Type('string'), call_position)
            compiler.prepend_code(f"""JSONParser {jp};
{jp}.json = NULL;
""")
            compiler.prepend_code(f"""string {contents} = {compiler.call(
    'File_contents', [file], call_position
).code};
{jp}.code = {contents};
{jp}.json = cJSON_Parse({contents});
if ({jp}.json == NULL) {{
    const char* {eptr} = cJSON_GetErrorPtr();
    if ({eptr} != NULL) {{
        {compiler.c_manager.err('JSON parsing error: %s', eptr)}
    }}
    
    {compiler.c_manager.err('JSON parsing error')}
}}
""")
            
            return Object(jp, Type('JSONParser'), call_position, free=jp_free)
        
        @c_dec(
            param_types=('string',), is_method=True, is_static=True,
            add_to_class=self, overloads={
                (('File',), 'JSONParser'): _JSONParser_new2
            }
        )
        def _JSONParser_new(compiler, call_position: Position, code: Object) -> Object:
            jp_free = Free(free_name='cJSON_Delete')
            jp = compiler.create_temp_var(Type('JSONParser'), call_position, free=jp_free)
            jp_free.object_name = f'{jp}.json'
            
            eptr = compiler.create_temp_var(Type('string'), call_position)
            compiler.prepend_code(f"""JSONParser {jp};
{jp}.code = {code.code};
{jp}.json = cJSON_Parse({jp}.code);
if ({jp}.json == NULL) {{
    const char* {eptr} = cJSON_GetErrorPtr();
    if ({eptr} != NULL) {{
        {compiler.c_manager.err('JSON parsing error: %s', eptr)}
    }}
    
    {compiler.c_manager.err('JSON parsing error')}
}}
""")
            
            return Object(jp, Type('JSONParser'), call_position, free=jp_free)
