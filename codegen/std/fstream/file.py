from codegen.objects import Object, Position, Free, Type, TempVar, Param
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec
from codegen.target import Target


def stat(codegen, call_position: Position, file: Object) -> Object:
    if codegen.target != Target.WINDOWS:
        call_position.warn_here('stat() is only supported on Windows')
    
    st: TempVar = codegen.create_temp_var(Type('Stat', 'struct stat'), call_position)
    codegen.prepend_code(f"""if (({file}).fp == NULL) {{
    {codegen.c_manager.err('File has been closed')}
}}

#ifdef OS_WINDOWS
    struct stat {st};
    if (stat(({file}).path, &{st}) != 0) {{
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
        codegen.add_toplevel_code("""#ifndef CURE_FSTREAM_H
typedef struct {
    FILE* fp;
    string path;
    string mode;
} File;
#endif
""")
        
        codegen.c_manager.wrap_struct_properties('file', Type('File'), [
            Param('path', Type('string')), Param('mode', Type('string'))
        ])
    
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _File_type(_, call_position: Position) -> Object:
            return Object('"File"', Type('string'), call_position)
        
        @c_dec(param_types=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_to_string(codegen, call_position: Position, file: Object) -> Object:
            f = f'({file})'
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position,
                '"File(path=%s)"', f'{f}.path'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
#         @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
#         def _File_files(codegen, call_position: Position, file: Object) -> Object:
#             array_type: Type = codegen.array_manager.define_array(Type('File'))
#             i = codegen.create_temp_var(Type('size_t'), call_position)
#             files_free_name: TempVar = codegen.create_temp_var(Type('function'), call_position)
#             files_free = Free(free_name=str(files_free_name))
#             files: TempVar = codegen.create_temp_var(array_type, call_position, free=files_free)
#             files_free.object_name = f'&{files}'
#             codegen.prepend_code(f"""void {files_free_name}({array_type.c_type}* {files}) {{
#     for (size_t {i} = 0; {i} < ({files})->length; {i}++) {{
#         free(({files})->elements[{i}].path);
#         if (({files})->elements[{i}].fp == NULL) continue;
#         fclose(({files})->elements[{i}].fp);
#     }}
# }}
# """)
            
#             placeholder_file: TempVar = codegen.create_temp_var(Type('File'), call_position)
#             f: TempVar = codegen.create_temp_var(Type('File'), call_position)
            
#             find_data: TempVar = codegen.create_temp_var(Type('WIN32_FIND_DATA'), call_position)
#             filename: TempVar = codegen.create_temp_var(Type('string'), call_position)
#             handle: TempVar = codegen.create_temp_var(Type('HANDLE'), call_position)
#             length: TempVar = codegen.create_temp_var(Type('int'), call_position)
#             codegen.prepend_code(f"""#if OS_WINDOWS
# {find_data.type.c_type} {find_data};
# HANDLE {handle} = FindFirstFile(({file}).path, &{find_data});
# if ({handle} == INVALID_HANDLE_VALUE) {{
#     {codegen.c_manager.err('Failed to find file: %s', f'({file}).path')}
# }}
# """)
#             codegen.prepend_code(f"""{array_type.c_type} {files} = {codegen.call(
#     f'{array_type.c_type}_make', [], call_position
# )};
# do {{
#     int {length} = WideCharToMultiByte(CP_UTF8, 0, {find_data}.cFileName, -1, NULL, 0, NULL, NULL);
#     string {filename} = (string)malloc({length});
#     {codegen.c_manager.buf_check(str(filename))}
#     WideCharToMultiByte(CP_UTF8, 0, {find_data}.cFileName, -1, {filename}, {length}, NULL, NULL);
    
#     File {placeholder_file} = {{ .path = {filename}, .fp = NULL, .mode = NULL }};
#     File {f};
#     if ({_File_is_dir(codegen, call_position, placeholder_file)}) {{
# """)
#             codegen.prepend_code(f"""       {f} = {_File_new3(
#             codegen, call_position, placeholder_file.OBJECT(),
#             Object('true', Type('bool'), call_position)
#         )};
#     }} else {{
# """)
#             codegen.prepend_code(f"""       {f} = {_File_new(
#             codegen, call_position, placeholder_file.OBJECT()
#         )};
#     }}
# """)
#             codegen.prepend_code(f"""       {codegen.call(
#         f'{array_type.c_type}_add', [Arg(files.OBJECT()), Arg(f.OBJECT())], call_position
#     )};
# }} while (FindNextFile({handle}, &{find_data}) != 0);
# #else
# {codegen.c_manager.symbol_not_supported('File.files')}
# #endif
# """)
            
#             return files.OBJECT()
        
        @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_contents(codegen, call_position: Position, file: Object) -> Object:
            reader_free = Free(free_name='fclose')
            reader: TempVar = codegen.create_temp_var(Type('FilePointer', 'FILE*'), call_position,
                                            free=reader_free)
            size: TempVar = codegen.create_temp_var(Type('string'), call_position)
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            read_size: TempVar = codegen.create_temp_var(Type('int'), call_position)
            f = f'({file})'
            codegen.prepend_code(f"""if ({
    codegen.c_manager._File_is_dir(codegen, call_position, file)
}) {{
    {codegen.c_manager.err('Cannot read directory: %s', f'{f}.path')}
}} else if (({file}).fp == NULL) {{
    {codegen.c_manager.err('File has been closed')}
}}

string {buf} = NULL;
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
            
            return buf.OBJECT()
        
        @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_extension(codegen, call_position: Position, file: Object) -> Object:
            extension: TempVar = codegen.create_temp_var(Type('string'), call_position)
            f = f'({file})'
            codegen.prepend_code(f"""if ({
    codegen.c_manager._File_is_dir(codegen, call_position, file)
}) {{
    {codegen.c_manager.err('Cannot get extension of directory: %s', f'{f}.path')}
}} else if (({file}).fp == NULL) {{
    {codegen.c_manager.err('File has been closed')}
}}

string {extension} = strrchr({f}.path, '.');
if ({extension} == NULL) {{
    {extension} = "";
}}
""")
            
            return extension.OBJECT()
        
#         @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
#         def _File_stat(codegen, call_position: Position, file: Object) -> Object:
#             st = stat(codegen, call_position, file)
#             stat_temp: TempVar = codegen.create_temp_var(Type('Stat'), call_position)
#             codegen.prepend_code(f"""if (({file}).fp == NULL) {{
#     {codegen.c_manager.err('File has been closed')}
# }}
# Stat {stat_temp} = {{ .st = &{st} }};
# """)
            
#             return stat_temp.OBJECT()
        
        @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_is_file(codegen, call_position: Position, file: Object) -> Object:
            st = stat(codegen, call_position, file)
            return Object(f'({st}.st_mode & S_IFREG != 0)', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_is_dir(codegen, call_position: Position, file: Object) -> Object:
            st = stat(codegen, call_position, file)
            return Object(f'({st}.st_mode & S_IFDIR != 0)', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_size(codegen, call_position: Position, file: Object) -> Object:
            st = stat(codegen, call_position, file)
            return Object(f'((int){st}.st_size)', Type('int'), call_position)
        
        @c_dec(
            param_types=(Param('file', Type('File')), Param('content', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _File_write(codegen, call_position: Position, file: Object, content: Object)\
            -> Object:
            codegen.prepend_code(f"""if ({
    codegen.c_manager._File_is_dir(codegen, call_position, file)
}) {{
    {codegen.c_manager.err('Cannot write to directory: %s', f'({file}).path')}
}} else if (({file}).fp == NULL) {{
    {codegen.c_manager.err('File has been closed')}
}}

fprintf(({file}).fp, "%s", {content});
""")
            return Object.NULL(call_position)
        
        @c_dec(param_types=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_flush(codegen, call_position: Position, file: Object) -> Object:
            codegen.prepend_code(f"""if ({
    codegen.c_manager._File_is_dir(codegen, call_position, file)
}) {{
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
            codegen.prepend_code(f"""if (({file}).fp == NULL) {{
    {codegen.c_manager.err('File has been closed')}
}}

fclose(({file}).fp);
({file}).fp = NULL;
""")
            return Object.NULL(call_position)
        
        def _File_new3(codegen, call_position: Position, path: Object, is_directory: Object) -> Object:
            f: TempVar = codegen.create_temp_var(Type('File'), call_position)
            codegen.prepend_code(f"""if ({is_directory}) {{
#if OS_WINDOWS
    File {f} = {{ .path = {path}, .fp = NULL, .mode = NULL }};
    if (!{codegen.c_manager._File_is_dir(codegen, call_position, f.OBJECT())}) {{
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
}} else {{
    File {f} = {_File_new(codegen, call_position, path)}
}}
""")
            
            return f.OBJECT()
            
            
        
        def _File_new2(codegen, call_position: Position, path: Object, mode: Object) -> Object:
            f: TempVar = codegen.create_temp_var(Type('File'), call_position)
            codegen.prepend_code(f"""File {f};
{f}.fp = fopen({path}, {mode});
if ({f}.fp == NULL) {{
    {codegen.c_manager.err('Failed to open file: %s', str(path))}
}}
{f}.path = {path};
{f}.mode = {mode};
""")
            
            return f.OBJECT()
        
        @c_dec(param_types=(Param('path', Type('string')),), is_method=True, is_static=True, overloads={
            OverloadKey(
                Type('File'), (Param('path', Type('string')), Param('mode', Type('string')))
            ): OverloadValue(_File_new2),
            OverloadKey(
                Type('File'), (Param('path', Type('string')), Param('is_directory', Type('bool')))
            ): OverloadValue(_File_new3)
        }, add_to_class=self)
        def _File_new(codegen, call_position: Position, path: Object) -> Object:
            return _File_new2(
                codegen, call_position, path, Object('"w"', Type('string'), call_position)
            )
