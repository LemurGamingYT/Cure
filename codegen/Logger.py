from codegen.objects import Object, Type, Param, Position, TempVar, Free
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec


class Logger:
    def __init__(self, c_manager) -> None:
        c_manager.codegen.add_toplevel_code("""typedef struct {
    FILE* out;
    string path;
} Logger;
""")
        c_manager.wrap_struct_properties('logger', Type('Logger'), [
            Param('path', Type('string'))
        ])
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Logger_type(_, call_position: Position) -> Object:
            return Object('"Logger"', Type('string'), call_position)
        
        @c_dec(param_types=(Param('logger', Type('Logger')),), is_method=True, add_to_class=self)
        def _Logger_to_string(codegen, call_position: Position, logger: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, '"Logger(path=%s)"', f'({logger}).path'
            )
            
            codegen.prepend_code(f"""{code}
if (({logger}).path == NULL) {buf_free.object_name} = "Logger(path=stdout)";
""")
            return Object.STRINGBUF(buf_free, call_position)
        
        
        @c_dec(
            param_types=(Param('logger', Type('Logger')), Param('content', Type('string'))),
            add_to_class=self, is_method=True
        )
        def _Logger_log(codegen, call_position: Position, logger: Object, content: Object) -> Object:
            codegen.prepend_code(f'fprintf(({logger}).out, "%s\\n", {str(content)});')
            return Object.NULL(call_position)
        
        @c_dec(param_types=(Param('logger', Type('Logger')),), add_to_class=self, is_method=True)
        def _Logger_dump(codegen, call_position: Position, logger: Object) -> Object:
            codegen.prepend_code(f'fflush(({logger}).out);')
            return Object.NULL(call_position)
        
        
        def Log_file(codegen, call_position: Position, path: Object) -> Object:
            logger_free = Free(free_name='fclose')
            logger: TempVar = codegen.create_temp_var(Type('Logger'), call_position, free=logger_free)
            logger_free.object_name = f'{logger}.out'
            codegen.prepend_code(f"""Logger {logger} = {{ .out = fopen({path}, "w"), .path = {path} }};
if ({logger}.out == NULL) {{
    {codegen.c_manager.err('Failed to open file %s', str(path))}
}}
""")

            return logger.OBJECT()
        
        @c_dec(is_method=True, is_static=True, add_to_class=self, overloads={
            OverloadKey(Type('Logger'), (Param('path', Type('string')),)): OverloadValue(Log_file)
        })
        def _Logger_new(codegen, call_position: Position) -> Object:
            logger: TempVar = codegen.create_temp_var(Type('Logger'), call_position)
            codegen.prepend_code(f"""Logger {logger} = {{ .out = stdout, .path = NULL }};
""")

            return logger.OBJECT()
