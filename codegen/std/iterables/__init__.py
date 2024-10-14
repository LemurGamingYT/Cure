from codegen.std.iterables.functions import IteratorFunctions
from codegen.std.iterables.linked_list import LinkedList
from codegen.std.iterables.buffer import buffer
from codegen.std.iterables.stack import Stack
from codegen.std.iterables.queue import Queue


class iterables:
    def __init__(self, codegen) -> None:
        codegen.c_manager.add_objects(IteratorFunctions(codegen), self)
        codegen.c_manager.add_objects(LinkedList(codegen), self)
        codegen.c_manager.add_objects(buffer(codegen), self)
        codegen.c_manager.add_objects(Stack(codegen), self)
        codegen.c_manager.add_objects(Queue(codegen), self)
