from codegen.std.iterables.linked_list import LinkedList
from codegen.std.iterables.stack import Stack
from codegen.std.iterables.queue import Queue


class iterables:
    def __init__(self, codegen) -> None:
        self.ll = LinkedList(codegen)
        self.stack = Stack(codegen)
        self.queue = Queue(codegen)
    
        codegen.c_manager.add_objects(self.stack, self)
        codegen.c_manager.add_objects(self.queue, self)
        codegen.c_manager.add_objects(self.ll, self)
