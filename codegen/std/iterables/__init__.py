from codegen.std.iterables.linked_list import LinkedList
from codegen.std.iterables.stack import Stack
from codegen.objects import Object, Position
from codegen.c_manager import c_dec


class iterables:
    def __init__(self, codegen) -> None:
        self.ll = LinkedList(codegen)
        self.stack = Stack(codegen)
    
    @c_dec(param_types=('type', 'int'), can_user_call=True)
    def _create_stack(self, codegen, call_position: Position, type: Object,
                      size: Object) -> Object:
        return self.stack.create_stack(codegen, call_position, type, size)
    
    @c_dec(param_types=('type',), can_user_call=True)
    def _create_linked_list(self, codegen, call_position: Position, type: Object) -> Object:
        return self.ll.create_linked_list(codegen, call_position, type)
