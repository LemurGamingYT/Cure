from dataclasses import dataclass, field
from typing import Any

from ir.nodes import ClassMembers, ClassMethod, ClassProperty, Position, Return, Identifier
from codegen.objects import Object, Type, Param, kwargs, TempVar
from codegen.c_manager import c_dec


@dataclass(**kwargs)
class Field:
    name: str
    type: Type
    default: Object | None = field(default=None)


class ClassManager:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
    
    def get_type(self, class_name: str) -> Type:
        return Type(class_name)
    
    def replace_this(self, name: str) -> str:
        return 'this' if self.is_this(name) else name
    
    def is_this(self, obj: Object | str) -> bool:
        if isinstance(obj, Object):
            return self.is_this(obj.code)
        
        return obj == '*(this)' or obj == 'this' or obj == '(*(this))'
    
    def initialiser(self, class_name: str, fields: list[Field]) -> str:
        return f"""typedef struct {{
    {'\n'.join(f'{field.type.c_type} {field.name};' for field in fields)}
}} {class_name};
""" if len(fields) > 0 else f"""typedef struct {{
    unsigned char _;
}} {class_name};
"""

    def property_to_code(self, property: ClassProperty, class_name: str, fields: list[Field]) -> None:
        cls_type = self.get_type(class_name)
        typ: Type = self.codegen.visit_TypeNode(property.type)
        default = self.codegen.visit(property.value) if property.value is not None else None
        fields.append(Field(property.name, typ, default))
        
        @c_dec(
            param_types=(Param('obj', cls_type),), is_property=True,
            func_name_override=f'{class_name}_{property.name}', add_to_class=self.codegen.c_manager,
            return_type=typ
        )
        def _(_, call_position: Position, obj: Object,
                name=property.name, t=typ) -> Object:
            return Object(f'(({obj}).{name})', t, call_position)
        
        @c_dec(
            param_types=(Param('obj', cls_type), Param('value', typ)), is_method=True,
            func_name_override=f'{class_name}_set_{property.name}', add_to_class=self.codegen.c_manager
        )
        def _(codegen, call_position: Position, obj: Object, value: Object,
                name=property.name) -> Object:
            codegen.prepend_code(f"""({obj}).{name} = {value};
""")
            return Object.NULL(call_position)

    def method_to_code(self, method: ClassMethod, class_name: str, fields: list[Field]) -> str:
        def eval_body():
            return self.codegen.visit_Body(method.body, params=params)
            
        cls_type = self.get_type(class_name)

        params: list[Param] = [Param('this', cls_type, True)] + [
            self.codegen.visit_ParamNode(param) for param in method.params
        ]
        return_type = self.codegen.visit_TypeNode(
            method.return_type) if method.return_type is not None else Type('nil')

        name = f'{class_name}_{method.name}'
        kwargs: dict[str, Any] = {}
        body: Object = eval_body()
        if method.name == class_name:
            name = f'{class_name}_new'
            return_type = cls_type
            kwargs = {'is_static': True}
            method.body.nodes.append(Return(method.body.pos, Identifier(method.body.pos, 'this')))
            body = eval_body()
            params = params[1:]

        @c_dec(
            param_types=tuple(params), is_method=True, return_type=return_type,
            func_name_override=name, add_to_class=self.codegen.c_manager,
            **kwargs
        )
        def _(codegen, call_position: Position, *args: Object) -> Object:
            new_args = list(args)

            if not codegen.scope.is_in_class:
                cls: str | TempVar
                if method.name == class_name:
                    instantiate_args = [
                        f'.{f.name} = {f.default}' for f in fields
                        if f.default is not None
                    ]
                    instantiate_expr = ''
                    if len(instantiate_args) > 0:
                        instantiate_expr = f' = {{{", ".join(instantiate_args)}}}'
                    
                    cls = codegen.create_temp_var(cls_type, call_position)
                    codegen.prepend_code(f"""{class_name} {cls}{instantiate_expr};
""")
                    new_args.insert(0, Object(f'&{cls}', cls_type, call_position))
                else:
                    cls = args[0].code
                    if not codegen.is_identifier(args[0].code) and not self.is_this(new_args[0]):
                        cls = codegen.create_temp_var(cls_type, call_position)
                        codegen.prepend_code(f"""{class_name} {cls};
""")
                        new_args[0].code = str(cls)
                    
                    if self.is_this(new_args[0]):
                        new_args[0].code = 'this'
                    else:
                        new_args[0].code = f'&{cls}'
            else:
                new_args[0].code = self.replace_this(new_args[0].code)
            
            args_str = ', '.join(arg.code for arg in new_args)
            return codegen.handle_free(
                body.free,
                Object(f'{name}({args_str})', return_type, call_position),
                call_position
            )
        
        params_str = ', '.join(str(p) for p in params)
        return f"""{return_type.c_type} {name}({params_str}) {{
{body}
}}
"""
    
    def create_class(self, class_name: str, members: ClassMembers) -> str:
        cls_type = self.get_type(class_name)
        code: list[str] = []
        self.codegen.valid_types.append(class_name)
        
        @c_dec(
            is_method=True, is_static=True,
            func_name_override=f'{class_name}_type', add_to_class=self.codegen.c_manager
        )
        def _(_, call_position: Position) -> Object:
            return Object(f'"{class_name}"', Type('string'), call_position)
        
        @c_dec(
            param_types=(Param('obj', cls_type),), is_method=True,
            func_name_override=f'{class_name}_to_string', add_to_class=self.codegen.c_manager
        )
        def _(_, call_position: Position, _obj: Object) -> Object:
            return Object(f'"class \'{class_name}\'"', Type('string'), call_position)
        
        fields: list[Field] = []
        without_properties = []
        for member in members:
            if isinstance(member, ClassProperty):
                self.property_to_code(member, class_name, fields)
            else:
                without_properties.append(member)
        
        for member in without_properties:
            code.append(self.method_to_code(member, class_name, fields))
        
        code.insert(0, self.initialiser(class_name, fields))
        return '\n'.join(code)
