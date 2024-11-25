from ir import Interface, InterfaceMethod


class InterfaceManager:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
    
    def create(self, node: Interface) -> str:
        name = node.name
        self.codegen.type_checker.add_type(name)
        
        members = []
        for method in [m for m in node.members if isinstance(m, InterfaceMethod)]:
            params_str = self.codegen.function_manager.params_str(method.params)
            return_type = self.codegen.visit_TypeNode(method.return_type)
            members.append(f'{return_type.c_type} (*{method.name})({params_str})')
        
        return f"""typedef struct {{
{'\n'.join(member + ';' for member in members)}
}} {name};
"""
