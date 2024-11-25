from typing import Iterable

from codegen.objects import Type, FunctionInfo
from ir.nodes import TypeNode


class TypeChecker:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        
        codegen.metadata.setdefault('valid_types', {
            Type('int'): Type('int'), Type('float'): Type('float'), Type('bool'): Type('bool'),
            Type('string'): Type('string'), Type('nil'): Type('nil'), Type('Math'): Type('Math'),
            Type('System'): Type('System'), Type('Time'): Type('Time'), Type('Cure'): Type('Cure'),
            Type('Fraction'): Type('Fraction'), Type('Vector2'): Type('Vector2'),
            Type('hex'): Type('hex'), Type('StringBuilder'): Type('StringBuilder'),
            Type('Timer'): Type('Timer'), Type('Logger'): Type('Logger'),
            Type('Random'): Type('Random')
        })
        
        # codegen.metadata.setdefault('function_info_name_map', {})
    
    def make_function_info(self, return_type: Type, param_types: Iterable[Type]) -> FunctionInfo:
        # seems to bring more problems than it solves
        # for info in self.codegen.metadata['function_info_name_map'].values():
        #     if info.return_type == return_type and info.param_types == tuple(param_types):
        #         return info
        
        info = FunctionInfo(return_type, tuple(param_types))
        self.typedef_function_ptr(info)
        
        # self.codegen.metadata['function_info_name_map'][info.typedef_name] = info
        return info
    
    def typedef_function_ptr(self, function_info: FunctionInfo) -> None:
        temp_name = self.codegen.get_unique_name()
        self.codegen.c_manager.reserve(temp_name)
        function_info.typedef_name = str(temp_name)
        
        return_type = function_info.return_type.c_type
        param_types = ', '.join(param_type.c_type for param_type in function_info.param_types)
        self.codegen.add_toplevel_code(f'typedef {return_type} (*{temp_name})({param_types});')
    
    def function_type(self, node: TypeNode) -> Type | None:
        if node.func_type is None:
            return None
        
        param_types = tuple(self.codegen.visit_TypeNode(param) for param in node.func_type.params)
        return_type = self.codegen.visit_TypeNode(node.func_type.return_type)
        return self.make_function_info(return_type, param_types).as_type()
    
    def get_type(self, type_: Type | str) -> Type | None:
        """Get the type of the given type. Handles generic types.

        Args:
            type_ (Type | str): The type to get the type of.

        Returns:
            Type | None: The true type of the input type or possibly None if the type is not valid.
        """
        
        if isinstance(type_, str):
            type_ = Type(type_)
        
        return self.codegen.metadata['valid_types'].get(type_)
    
    def add_type(self, type_: Type | str | Iterable[Type] | Iterable[str] | dict[Type, Type],
                 value_type: Type | None = None) -> None:
        """Add a new type to `valid_types` which is used to check whether a type is valid.

        Args:
            type_ (Type | str | Iterable[Type] | Iterable[str] | dict[Type, Type]): The type(s) to add.
            value_type (Type | None, optional): The type of the type. Defaults to the type.
        """
        
        if isinstance(type_, str):
            type_ = Type(type_)
        elif isinstance(type_, dict):
            for k, v in type_.items():
                self.add_type(k, v)
            return
        elif isinstance(type_, Iterable):
            for t in type_:
                self.add_type(t)
            return
        
        self.codegen.metadata['valid_types'][type_] = value_type or type_

    def is_valid_type(self, type_: Type | str) -> bool:
        """Checks whether a type is valid.

        Args:
            type_ (Type | str): The type to check.

        Returns:
            bool: True if the type is valid, False otherwise.
        """
        
        if isinstance(type_, str):
            type_ = Type(type_)
        
        return type_ in self.codegen.metadata['valid_types']
    
    def set_type_value(self, type_: Type | str, value_type: Type) -> None:
        """Sets the value type of a type.

        Args:
            type_ (Type | str): The type to set the value type of.
            value_type (Type): The value type to set.
        """

        if isinstance(type_, str):
            type_ = Type(type_)

        self.codegen.metadata['valid_types'][type_] = value_type
