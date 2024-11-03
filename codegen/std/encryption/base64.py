from codegen.objects import Object, Position, Free, Type, Arg, TempVar, Param
from codegen.c_manager import c_dec


class base64:
    def __init__(self, codegen) -> None:
        codegen.c_manager.reserve(('encoding_table', 'decoding_table', 'mod_table'))
        codegen.add_toplevel_code("""static char encoding_table[] = {
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
    'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', '0', '1', '2', '3',
    '4', '5', '6', '7', '8', '9', '+', '/'
};
static char* decoding_table = NULL;
static int mod_table[] = {0, 2, 1};
""")
    
        @c_dec(param_types=(Param('data', Type('string')),), can_user_call=True, add_to_class=self)
        def _base64_encode(codegen, call_position: Position, data: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            codegen.c_manager.include('<stdint.h>', codegen)
            
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            input_length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            output_length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            j: TempVar = codegen.create_temp_var(Type('int'), call_position)
            octet_a: TempVar = codegen.create_temp_var(Type('int'), call_position)
            octet_b: TempVar = codegen.create_temp_var(Type('int'), call_position)
            octet_c: TempVar = codegen.create_temp_var(Type('int'), call_position)
            triple: TempVar = codegen.create_temp_var(Type('int'), call_position)
            d = f'({data})'
            data_len: Object = codegen.call('string_length', [Arg(data)], call_position)
            codegen.prepend_code(f"""size_t {input_length} = {data_len};
size_t {output_length} = 4 * (({input_length} + 2) / 3);
string {buf} = (string)malloc({output_length});
{codegen.c_manager.buf_check(buf)}

for (int {i} = 0, {j} = 0; {i} < {input_length};) {{
    uint32_t {octet_a} = {i} < {input_length} ? (unsigned char){d}[{i}++] : 0;
    uint32_t {octet_b} = {i} < {input_length} ? (unsigned char){d}[{i}++] : 0;
    uint32_t {octet_c} = {i} < {input_length} ? (unsigned char){d}[{i}++] : 0;

    uint32_t {triple} = ({octet_a} << 0x10) + ({octet_b} << 0x08) + {octet_c};

    {buf}[{j}++] = encoding_table[({triple} >> 3 * 6) & 0x3F];
    {buf}[{j}++] = encoding_table[({triple} >> 2 * 6) & 0x3F];
    {buf}[{j}++] = encoding_table[({triple} >> 1 * 6) & 0x3F];
    {buf}[{j}++] = encoding_table[({triple} >> 0 * 6) & 0x3F];
}}

for (int {i} = 0; {i} < mod_table[{input_length} % 3]; {i}++)
    {buf}[{output_length} - 1 - {i}] = '=';

{buf}[{output_length}] = '\\0';
""")
            
            return buf.OBJECT()
        
        @c_dec(param_types=(Param('encoded', Type('string')),), can_user_call=True, add_to_class=self)
        def _base64_decode(codegen, call_position: Position, enc: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            codegen.c_manager.include('<stdint.h>', codegen)
            
            e = f'({enc})'
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            input_length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            output_length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            j: TempVar = codegen.create_temp_var(Type('int'), call_position)
            sextet_a: TempVar = codegen.create_temp_var(Type('int'), call_position)
            sextet_b: TempVar = codegen.create_temp_var(Type('int'), call_position)
            sextet_c: TempVar = codegen.create_temp_var(Type('int'), call_position)
            sextet_d: TempVar = codegen.create_temp_var(Type('int'), call_position)
            triple: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""unsigned char* {buf} = NULL;
if (decoding_table == NULL) {{
    decoding_table = malloc(256);
    {codegen.c_manager.buf_check('decoding_table')}

    for (int {i} = 0; {i} < 64; {i}++)
        decoding_table[(unsigned char)encoding_table[{i}]] = {i};
}}

size_t {input_length} = {codegen.call('string_length', [Arg(enc)], call_position).code};
if ({input_length} % 4 != 0) {{
    {codegen.c_manager.err('Invalid base64 string')}
}}

size_t {output_length} = {input_length} / 4 * 3;
if ({e}[{input_length} - 1] == '=') ({output_length})--;
if ({e}[{input_length} - 2] == '=') ({output_length})--;

{buf} = (unsigned char*)malloc({output_length} + 1);
{codegen.c_manager.buf_check(buf)}

for (int {i} = 0, {j} = 0; {i} < {input_length};) {{
    uint32_t {sextet_a} = {e}[{i}] == '=' ? 0 & {i}++ : decoding_table[(unsigned char){e}[{i}++]];
    uint32_t {sextet_b} = {e}[{i}] == '=' ? 0 & {i}++ : decoding_table[(unsigned char){e}[{i}++]];
    uint32_t {sextet_c} = {e}[{i}] == '=' ? 0 & {i}++ : decoding_table[(unsigned char){e}[{i}++]];
    uint32_t {sextet_d} = {e}[{i}] == '=' ? 0 & {i}++ : decoding_table[(unsigned char){e}[{i}++]];

    uint32_t {triple} = ({sextet_a} << 3 * 6)
    + ({sextet_b} << 2 * 6)
    + ({sextet_c} << 1 * 6)
    + ({sextet_d} << 0 * 6);

    if ({j} < {output_length}) {buf}[{j}++] = ({triple} >> 2 * 8) & 0xFF;
    if ({j} < {output_length}) {buf}[{j}++] = ({triple} >> 1 * 8) & 0xFF;
    if ({j} < {output_length}) {buf}[{j}++] = ({triple} >> 0 * 8) & 0xFF;
}}

{buf}[{output_length}] = '\\0';
free(decoding_table);
decoding_table = NULL;
""")
            
            return buf.OBJECT()
