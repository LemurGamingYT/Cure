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
    
        @c_dec(params=(Param('code', Type('string')),), can_user_call=True, add_to_class=self)
        def _asm(codegen, call_position: Position, code: Object) -> Object:
            if not codegen.is_string_literal(code):
                call_position.error_here('string literal expected for inlining assembly')
            
            codegen.prepend_code(f'__asm__({code});')
            return Object.NULL(call_position)
        
        @c_dec(params=(Param('var', Type('any')),), can_user_call=True, add_to_class=self)
        def _addr_of(codegen, call_position: Position, var: Object) -> Object:
            if codegen.is_identifier(var):
                return Object(f'&({var})', Type('hex'), call_position)
            else:
                call_position.error_here(f'Cannot get address of non-variable \'{var}\'')
        
        @c_dec(params=(Param('code', Type('string')),), can_user_call=True, add_to_class=self)
        def _insert_c_code(codegen, call_position: Position, code: Object) -> Object:
            if not codegen.is_string_literal(code):
                call_position.error_here('Inserting C code can only be done as a string literal')
            
            codegen.prepend_code(f'{str(code)[1:-1]};')
            return Object.NULL(call_position)
