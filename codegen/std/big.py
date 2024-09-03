from codegen.objects import Object, Position, Free, Type, Arg
from codegen.c_manager import c_dec


MAX_DIGITS = 1000

class big:
    def __init__(self, codegen) -> None:
        codegen.valid_types.extend(('BigInt', 'BigFloat'))
        codegen.add_toplevel_code(f"""#ifndef CURE_BIG_H
typedef struct {{
    char digits[{MAX_DIGITS}];
    size_t length;
}} BigInt;

typedef struct {{
    BigInt integer_part;
    BigInt fractional_part;
    int exponent;
}} BigFloat;
#define CURE_BIG_H
#endif
""")
    
    @c_dec(is_method=True)
    def _BigFloat_type(self, _, call_position: Position) -> Object:
        return Object('"BigFloat"', Type('string'), call_position)
    
    @c_dec(param_types=('BigFloat',), is_method=True)
    def _BigFloat_to_string(self, codegen, call_position: Position, bf: Object) -> Object:
        codegen.c_manager.include('<string.h>', codegen)
        
        buf_free = Free()
        buf = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
        int_part = codegen.create_temp_var(Type('string'), call_position)
        frac_part = codegen.create_temp_var(Type('string'), call_position)
        total_length = codegen.create_temp_var(Type('int'), call_position)
        
        codegen.prepend_code(f"""string {buf} = NULL;
string {int_part} = {self._BigInt_to_string(
codegen, call_position,
Object(f'({bf.code}).integer_part', Type('BigInt'), call_position)
).code};
string {frac_part} = {self._BigInt_to_string(
codegen, call_position,
Object(f'({bf.code}).fractional_part', Type('BigInt'), call_position)
).code};

int {total_length} = strlen({int_part}) + strlen({frac_part}) + 20;
{buf} = (string)malloc({total_length});
{codegen.c_manager.buf_check(buf)}

snprintf({buf}, {total_length}, "%s.%se%d", {int_part}, {frac_part}, ({bf.code}).exponent);
free({int_part});
free({frac_part});
""")
        
        return Object(buf, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('BigFloat', 'BigFloat'))
    def _BigFloat_add_BigFloat(self, codegen, call_position: Position, a: Object,
                               b: Object) -> Object:
        res = codegen.create_temp_var(Type('BigFloat'), call_position)
        codegen.prepend_code(f"""BigFloat {res};
{res}.integer_part = {self._BigInt_add_BigInt(
    codegen, call_position,
    Object(f'({a.code}).integer_part', Type('BigInt'), call_position),
    Object(f'({b.code}).integer_part', Type('BigInt'), call_position)
).code};
{res}.fractional_part = {self._BigInt_add_BigInt(
    codegen, call_position,
    Object(f'({a.code}).fractional_part', Type('BigInt'), call_position),
    Object(f'({b.code}).fractional_part', Type('BigInt'), call_position)
).code};
{res}.exponent = ({a.code}).exponent > ({b.code}).exponent ? ({a.code}).exponent
    : ({b.code}).exponent;
while ({res}.fractional_part.length > 0 && {res}.fractional_part.digits[
    {res}.fractional_part.length - 1
] == 0) {{
    {res}.fractional_part.length--;
}}
""")
        
        return Object(res, Type('BigFloat'), call_position)
    
    @c_dec(param_types=('BigFloat', 'BigFloat'))
    def _BigFloat_sub_BigFloat(self, codegen, call_position: Position, a: Object,
                               b: Object) -> Object:
        res = codegen.create_temp_var(Type('BigFloat'), call_position)
        codegen.prepend_code(f"""BigFloat {res} = {{
    .integer_part = {self._BigInt_sub_BigInt(
        codegen, call_position,
        Object(f'({a.code}).integer_part', Type('BigInt'), call_position),
        Object(f'({b.code}).integer_part', Type('BigInt'), call_position)
    ).code},
    .fractional_part = {self._BigInt_sub_BigInt(
        codegen, call_position,
        Object(f'({a.code}).fractional_part', Type('BigInt'), call_position),
        Object(f'({b.code}).fractional_part', Type('BigInt'), call_position)
    ).code},
    .exponent = ({a.code}).exponent > ({b.code}).exponent ? ({a.code}).exponent : ({b.code}).exponent
}};

while ({res}.fractional_part.length > 0 && {res}.fractional_part.digits[
    {res}.fractional_part.length - 1
] == 0) {{
    {res}.fractional_part.length--;
}}
""")
        
        return Object(res, Type('BigFloat'), call_position)
    
    @c_dec(param_types=('BigFloat', 'float'))
    def _BigFloat_add_float(self, codegen, call_position: Position, bf: Object, f: Object) -> Object:
        float_str = codegen.call('float_to_string', [Arg(f)], call_position)
        float_as_bf = self._BigFloat_new(codegen, call_position, float_str)
        return self._BigFloat_add_BigFloat(codegen, call_position, bf, float_as_bf)
    
    @c_dec(param_types=('string',), is_method=True, is_static=True)
    def _BigFloat_new(self, codegen, call_position: Position, num: Object) -> Object:
        temp = codegen.create_temp_var(Type('BigFloat'), call_position)
        string = codegen.create_temp_var(Type('string'), call_position)
        int_part = codegen.create_temp_var(Type('string'), call_position)
        frac_part = codegen.create_temp_var(Type('string'), call_position)
        exp_part = codegen.create_temp_var(Type('string'), call_position)
        codegen.prepend_code(f"""BigFloat {temp};
char {string}[] = {num.code};
string {int_part} = strtok({string}, ".");
string {frac_part} = strtok(NULL, "e");
string {exp_part} = strtok(NULL, "");
""")
        codegen.prepend_code(f"""{temp}.integer_part = {self._BigInt_new(
    codegen, call_position,
    Object(int_part, Type('string'), call_position)
).code};
{temp}.fractional_part = {self._BigInt_new(
    codegen, call_position,
    Object(frac_part or '0', Type('string'), call_position)
).code};
{temp}.exponent = {exp_part} ? atoi({exp_part}) : 0;
""")

        return Object(temp, Type('BigFloat'), call_position)
    
    @c_dec()
    def _BigInt_type(self, _, call_position: Position) -> Object:
        return Object('"BigInt"', Type('string'), call_position)
    
    @c_dec(param_types=('BigInt',))
    def _BigInt_to_string(self, codegen, call_position: Position, bint: Object) -> Object:
        buf_free = Free()
        buf = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
        length = codegen.create_temp_var(Type('int'), call_position)
        i = codegen.create_temp_var(Type('int'), call_position)
        
        codegen.prepend_code(f"""string {buf} = NULL;
int {length} = 0;
for (int {i} = 0; {i} < ({bint.code}).length; {i}++) {{
{length} += snprintf(NULL, 0, "%d", ({bint.code}).digits[{i}]);
}}

{buf} = (string)malloc({length} + 1);
{codegen.c_manager.buf_check(buf)}
{buf}[0] = '\\0';
for (int {i} = ({bint.code}).length - 1; {i} >= 0; {i}--) {{
""")
        codegen.prepend_code(f"""strcat({buf}, {codegen.c_manager._int_to_string(
codegen, call_position,
Object(f'(({bint.code}).digits[{i}])', Type('int'), call_position)
).code});
}}

{buf}[{length}] = '\\0';
""")
        
        return Object(buf, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('BigInt', 'BigInt'))
    def _BigInt_add_BigInt(self, codegen, call_position: Position,
                            a: Object, b: Object) -> Object:
        res = codegen.create_temp_var(Type('BigInt'), call_position)
        carry = codegen.create_temp_var(Type('int'), call_position)
        i = codegen.create_temp_var(Type('int'), call_position)
        added = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""BigInt {res} = {{ .length = 0 }};
int {carry} = 0;
for (int {i} = 0; {i} < ({a.code}).length || {i} < ({b.code}).length || {carry}; {i}++) {{
    int {added} = {carry};
    if ({i} < ({a.code}).length) {added} += ({a.code}).digits[{i}];
    if ({i} < ({b.code}).length) {added} += ({b.code}).digits[{i}];
    {res}.digits[{res}.length++] = {added} % 10;
    {carry} = {added} / 10;
}}
""")
        
        return Object(res, Type('BigInt'), call_position)
    
    @c_dec(param_types=('BigInt', 'BigInt'))
    def _BigInt_sub_BigInt(self, codegen, call_position: Position,
                            a: Object, b: Object) -> Object:
        res = codegen.create_temp_var(Type('BigInt'), call_position)
        borrow = codegen.create_temp_var(Type('int'), call_position)
        i = codegen.create_temp_var(Type('int'), call_position)
        diff = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""BigInt {res} = {{ .length = 0 }};
int {borrow} = 0;
for (int {i} = 0; {i} < ({a.code}).length; {i}++) {{
    int {diff} = ({a.code}).digits[{i}] - ({i} < ({b.code}).length
        ? ({b.code}).digits[{i}] : 0) - {borrow};
    if ({diff} < 0) {{
        {diff} += 10;
        {borrow} = 1;
    }} else {{
        {borrow} = 0;
    }}

    {res}.digits[{res}.length++] = {diff};
}}

while ({res}.length > 1 && {res}.digits[{res}.length - 1] == 0) {{
{res}.length--;
}}
""")
        
        return Object(res, Type('BigInt'), call_position)
    
    @c_dec(param_types=('string',), is_method=True, is_static=True)
    def _BigInt_new(self, codegen, call_position: Position, num: Object) -> Object:
        temp = codegen.create_temp_var(Type('BigInt'), call_position)
        i = codegen.create_temp_var(Type('int'), call_position)
        num_len = codegen.c_manager._string_length(codegen, call_position, num)
        codegen.prepend_code(f"""if ({num_len.code} > {MAX_DIGITS}) {{
    {codegen.c_manager.err('Digit length too long for BigInt: %d', num_len.code)}
}}
BigInt {temp} = {{ .length = {num_len.code} }};
for (size_t {i} = 0; {i} < {temp}.length; {i}++) {{
    {temp}.digits[{i}] = ({num.code})[{temp}.length - {i} - 1] - '0';
}}
""")
        
        return Object(temp, Type('BigInt'), call_position)
