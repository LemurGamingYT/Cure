from codegen.objects import Object, Position, Free, Type, Arg
from codegen.c_manager import c_dec


def stat(codegen, call_position: Position, file: Object) -> Object:
    codegen.c_manager.include('<sys/stat.h>', codegen)
    
    st = codegen.create_temp_var(Type('Stat', 'struct stat'), call_position)
    codegen.prepend_code(f"""#ifdef OS_WINDOWS
    struct stat {st};
    if (stat(({file}).path, &{st}) != 0) {{
        {codegen.c_manager.err('stat() failed')}
    }}
#else
{codegen.c_manager.symbol_not_supported('stat()')}
#endif
""")
    
    return Object(st, Type('Stat', 'struct stat'), call_position)


class File:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""#ifndef CURE_FSTREAM_H
typedef struct {
    FILE* fp;
    string path;
    string mode;
} File;
#endif
""")
    
    @c_dec(is_method=True, is_static=True)
    def _File_type(self, _, call_position: Position) -> Object:
        return Object('"File"', Type('string'), call_position)
    
    @c_dec(param_types=('File',), is_method=True)
    def _File_to_string(self, codegen, call_position: Position, file: Object) -> Object:
        f = f'({file})'
        code, buf_free = codegen.c_manager.fmt_length(
            codegen, call_position,
            '"File(path=%s)"', f'{f}.path'
        )
        
        codegen.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_path(self, _, call_position: Position, file: Object) -> Object:
        return Object(f'(({file}).path)', Type('string'), call_position)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_mode(self, _, call_position: Position, file: Object) -> Object:
        return Object(f'(({file}).mode)', Type('string'), call_position)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_contents(self, codegen, call_position: Position, file: Object) -> Object:
        reader_free = Free(free_name='fclose')
        reader = codegen.create_temp_var(Type('FilePointer', 'FILE*'), call_position,
                                          free=reader_free)
        size = codegen.create_temp_var(Type('string'), call_position)
        buf_free = Free()
        buf = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
        read_size = codegen.create_temp_var(Type('int'), call_position)
        f = f'({file})'
        codegen.prepend_code(f"""string {buf} = NULL;
FILE* {reader} = fopen({f}.path, "rb");
if ({reader} == NULL) {{
    {codegen.c_manager.err('Failed to open file: %s', f'{f}.path')}
}}

if (fseek({reader}, 0, SEEK_END) != 0) {{
    {codegen.c_manager.err('Failed to seek end of file: %s', f'{f}.path')}
}}

long {size} = ftell({reader});
if ({size} == -1L) {{
    {codegen.c_manager.err('Failed to determine file size: %s', f'{f}.path')}
}}

if (fseek({reader}, 0, SEEK_SET) != 0) {{
    {codegen.c_manager.err('Failed to seek start of file: %s', f'{f}.path')}
}}

{buf} = (string)malloc({size} + 1);
{codegen.c_manager.buf_check(buf)}

size_t {read_size} = fread({buf}, 1, {size}, {reader});
if ({read_size} != {size}) {{
    {codegen.c_manager.err('Failed to read file: %s', f'{f}.path')}
}}

{buf}[{size}] = '\\0';
""")
        
        return Object(buf, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_extension(self, codegen, call_position: Position, file: Object) -> Object:
        extension = codegen.create_temp_var(Type('string'), call_position)
        f = f'({file})'
        codegen.prepend_code(f"""string {extension} = strrchr({f}.path, '.');
if ({extension} == NULL) {{
    {extension} = "";
}}
""")
        
        return Object(extension, Type('string'), call_position)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_is_file(self, codegen, call_position: Position, file: Object) -> Object:
        st = stat(codegen, call_position, file)
        return Object(f'({st}.st_mode & S_IFREG != 0)', Type('bool'), call_position)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_is_dir(self, codegen, call_position: Position, file: Object) -> Object:
        st = stat(codegen, call_position, file)
        return Object(f'({st}.st_mode & S_IFDIR != 0)', Type('bool'), call_position)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_size(self, codegen, call_position: Position, file: Object) -> Object:
        st = stat(codegen, call_position, file)
        return Object(f'((int){st}.st_size)', Type('int'), call_position)
    
    @c_dec(param_types=('File', 'string'), is_method=True)
    def _File_write(self, codegen, call_position: Position, file: Object, content: Object)\
        -> Object:
        codegen.prepend_code(f'fprintf(({file}).fp, "%s", {content});')
        return Object('NULL', Type('nil'), call_position)
    
    @c_dec(param_types=('File', 'string'), is_method=True)
    def _File_flush(self, codegen, call_position: Position, file: Object) -> Object:
        codegen.prepend_code(f'fflush(({file}).fp);')
        return Object('NULL', Type('nil'), call_position)
    
    @c_dec(param_types=('File', 'string'), is_method=True)
    def _File_remove(self, codegen, call_position: Position, file: Object) -> Object:
        return codegen.call(
            'remove_file', [Arg(Object(f'({file}).path', Type('string'), call_position))],
            call_position
        )
    
    @c_dec(param_types=('File', 'string'), is_method=True)
    def _File_rename(self, codegen, call_position: Position, file: Object, new_name: Object)\
        -> Object:
        return codegen.call(
            'rename_file', [
                Arg(Object(f'({file}).path', Type('string'), call_position)), new_name
            ], call_position
        )
    
    @c_dec(param_types=('File',), is_method=True)
    def _File_close(self, codegen, call_position: Position, file: Object) -> Object:
        codegen.prepend_code(f'fclose(({file}).fp);')
        return Object('NULL', Type('nil'), call_position)
