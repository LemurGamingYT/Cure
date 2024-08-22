from cure.objects import Object, Position, Type
from cure.std.fstream.file import File, stat
from cure.c_manager import c_dec


class fstream:
    def __init__(self, compiler) -> None:
        self.file = File(compiler)
        
        compiler.valid_types.append('File')
        
        compiler.c_manager.add_objects(self.file, self)
    
    
    @c_dec(param_types=('string', 'string'), can_user_call=True)
    def _open_file(self, compiler, call_position: Position, path: Object, mode: Object) -> Object:
        f = compiler.create_temp_var(Type('File'), call_position)
        compiler.prepend_code(f"""File {f};
{f}.fp = fopen({path.code}, {mode.code});
if ({f}.fp == NULL) {{
    {compiler.c_manager.err('Failed to open file: %s', path.code)}
}}
{f}.path = {path.code};
{f}.mode = {mode.code};
""")
        
        return Object(f, Type('File'), call_position)
    
    def _create_file2(self, compiler, call_position: Position, path: Object) -> Object:
        f = compiler.create_temp_var(Type('FilePointer', 'FILE*'), call_position)
        compiler.prepend_code(f"""FILE* {f} = fopen({path.code}, "w");
if (({f}) == NULL) {{
    {compiler.c_manager.err('Failed to create file: %s', path.code)}
}}

fclose({f});
""")
        
        return Object('NULL', Type('nil'), call_position)
    
    @c_dec(param_types=('string', 'string'), can_user_call=True, overloads={
        (('string',), 'nil'): _create_file2
    })
    def _create_file(self, compiler, call_position: Position, path: Object, mode: Object)\
        -> Object:
        self._create_file2(compiler, call_position, path)
        return self._open_file(compiler, call_position, path, mode)
    
    @c_dec(param_types=('string',), can_user_call=True)
    def _remove_file(self, compiler, call_position: Position, path: Object) -> Object:
        compiler.prepend_code(f"""if (remove({path.code}) != 0) {{
    {compiler.c_manager.err('Failed to remove file: %s', {path.code})}
}}""")
        return Object('NULL', Type('nil'), call_position)
    
    @c_dec(param_types=('string', 'string'), can_user_call=True)
    def _rename_file(self, compiler, call_position: Position, path: Object, new_path: Object)\
        -> Object:
        compiler.prepend_code(f"""if (rename({path.code}, {new_path.code}) != 0) {{
    {compiler.c_manager.err('Failed to rename file: %s', {path.code})}
}}""")
        return Object('NULL', Type('nil'), call_position)
    
    @c_dec(param_types=('string',), can_user_call=True)
    def _file_exists(self, compiler, call_position: Position, path: Object) -> Object:
        st = stat(compiler, call_position, path)
        return Object(f'({st.code}.st_mode & S_IFREG != 0)', Type('bool'), call_position)
    
    
    @c_dec(param_types=('string', 'string'), is_method=True, is_static=True)
    def _File_new(self, compiler, call_position: Position, path: Object, mode: Object) -> Object:
        return self._open_file(compiler, call_position, path, mode)
    
    @c_dec(param_types=('string',), is_method=True, is_static=True)
    def _File_new(self, compiler, call_position: Position, path: Object) -> Object:
        return self._open_file(
            compiler, call_position, path,
            Object('"w"', Type('string'), call_position)
        )
