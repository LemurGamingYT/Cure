from codegen.objects import Object, Position, Type, Free, TempVar, Param
from codegen.c_manager import c_dec, INCLUDES


INIPARSER_PATH = INCLUDES / 'iniparser'

class ini:
    def __init__(self, codegen) -> None:
        codegen.c_manager.include(f'"{(INIPARSER_PATH / 'iniparser.h').as_posix()}"', codegen)
        codegen.extra_compile_args.append((INIPARSER_PATH / '*.c').as_posix())
        codegen.c_manager.reserve((
            'iniparser_set_error_callback', 'iniparser_getnsec', 'iniparser_getsecname',
            'iniparser_dump_ini', 'iniparser_dumpsection_ini', 'iniparser_dump',
            'iniparser_getseckeys', 'iniparser_getsecnkeys', 'iniparser_getseckeys',
            'iniparser_getstring', 'iniparser_getint', 'iniparser_getlongint', 'iniparser_getint64',
            'iniparser_getuint64', 'iniparser_getdouble', 'iniparser_getboolean', 'iniparser_set',
            'iniparser_unset', 'iniparser_find_entry', 'iniparser_load', 'iniparser_load_file',
            'iniparser_freedict', 'dictionary', 'dictionary_hash', 'dictionary_new',
            'dictionary_del', 'dictionary_get', 'dictionary_set', 'dictionary_unset',
            'dictionary_dump'
        ))
        
        codegen.add_toplevel_code("""typedef struct {
    dictionary* ini;
    const string path;
} INIParser;
""")
        
        codegen.c_manager.init_class(self, 'INIParser', Type('INIParser'))
        
        @c_dec(param_types=(Param('ini', Type('INIParser')),), add_to_class=self, is_method=True)
        def _INIParser_to_string(codegen, call_position: Position, ip: Object) -> Object:
            builder: Object = codegen.c_manager._StringBuilder_new(codegen, call_position)
            codegen.c_manager._StringBuilder_capture_stdout(codegen, call_position, builder)
            
            codegen.prepend_code(f"""iniparser_dump(({ip}).ini, stdout);
""")
            
            codegen.c_manager._StringBuilder_release_stdout(codegen, call_position, builder)
            return codegen.c_manager._StringBuilder_str(codegen, call_position, builder)
        
        @c_dec(
            param_types=(Param('path', Type('string')),), is_method=True, is_static=True,
            add_to_class=self
        )
        def _INIParser_new(codegen, call_position: Position, path: Object) -> Object:
            ip_free = Free(free_name='iniparser_freedict')
            ip: TempVar = codegen.create_temp_var(Type('INIParser'), call_position, free=ip_free)
            ip_free.object_name = f'{ip}.ini'
            
            codegen.prepend_code(f"""INIParser {ip} = {{
    .path = {path}, .ini = iniparser_load({path})
}};
if ({ip}.ini == NULL) {{
    {codegen.c_manager.err('Failed to load INI file')}
}}
""")

            return ip.OBJECT()

        @c_dec(
            param_types=(Param('ini', Type('INIParser')), Param('key', Type('string')),
                         Param('default', Type('T'))),
            is_method=True, add_to_class=self, generic_params=('T',), return_type=Type('{T}')
        )
        def _INIParser_read(_, call_position: Position, ini: Object, key: Object,
                                default: Object, *, T: Type) -> Object:
            method = ''
            if T == Type('int'):
                method = 'getint'
            elif T == Type('float'):
                method = 'getdouble'
            elif T == Type('string'):
                method = 'getstring'
            elif T == Type('bool'):
                method = 'getboolean'
            else:
                call_position.error_here(f'Unsupported type {T} for read method of INI parser')
            
            return Object(
                f'({T})iniparser_{method}(({ini}).ini, {key}, {default})',
                T, call_position
            )
        
        @c_dec(
            param_types=(Param('ini', Type('INIParser')), Param('key', Type('string')),
                         Param('value', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _INIParser_write(_, call_position: Position, ini: Object, key: Object,
                             value: Object) -> Object:
            return Object(
                f'(iniparser_set({ini}, {key}, {value}) == 0)',
                Type('bool'), call_position
            )
