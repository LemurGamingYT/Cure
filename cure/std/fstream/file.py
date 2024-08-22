from cure.objects import Object, Position, Free, Type
from cure.c_manager import c_dec


def stat(compiler, call_position: Position, file: Object) -> Object:
    compiler.c_manager.include('<sys/stat.h>', compiler)
    
    st = compiler.create_temp_var(Type('Stat', 'struct stat'), call_position)
    compiler.prepend_code(f"""#ifdef OS_WINDOWS
    struct stat {st};
    if (stat(({file.code}).path, &{st}) != 0) {{
        {compiler.c_manager.err('stat() failed')}
    }}
#else
#error "stat() is not implemented on this platform"
#endif
""")
        
    return Object(st, Type('Stat', 'struct stat'), call_position)


class File:
    def __init__(self, compiler) -> None:
        compiler.add_toplevel_code("""typedef struct {
    FILE* fp;
    string path;
    string mode;
} File;
""")
    
    @c_dec()
    def _File_type(self, _, call_position: Position) -> Object:
        return Object('"File"', Type('string'), call_position)
    
    @c_dec(param_types=('File',))
    def _File_to_string(self, compiler, call_position: Position, file: Object) -> Object:
        f = f'({file.code})'
        code, buf_free = compiler.c_manager.fmt_length(
            compiler, call_position,
            'File(path=%s)',
            f'{f}.path'
        )
        
        compiler.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_path(self, _, call_position: Position, file: Object) -> Object:
        return Object(f'({file.code}).path', Type('string'), call_position)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_mode(self, _, call_position: Position, file: Object) -> Object:
        return Object(f'({file.code}).mode', Type('string'), call_position)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_contents(self, compiler, call_position: Position, file: Object) -> Object:
        reader = compiler.create_temp_var(Type('FilePointer', 'FILE*'), call_position)
        size = compiler.create_temp_var(Type('string'), call_position)
        buf_free = Free()
        buf = compiler.create_temp_var(Type('string'), call_position, free=buf_free)
        read_size = compiler.create_temp_var(Type('int'), call_position)
        f = f'({file.code})'
        compiler.prepend_code(f"""string {buf} = NULL;
FILE* {reader} = fopen({f}.path, "rb");
if ({reader} == NULL) {{
    {compiler.c_manager.err('Failed to open file: %s', f'{f}.path')}
}}

if (fseek({reader}, 0, SEEK_END) != 0) {{
    fclose({reader});
    {compiler.c_manager.err('Failed to seek end of file: %s', f'{f}.path')}
}}

long {size} = ftell({reader});
if ({size} == -1L) {{
    fclose({reader});
    {compiler.c_manager.err('Failed to determine file size: %s', f'{f}.path')}
}}

if (fseek({reader}, 0, SEEK_SET) != 0) {{
    fclose({reader});
    {compiler.c_manager.err('Failed to seek start of file: %s', f'{f}.path')}
}}

{buf} = (string)malloc({size} + 1);
{compiler.c_manager.buf_check(buf)}

size_t {read_size} = fread({buf}, 1, {size}, {reader});
if ({read_size} != {size}) {{
    free({buf});
    fclose({reader});
    {compiler.c_manager.err('Failed to read file: %s', f'{f}.path')}
}}

{buf}[{size}] = '\\0';
fclose({reader});
""")
        
        return Object(buf, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_extension(self, compiler, call_position: Position, file: Object) -> Object:
        extension = compiler.create_temp_var(Type('string'), call_position)
        f = f'({file.code})'
        compiler.prepend_code(f"""string {extension} = strrchr({f}.path, '.');
if ({extension} == NULL) {{
    {extension} = "";
}}
""")
        
        return Object(extension, Type('string'), call_position)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_is_file(self, compiler, call_position: Position, file: Object) -> Object:
        st = stat(compiler, call_position, file)
        return Object(f'({st.code}.st_mode & S_IFREG != 0)', Type('bool'), call_position)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_is_dir(self, compiler, call_position: Position, file: Object) -> Object:
        st = stat(compiler, call_position, file)
        return Object(f'({st.code}.st_mode & S_IFDIR != 0)', Type('bool'), call_position)
    
    @c_dec(param_types=('File',), is_property=True)
    def _File_size(self, compiler, call_position: Position, file: Object) -> Object:
        st = stat(compiler, call_position, file)
        return Object(f'((float){st.code}.st_size)', Type('float'), call_position)
    
    @c_dec(param_types=('File', 'string'), is_method=True)
    def _File_write(self, compiler, call_position: Position, file: Object, content: Object)\
        -> Object:
        compiler.prepend_code(f'fprintf(({file.code}).fp, "%s", {content.code})')
        return Object('NULL', Type('nil'), call_position)
    
    @c_dec(param_types=('File', 'string'), is_method=True)
    def _File_flush(self, compiler, call_position: Position, file: Object) -> Object:
        compiler.prepend_code(f'fflush(({file.code}).fp);')
        return Object('NULL', Type('nil'), call_position)
    
    @c_dec(param_types=('File', 'string'), is_method=True)
    def _File_remove(self, compiler, call_position: Position, file: Object) -> Object:
        return self._remove_file(
            compiler, call_position,
            Object(f'({file.code}).path', Type('string'), call_position)
        )
    
    @c_dec(param_types=('File', 'string'), is_method=True)
    def _File_rename(self, compiler, call_position: Position, file: Object, new_name: Object)\
        -> Object:
        return self._rename_file(
            compiler, call_position,
            Object(f'({file.code}).path', Type('string'), call_position),
            new_name
        )
    
    @c_dec(param_types=('File',), is_method=True)
    def _File_close(self, compiler, call_position: Position, file: Object) -> Object:
        compiler.prepend_code(f'fclose(({file.code}).fp);')
        return Object('NULL', Type('nil'), call_position)
