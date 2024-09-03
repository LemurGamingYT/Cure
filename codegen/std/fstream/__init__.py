from codegen.objects import Object, Position, Type
from codegen.std.fstream.file import File, stat
from codegen.c_manager import c_dec


class fstream:
    def __init__(self, codegen) -> None:
        self.file = File(codegen)
        
        codegen.valid_types.append('File')
        codegen.add_toplevel_code("""#ifndef CURE_FSTREAM_H
#define CURE_FSTREAM_H
#endif
""")
        
        codegen.c_manager.add_objects(self.file, self)
        
        def _File_new2(codegen, call_position: Position, path: Object, mode: Object) -> Object:
            return self._open_file(codegen, call_position, path, mode)
        
        @c_dec(param_types=('string',), is_method=True, is_static=True, overloads={
            (('string', 'string'), 'File'): _File_new2
        }, add_to_class=self)
        def _File_new(codegen, call_position: Position, path: Object) -> Object:
            return self._open_file(
                codegen, call_position, path,
                Object('"w"', Type('string'), call_position)
            )
    
    
    @c_dec(param_types=('string', 'string'), can_user_call=True)
    def _open_file(self, codegen, call_position: Position, path: Object, mode: Object) -> Object:
        f = codegen.create_temp_var(Type('File'), call_position)
        codegen.prepend_code(f"""File {f};
{f}.fp = fopen({path}, {mode});
if ({f}.fp == NULL) {{
    {codegen.c_manager.err('Failed to open file: %s', path.code)}
}}
{f}.path = {path};
{f}.mode = {mode};
""")
        
        return Object(f, Type('File'), call_position)
    
    def _create_file2(self, codegen, call_position: Position, path: Object) -> Object:
        f = codegen.create_temp_var(Type('FilePointer', 'FILE*'), call_position)
        codegen.prepend_code(f"""FILE* {f} = fopen({path}, "w");
if (({f}) == NULL) {{
    {codegen.c_manager.err('Failed to create file: %s', path.code)}
}}

fclose({f});
""")
        
        return Object.NULL(call_position)
    
    @c_dec(param_types=('string', 'string'), can_user_call=True, overloads={
        (('string',), 'nil'): _create_file2
    })
    def _create_file(self, codegen, call_position: Position, path: Object, mode: Object)\
        -> Object:
        self._create_file2(codegen, call_position, path)
        return self._open_file(codegen, call_position, path, mode)
    
    @c_dec(param_types=('string',), can_user_call=True)
    def _remove_file(self, codegen, call_position: Position, path: Object) -> Object:
        codegen.prepend_code(f"""if (remove({path.code}) != 0) {{
    {codegen.c_manager.err('Failed to remove file: %s', {path.code})}
}}
""")
        return Object.NULL(call_position)
    
    @c_dec(param_types=('string', 'string'), can_user_call=True)
    def _rename_file(self, codegen, call_position: Position, path: Object, new_path: Object)\
        -> Object:
        codegen.prepend_code(f"""if (rename({path}, {new_path}) != 0) {{
    {codegen.c_manager.err('Failed to rename file: %s', {path})}
}}
""")
        return Object.NULL(call_position)
    
    @c_dec(param_types=('string',), can_user_call=True)
    def _file_exists(self, codegen, call_position: Position, path: Object) -> Object:
        st = stat(codegen, call_position, path)
        return Object(f'({st}.st_mode & S_IFREG != 0)', Type('bool'), call_position)
