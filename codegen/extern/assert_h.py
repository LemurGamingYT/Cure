from codegen.objects import Object, Position, Type, Param
from codegen.c_manager import c_dec


class assert_h:
    def __init__(self, _) -> None:
        @c_dec(param_types=(Param('expression', Type('bool')),), can_user_call=True, add_to_class=self)
        def _assert(codegen, call_position: Position, expression: Object) -> Object:
            codegen.c_manager.include('<assert.h>', codegen)
            codegen.prepend_code(f'(assert({expression}))')
            return Object.NULL(call_position)

        @c_dec(param_types=(
            Param('boolean_expression', Type('bool')), Param('message', Type('string'))
        ), can_user_call=True, add_to_class=self)
        def _static_assert(codegen, call_position: Position, boolean_expression: Object,
                        message: Object) -> Object:
            codegen.c_manager.include('<assert.h>', codegen)
            codegen.prepend_code(f'(static_assert({boolean_expression}, {message}))')
            return Object.NULL(call_position)
