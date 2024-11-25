from codegen.objects import Object, Position, Type, Param, TempVar, Free
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec


class Random:
    def __init__(self, c_manager) -> None:
        c_manager.reserve('__Random_charset')
        c_manager.codegen.add_toplevel_code("""typedef struct {
    int seed, state;
} Random;

const char __Random_charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
""")
        
        c_manager.init_class(self, 'Random', Type('Random'))
        
        def random_no_seed(codegen, call_position: Position) -> Object:
            return _Random_new(
                codegen, call_position, Object('(int)time(NULL)', Type('int'), call_position)
            )
        
        @c_dec(
            params=(Param('seed', Type('int')),), is_method=True, is_static=True,
            add_to_class=self, overloads={
                OverloadKey(Type('Random'), ()): OverloadValue(random_no_seed)
            }
        )
        def _Random_new(codegen, call_position: Position, seed: Object) -> Object:
            r: TempVar = codegen.create_temp_var(Type('Random'), call_position)
            codegen.prepend_code(f'Random {r} = {{ .seed = {seed}, .state = {seed} }};')
            return r.OBJECT()

        def internal_next(codegen, call_position: Position, r: Object) -> Object:
            x: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""unsigned int {x} = {r.attr('state')};
{x} ^= {x} << 13;
{x} ^= {x} >> 17;
{x} ^= {x} << 5;
{r.attr('state')} = {x};
""")
            
            return x.OBJECT()

        @c_dec(params=(Param('r', Type('Random')),), is_method=True, add_to_class=self)
        def _Random_next(codegen, call_position: Position, r: Object) -> Object:
            return internal_next(codegen, call_position, r).cast(Type('int'))
    
        def rand_start0(codegen, call_position: Position, r: Object, max: Object) -> Object:
            return _Random_next_int(
                codegen, call_position, r,
                Object('0', Type('int'), call_position), max
            )
        
        @c_dec(
            params=(
                Param('r', Type('Random')), Param('min', Type('int')),
                Param('max', Type('int')),
            ), is_method=True, add_to_class=self, overloads={
                OverloadKey(Type('int'), (
                    Param('r', Type('Random')), Param('max', Type('int'))
                )): OverloadValue(rand_start0)
            }
        )
        def _Random_next_int(codegen, call_position: Position, r: Object, min: Object,
                             max: Object) -> Object:
            return Object(
                f'(({min}) + ({internal_next(codegen, call_position, r)} % (({max}) - ({min}))))',
                Type('int'), call_position
            )
        
        def Random_charset_strings(codegen, call_position: Position, r: Object, length: Object,
                                   charset: Object) -> Object:
            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""string {res} = (string)malloc(({length}) + 1);
{codegen.c_manager.buf_check(str(res))}
for (int {i} = 0; {i} < {length}; {i}++) {{
""")
            codegen.prepend_code(f"""{res}[{i}] = {charset}[
        {internal_next(codegen, call_position, r)} % (sizeof({charset}) - 1)
    ];
}}

{res}[{length}] = '\\0';
""")
            
            return res.OBJECT()
        
        @c_dec(
            params=(Param('r', Type('Random')), Param('length', Type('int'))),
            is_method=True, add_to_class=self, overloads={
                OverloadKey(Type('string'), (
                    Param('r', Type('Random')), Param('length', Type('int')),
                    Param('charset', Type('string'))
                )): OverloadValue(Random_charset_strings)
            }
        )
        def _Random_next_string(codegen, call_position: Position, r: Object, length: Object) -> Object:
            return Random_charset_strings(
                codegen, call_position, r, length,
                Object('__Random_charset', Type('string'), call_position)
            )
        
        @c_dec(
            params=(Param('r', Type('Random')),), is_method=True, add_to_class=self
        )
        def _Random_next_bool(_, call_position: Position, r: Object) -> Object:
            return Object(f'({r.attr("state")} % 2 == 1)', Type('bool'), call_position)
