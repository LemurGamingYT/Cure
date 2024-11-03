from ir.nodes import (
    Call, Program, Foreach, RangeFor, Node, Body, FuncDecl, While, If, AnonymousFunc,
    ClassMethod, Identifier, ArgNode, Array, Attribute, New,
    # Value
)
from ir.base_transformer import IRTransformer
# from codegen.objects import Type


class Optimizer(IRTransformer):
    def __init__(self, ir: Program, codegen) -> None:
        super().__init__(ir)
        
        self.codegen = codegen
        self.uses_args = False
    
    def optimize(self) -> Node:
        return self.transform(self.ir) # type: ignore
    
    def transform_Program(self, node: Program) -> Program:
        node.nodes = [self.transform(node) for node in node.nodes]
        return node
    
    def transform_FuncDecl(self, node: FuncDecl) -> FuncDecl:
        node.body = self.transform_Body(node.body)
        return node
    
    def transform_AnonymousFunc(self, node: AnonymousFunc) -> AnonymousFunc:
        node.body = self.transform_Body(node.body)
        return node
    
    def transform_ClassMethod(self, node: ClassMethod) -> ClassMethod:
        node.body = self.transform_Body(node.body)
        return node
    
    def transform_Body(self, node: Body) -> Body:
        return Body(node.pos, [self.transform(node) for node in node.nodes])
    
    def transform_While(self, node: While) -> While:
        node.body = self.transform_Body(node.body)
        return node
    
    def transform_If(self, node: If) -> If:
        node.body = self.transform_Body(node.body)
        if node.else_body:
            node.else_body = self.transform_Body(node.else_body)
        for i, (expr, body) in enumerate(node.elseifs):
            node.elseifs[i] = (expr, self.transform_Body(body))
        
        return node
    
    def transform_RangeFor(self, node: RangeFor) -> RangeFor:
        node.body = self.transform_Body(node.body)
        return node
    
    def transform_Foreach(self, node: Foreach) -> Foreach | RangeFor:
        # if isinstance(node.expr, Call):
        #     args = [self.codegen.visit_ArgNode(arg) for arg in node.expr.args]
        #     if node.expr.name == 'range' and all(arg.value.type == Type('int') for arg in args):
        #         start: Node | None = None
        #         end: Node | None = None
        #         if len(args) == 1:
        #             start = Value(node.expr.args[0].pos, '0', 'int')
        #             end = node.expr.args[0].expr
        #         elif len(args) == 2:
        #             start = node.expr.args[0].expr
        #             end = node.expr.args[1].expr
        #         else:
        #             node.pos.error_here('Invalid range call')
                
        #         if start is None or end is None:
        #             node.pos.warn_here('Failed to optimize foreach range loop')
        #             return node
                
        #         return RangeFor(
        #             node.pos, node.loop_name, start, end, node.body
        #         )
        
        return node
    
    def transform_ArgNode(self, node: ArgNode) -> ArgNode:
        node.expr = self.transform(node.expr)
        return node
    
    def transform_Call(self, node: Call) -> Call:
        node.args = [self.transform_ArgNode(arg) for arg in node.args]
        return node
    
    def transform_Array(self, node: Array) -> Array:
        node.elements = [self.transform_ArgNode(node) for node in node.elements]
        return node
    
    def transform_Attribute(self, node: Attribute) -> Attribute:
        if node.args is not None:
            node.args = [self.transform_ArgNode(node) for node in node.args]
        
        return node
    
    def transform_New(self, node: New) -> New:
        node.args = [self.transform_ArgNode(node) for node in node.args]
        return node
    
    def transform_Identifier(self, node: Identifier) -> Identifier:
        if node.name == 'args':
            self.uses_args = True
        
        return node
