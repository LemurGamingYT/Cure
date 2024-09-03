from codegen.objects import Object, Position, Free, Type
from codegen.c_manager import c_dec


class RLE:
    @c_dec(param_types=('string',), can_user_call=True)
    def _rle_compress(self, codegen, call_position: Position, string: Object) -> Object:
        codegen.c_manager.include('<string.h>', codegen)
        
        input_len = codegen.create_temp_var(Type('int'), call_position)
        encoded_free = Free()
        encoded = codegen.create_temp_var(Type('string'), call_position, free=encoded_free)
        count = codegen.create_temp_var(Type('int'), call_position)
        j = codegen.create_temp_var(Type('int'), call_position)
        i = codegen.create_temp_var(Type('int'), call_position)
        s = f'({string})'
        
        codegen.prepend_code(f"""string {encoded};
if ({s} == NULL || *{s} == '\\0') {{
    {encoded} = strdup("");
}} else {{
    size_t {input_len} = strlen({s});
    {encoded} = (string)malloc({input_len} * 2 + 1);
    {codegen.c_manager.buf_check(encoded)}
    
    size_t {count} = 1;
    size_t {j} = 0;
    for (size_t {i} = 1; {i} <= {input_len}; {i}++) {{
        if ({i} < {input_len} && {s}[{i}] == {s}[{i}-1]) {{
            {count}++;
        }} else {{
            {j} += sprintf({encoded} + {j}, "%d%c", {count}, {s}[{i}-1]);
            {count} = 1;
        }}
    }}
    
    {encoded}[{j}] = '\\0';
    {encoded} = (string)realloc({encoded}, {j} + 1);
}}
""")
        
        return Object(encoded, Type('string'), call_position, free=encoded_free)

    @c_dec(param_types=('string',), can_user_call=True)
    def _rle_decompress(self, codegen, call_position: Position, string: Object) -> Object:
        codegen.c_manager.include('<string.h>', codegen)
        
        input_len = codegen.create_temp_var(Type('int'), call_position)
        decoded_free = Free()
        decoded = codegen.create_temp_var(Type('string'), call_position, free=decoded_free)
        j = codegen.create_temp_var(Type('int'), call_position)
        i = codegen.create_temp_var(Type('int'), call_position)
        k = codegen.create_temp_var(Type('int'), call_position)
        count = codegen.create_temp_var(Type('int'), call_position)
        s = f'({string.code})'
        
        codegen.prepend_code(f"""string {decoded};
if ({s} == NULL || *{s} == '\\0') {{
    {decoded} = strdup("");
}} else {{
    size_t {input_len} = strlen({s});
    {decoded} = (string)malloc({input_len} * {input_len} + 1);
    {codegen.c_manager.buf_check(decoded)}
    
    size_t {j} = 0;
    for (size_t {i} = 0; {i} < {input_len}; {i}++) {{
        size_t {count} = 0;
        while ({s}[{i}] >= '0' && {s}[{i}] <= '9') {{
            {count} = {count} * 10 + ({s}[{i}] - '0');
            {i}++;
        }}
        
        for (size_t {k} = 0; {k} < {count}; {k}++) {{
            {decoded}[{j}++] = {s}[{i}];
        }}
    }}
    
    {decoded}[{j}] = '\\0';
    {decoded} = (string)realloc({decoded}, {j} + 1);
}}
""")
        
        return Object(decoded, Type('string'), call_position, free=decoded_free)
