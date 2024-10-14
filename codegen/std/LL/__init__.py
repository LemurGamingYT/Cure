from codegen.objects import Object, Position, Type, Param
from codegen.std.LL.bitfield import BitField
from codegen.std.LL.pointer import Pointer
from codegen.std.LL.process import Process
from codegen.c_manager import c_dec


class LL:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type(('Pointer', 'Process', 'BitField'))
        codegen.add_toplevel_code("""#ifndef CURE_LL_H
#define CURE_LL_H
""")
        codegen.c_manager.add_objects(Pointer(codegen), self)
        codegen.c_manager.add_objects(Process(codegen), self)
        codegen.c_manager.add_objects(BitField(codegen), self)
        codegen.add_toplevel_code('#endif')
    
        @c_dec(param_types=(Param('code', Type('string')),), can_user_call=True, add_to_class=self)
        def _asm(codegen, call_position: Position, code: Object) -> Object:
            if not codegen.is_string_literal(code):
                call_position.error_here('string literal expected for inlining assembly')
            
            codegen.prepend_code(f'__asm__({code});')
            return Object.NULL(call_position)
