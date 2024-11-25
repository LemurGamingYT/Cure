from codegen.objects import Object, Position, Type, Param
from codegen.extern.stddef_h import size_t
from codegen.c_manager import c_dec


class stdalign_h:
    def __init__(self, _) -> None:
        @c_dec(params=(Param('type', Type('any')),), can_user_call=True, add_to_class=self)
        def _alignof(_, call_position: Position, type: Object) -> Object:
            return Object(f'(alignof({type}))', size_t, call_position)
