from codegen.objects import Object, Type, Position, Param
from codegen.c_manager import c_dec


class Cure:
    def __init__(self, _) -> None:
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _Cure_version(_, call_position: Position) -> Object:
            return Object('VERSION', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _Cure_flags(codegen, call_position: Position) -> Object:
            return codegen.c_manager.c_array_from_list(codegen, call_position, Type('string'), [
                Object(f'"{flag}"', Type('string'), call_position)
                for flag in codegen.extra_compile_args
            ])
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _Cure_dependencies(codegen, call_position: Position) -> Object:
            return codegen.c_manager.c_array_from_list(codegen, call_position, Type('string'), [
                Object(dep if dep.startswith('"') else f'"{dep}"', Type('string'), call_position)
                for dep in codegen.c_manager.includes
            ])
        
        @c_dec(
            param_types=(Param('src', Type('string')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Cure_compile(codegen, call_position: Position, src: Object) -> Object:
            from codegen import str_to_c
            if not codegen.is_string_literal(str(src)):
                call_position.error_here('Source code must be a string literal')
            
            _, code = str_to_c(str(src)[1:-1], codegen.scope)
            codegen.prepend_code(code)
            return Object.NULL(call_position)
