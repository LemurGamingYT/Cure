from codegen.objects import Object, Position, Type, Param, TempVar
from codegen.extern.stddef_h import size_t
from codegen.c_manager import c_dec


file_ptr = Type('FILE', 'FILE*')
fpos_ptr = Type('fpos_t', 'fpos_t*')
long = Type('long', compatible_types=('int',))


def get_args_str(*args) -> str:
    return (', ' + ', '.join(str(arg) for arg in args)) if len(args) > 0 else ''


class stdio_h:
    def __init__(self, codegen):
        codegen.type_checker.add_type(file_ptr)
        codegen.type_checker.add_type(fpos_ptr)
        codegen.type_checker.add_type(long)

        @c_dec(params=(Param('stream', file_ptr),), can_user_call=True, add_to_class=self)
        def _fclose(_, call_position: Position, stream: Object) -> Object:
            return Object(f'(fclose({stream}))', Type('int'), call_position)

        @c_dec(
            params=(Param('filename', Type('string')), Param('mode', Type('string'))),
            can_user_call=True, add_to_class=self
        )
        def _fopen(_, call_position: Position, filename: Object, mode: Object) -> Object:
            return Object(f'(fopen({filename}, {mode}))', file_ptr, call_position)

        @c_dec(params=(
            Param('ptr', Type('any')), Param('size', size_t), Param('nmemb', size_t),
            Param('stream', file_ptr)
        ), can_user_call=True, add_to_class=self)
        def _fwrite(codegen, call_position: Position, ptr: Object, size: Object, nmemb: Object,
                    stream: Object) -> Object:
            pointer: TempVar | Object
            if ptr.type == Type('string'):
                pointer = ptr
            else:
                pointer = str(codegen.create_temp_var(Type('void*'), call_position))
                codegen.prepend_code(f'{ptr.type.c_type} {pointer} = {ptr};')
                pointer = f'&{pointer}'
            
            return Object(f'(fwrite({pointer}, {size}, {nmemb}, {stream}))', size_t, call_position)

        @c_dec(params=(Param('stream', file_ptr),), can_user_call=True, add_to_class=self)
        def _clearerr(codegen, call_position: Position, stream: Object) -> Object:
            codegen.prepend_code(f'clearerr({stream});')
            return Object.NULL(call_position)

        @c_dec(params=(Param('stream', file_ptr),), can_user_call=True, add_to_class=self)
        def _feof(_, call_position: Position, stream: Object) -> Object:
            return Object(f'(feof({stream}))', Type('int'), call_position)

        @c_dec(params=(Param('stream', file_ptr),), can_user_call=True, add_to_class=self)
        def _ferror(_, call_position: Position, stream: Object) -> Object:
            return Object(f'(ferror({stream}))', Type('int'), call_position)

        @c_dec(params=(Param('stream', file_ptr),), can_user_call=True, add_to_class=self)
        def _fflush(_, call_position: Position, stream: Object) -> Object:
            return Object(f'(fflush({stream}))', Type('int'), call_position)

        @c_dec(params=(
            Param('filename', Type('string')), Param('mode', Type('string')), Param('stream', file_ptr)
        ), can_user_call=True, add_to_class=self)
        def _freopen(_, call_position: Position, filename: Object, mode: Object,
                     stream: Object) -> Object:
            return Object(f'(freopen({filename}, {mode}, {stream}))', file_ptr, call_position)

        @c_dec(params=(
            Param('stream', file_ptr), Param('offset', long), Param('whence', Type('int'))
        ), can_user_call=True, add_to_class=self)
        def _fseek(_, call_position: Position, stream: Object, offset: Object,
                   whence: Object) -> Object:
            return Object(f'(fseek({stream}, {offset}, {whence}))', Type('int'), call_position)

        @c_dec(params=(Param('stream', file_ptr),), can_user_call=True, add_to_class=self)
        def _ftell(_, call_position: Position, stream: Object) -> Object:
            return Object(f'(ftell({stream}))', long, call_position)

        @c_dec(params=(Param('filename', Type('string')),), can_user_call=True, add_to_class=self)
        def _remove(_, call_position: Position, filename: Object) -> Object:
            return Object(f'(remove({filename}))', Type('int'), call_position)

        @c_dec(params=(
            Param('filename', Type('string')), Param('new_filename', Type('string'))
        ), can_user_call=True, add_to_class=self)
        def _rename(_, call_position: Position, filename: Object, new_filename: Object) -> Object:
            return Object(f'(rename({filename}, {new_filename}))', Type('int'), call_position)

        @c_dec(params=(Param('stream', file_ptr),), can_user_call=True, add_to_class=self)
        def _rewind(codegen, call_position: Position, stream: Object) -> Object:
            codegen.prepend_code(f'rewind({stream});')
            return Object.NULL(call_position)

        @c_dec(
            params=(Param('stream', file_ptr), Param('buffer', Type('string'))),
            can_user_call=True, add_to_class=self
        )
        def _setbuf(codegen, call_position: Position, stream: Object, buffer: Object) -> Object:
            codegen.prepend_code(f'setbuf({stream}, {buffer});')
            return Object.NULL(call_position)

        @c_dec(params=(
            Param('stream', file_ptr), Param('buffer', Type('string')), Param('mode', Type('int')),
            Param('size', size_t)
        ), can_user_call=True, add_to_class=self)
        def _setvbuf(codegen, call_position: Position, stream: Object, buffer: Object, mode: Object,
                    size: Object) -> Object:
            codegen.prepend_code(f'setvbuf({stream}, {buffer}, {mode}, {size});')
            return Object.NULL(call_position)

        @c_dec(can_user_call=True, add_to_class=self)
        def _tmpfile(_, call_position: Position) -> Object:
            return Object('(tmpfile())', file_ptr, call_position)

        @c_dec(params=(Param('str', Type('string')),), can_user_call=True, add_to_class=self)
        def _tmpnam(_, call_position: Position, str: Object) -> Object:
            return Object(f'(tmpnam({str}))', Type('string'), call_position)

        @c_dec(params=(Param('stream', file_ptr),), can_user_call=True, add_to_class=self)
        def _fprintf(_, call_position: Position, stream: Object, format: Object, *args) -> Object:
            return Object(
                f'(fprintf({stream}, {format}{get_args_str(*args)}))',
                Type('int'), call_position
            )

        @c_dec(
            params=(Param('format', Type('string')), Param('*', Type('*'))),
            can_user_call=True, add_to_class=self
        )
        def _printf(_, call_position: Position, format: Object, *args) -> Object:
            return Object(f'(printf({format}{get_args_str(*args)}))', Type('int'), call_position)
