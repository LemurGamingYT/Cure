from typing import Any

from ir.nodes import Node


class IRVisitor:
    def visit(self, node: Node) -> Any:
        method = getattr(self, f'visit_{node.__class__.__name__}', None)
        if method is not None:
            return method(node)
        
        raise NotImplementedError(f'Unknown node type \'{node.__class__.__name__}\'')
