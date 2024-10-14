from codegen.objects import Object, Position, Free, Type, Arg, TempVar, Param
from codegen.c_manager import c_dec


class BigFloat:
    def __init__(self, codegen) -> None:
        codegen.c_manager.init_class(self, 'BigFloat', Type('BigFloat'))
        codegen.add_toplevel_code("""typedef struct {
    BigInt integer_part;
    BigInt fractional_part;
    int exponent;
} BigFloat;
""")
        
        @c_dec(param_types=(Param('bf', Type('BigFloat')),), is_method=True, add_to_class=self)
        def _BigFloat_to_string(codegen, call_position: Position, bf: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free,
                                                   default_expr='NULL')
            int_part: TempVar = codegen.create_temp_var(Type('string'), call_position)
            frac_part: TempVar = codegen.create_temp_var(Type('string'), call_position)
            total_length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            
            codegen.prepend_code(f"""string {int_part} = {codegen.call('BigInt_to_string',
    [Arg(Object(f'({bf}).integer_part', Type('BigInt'), call_position))], call_position
)};
string {frac_part} = {codegen.call('BigInt_to_string',
    [Arg(Object(f'({bf}).fractional_part', Type('BigInt'), call_position))], call_position
)};

int {total_length} = strlen({int_part}) + strlen({frac_part}) + 20;
{buf} = (string)malloc({total_length});
{codegen.c_manager.buf_check(buf)}

snprintf({buf}, {total_length}, "%s.%se%d", {int_part}, {frac_part}, ({bf}).exponent);
free({int_part});
free({frac_part});
""")
            
            return buf.OBJECT()
        
        @c_dec(
            param_types=(Param('bf', Type('BigFloat')), Param('bf', Type('BigFloat'))),
            add_to_class=self
        )
        def _BigFloat_add_BigFloat(codegen, call_position: Position, a: Object,
                                b: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('BigFloat'), call_position)
            codegen.prepend_code(f"""BigFloat {res};
{res}.integer_part = {codegen.call('BigInt_add_BigInt',
    [
        Arg(Object(f'({a}).integer_part', Type('BigInt'), call_position)),
        Arg(Object(f'({b}).integer_part', Type('BigInt'), call_position))
    ], call_position
)};
{res}.fractional_part = {codegen.call('BigInt_add_BigInt',
    [
        Arg(Object(f'({a}).fractional_part', Type('BigInt'), call_position)),
        Arg(Object(f'({b}).fractional_part', Type('BigInt'), call_position))
    ], call_position
)};
{res}.exponent = ({a}).exponent > ({b}).exponent ? ({a}).exponent
    : ({b}).exponent;
while ({res}.fractional_part.length > 0 && {res}.fractional_part.digits[
    {res}.fractional_part.length - 1
] == 0) {{
    {res}.fractional_part.length--;
}}
""")
            
            return res.OBJECT()
        
        @c_dec(
            param_types=(Param('bf', Type('BigFloat')), Param('bf', Type('BigFloat'))),
            add_to_class=self
        )
        def _BigFloat_sub_BigFloat(codegen, call_position: Position, a: Object,
                                b: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('BigFloat'), call_position)
            codegen.prepend_code(f"""BigFloat {res} = {{
    .integer_part = {codegen.call('BigInt_sub_BigInt',
        [
            Arg(Object(f'({a}).integer_part', Type('BigInt'), call_position)),
            Arg(Object(f'({b}).integer_part', Type('BigInt'), call_position))
        ], call_position
    )},
    .fractional_part = {codegen.call('BigInt_sub_BigInt',
        [
            Arg(Object(f'({a}).fractional_part', Type('BigInt'), call_position)),
            Arg(Object(f'({b}).fractional_part', Type('BigInt'), call_position))
        ], call_position
    )},
    .exponent = ({a}).exponent > ({b}).exponent ? ({a}).exponent : ({b}).exponent
}};

while ({res}.fractional_part.length > 0 && {res}.fractional_part.digits[
    {res}.fractional_part.length - 1
] == 0) {{
    {res}.fractional_part.length--;
}}
""")
            
            return res.OBJECT()
        
        @c_dec(
            param_types=(Param('bf', Type('BigFloat')), Param('f', Type('float'))),
            add_to_class=self
        )
        def _BigFloat_add_float(codegen, call_position: Position, bf: Object, f: Object) -> Object:
            float_str: Object = codegen.call('float_to_string', [Arg(f)], call_position)
            float_as_bf = _BigFloat_new(codegen, call_position, float_str)
            return _BigFloat_add_BigFloat(codegen, call_position, bf, float_as_bf)
        
        @c_dec(
            param_types=(Param('num', Type('string')),), is_method=True, is_static=True,
            add_to_class=self
        )
        def _BigFloat_new(codegen, call_position: Position, num: Object) -> Object:
            temp: TempVar = codegen.create_temp_var(Type('BigFloat'), call_position)
            string: TempVar = codegen.create_temp_var(Type('string'), call_position)
            int_part: TempVar = codegen.create_temp_var(Type('string'), call_position)
            frac_part: TempVar = codegen.create_temp_var(Type('string'), call_position)
            exp_part: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""BigFloat {temp};
char {string}[] = {num};
string {int_part} = strtok({string}, ".");
string {frac_part} = strtok(NULL, "e");
string {exp_part} = strtok(NULL, "");
""")
            codegen.prepend_code(f"""{temp}.integer_part = {codegen.call('BigInt_new',
    [Arg(int_part.OBJECT())], call_position
)};
{temp}.fractional_part = {codegen.call('BigInt_new',
    [Arg(Object(str(frac_part) or '0', Type('string'), call_position))], call_position
)};
{temp}.exponent = {exp_part} ? atoi({exp_part}) : 0;
""")

            return temp.OBJECT()
