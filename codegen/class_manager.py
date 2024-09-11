from ir.nodes import ClassMembers, ClassMethod, Position, TypeNode
from codegen.objects import Object, Type, Param, Function, Arg
from codegen.c_manager import c_dec


class ClassManager:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
    
    def method_to_function(self, method: ClassMethod) -> Function:
        """Convert a `ClassMethod` to a `Function` for easier class code generation.

        Args:
            method (ClassMethod): The `ClassMethod` to convert.

        Returns:
            Function: The output `Function` class.
        """
        
        params: list[Param] = [self.codegen.visit_ParamNode(p) for p in method.params]
        if any(p.default is not None for p in params):
            method.pos.error_here('Class methods to do not support default arguments')
        
        return Function(
            method.name,
            self.codegen.visit_TypeNode(method.return_type)\
                if method.return_type is not None else Type('nil'),
            params,
            self.codegen.visit_Body(method.body, params=params)
        )
    
    def define_default_attributes(self, class_name: str) -> None:
        """Define the default `type` and `to_string` attributes on the class.

        Args:
            class_name (str): The class name.
        """
        
        @c_dec(
            add_to_class=self.codegen.c_manager, func_name_override=f'{class_name}_type',
            is_method=True, is_static=True
        )
        def _(_, call_position: Position) -> Object:
            return Object(f'"{class_name}"', Type('string'), call_position)
        
        @c_dec(
            add_to_class=self.codegen.c_manager, func_name_override=f'{class_name}_to_string',
            param_types=(class_name,), is_method=True
        )
        def _(_, call_position: Position, _obj: Object) -> Object:
            return Object(f'"class \'{class_name}\'"', Type('string'), call_position)
    
    def struct_code(self, class_name: str, members: ClassMembers) -> str:
        """Get the base struct C code.
        
        Args:
            class_name (str): The name of the class.
            members (ClassMembers): The members of the class.
        
        Returns:
            str: The C struct code.
        """
        
        struct_fields: list[Param] = []
        code = ''
        init_idx = -1
        for i, member in enumerate(members):
            if member.name == 'init' and isinstance(member, ClassMethod):
                member.return_type = TypeNode(member.pos, class_name)
                member.name = (callee := f'{class_name}_new')
                func = self.method_to_function(member)
                struct_fields.extend(func.params)
                init_idx = i
                
                for p in func.params:
                    @c_dec(
                        param_types=(class_name,),
                        add_to_class=self.codegen.c_manager,
                        func_name_override=f'{class_name}_{p.name}',
                        is_property=True
                    )
                    def _(_, call_position: Position, obj: Object,
                            typ=p.type, name=p.name) -> Object:
                        return Object(f'(({obj}).{name})', typ, call_position)
                    
                    @c_dec(
                        param_types=(class_name, p.type.c_type),
                        add_to_class=self.codegen.c_manager,
                        func_name_override=f'{class_name}_set_{p.name}',
                        is_method=True
                    )
                    def _(codegen, call_position: Position, obj: Object, value: Object,
                          name=p.name) -> Object:
                        codegen.prepend_code(f'({obj}).{name} = {value};')
                        return Object.NULL(call_position)
                
                params_str = ', '.join(str(p) for p in func.params)
                code += f"""{class_name} {callee}({params_str}) {{
{self.codegen.visit_Body(member.body, params=func.params)}
return ({class_name}){{ {", ".join(f'.{p.name} = {p.name}' for p in func.params)} }};
}}
"""
                
                @c_dec(
                    param_types=tuple(p.type.c_type for p in func.params),
                    is_static=True, is_method=True,
                    add_to_class=self.codegen.c_manager, func_name_override=callee
                )
                def _(_, call_position: Position, *args) -> Object:
                    return Object(
                        func.call_code([Arg(arg) for arg in args]),
                        func.returns, call_position
                    )
                
                break
        
        if init_idx != -1:
            members.pop(init_idx)
        
        return f"""typedef struct {{
    unsigned char _;
}} {class_name};
{code}
""" if init_idx == -1 else f"""typedef struct {{
    {'\n'.join(str(field) + ';' for field in struct_fields)}
}} {class_name};
{code}
"""

    def define_method(self, class_name: str, method: ClassMethod) -> str:
        """Define the class' members based on the `members` parameter.

        Args:
            class_name (str): The name of the class.
            method (ClassMethod): The ClassMethod that represents the method of `class_name`.
        
        Returns:
            str: The C code for the method.
        """
        
        method.name = (callee := f'{class_name}_{method.name}')
        func = self.method_to_function(method)
        all_params = [Param('self', Type(class_name), True)] + func.params
        params_str = ', '.join(str(p) for p in all_params)
        body = self.codegen.visit_Body(method.body, params=all_params)
        
        @c_dec(
            param_types=tuple(p.type.c_type for p in func.params),
            add_to_class=self.codegen.c_manager, func_name_override=callee,
            is_method=True
        )
        def _(codegen, call_position: Position, *args, body=body) -> Object:
            obj = func(codegen, call_position, *[Arg(arg) for arg in args])
            if obj is None:
                call_position.error_here(f'Method \'{callee}\' returned absolutely nothing')
            
            return codegen.handle_free(body.free, obj, call_position)
        
        return f"""{func.returns.c_type} {callee}({params_str}) {{
{body}
}}
"""
    
    def create_class(self, class_name: str, members: ClassMembers) -> str:
        """Define a class.

        Args:
            class_name (str): The name of the class.
            members (ClassMembers): The members of the class.

        Returns:
            str: The C code to make the class and it's members
        """
        
        self.codegen.valid_types.append(class_name)
        
        self.define_default_attributes(class_name)
        code = self.struct_code(class_name, members)
        
        for member in members:
            if isinstance(member, ClassMethod):
                code += f"""
{self.define_method(class_name, member)}
"""
        
        return code
