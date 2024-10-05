from codegen.objects import Object, Position, Free, Type, TempVar, Param
from codegen.std.big.constants import MAX_DIGITS
from codegen.c_manager import c_dec


class BigInt:
    def __init__(self) -> None:
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _BigInt_type(_, call_position: Position) -> Object:
            return Object('"BigInt"', Type('string'), call_position)
        
        @c_dec(param_types=(Param('bi', Type('BigInt')),), add_to_class=self)
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
        
        @c_dec(
            param_types=(Param('bi', Type('BigInt')), Param('bi', Type('BigInt'))),
            add_to_class=self
        )
        def _BigInt_add_BigInt(codegen, call_position: Position, a: Object, b: Object) -> Object:
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
        
        @c_dec(
            param_types=(Param('bi', Type('BigInt')), Param('bi', Type('BigInt'))),
            add_to_class=self
        )
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
        
        @c_dec(
            param_types=(Param('num', Type('string')),),
            is_method=True, is_static=True, add_to_class=self
        )
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
