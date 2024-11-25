from codegen.objects import (
    Object, Position, Free, Type, Param, TempVar, StringableWithPosition, Stringable
)
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec, INCLUDES
from codegen.target import Target


class File:
    def __init__(self, codegen) -> None:
        codegen.c_manager.include(f'"{INCLUDES}/fileio/fileio.h"', codegen)
        codegen.extra_compile_args.append(f'{INCLUDES}/fileio/fileio.c')
        codegen.add_toplevel_code('typedef FileIO File;')
        codegen.c_manager.reserve((
            'FILEIO_H', 'FileIO', 'FILEIO_NULL', 'fileio_is_valid', 'fileio_open', 'fileio_free',
            'fileio_read', 'fileio_read_string', 'fileio_write', 'fileio_size', 'fileio_exists',
            'fileio_delete', 'fileio_rename', 'fileio_suffix', 'fileio_stem', 'fileio_is_dir',
            'fileio_is_file', 'fileio_is_link', 'fileio_absolute', 'fileio_relative', 'fileio_touch',
            'fileio_mkdir', 'fileio_rmdir'
        ))
        
        if codegen.target == Target.WINDOWS:
            codegen.extra_compile_args.append('-lShlwapi')
        
        codegen.c_manager.init_class(self, 'File', Type('File'))
        codegen.c_manager.wrap_struct_properties('file', Type('File'), [
            Param('filename', Type('string'))
        ])
        
        def create_from_io(codegen, pos: Position, fileio: Stringable) -> TempVar:
            fileio_free = Free(free_name='fileio_free')
            fileio_var: TempVar = codegen.create_temp_var(Type('File'), pos, free=fileio_free)
            fileio_free.object_name = f'&{fileio_var}'
            codegen.prepend_code(f'File {fileio_var} = {fileio};')
            return fileio_var
        
        def create_temp_fileio(codegen, file: StringableWithPosition) -> str:
            return f'&{codegen.create_temp_var(Type("File"), file.position, default_expr=str(file))}'
        
        @c_dec(params=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_to_string(codegen, call_position: Position, file: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position,
                '"File(filename=%s)"', f'({file}).filename'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
    
        @c_dec(params=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_contents(codegen, call_position: Position, file: Object) -> Object:
            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free)
            temp = create_temp_fileio(codegen, file)
            codegen.prepend_code(f'string {res} = fileio_read_string({temp});')
            return res.OBJECT()
        
        @c_dec(params=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_size(_, call_position: Position, file: Object) -> Object:
            return Object(
                f'((int)fileio_size({create_temp_fileio(codegen, file)}))',
                Type('int'), call_position
            )
        
        @c_dec(params=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_suffix(_, call_position: Position, file: Object) -> Object:
            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free)
            codegen.prepend_code(
                f'string {res} = fileio_suffix({create_temp_fileio(codegen, file)});'
            )
            return res.OBJECT()
        
        @c_dec(params=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_stem(_, call_position: Position, file: Object) -> Object:
            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free)
            codegen.prepend_code(f'string {res} = fileio_stem({create_temp_fileio(codegen, file)});')
            return res.OBJECT()
        
        @c_dec(params=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_exists(_, call_position: Position, file: Object) -> Object:
            return Object(
                f'(fileio_exists({create_temp_fileio(codegen, file)}))',
                Type('bool'), call_position
            )
        
        @c_dec(params=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_is_dir(_, call_position: Position, file: Object) -> Object:
            return Object(
                f'(fileio_is_dir({create_temp_fileio(codegen, file)}))',
                Type('bool'), call_position
            )
        
        @c_dec(params=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_is_file(_, call_position: Position, file: Object) -> Object:
            return Object(
                f'(fileio_is_file({create_temp_fileio(codegen, file)}))',
                Type('bool'), call_position
            )
        
        @c_dec(params=(Param('file', Type('File')),), is_property=True, add_to_class=self)
        def _File_is_link(_, call_position: Position, file: Object) -> Object:
            return Object(
                f'(fileio_is_link({create_temp_fileio(codegen, file)}))',
                Type('bool'), call_position
            )
        
        @c_dec(params=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_touch(_, call_position: Position, file: Object) -> Object:
            return Object(
                f'(fileio_touch({create_temp_fileio(codegen, file)}))',
                Type('bool'), call_position
            )
        
        @c_dec(params=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_mkdir(_, call_position: Position, file: Object) -> Object:
            return Object(
                f'(fileio_mkdir({create_temp_fileio(codegen, file)}))',
                Type('bool'), call_position
            )
        
        @c_dec(params=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_rmdir(_, call_position: Position, file: Object) -> Object:
            return Object(
                f'(fileio_rmdir({create_temp_fileio(codegen, file)}))',
                Type('bool'), call_position
            )
        
        @c_dec(
            params=(Param('file', Type('File')), Param('data', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _File_write(_, call_position: Position, file: Object, data: Object) -> Object:
            return Object(
                f'(fileio_write({create_temp_fileio(codegen, file)}, {data}))',
                Type('int'), call_position
            )
        
        @c_dec(params=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_absolute(_, call_position: Position, file: Object) -> Object:
            return create_from_io(
                codegen, call_position,
                f'fileio_absolute({create_temp_fileio(codegen, file)})'
            ).OBJECT()
        
        @c_dec(
            params=(Param('file', Type('File')), Param('to', Type('File'))),
            is_method=True, add_to_class=self
        )
        def _File_relative_to(_, call_position: Position, file: Object, to: Object) -> Object:
            return create_from_io(
                codegen, call_position,
                f'fileio_relative_to({create_temp_fileio(codegen, file)}, {to})'
            ).OBJECT()
        
        @c_dec(params=(Param('file', Type('File')),), is_method=True, add_to_class=self)
        def _File_delete(_, call_position: Position, file: Object) -> Object:
            return Object(
                f'(fileio_delete({create_temp_fileio(codegen, file)}))',
                Type('bool'), call_position
            )
        
        @c_dec(
            params=(Param('file', Type('File')), Param('new_name', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _File_rename(_, call_position: Position, file: Object, new_name: Object) -> Object:
            return Object(
                f'(fileio_rename({create_temp_fileio(codegen, file)}, {new_name}))',
                Type('bool'), call_position
            )
        
        def File_as_child_of(codegen, call_position: Position, filename: Object,
                             parent: Object) -> Object:
            parent_var: TempVar = codegen.create_temp_var(Type('File'), call_position)
            codegen.prepend_code(f'File {parent_var} = {parent};')
            return Object(
                f'(fileio_as_child_of({filename}, &{parent_var}))',
                Type('File'), call_position
            )
        
        @c_dec(
            params=(Param('filename', Type('string')),), is_method=True, is_static=True,
            add_to_class=self, overloads={
                OverloadKey(Type('File'), (
                    Param('filename', Type('string')), Param('parent', Type('File'))
                )): OverloadValue(File_as_child_of)
            }
        )
        def _File_new(codegen, call_position: Position, filename: Object) -> Object:
            return create_from_io(codegen, call_position, f'fileio_open({filename})').OBJECT()
