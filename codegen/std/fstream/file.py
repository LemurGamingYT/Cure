from codegen.objects import Object, Position, Free, Type, TempVar, Param, Arg
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec
from codegen.target import Target


def stat(codegen, call_position: Position, path: str) -> Object:
    if codegen.target != Target.WINDOWS:
        call_position.warn_here('stat() is only supported on Windows')
    
    st: TempVar = codegen.create_temp_var(Type('Stat', 'struct stat'), call_position)
    codegen.prepend_code(f"""#ifdef OS_WINDOWS
    struct stat {st};
    if (stat({path}, &{st}) != 0) {{
        {codegen.c_manager.err('stat() failed')}
    }}
#else
{codegen.c_manager.symbol_not_supported('stat()')}
#endif
""")
    
    return st.OBJECT()


class File:
    def __init__(self, codegen) -> None:
        codegen.c_manager.include('<sys/stat.h>', codegen)
        codegen.add_toplevel_code("""typedef struct {
    FILE* fp;
    string path, mode;
} File;
""")
        
        codegen.c_manager.init_class(self, 'File', Type('File'))
        codegen.c_manager.wrap_struct_properties('file', Type('File'), [
            Param('path', Type('string')), Param('mode', Type('string'))
        ])
        
        @c_dec(param_types=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_to_string(codegen, call_position: Position, file: Object) -> Object:
            f = f'({file})'
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position,
                '"File(path=%s)"', f'{f}.path'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_line_count(codegen, call_position: Position, file: Object) -> Object:
            content: TempVar = codegen.create_temp_var(Type('string'), call_position)
            length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            count: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            f = f'({file})'
            codegen.prepend_code(f"""if ({_File_is_dir(codegen, call_position, file)}) {{
    {codegen.c_manager.err('Cannot read directory: %s', f'{f}.path')}
}} else if (({file}).fp == NULL) {{
    {codegen.c_manager.err('File has been closed')}
}}

int {count} = 0;
string {content} = {_File_contents(codegen, call_position, file)};
size_t {length} = strlen({content});
for (size_t {i} = 0; {i} < {length}; {i}++) {{
    if ({content}[{i}] == '\\n') {count}++;
}}

free({content});
""")
            
            return count.OBJECT()
        
        @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_contents(codegen, call_position: Position, file: Object) -> Object:
            reader_free = Free(free_name='fclose')
            reader: TempVar = codegen.create_temp_var(Type('FilePointer', 'FILE*'), call_position,
                                            free=reader_free, default_expr='NULL')
            size: TempVar = codegen.create_temp_var(Type('string'), call_position)
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free,
                                                   default_expr='NULL')
            read_size: TempVar = codegen.create_temp_var(Type('int'), call_position)
            f = f'({file})'
            codegen.prepend_code(f"""if ({_File_is_dir(codegen, call_position, file)}) {{
    {codegen.c_manager.err('Cannot read directory: %s', f'{f}.path')}
}} else if (({file}).fp == NULL) {{
    {codegen.c_manager.err('File has been closed')}
}}

{reader} = fopen({f}.path, "rb");
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
            
            return buf.OBJECT()
        
        @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_extension(codegen, call_position: Position, file: Object) -> Object:
            extension: TempVar = codegen.create_temp_var(Type('string'), call_position)
            f = f'({file})'
            codegen.prepend_code(f"""if ({_File_is_dir(codegen, call_position, file)}) {{
    {codegen.c_manager.err('Cannot get extension of directory: %s', f'{f}.path')}
}}

string {extension} = strrchr({f}.path, '.');
if ({extension} == NULL) {{
    {extension} = "";
}}
""")
            
            return extension.OBJECT()
        
        @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_is_file(codegen, call_position: Position, file: Object) -> Object:
            st = stat(codegen, call_position, f'({file}).path')
            return Object(f'({st}.st_mode & S_IFREG != 0)', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_is_dir(codegen, call_position: Position, file: Object) -> Object:
            st = stat(codegen, call_position, f'({file}).path')
            return Object(f'({st}.st_mode & S_IFDIR != 0)', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_size(codegen, call_position: Position, file: Object) -> Object:
            st = stat(codegen, call_position, f'({file}).path')
            return Object(f'((int){st}.st_size)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_readonly(codegen, call_position: Position, file: Object) -> Object:
            attributes: TempVar = codegen.create_temp_var(Type('DWORD'), call_position)
            codegen.prepend_code(f"""#ifdef OS_WINDOWS
DWORD {attributes} = GetFileAttributes(({file}).path);
if ({attributes} == INVALID_FILE_ATTRIBUTES) {{
    {codegen.c_manager.err('Failed to get file attributes: %s', f'({file}).path')}
}}
#else
{codegen.c_manager.symbol_not_supported('File.readonly')}
#endif
""")
            
            return Object(f'({attributes} & FILE_ATTRIBUTE_READONLY != 0)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(Param('file', Type('File')), Param('value', Type('bool')),),
            is_method=True, add_to_class=self
        )
        def _File_set_readonly(codegen, call_position: Position, file: Object, value: Object) -> Object:
            attributes: TempVar = codegen.create_temp_var(Type('DWORD'), call_position)
            codegen.prepend_code(f"""#ifdef OS_WINDOWS
if ({value}) {{
    if (SetFileAttributes(({file}).path, FILE_ATTRIBUTE_READONLY) != 0) {{
        {codegen.c_manager.err('Failed to set file attributes: %s', f'({file}).path')}
    }}
}} else {{
    DWORD {attributes} = GetFileAttributes(({file}).path);
    if ({attributes} == INVALID_FILE_ATTRIBUTES) {{
        {codegen.c_manager.err('Failed to get file attributes: %s', f'({file}).path')}
    }}
    
    {attributes} &= ~FILE_ATTRIBUTE_READONLY;
    if (SetFileAttributes(({file}).path, {attributes}) != 0) {{
        {codegen.c_manager.err('Failed to set file attributes: %s', f'({file}).path')}
    }}
}}
#else
{codegen.c_manager.symbol_not_supported('File.set_readonly()')}
#endif
""")
            
            return Object.NULL(call_position)
        
        @c_dec(param_types=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_get_files(codegen, call_position: Position, file: Object) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.warn_here('File.get_files() is only supported on Windows')
            
            array_type: Type = codegen.array_manager.define_array(Type('File'))
            files: Object = codegen.call(f'{array_type.c_type}_make', [], call_position)
            
            find_data: TempVar = codegen.create_temp_var(Type('WIN32_FIND_DATA'), call_position)
            search_path: TempVar = codegen.create_temp_var(Type('string'), call_position)
            full_path: TempVar = codegen.create_temp_var(Type('string'), call_position)
            filename: TempVar = codegen.create_temp_var(Type('string'), call_position)
            h_find: TempVar = codegen.create_temp_var(Type('HANDLE'), call_position)
            f: TempVar = codegen.create_temp_var(Type('File'), call_position)
            codegen.prepend_code(f"""if (!{_File_is_dir(codegen, call_position, file)}) {{
    {codegen.c_manager.err('Can only get files from directories')}
}}

char {search_path}[MAX_PATH];
snprintf({search_path}, MAX_PATH, "%s\\\\*", ({file}).path);

WIN32_FIND_DATA {find_data};
HANDLE {h_find} = FindFirstFile({search_path}, &{find_data});
if ({h_find} == INVALID_HANDLE_VALUE) {{
    {codegen.c_manager.err('Failed to find first file in directory: %s', f'({file}).path')}
}}

do {{
    string {filename} = {find_data}.cFileName;
    if (strcmp({filename}, ".") == 0 || strcmp({filename}, "..") == 0) continue;
    char {full_path}[MAX_PATH];
    snprintf({full_path}, MAX_PATH, "%s\\\\%s", ({file}).path, {filename});
    File {f} = {{ .fp = NULL, .path = {full_path}, .mode = "r" }};
""")
            codegen.prepend_code(f"""{codegen.call(
    f'{array_type.c_type}_add', [Arg(files), Arg(f.OBJECT())], call_position
)};
}} while (FindNextFile({h_find}, &{find_data}) != 0);

FindClose({h_find});
""")
            
            return files
        
        @c_dec(
            param_types=(Param('file', Type('File')), Param('content', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _File_write(codegen, call_position: Position, file: Object, content: Object)\
            -> Object:
            codegen.prepend_code(f"""if ({_File_is_dir(codegen, call_position, file)}) {{
    {codegen.c_manager.err('Cannot write to directory: %s', f'({file}).path')}
}} else if (({file}).fp == NULL) {{
    {codegen.c_manager.err('File has been closed')}
}}

fprintf(({file}).fp, "%s", {content});
""")
            return Object.NULL(call_position)
        
        @c_dec(param_types=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_flush(codegen, call_position: Position, file: Object) -> Object:
            codegen.prepend_code(f"""if ({_File_is_dir(codegen, call_position, file)}) {{
    {codegen.c_manager.err('Cannot flush directory: %s', f'({file}).path')}
}} else if (({file}).fp == NULL) {{
    {codegen.c_manager.err('File has been closed')}
}}

fflush(({file}).fp);
""")
            return Object.NULL(call_position)
        
        @c_dec(param_types=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_remove(codegen, call_position: Position, file: Object) -> Object:
            codegen.prepend_code(f"""if (remove(({file}).path) != 0) {{
    {codegen.c_manager.err('Failed to remove file: %s', f'({file}).path')}
}} else if (({file}).fp == NULL) {{
    {codegen.c_manager.err('File has been closed')}
}}

({file}).fp = NULL;
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('file', Type('File')), Param('new_name', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _File_rename(codegen, call_position: Position, file: Object, new_name: Object)\
            -> Object:
            codegen.prepend_code(f"""if (rename(({file}).path, {new_name}) != 0) {{
    {codegen.c_manager.err('Failed to rename file: %s', f'({file}).path')}
}} else if (({file}).fp == NULL) {{
    {codegen.c_manager.err('File has been closed')}
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(param_types=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_close(codegen, call_position: Position, file: Object) -> Object:
            codegen.prepend_code(f"""if (({file}).fp == NULL && ({file}).mode != NULL) {{
    {codegen.c_manager.err('File has been closed')}
}} else if (({file}).fp == NULL && ({file}).mode == NULL) {{
    {codegen.c_manager.err('Directories do not need to be closed')}
}}

fclose(({file}).fp);
({file}).fp = NULL;
""")
            return Object.NULL(call_position)
        
        
        @c_dec(
            param_types=(Param('path', Type('string')),), is_method=True, is_static=True,
            add_to_class=self
        )
        def _File_dir(codegen, call_position: Position, path: Object) -> Object:
            f: TempVar = codegen.create_temp_var(
                Type('File'), call_position,
                default_expr=f'{{ .fp = NULL, .mode = NULL, .path = {path} }}'
            )
            codegen.prepend_code(f"""#if OS_WINDOWS
    if (!{_File_is_dir(codegen, call_position, f.OBJECT())}) {{
        {codegen.c_manager.err('Path is not a directory: %s', str(path))}
    }}

    if (CreateDirectory({path}, NULL) != 0) {{
        if (GetLastError() == ERROR_ALREADY_EXISTS) {{
            {codegen.c_manager.err('Directory already exists: %s', str(path))}
        }} else if (GetLastError() == ERROR_PATH_NOT_FOUND) {{
            {codegen.c_manager.err('Invalid path to create directory: %s', str(path))}
        }} else {{
            {codegen.c_manager.err('Failed to create directory: %s', str(path))}
        }}
    }}
#else
{codegen.c_manager.symbol_not_supported('create_directory')}
#endif
""")
            
            return f.OBJECT()
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _File_temp(codegen, call_position: Position) -> Object:
            f_free = Free(free_name='fclose')
            f: TempVar = codegen.create_temp_var(Type('File'), call_position, free=f_free)
            f_free.object_name = f'{f}.fp'
            
            codegen.prepend_code(f"""File {f} = {{ .fp = tmpfile(), .mode = "wb+", .path = "temp" }};
if ({f}.fp == NULL) {{
    {codegen.c_manager.err('Failed to create temporary file')}
}}
""")

            return f.OBJECT()
        
        @c_dec(
            param_types=(Param('path', Type('string')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _File_exists(codegen, call_position: Position, path: Object) -> Object:
            st = stat(codegen, call_position, f'({path})')
            return Object(f'({st}.st_mode & S_IFREG != 0)', Type('bool'), call_position)
        
        def _File_new2(codegen, call_position: Position, path: Object, mode: Object) -> Object:
            f: TempVar = codegen.create_temp_var(
                Type('File'), call_position,
                default_expr=f'{{ .fp = NULL, .mode = NULL, .path = {path} }}'
            )
            codegen.prepend_code(f"""if ({_File_is_dir(codegen, call_position, f.OBJECT())}) {{
#if OS_WINDOWS
    if (CreateDirectory({path}, NULL) != 0) {{
        if (GetLastError() == ERROR_ALREADY_EXISTS) {{
            {codegen.c_manager.err('Directory already exists: %s', str(path))}
        }} else if (GetLastError() == ERROR_PATH_NOT_FOUND) {{
            {codegen.c_manager.err('Invalid path to create directory: %s', str(path))}
        }} else {{
            {codegen.c_manager.err('Failed to create directory: %s', str(path))}
        }}
    }}
#else
{codegen.c_manager.symbol_not_supported('create_directory')}
#endif
}} else {{
    {f}.fp = fopen({path}, {mode});
    if ({f}.fp == NULL) {{
        {codegen.c_manager.err('Failed to open file: %s', str(path))}
    }}
    {f}.path = {path};
    {f}.mode = {mode};
}}
""")
            
            return f.OBJECT()
        
        @c_dec(param_types=(Param('path', Type('string')),), is_method=True, is_static=True, overloads={
            OverloadKey(
                Type('File'), (Param('path', Type('string')), Param('mode', Type('string')))
            ): OverloadValue(_File_new2)
        }, add_to_class=self)
        def _File_new(codegen, call_position: Position, path: Object) -> Object:
            return _File_new2(
                codegen, call_position, path, Object('"w"', Type('string'), call_position)
            )
