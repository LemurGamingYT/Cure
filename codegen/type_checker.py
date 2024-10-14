from typing import Iterable

from codegen.objects import Type, POS_ZERO, EnvItem
from ir.nodes import TypeNode


class TypeChecker:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        
        self.valid_types: set[Type] = {
            Type('int'), Type('float'), Type('bool'), Type('string'), Type('nil'), Type('Math'),
            Type('System'), Type('Time'), Type('Cure'), Type('Fraction'), Type('Vector2'), Type('hex'),
            Type('StringBuilder'), Type('Timer'), Type('Logger')
        }
    
    def array_type(self, node: TypeNode) -> Type | None:
        if node.array_type is None:
            return None
        
        return self.codegen.array_manager.define_array(self.codegen.visit_TypeNode(node.array_type))
    
    def dict_type(self, node: TypeNode) -> Type | None:
        if node.dict_types is None:
            return None
        
        return self.codegen.dict_manager.define_dict(
            self.codegen.visit_TypeNode(node.dict_types[0]),
            self.codegen.visit_TypeNode(node.dict_types[1])
        )
    
    def function_type(self, node: TypeNode) -> Type | None:
        if node.func_type is None:
            return None
        
        param_types = tuple(self.codegen.visit_TypeNode(param) for param in node.func_type.params)
        return_type = self.codegen.visit_TypeNode(node.func_type.return_type)
        return self.codegen.function_manager.make_function_type(return_type, param_types, node.pos)
    
    def get_type(self, type_: Type | str) -> Type:
        """Get the type of the given type. Handles generic types.

        Args:
            type_ (Type | str): The type to get the type of.

        Returns:
            Type: The true type of the input type.
        """
        
        if isinstance(type_, str):
            type_ = Type(type_)
        
        return type_
    
    def add_type(self, type_: Type | str | Iterable[Type] | Iterable[str]) -> None:
        """Add a new type to `valid_types` which is used to check whether a type is valid.

        Args:
            type_ (Type | str | Iterable[Type] | Iterable[str]): The type(s) to add.
        """
        
        if isinstance(type_, str):
            type_ = Type(type_)
        elif isinstance(type_, Iterable):
            for t in type_:
                self.add_type(t)
            return
        
        self.codegen.scope.env[type_.type] = EnvItem(type_.type, type_, (self.codegen.pos or POS_ZERO))
        self.valid_types.add(type_)

    def is_valid_type(self, type_: Type | str) -> bool:
        """Checks whether a type is valid.

        Args:
            type_ (Type | str): The type to check.

        Returns:
            bool: True if the type is valid, False otherwise.
        """
        
        if isinstance(type_, str):
            type_ = Type(type_)
        
        return type_ in self.valid_types
