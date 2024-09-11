from codegen.objects import Object, Position, Free, Type, Arg, TempVar
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
    
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _BigFloat_type(_, call_position: Position) -> Object:
            return Object('"BigFloat"', Type('string'), call_position)
        
        @c_dec(param_types=('BigFloat',), is_method=True, add_to_class=self)
        def _BigFloat_to_string(codegen, call_position: Position, bf: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            int_part: TempVar = codegen.create_temp_var(Type('string'), call_position)
            frac_part: TempVar = codegen.create_temp_var(Type('string'), call_position)
            total_length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            
            codegen.prepend_code(f"""string {buf} = NULL;
string {int_part} = {_BigInt_to_string(
    codegen, call_position,
    Object(f'({bf}).integer_part', Type('BigInt'), call_position)
)};
string {frac_part} = {_BigInt_to_string(
    codegen, call_position,
    Object(f'({bf}).fractional_part', Type('BigInt'), call_position)
)};

int {total_length} = strlen({int_part}) + strlen({frac_part}) + 20;
{buf} = (string)malloc({total_length});
{codegen.c_manager.buf_check(buf)}

snprintf({buf}, {total_length}, "%s.%se%d", {int_part}, {frac_part}, ({bf}).exponent);
free({int_part});
free({frac_part});
""")
            
            return buf.OBJECT()
        
        @c_dec(param_types=('BigFloat', 'BigFloat'), add_to_class=self)
        def _BigFloat_add_BigFloat(codegen, call_position: Position, a: Object,
                                b: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('BigFloat'), call_position)
            codegen.prepend_code(f"""BigFloat {res};
{res}.integer_part = {_BigInt_add_BigInt(
    codegen, call_position,
    Object(f'({a}).integer_part', Type('BigInt'), call_position),
    Object(f'({b}).integer_part', Type('BigInt'), call_position)
)};
{res}.fractional_part = {_BigInt_add_BigInt(
    codegen, call_position,
    Object(f'({a}).fractional_part', Type('BigInt'), call_position),
    Object(f'({b}).fractional_part', Type('BigInt'), call_position)
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
        
        @c_dec(param_types=('BigFloat', 'BigFloat'), add_to_class=self)
        def _BigFloat_sub_BigFloat(codegen, call_position: Position, a: Object,
                                b: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('BigFloat'), call_position)
            codegen.prepend_code(f"""BigFloat {res} = {{
    .integer_part = {_BigInt_sub_BigInt(
        codegen, call_position,
        Object(f'({a}).integer_part', Type('BigInt'), call_position),
        Object(f'({b}).integer_part', Type('BigInt'), call_position)
    )},
    .fractional_part = {_BigInt_sub_BigInt(
        codegen, call_position,
        Object(f'({a}).fractional_part', Type('BigInt'), call_position),
        Object(f'({b}).fractional_part', Type('BigInt'), call_position)
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
        
        @c_dec(param_types=('BigFloat', 'float'), add_to_class=self)
        def _BigFloat_add_float(codegen, call_position: Position, bf: Object, f: Object) -> Object:
            float_str: Object = codegen.call('float_to_string', [Arg(f)], call_position)
            float_as_bf = _BigFloat_new(codegen, call_position, float_str)
            return _BigFloat_add_BigFloat(codegen, call_position, bf, float_as_bf)
        
        @c_dec(param_types=('string',), is_method=True, is_static=True, add_to_class=self)
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
            codegen.prepend_code(f"""{temp}.integer_part = {_BigInt_new(
    codegen, call_position, int_part.OBJECT()
)};
{temp}.fractional_part = {_BigInt_new(
    codegen, call_position,
    Object(str(frac_part) or '0', Type('string'), call_position)
)};
{temp}.exponent = {exp_part} ? atoi({exp_part}) : 0;
""")

            return temp.OBJECT()
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _BigInt_type(_, call_position: Position) -> Object:
            return Object('"BigInt"', Type('string'), call_position)
        
        @c_dec(param_types=('BigInt',), add_to_class=self)
        def _BigInt_to_string(codegen, call_position: Position, bint: Object) -> Object:
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            
            codegen.prepend_code(f"""string {buf} = NULL;
int {length} = 0;
for (int {i} = 0; {i} < ({bint}).length; {i}++) {{
{length} += snprintf(NULL, 0, "%d", ({bint}).digits[{i}]);
}}

{buf} = (string)malloc({length} + 1);
{codegen.c_manager.buf_check(buf)}
{buf}[0] = '\\0';
for (int {i} = ({bint}).length - 1; {i} >= 0; {i}--) {{
""")
            codegen.prepend_code(f"""strcat({buf}, {codegen.c_manager._int_to_string(
    codegen, call_position,
    Object(f'(({bint}).digits[{i}])', Type('int'), call_position)
)});
}}

{buf}[{length}] = '\\0';
""")
            
            return buf.OBJECT()
        
        @c_dec(param_types=('BigInt', 'BigInt'), add_to_class=self)
        def _BigInt_add_BigInt(codegen, call_position: Position,
                                a: Object, b: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('BigInt'), call_position)
            carry: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            added: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""BigInt {res} = {{ .length = 0 }};
int {carry} = 0;
for (int {i} = 0; {i} < ({a}).length || {i} < ({b}).length || {carry}; {i}++) {{
    int {added} = {carry};
    if ({i} < ({a}).length) {added} += ({a}).digits[{i}];
    if ({i} < ({b}).length) {added} += ({b}).digits[{i}];
    {res}.digits[{res}.length++] = {added} % 10;
    {carry} = {added} / 10;
}}
""")
            
            return res.OBJECT()
        
        @c_dec(param_types=('BigInt', 'BigInt'), add_to_class=self)
        def _BigInt_sub_BigInt(codegen, call_position: Position,
                                a: Object, b: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('BigInt'), call_position)
            borrow: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            diff: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""BigInt {res} = {{ .length = 0 }};
int {borrow} = 0;
for (int {i} = 0; {i} < ({a}).length; {i}++) {{
    int {diff} = ({a}).digits[{i}] - ({i} < ({b}).length
        ? ({b}).digits[{i}] : 0) - {borrow};
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
            
            return res.OBJECT()
        
        @c_dec(param_types=('string',), is_method=True, is_static=True, add_to_class=self)
        def _BigInt_new(codegen, call_position: Position, num: Object) -> Object:
            temp: TempVar = codegen.create_temp_var(Type('BigInt'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            num_len: Object = codegen.c_manager._string_length(codegen, call_position, num)
            codegen.prepend_code(f"""if ({str(num_len)} > {MAX_DIGITS}) {{
    {codegen.c_manager.err('Digit length too long for BigInt: %d', str(num_len))}
}}
BigInt {temp} = {{ .length = {str(num_len)} }};
for (size_t {i} = 0; {i} < {temp}.length; {i}++) {{
    {temp}.digits[{i}] = ({num})[{temp}.length - {i} - 1] - '0';
}}
""")
            
            return temp.OBJECT()
