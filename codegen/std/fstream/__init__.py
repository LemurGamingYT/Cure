from codegen.objects import Object, Position, Type, Param
from codegen.std.fstream.file import File, stat
from codegen.c_manager import c_dec


class fstream:
    def __init__(self, codegen) -> None:
        codegen.add_type('File')
        codegen.c_manager.add_objects(File(codegen), self)
        codegen.add_toplevel_code("""#ifndef CURE_FSTREAM_H
#define CURE_FSTREAM_H
#endif
""")
        
        @c_dec(param_types=(Param('path', Type('string')),), can_user_call=True, add_to_class=self)
        def _file_exists(codegen, call_position: Position, path: Object) -> Object:
            st = stat(codegen, call_position, path)
            return Object(f'({st}.st_mode & S_IFREG != 0)', Type('bool'), call_position)
