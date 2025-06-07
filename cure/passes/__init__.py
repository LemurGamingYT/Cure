from copy import copy
from abc import ABC

from cure.ir import Node, Program, Scope


class CompilerPass(ABC):
    def __init__(self, scope: Scope):
        self.scope = scope
    
    @classmethod
    def run(cls, scope: Scope, program: Program):
        self = cls(scope)
        return self.run_on(program)
    
    def run_on(self, node: Node):
        method_name = f'run_on_{type(node).__name__}'
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(node)
        else:
            raise AttributeError(f'No method {method_name}')

    def run_on_children(self, node: Node):
        new_node = copy(node)
        for child in new_node.children:
            child = self.run_on(child)
        
        return new_node
