from string import ascii_letters

from cure.objects import Object, Position, Free, Type
from cure.c_manager import c_dec


class base64:
    def __init__(self, compiler) -> None:
        compiler.c_manager.RESERVED_NAMES.extend((
            'base64_table', 'mod_table', 'base64_reverse_table'
        ))
        compiler.add_toplevel_code(f"""static const char base64_table[] = "{ascii_letters}+/";
static int mod_table[] = {{0, 2, 1}};
static const unsigned char base64_reverse_table[] = {{
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 62, 64, 64, 64, 63,
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 64, 64, 64, 0, 64, 64, 64, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 64, 64, 64, 64, 64, 64, 26, 27,
    28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64
}};
""")
    
    # FIXME: encode does not work for many strings
    @c_dec(
        param_types=('string',),
        can_user_call=True
    )
    def _base64_encode(self, compiler, call_position: Position, data: Object) -> Object:
        compiler.c_manager.include('<string.h>', compiler)
        compiler.c_manager.include('<stdint.h>', compiler)
        
        buf_free = Free()
        buf = compiler.create_temp_var(Type('string'), call_position, free=buf_free)
        ilen = compiler.create_temp_var(Type('int'), call_position)
        olen = compiler.create_temp_var(Type('int'), call_position)
        i = compiler.create_temp_var(Type('int'), call_position)
        j = compiler.create_temp_var(Type('int'), call_position)
        octet_a = compiler.create_temp_var(Type('int'), call_position)
        octet_b = compiler.create_temp_var(Type('int'), call_position)
        octet_c = compiler.create_temp_var(Type('int'), call_position)
        triple = compiler.create_temp_var(Type('int'), call_position)
        d = f'({data.code})'
        data_len = compiler.call('string_length', [data], call_position)
        compiler.prepend_code(f"""size_t {ilen} = {data_len.code};
size_t {olen} = 4 * (({ilen} + 2) / 3);
string {buf} = (string)malloc({olen} + 1);
{compiler.c_manager.buf_check(buf)}

for (size_t {i} = 0, {j} = 0; {i} < {ilen};) {{
    uint32_t {octet_a} = {i} < {ilen} ? (unsigned char){d}[{i}++] : 0;
    uint32_t {octet_b} = {i} < {ilen} ? (unsigned char){d}[{i}++] : 0;
    uint32_t {octet_c} = {i} < {ilen} ? (unsigned char){d}[{i}++] : 0;

    uint32_t {triple} = ({octet_a} << 16) + ({octet_b} << 8) + {octet_c};

    {buf}[{j}++] = base64_table[({triple} >> 18) & 0x3F];
    {buf}[{j}++] = base64_table[({triple} >> 12) & 0x3F];
    {buf}[{j}++] = base64_table[({triple} >> 6) & 0x3F];
    {buf}[{j}++] = base64_table[{triple} & 0x3F];
}}

for (size_t {i} = 0; {i} < (3 - ({ilen} % 3)) % 3; ++{i}) {{
    {buf}[{olen} - 1 - {i}] = '=';
}}

{buf}[{olen}] = '\\0';
""")
        
        return Object(buf, Type('string'), call_position, free=buf_free)
    
    @c_dec(
        param_types=('string',),
        can_user_call=True
    )
    def _base64_decode(self, compiler, call_position: Position, enc: Object) -> Object:
        compiler.c_manager.include('<string.h>', compiler)
        compiler.c_manager.include('<stdint.h>', compiler)
        
        e = f'({enc.code})'
        buf_free = Free()
        buf = compiler.create_temp_var(Type('string'), call_position, free=buf_free)
        ilen = compiler.create_temp_var(Type('int'), call_position)
        olen = compiler.create_temp_var(Type('int'), call_position)
        i = compiler.create_temp_var(Type('int'), call_position)
        j = compiler.create_temp_var(Type('int'), call_position)
        sextet_a = compiler.create_temp_var(Type('int'), call_position)
        sextet_b = compiler.create_temp_var(Type('int'), call_position)
        sextet_c = compiler.create_temp_var(Type('int'), call_position)
        sextet_d = compiler.create_temp_var(Type('int'), call_position)
        triple = compiler.create_temp_var(Type('int'), call_position)
        
        enc_len = compiler.call('string_length', [enc], call_position)
        compiler.prepend_code(f"""string {buf} = NULL;
size_t {ilen} = {enc_len.code};
if ({ilen} % 4 != 0) {{
    {compiler.c_manager.err('Invalid base64 string length')}
}}

size_t {olen} = {ilen} / 4 * 3;
if ({e}[{ilen} - 1] == '=') {olen}--;
if ({e}[{ilen} - 2] == '=') {olen}--;

{buf} = (string)malloc({olen} + 1);
{compiler.c_manager.buf_check(buf)}

for (size_t {i} = 0, {j} = 0; {i} < {ilen};) {{
    uint32_t {sextet_a} = {e}[{i}] == '=' ? 0 : base64_reverse_table[(unsigned char){e}[{i}++]];
    uint32_t {sextet_b} = {e}[{i}] == '=' ? 0 : base64_reverse_table[(unsigned char){e}[{i}++]];
    uint32_t {sextet_c} = {e}[{i}] == '=' ? 0 : base64_reverse_table[(unsigned char){e}[{i}++]];
    uint32_t {sextet_d} = {e}[{i}] == '=' ? 0 : base64_reverse_table[(unsigned char){e}[{i}++]];

    uint32_t {triple} = ({sextet_a} << 18) + ({sextet_b} << 12) + ({sextet_c} << 6) + {sextet_d};

    if ({j} < {olen}) {buf}[{j}++] = ({triple} >> 16) & 0xFF;
    if ({j} < {olen}) {buf}[{j}++] = ({triple} >> 8) & 0xFF;
    if ({j} < {olen}) {buf}[{j}++] = {triple} & 0xFF;
}}

{buf}[{olen}] = '\\0';
""")
        
        return Object(buf, Type('string'), call_position, free=buf_free)
