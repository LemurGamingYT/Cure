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
    
    # FIXME: Fix this function. Breaks with generic functions and function overloading
    # def visit_FuncDecl(self, node: FuncDecl) -> None:
    #     name = node.name
    #     return_type = self.codegen.visit_TypeNode(node.return_type) if node.return_type is not None\
    #         else Type('nil')
    #     params = [self.codegen.visit_ParamNode(param) for param in node.params]
    #     self.codegen.function_manager.check_duplicate_params(tuple(params), node.pos)
    #     _, new_name, func = self.codegen.function_manager.handle_function_overload(
    #         name, return_type, node.pos, params, node.modifications, None, node.generic_params
    #     )
    #     if new_name is not None:
    #         name = new_name
    #     else:
    #         self.codegen.scope.env[name] = EnvItem(
    #             name, Type('function'), node.pos, func, added_by_preprocessor=True
    #         )
        
    #     signature = self.codegen.function_manager.get_definition_signature(
    #         name, return_type, params, None
    #     )
        
    #     self.codegen.add_toplevel_code(signature)
    
    def visit_Test(self, node: Test) -> None:
        self.tests.append(node)
        self.codegen.add_toplevel_code(f'nil {node.name}_test();')
