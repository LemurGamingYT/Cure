from typing import Any

from ir.nodes import Node, Position


class IRVisitor:
    def __init__(self) -> None:
        self.pos: Position | None = None
    
    def visit(self, node: Node) -> Any:
        method = getattr(self, f'visit_{node.__class__.__name__}', None)
        if method is not None:
            self.pos = node.pos
            return method(node)
