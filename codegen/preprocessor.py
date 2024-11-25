from ir.base_visitor import IRVisitor
from ir.nodes import Program, Test


class Preprocessor(IRVisitor):
    def __init__(self, codegen) -> None:
        self.tests: list[Test] = []
        self.codegen = codegen
    
    def preprocess(self, program: Program) -> None:
        """Pre-process the IR.

        Args:
            program (Program): The IR program.
        """
        
        return self.visit(program)
    
    
    def visit_Program(self, node: Program) -> None:
        for stmt in node.nodes:
            self.visit(stmt)
    
    def visit_Test(self, node: Test) -> None:
        self.tests.append(node)
        self.codegen.add_toplevel_code(f'nil {node.name}_test();')
