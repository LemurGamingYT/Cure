from codegen.objects import Object, Type, Param, Position, TempVar, Free
from codegen.c_manager import c_dec


class strings:
    def __init__(self, _) -> None:
        @c_dec(
            param_types=(Param('size', Type('int')),), is_method=True, add_to_class=self,
            is_static=True
        )
        def _string_new(codegen, call_position: Position, size: Object) -> Object:
            string_free = Free()
            string: TempVar = codegen.create_temp_var(Type('string'), call_position, free=string_free)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""string {string} = (string)malloc({size} * sizeof(char) + 1);
for (size_t {i} = 0; {i} < {size}; {i}++)
    {string}[{i}] = ' ';
{string}[{size}] = '\\0';
""")
            return string.OBJECT()
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_length(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            return Object(f'((int)strlen({s}))', Type('int'), call_position)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_empty(codegen, call_position: Position, s: Object) -> Object:
            return Object(
                f'({_string_length(codegen, call_position, s)} == 0)',
                Type('bool'), call_position
            )
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_char(codegen, call_position: Position, s: Object) -> Object:
            return Object(
                f'({_string_length(codegen, call_position, s)} == 1)',
                Type('bool'), call_position
            )
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_digit(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            codegen.c_manager.include('<ctype.h>', codegen)
            
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!isdigit(({s})[{i}])) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_lower(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            codegen.c_manager.include('<ctype.h>', codegen)
            
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!islower(({s})[{i}])) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_upper(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            codegen.c_manager.include('<ctype.h>', codegen)

            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!isupper(({s})[{i}])) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_alpha(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            codegen.c_manager.include('<ctype.h>', codegen)

            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!isalpha(({s})[{i}])) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_alnum(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            codegen.c_manager.include('<ctype.h>', codegen)
            
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!isalnum(({s})[{i}])) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_reversed(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            
            char: TempVar = codegen.create_temp_var(Type('char'), call_position)
            first: TempVar = codegen.create_temp_var(Type('int'), call_position)
            last: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free)
            codegen.prepend_code(f"""string {res} = strdup({s});
{codegen.c_manager.buf_check(res)}
char {char};
int {first} = 0;
int {last} = {_string_length(codegen, call_position, s)} - 1;
while ({first} < {last}) {{
    {char} = {s}[{first}];
    {res}[{first}] = {s}[{last}];
    {res}[{last}] = {char};
    {first}++;
    {last}--;
}}
""")
            
            return res.OBJECT()
        
        @c_dec(param_types=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_lower(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            codegen.c_manager.include('<ctype.h>', codegen)
            
            strlen = _string_length(codegen, call_position, s)
            
            temp_free = Free()
            temp_var: TempVar = codegen.create_temp_var(Type('string'), call_position, free=temp_free)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""string {temp_var} = (string)malloc({strlen} + 1);
{codegen.c_manager.buf_check(temp_var)}
for (size_t {i} = 0; {i} < {strlen}; {i}++)
    {temp_var}[{i}] = tolower({s}[{i}]);
{temp_var}[{strlen}] = '\\0';
""")
            
            return Object.STRINGBUF(temp_free, call_position)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_upper(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            codegen.c_manager.include('<ctype.h>', codegen)

            strlen = _string_length(codegen, call_position, s)

            temp_free = Free()
            temp_var: TempVar = codegen.create_temp_var(Type('string'), call_position, free=temp_free)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""string {temp_var} = (string)malloc({strlen} + 1);
{codegen.c_manager.buf_check(temp_var)}
for (size_t {i} = 0; {i} < {strlen}; {i}++)
    {temp_var}[{i}] = toupper({s}[{i}]);
{temp_var}[{strlen}] = '\\0';
""")

            return Object.STRINGBUF(temp_free, call_position)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_title(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            codegen.c_manager.include('<ctype.h>', codegen)
            
            temp_free = Free()
            temp_var: TempVar = codegen.create_temp_var(Type('string'), call_position, free=temp_free)
            lv: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""string {temp_var} = strdup({s});
{codegen.c_manager.buf_check(temp_var)}
for (string {lv} = {temp_var}; *{lv} != '\\0'; ++{lv})
    *{lv} = ({lv} == {temp_var} || *({lv} - 1) == ' ') ? toupper(*{lv}) : tolower(*{lv});
""")
            
            return Object.STRINGBUF(temp_free, call_position)
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('prefix', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _string_startswith(codegen, call_position: Position, s: Object, prefix: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)

            return Object(
                f'(strncmp({s}, {prefix}, {_string_length(codegen, call_position, prefix)}) == 0)',
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('suffix', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _string_endswith(codegen, call_position: Position, s: Object, suffix: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            
            su = str(suffix)
            slen: TempVar = codegen.create_temp_var(Type('int'), call_position)
            suffix_len: TempVar = _string_length(codegen, call_position, suffix)
            sulen: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""size_t {slen} = {_string_length(codegen, call_position, s)};
size_t {sulen} = {suffix_len};
""")
            return Object(
                f"""({slen} < {sulen} ? false : (strncmp(
                    ({s}) + {slen} - {sulen}, {su}, {sulen}) == 0)
                )""",
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('index', Type('int'))),
            is_method=True, add_to_class=self
        )
        def _string_at(codegen, call_position: Position, s: Object, index: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            
            strlen = _string_length(codegen, call_position, s)
            temp_var: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""if (({index}) > {strlen} - 1) {{
    {codegen.c_manager.err('Index out of bounds on string')}
}}
static char {temp_var}[2];
{temp_var}[0] = ({s})[{index}];
{temp_var}[1] = '\\0';
""")
            
            return temp_var.OBJECT()
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('substr', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _string_has(codegen, call_position: Position, s: Object, substr: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            return Object(
                f'(strstr({s}, {substr}) != NULL)',
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('arr', Type('array[string]', 'string_array'))),
            is_method=True, add_to_class=self
        )
        def _string_join(codegen, call_position: Position, s: Object, arr: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            
            tlen: TempVar = codegen.create_temp_var(Type('int'), call_position)
            sep_len: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free)
            count: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            a = f'({arr})'
            codegen.prepend_code(f"""size_t {tlen} = 0;
size_t {sep_len} = {_string_length(codegen, call_position, s)};
int {count} = 0;
for (int {i} = 0; {i} < {a}.length; {i}++) {{
    {tlen} += {_string_length(
    codegen, call_position, Object(f'{a}.elements[{i}]', Type('string'), call_position)
)};
    if ({i} > 0) {{
        {tlen} += {sep_len};
    }}
    {count}++;
}}

string {res} = (string)malloc({tlen} + 1);
{codegen.c_manager.buf_check(res)}
{res}[0] = '\\0';
for (int {i} = 0; {i} < {a}.length; {i}++) {{
    if ({i} > 0) {{
        strcat({res}, {s});
    }}
    strcat({res}, {a}.elements[{i}]);
}}
""")
            
            return Object.STRINGBUF(res_free, call_position)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_parse_int(codegen, call_position: Position, s: Object) -> Object:
            return codegen.c_manager._string_to_int(codegen, call_position, s)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_parse_float(codegen, call_position: Position, s: Object) -> Object:
            return codegen.c_manager._string_to_float(codegen, call_position, s)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_parse_bool(codegen, call_position: Position, string: Object) -> Object:
            return codegen.c_manager._string_to_bool(codegen, call_position, string)
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('substr', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _string_find(codegen, call_position: Position, s: Object, substring: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            idx: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {idx} = -1;
for (size_t {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (strncmp(
        {s} + {i},
        {substring},
        {_string_length(codegen, call_position, substring)}
    ) == 0) {{
        {idx} = {i};
        break;
    }}
}}
""")
            
            return idx.OBJECT()
        
        @c_dec(
            param_types=(
                Param('s', Type('string')), Param('start', Type('int')), Param('end', Type('int'))
            ), is_method=True, add_to_class=self
        )
        def _string_slice(codegen, call_position: Position, s: Object, start: Object,
                          end: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            start_var: TempVar = codegen.create_temp_var(Type('int'), call_position)
            end_var: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""string {buf} = NULL;
int {start_var} = {start};
int {end_var} = {end};
if ({start_var} < 0 || {end_var} < 0) {{
    {codegen.c_manager.err('Index out of bounds on string slice')}
}} else if ({start_var} > {end_var}) {{
    {codegen.c_manager.err('Start index must be less than end index')}
}}

{buf} = (string)malloc({end_var} - {start_var} + 1);
{codegen.c_manager.buf_check(str(buf))}
strncpy({buf}, ({s}) + {start_var}, {end_var} - {start_var} + 1);
{buf}[{end_var} - {start_var} + 1] = '\\0';
""")
            
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('*', Type('*'))),
            is_method=True, add_to_class=self
        )
        def _string_format(codegen, call_position: Position, s: Object, *args: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, str(s),
                *[str(arg) for arg in args]
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('i', Type('int'))),
            return_type=Type('string'), add_to_class=self
        )
        def _iter_string(codegen, call_position: Position, string: Object, i: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            return _string_at(codegen, call_position, string, i)
        
        @c_dec(param_types=(Param('s', Type('string')), Param('i', Type('int'))), add_to_class=self)
        def _index_string(codegen, call_position: Position, string: Object, i: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            return _string_at(codegen, call_position, string, i)
