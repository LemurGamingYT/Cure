from compiler.std.decorator import std_decorator
from compiler.constants import Type, Statement


@std_decorator({'x': {Type.all_types}})
def _print(_, x: Statement) -> Statement:
    if x.type == Type.string:
        return Statement(f'printf("%s\\n", {x.code})', Type.nil)

    return Statement(f'printf("%s\\n", {x.str_type}_repr({x.code}))', Type.nil)


@std_decorator({'x': {Type.all_types}})
def _to_string(_, x: Statement) -> Statement:
    if x.type == Type.string:
        return x

    return Statement(f'{x.str_type}_repr({x.code})', Type.string)


@std_decorator({'x': {Type.float, Type.int, Type.bool, Type.string}})
def _to_int(_, x: Statement) -> Statement:
    if x.type == Type.int:
        return x

    return Statement(f'{x.str_type}_to_Int({x.code})', Type.int)


@std_decorator({'x': {Type.float, Type.int, Type.string}})
def _to_float(_, x: Statement) -> Statement:
    if x.type == Type.float:
        return x

    return Statement(f'{x.str_type}_to_Float({x.code})', Type.float)


@std_decorator({'x': {Type.all_types}})
def _to_bool(_, x: Statement) -> Statement:
    if x.type == Type.bool:
        return x

    return Statement(f'{x.str_type}_to_Bool({x.code})', Type.bool)


@std_decorator({'x': {Type.all_types}})
def _type(_, x: Statement) -> Statement:
    return Statement(f'{x.str_type}_type({x.code})', Type.string)


public_funcs = {
    'print': _print,
    'to_string': _to_string,
    'to_int': _to_int,
    'to_float': _to_float,
    'to_bool': _to_bool,
    'typeof': _type
}
