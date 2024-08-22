from cure.std.iterables.linked_list import LinkedList
from cure.std.iterables.stack import Stack
from cure.objects import Object, Position
from cure.c_manager import c_dec


class iterables:
    def __init__(self, compiler) -> None:
        self.ll = LinkedList(compiler)
        self.stack = Stack(compiler)
        self.compiler = compiler
    
    @c_dec(param_types=('type', 'int'), can_user_call=True)
    def _create_stack(self, compiler, call_position: Position, type: Object,
                      size: Object) -> Object:
        return self.stack.create_stack(compiler, call_position, type, size)
    
    @c_dec(param_types=('type',), can_user_call=True)
    def _create_linked_list(self, compiler, call_position: Position, type: Object) -> Object:
        return self.ll.create_linked_list(compiler, call_position, type)
