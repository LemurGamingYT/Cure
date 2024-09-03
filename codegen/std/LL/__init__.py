from codegen.objects import Object, Position
from codegen.std.LL.pointer import Pointer
from codegen.c_manager import c_dec


class LL:
    def __init__(self, codegen) -> None:
        self.ptr = Pointer(codegen)
        
        codegen.add_toplevel_code("""#ifndef CURE_LL_H
#define CURE_LL_H
#endif
""")
        codegen.c_manager.add_objects(self.ptr, self)
    
    @c_dec(param_types=('string',), can_user_call=True)
    def _asm(self, codegen, call_position: Position, string: Object) -> Object:
        if not codegen.is_string_literal(string):
            call_position.error_here('string literal expected for inlining assembly')
        
        codegen.prepend_code(f'__asm__({string});')
        return Object.NULL(call_position)
