from codegen.objects import Object, Position, Type, Param
from codegen.extern.stddef_h import size_t
from codegen.extern.stdio_h import long
from codegen.c_manager import c_dec


div_t = Type('div_t')
ldiv_t = Type('ldiv_t')
void_ptr = Type('void*')

class stdlib_h:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type(div_t)
        codegen.type_checker.add_type(ldiv_t)
        codegen.type_checker.add_type(void_ptr)
        
        codegen.add_toplevel_constant('EXIT_SUCCESS', Type('int'), add_code=False)
        codegen.add_toplevel_constant('EXIT_FAILURE', Type('int'), add_code=False)
        codegen.add_toplevel_constant('RAND_MAX', Type('int'), add_code=False)
        codegen.add_toplevel_constant('RAND_MIN', Type('int'), add_code=False)
        codegen.add_toplevel_constant('MB_CUR_MAX', Type('int'), add_code=False)

        @c_dec(params=(Param('div_t', div_t),), is_property=True, add_to_class=self)
        def quotient(_, call_position: Position, div_t: Object) -> Object:
            return Object(f'({div_t}).quot', Type('int'), call_position)

        @c_dec(params=(Param('div_t', div_t),), is_property=True, add_to_class=self)
        def remainder(_, call_position: Position, div_t: Object) -> Object:
            return Object(f'({div_t}).rem', Type('int'), call_position)

        @c_dec(params=(Param('str', Type('string')),), can_user_call=True, add_to_class=self)
        def _atoi(_, call_position: Position, str: Object) -> Object:
            return Object(f'(atoi({str}))', Type('int'), call_position)

        @c_dec(
            params=(Param('nitems', size_t), Param('size', size_t)),
            can_user_call=True, add_to_class=self
        )
        def _calloc(_, call_position: Position, nitems: Object, size: Object) -> Object:
            return Object(f'(calloc({nitems}, {size}))', void_ptr, call_position)

        @c_dec(params=(Param('size', size_t),), can_user_call=True, add_to_class=self)
        def _malloc(_, call_position: Position, size: Object) -> Object:
            return Object(f'(malloc({size}))', void_ptr, call_position)

        @c_dec(params=(Param('ptr', void_ptr),), can_user_call=True, add_to_class=self)
        def _free(codegen, call_position: Position, ptr: Object) -> Object:
            codegen.prepend_code(f'free({ptr});')
            return Object.NULL(call_position)

        @c_dec(
            params=(Param('ptr', void_ptr), Param('size', size_t)),
            can_user_call=True, add_to_class=self
        )
        def _realloc(_, call_position: Position, ptr: Object, size: Object) -> Object:
            return Object(f'(realloc({ptr}, {size}))', size_t, call_position)

        @c_dec(params=(Param('x', Type('int')),), can_user_call=True, add_to_class=self)
        def _abs(_, call_position: Position, x: Object) -> Object:
            return Object(f'(abs({x}))', Type('int'), call_position)

        @c_dec(
            params=(Param('numer', Type('int')), Param('denom', Type('int'))),
            can_user_call=True, add_to_class=self
        )
        def _div(_, call_position: Position, numer: Object, denom: Object) -> Object:
            return Object(f'(div({numer}, {denom}))', div_t, call_position)

        @c_dec(params=(Param('x', long),), can_user_call=True, add_to_class=self)
        def _labs(_, call_position: Position, x: Object) -> Object:
            return Object(f'(labs({x}))', long, call_position)

        @c_dec(
            params=(Param('numer', long), Param('denom', long)),
            can_user_call=True, add_to_class=self
        )
        def _ldiv(_, call_position: Position, numer: Object, denom: Object) -> Object:
            return Object(f'(ldiv({numer}, {denom}))', ldiv_t, call_position)

        @c_dec(can_user_call=True, add_to_class=self)
        def _rand(_, call_position: Position) -> Object:
            return Object('(rand())', Type('int'), call_position)

        @c_dec(params=(Param('seed', Type('int')),), can_user_call=True, add_to_class=self)
        def _srand(_, call_position: Position, seed: Object) -> Object:
            return Object(f'(srand({seed}))', Type('nil'), call_position)
        
        @c_dec(params=(Param('name', Type('string')),), can_user_call=True, add_to_class=self)
        def _getenv(_, call_position: Position, name: Object) -> Object:
            return Object(f'(getenv({name}))', Type('string'), call_position)
        
        @c_dec(params=(Param('string', Type('string')),), can_user_call=True, add_to_class=self)
        def _system(_, call_position: Position, string: Object) -> Object:
            return Object(f'(system({string}))', Type('int'), call_position)
        
        @c_dec(params=(
            Param('str', Type('string')), Param('n', size_t)
        ), can_user_call=True, add_to_class=self)
        def _mblen(_, call_position: Position, str: Object, n: Object) -> Object:
            return Object(f'(mblen({str}, {n}))', Type('int'), call_position)
        
        @c_dec(can_user_call=True, add_to_class=self)
        def _abort(codegen, call_position: Position) -> Object:
            codegen.prepend_code('abort();')
            return Object.NULL(call_position)
        
        @c_dec(params=(Param('status', Type('int')),), can_user_call=True, add_to_class=self)
        def _exit(_, call_position: Position, status: Object) -> Object:
            codegen.prepend_code(f'exit({status});')
            return Object.NULL(call_position)
