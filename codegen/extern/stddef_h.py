from codegen.objects import Object, Position, Param, Type
from codegen.c_manager import c_dec


size_t = Type('size_t', compatible_types=('int',))
ptrdiff_t = Type('ptrdiff_t')
wchar_t = Type('wchar_t')

class stddef_h:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type(size_t)
        codegen.type_checker.add_type(ptrdiff_t)
        codegen.type_checker.add_type(wchar_t)
        
        codegen.add_toplevel_constant('NULL', Type('nil'), add_code=False)

        @c_dec(params=(
            Param('type', Type('any')), Param('member-designator', Type('any'))
        ), can_user_call=True, add_to_class=self)
        def _offsetof(_, call_position: Position, type: Object, member_designator: Object) -> Object:
            return Object(f'(offsetof({type}, {member_designator}))', size_t, call_position)
