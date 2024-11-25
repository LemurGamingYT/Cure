from logging import debug
from typing import Any

from codegen.objects import Object, Type, Param, TempVar, EnvItem, Class, Field, Free
from ir.nodes import ClassMembers, ClassMethod, ClassProperty, Position
from codegen.c_manager import c_dec
from ir import op_map


# the free name used in all of the class free functions
FREE_NAME = 'cls'

class ClassManager:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
    
    def get_type(self, class_name: str) -> Type:
        return Type(class_name)
    
    def get_free_name(self, class_: Class) -> str:
        return f'{class_.name}_free'
    
    def has_method(self, name: str, members: ClassMembers) -> ClassMethod | None:
        for member in members:
            if isinstance(member, ClassMethod) and member.name == name:
                return member
        
        return None
    
    def is_operator_overload_name(self, name: str) -> tuple[bool, str]:
        if len((split_name := name.split('_'))) == 2 and split_name[0] in op_map.values():
            op_name, _ = split_name
            op_symbol = list(op_map.keys())[list(op_map.values()).index(op_name)]
            return True, op_symbol
        
        return False, ''
    
    def handle_name(self, method: ClassMethod, params: list[Param], class_: Class) -> str:
        name = method.name
        if name.startswith('~'):
            name = f'{class_.type}_deconstructor_{name[1:]}'
            class_.destructor_methods.append(name)
            if len(method.params) > 0:
                method.pos.error_here('Destructor cannot have parameters')
            
            return name
        
        if name not in op_map:
            is_overload_name, op_symbol = self.is_operator_overload_name(name)
            if is_overload_name:
                method.pos.info_here('This overloads an operator. If this is intentional, '\
                    f'use the operator symbol \'{op_symbol}\' instead of it\'s name')
            
            return f'{class_.type.c_type}_{name}'
        
        if len(params) != 2:
            method.pos.error_here('Operator overloading function must have exactly 2 parameters')
        
        op_name = op_map[name]
        other_param = params[1]
        return f'{class_.type.c_type}_{op_name}_{other_param.type.c_type}'
    
    def initialiser(self, class_name: str, fields: list[Field]) -> str:
        return f"""typedef struct {{
    {'\n'.join(f'{field.type.c_type} {field.name};' for field in fields)}
}} {class_name};
""" if len(fields) > 0 else f"""typedef struct {{
    unsigned char _;
}} {class_name};
"""

    def property_to_code(self, property: ClassProperty, cls_type: Type, class_: Class) -> None:
        typ: Type = self.codegen.visit_TypeNode(property.type)
        default = self.codegen.visit(property.value) if property.value is not None else None
        class_.fields.append(Field(property.name, typ, default, property.public))
        
        @c_dec(
            params=(Param('obj', cls_type),), is_property=True,
            func_name_override=f'{cls_type}_{property.name}', add_to_class=self.codegen.c_manager,
            return_type=typ
        )
        def _(codegen, call_position: Position, obj: Object,
                name=property.name, t=typ, public=property.public) -> Object:
            if not public and not codegen.scope.is_in_class:
                call_position.error_here(f'\'{name}\' is not public')
            
            return Object(f'(({obj}).{name})', t, call_position)
        
        @c_dec(
            params=(Param('obj', cls_type), Param('value', typ)), is_method=True,
            func_name_override=f'{cls_type}_set_{property.name}', add_to_class=self.codegen.c_manager
        )
        def _(codegen, call_position: Position, obj: Object, value: Object,
                name=property.name, public=property.public) -> Object:
            if not public and not codegen.scope.is_in_class:
                call_position.error_here(f'\'{name}\' is not public')
            
            codegen.prepend_code(f"""({obj}).{name} = {value};
""")
            if value.free is not None:
                codegen.scope.remove_free(value.free)
                
                cls_name_free = value.free.replace_from_class(Free(
                    object_name=f'{value.free.object_name}',
                    basic_name=f'(*{FREE_NAME}).{name}'
                ))
                
                if cls_name_free not in class_.free_members:
                    class_.free_members.append(value.free.replace_from_class(cls_name_free))
            
            return Object.NULL(call_position)

    def method_to_code(self, method: ClassMethod, cls_type: Type, class_: Class) -> str:
        def eval_body(**kwargs) -> Object:
            return self.codegen.visit_Body(method.body, params=params, **kwargs)
        
        if method.extend_type is not None:
            method.pos.error_here('Type extension is not allowed in a class context')

        this = Param('this', cls_type, True)
        params: list[Param] = [this] + [
            self.codegen.visit_ParamNode(param) for param in method.params
        ]
        params_str = self.codegen.function_manager.params_str(params)
        
        return_type = self.codegen.visit_TypeNode(
            method.return_type) if method.return_type is not None else Type('nil')

        name = self.handle_name(method, params, class_)
        kwargs: dict[str, Any] = {'is_static': method.is_static}
        body: Object = eval_body()
        if method.name == cls_type.type:
            name = f'{cls_type}_new'
            return_type = Type('nil')
            params = params[1:]
            kwargs['is_static'] = True
        elif kwargs['is_static']:
            params = params[1:]
            params_str = self.codegen.function_manager.params_str(params)
        
        if not method.is_overriding:
            for base in class_.bases:
                if base.class_ is None:
                    continue
                
                if any(m.name == method.name for m in base.class_.members):
                    method.pos.error_here(
                        f'\'{method.name}\' is defined in a base class. If you meant to override it, '\
                        'use the \'override\' keyword'
                    )

        @c_dec(
            params=tuple(params), is_method=True, return_type=return_type,
            func_name_override=name, add_to_class=self.codegen.c_manager, **kwargs
        )
        def _(codegen, call_position: Position, *args: Object) -> Object:
            if not method.is_public and not codegen.scope.is_in_class:
                call_position.error_here(f'\'{method.name}\' is not public')
            
            passing_args = [*args]
            if method.name == cls_type.type:
                free_name = Free(free_name=self.get_free_name(class_))
                cls: TempVar = codegen.create_temp_var(cls_type, call_position, free=free_name)
                free_name.object_name = f'&{cls}'
                passing_args.insert(0, cls.REFERENCE())
                codegen.prepend_code(f"""{cls_type.c_type} {cls} = {{0}};
{name}({', '.join(str(arg) for arg in passing_args)});
""")
                for field in class_.fields:
                    if field.default is None:
                        continue
                    
                    codegen.prepend_code(f'{cls}.{field.name} = {field.default};')
                
                return cls.OBJECT()
            else:
                if len(passing_args) > 0:
                    # if the first argument is an identifier, this means that the class instance was
                    # accidentally not passed as a pointer
                    if codegen.is_identifier(passing_args[0]):
                        passing_args[0] = Object(f'&({passing_args[0]})', cls_type, call_position)
                    else:
                        # if the first argument is not an identifier and not passed as a pointer,
                        # it must be an expression that evaluates to the class
                        if not str(passing_args[0]).startswith('&'):
                            # extract out into a temporary variable to pass as a pointer
                            cls = codegen.create_temp_var(cls_type, call_position)
                            codegen.prepend_code(f'{cls_type.c_type} {cls} = {passing_args[0]};')
                            passing_args[0] = cls.REFERENCE()
            
            args_str = ', '.join(str(arg) for arg in passing_args)
            return codegen.handle_free(
                body.free, Object(f'{name}({args_str})', return_type, call_position),
                call_position
            )
        
        return f"""{return_type.c_type} {name}({params_str}) {{
{body}
}}
"""

    def inherit(self, cls_type: Type, base: Class, class_: Class) -> str:
        inheritance_code: list[str] = []
        for member in base.members:
            if member.name == base.name:
                continue # skip constructor
            
            if isinstance(member, ClassProperty):
                self.property_to_code(member, cls_type, class_)
            else:
                if any(m.name == member.name for m in class_.members):
                    continue
                
                member.is_overriding = True
                inheritance_code.append(self.method_to_code(member, cls_type, class_))
        
        return '\n'.join(inheritance_code)
    
    def create_class(
        self, class_name: str, members: ClassMembers, pos: Position, bases: list[EnvItem]
    ) -> str:
        cls_type = self.get_type(class_name)
        code: list[str] = []
        self.codegen.type_checker.add_type(cls_type)
        fields: list[Field] = [] # modified later
        class_ = Class(class_name, cls_type, pos, bases, fields, members)
        self.codegen.scope.env[class_name] = EnvItem(class_name, cls_type, pos, class_=class_)
        free_name = self.get_free_name(class_)
        self.codegen.c_manager.init_class(self.codegen.c_manager, class_name, cls_type)
        
        for base in bases:
            base_cls = base.class_
            if base_cls is None:
                continue

            code.append(self.inherit(cls_type, base_cls, class_))
        
        if (type_method := self.has_method('type', members)) is not None:
            type_method.pos.error_here('Type method cannot be defined in a class')
        
        without_properties = []
        for member in members:
            if isinstance(member, ClassProperty):
                self.property_to_code(member, cls_type, class_)
            else:
                without_properties.append(member)
        
        self.codegen.add_toplevel_code(self.initialiser(class_name, fields))
        
        for member in without_properties:
            code.append(self.method_to_code(member, cls_type, class_))
        
        debug(f'\'{class_name}\' has {len(members)} members, needs {len(class_.free_members)} '\
            f'frees, has {len(class_.destructor_methods)} deconstructors and {len(fields)} fields')
        return '\n'.join(code) + f"""void {free_name}({cls_type.c_type}* {FREE_NAME}) {{
    {'\n'.join(f'{deconstructor}({FREE_NAME});' for deconstructor in class_.destructor_methods)}
    {'\n'.join(free.code for free in class_.free_members)}
}}
"""
