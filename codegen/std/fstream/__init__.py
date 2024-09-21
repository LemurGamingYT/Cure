from codegen.objects import Object, Position, Type, TempVar, Param
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
            return _open_file(codegen, call_position, path, mode)
        
        @c_dec(param_types=(Param('path', Type('string')),), is_method=True, is_static=True, overloads={
            ((Param('path', Type('string')), Param('mode', Type('string'))), Type('File')): _File_new2
        }, add_to_class=self)
        def _File_new(codegen, call_position: Position, path: Object) -> Object:
            return _open_file(
                codegen, call_position, path,
                Object('"w"', Type('string'), call_position)
            )
    
        @c_dec(
            param_types=(Param('path', Type('string')), Param('mode', Type('string'))),
            can_user_call=True, add_to_class=self
        )
        def _open_file(codegen, call_position: Position, path: Object, mode: Object) -> Object:
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
        
        def _create_file2(codegen, call_position: Position, path: Object) -> Object:
            f: TempVar = codegen.create_temp_var(Type('FilePointer', 'FILE*'), call_position)
            codegen.prepend_code(f"""FILE* {f} = fopen({path}, "w");
if (({f}) == NULL) {{
    {codegen.c_manager.err('Failed to create file: %s', str(path))}
}}

fclose({f});
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('path', Type('string')), Param('mode', Type('string'))),
            can_user_call=True, add_to_class=self, overloads={
                ((Param('path', Type('string')),), Type('File')): _create_file2
            }
        )
        def _create_file(codegen, call_position: Position, path: Object, mode: Object)\
            -> Object:
            _create_file2(codegen, call_position, path)
            return _open_file(codegen, call_position, path, mode)
        
        @c_dec(param_types=(Param('path', Type('string')),), can_user_call=True, add_to_class=self)
        def _remove_file(codegen, call_position: Position, path: Object) -> Object:
            codegen.prepend_code(f"""if (remove({path}) != 0) {{
    {codegen.c_manager.err('Failed to remove file: %s', str(path))}
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('path', Type('string')), Param('new_path', Type('string'))),
            can_user_call=True, add_to_class=self
        )
        def _rename_file(codegen, call_position: Position, path: Object, new_path: Object)\
            -> Object:
            codegen.prepend_code(f"""if (rename({path}, {new_path}) != 0) {{
    {codegen.c_manager.err('Failed to rename file: %s', str(path))}
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(param_types=(Param('path', Type('string')),), can_user_call=True, add_to_class=self)
        def _file_exists(codegen, call_position: Position, path: Object) -> Object:
            st = stat(codegen, call_position, path)
            return Object(f'({st}.st_mode & S_IFREG != 0)', Type('bool'), call_position)
