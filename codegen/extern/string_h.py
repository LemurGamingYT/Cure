from codegen.objects import Object, Position, Type, Param
from codegen.extern.stdlib_h import void_ptr
from codegen.extern.stddef_h import size_t
from codegen.c_manager import c_dec


char_ptr = Type('char*', compatible_types=('string',))

class string_h:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type(char_ptr)
        
        @c_dec(
            params=(Param('str', void_ptr), Param('c', Type('int')), Param('n', size_t)),
            can_user_call=True, add_to_class=self
        )
        def _memchr(_, call_position: Position, str: Object, c: Object, n: Object) -> Object:
            return Object(f'(memchr({str}, {c}, {n}))', void_ptr, call_position)
        
        @c_dec(
            params=(Param('str1', void_ptr), Param('str2', void_ptr), Param('n', size_t)),
            can_user_call=True, add_to_class=self
        )
        def _memcmp(_, call_position: Position, str1: Object, str2: Object, n: Object) -> Object:
            return Object(f'(memcmp({str1}, {str2}, {n}))', Type('int'), call_position)
        
        @c_dec(
            params=(Param('dest', void_ptr), Param('src', void_ptr), Param('n', size_t)),
            can_user_call=True, add_to_class=self
        )
        def _memcpy(_, call_position: Position, dest: Object, src: Object, n: Object) -> Object:
            return Object(f'(memcpy({dest}, {src}, {n}))', void_ptr, call_position)
        
        @c_dec(
            params=(Param('dest', void_ptr), Param('src', void_ptr), Param('n', size_t)),
            can_user_call=True, add_to_class=self
        )
        def _memmove(_, call_position: Position, dest: Object, src: Object, n: Object) -> Object:
            return Object(f'(memmove({dest}, {src}, {n}))', void_ptr, call_position)
        
        @c_dec(
            params=(Param('str', void_ptr), Param('c', Type('int')), Param('n', size_t)),
            can_user_call=True, add_to_class=self
        )
        def _memset(_, call_position: Position, str: Object, c: Object, n: Object) -> Object:
            return Object(f'(memset({str}, {c}, {n}))', void_ptr, call_position)
        
        @c_dec(
            params=(Param('dest', char_ptr), Param('src', char_ptr)),
            can_user_call=True, add_to_class=self
        )
        def _strcat(_, call_position: Position, dest: Object, src: Object) -> Object:
            return Object(f'(strcat({dest}, {src}))', char_ptr, call_position)
        
        @c_dec(
            params=(Param('dest', char_ptr), Param('src', char_ptr), Param('n', size_t)),
            can_user_call=True, add_to_class=self
        )
        def _strncat(_, call_position: Position, dest: Object, src: Object, n: Object) -> Object:
            return Object(f'(strncat({dest}, {src}, {n}))', char_ptr, call_position)
        
        @c_dec(
            params=(Param('str', char_ptr), Param('c', Type('int'))),
            can_user_call=True, add_to_class=self
        )
        def _strchr(_, call_position: Position, str: Object, c: Object) -> Object:
            return Object(f'(strchr({str}, {c}))', char_ptr, call_position)
        
        @c_dec(
            params=(Param('str1', char_ptr), Param('str2', char_ptr)),
            can_user_call=True, add_to_class=self
        )
        def _strcmp(_, call_position: Position, str1: Object, str2: Object) -> Object:
            return Object(f'(strcmp({str1}, {str2}))', Type('int'), call_position)
        
        @c_dec(
            params=(Param('str1', char_ptr), Param('str2', char_ptr), Param('n', size_t)),
            can_user_call=True, add_to_class=self
        )
        def _strncmp(_, call_position: Position, str1: Object, str2: Object, n: Object) -> Object:
            return Object(f'(strncmp({str1}, {str2}, {n}))', Type('int'), call_position)
        
        @c_dec(
            params=(Param('str', char_ptr),),
            can_user_call=True, add_to_class=self
        )
        def _strlen(_, call_position: Position, str: Object) -> Object:
            return Object(f'(strlen({str}))', Type('size_t'), call_position)
        
        @c_dec(
            params=(Param('str1', char_ptr), Param('str2', char_ptr)),
            can_user_call=True, add_to_class=self
        )
        def _strcoll(_, call_position: Position, str1: Object, str2: Object) -> Object:
            return Object(f'(strcoll({str1}, {str2}))', Type('int'), call_position)
        
        @c_dec(
            params=(Param('dest', char_ptr), Param('src', char_ptr)),
            can_user_call=True, add_to_class=self
        )
        def _strcpy(_, call_position: Position, dest: Object, src: Object) -> Object:
            return Object(f'(strcpy({dest}, {src}))', char_ptr, call_position)
        
        @c_dec(
            params=(Param('dest', char_ptr), Param('src', char_ptr), Param('n', size_t)),
            can_user_call=True, add_to_class=self
        )
        def _strncpy(_, call_position: Position, dest: Object, src: Object, n: Object) -> Object:
            return Object(f'(strncpy({dest}, {src}, {n}))', char_ptr, call_position)
        
        @c_dec(
            params=(Param('str1', char_ptr), Param('str2', char_ptr)),
            can_user_call=True, add_to_class=self
        )
        def _strcspn(_, call_position: Position, str1: Object, str2: Object) -> Object:
            return Object(f'(strcspn({str1}, {str2}))', size_t, call_position)
        
        @c_dec(
            params=(Param('errnum', Type('int')),),
            can_user_call=True, add_to_class=self
        )
        def _strerror(_, call_position: Position, errnum: Object) -> Object:
            return Object(f'(strerror({errnum}))', char_ptr, call_position)
        
        @c_dec(
            params=(Param('str1', char_ptr), Param('str2', char_ptr)),
            can_user_call=True, add_to_class=self
        )
        def _strpbrk(_, call_position: Position, str1: Object, str2: Object) -> Object:
            return Object(f'(strpbrk({str1}, {str2}))', char_ptr, call_position)
        
        @c_dec(
            params=(Param('str', char_ptr), Param('c', Type('int'))),
            can_user_call=True, add_to_class=self
        )
        def _strrchr(_, call_position: Position, str: Object, c: Object) -> Object:
            return Object(f'(strrchr({str}, {c}))', char_ptr, call_position)
        
        @c_dec(
            params=(Param('str1', char_ptr), Param('str2', char_ptr)),
            can_user_call=True, add_to_class=self
        )
        def _strspn(_, call_position: Position, str1: Object, str2: Object) -> Object:
            return Object(f'(strspn({str1}, {str2}))', size_t, call_position)
        
        @c_dec(
            params=(Param('haystack', char_ptr), Param('needle', char_ptr)),
            can_user_call=True, add_to_class=self
        )
        def _strstr(_, call_position: Position, haystack: Object, needle: Object) -> Object:
            return Object(f'(strstr({haystack}, {needle}))', char_ptr, call_position)
        
        @c_dec(
            params=(Param('str', char_ptr), Param('delim', char_ptr)),
            can_user_call=True, add_to_class=self
        )
        def _strtok(_, call_position: Position, str: Object, delim: Object) -> Object:
            return Object(f'(strtok({str}, {delim}))', char_ptr, call_position)
        
        @c_dec(
            params=(Param('dest', char_ptr), Param('src', char_ptr), Param('n', size_t)),
            can_user_call=True, add_to_class=self
        )
        def _strxfrm(_, call_position: Position, dest: Object, src: Object, n: Object) -> Object:
            return Object(f'(strxfrm({dest}, {src}, {n}))', size_t, call_position)
