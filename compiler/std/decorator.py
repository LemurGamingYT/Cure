from typing import Callable, Any
from functools import wraps

from compiler.constants import Statement, Type, error


def check_param_types(types: set[Type], value: Statement) -> None:
    value_type = value.type
    
    if value_type not in types and Type.all_types not in types:
        types = ' or '.join(t.str_type for t in types)
        error('Type', f'Expected type \'{types}\' but got type \'{value_type.str_type}\'')


def std_decorator(params: dict = None) -> Callable:
    params = {} or params
    def decorator(func: Callable) -> Callable:
        setattr(func, 'params', params)
        
        @wraps(func)
        def wrapper(compiler, args, **kwargs) -> Any:
            for arg, param in zip(args, params.values()):
                check_param_types(param, arg)

            return func(compiler, *args, **kwargs)
        
        return wrapper
    
    return decorator
