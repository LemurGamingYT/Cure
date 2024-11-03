from ir.nodes import Node, Position, Program


class IRTransformer:
    def __init__(self, ir: Program) -> None:
        self.pos: Position | None = None
        self.ir = ir
    
    def transform(self, node: Node) -> Node:
        method = getattr(self, f'transform_{node.__class__.__name__}', None)
        if method is not None:
            self.pos = node.pos
            return method(node)
        
        self.pos = node.pos
        return node
