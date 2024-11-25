from codegen.objects import Object, Type, Param, Position, TempVar, Free
from codegen.array_manager import get_index
from codegen.c_manager import c_dec


class strings:
    def __init__(self, _) -> None:
        @c_dec(
            params=(Param('size', Type('int')),), is_method=True, add_to_class=self,
            is_static=True
        )
        def _string_new(codegen, call_position: Position, size: Object) -> Object:
            string_free = Free()
            string: TempVar = codegen.create_temp_var(Type('string'), call_position, free=string_free,
                                                      default_expr=f'string_new({size})')
            return string.OBJECT()
        
        @c_dec(params=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_length(_, call_position: Position, s: Object) -> Object:
            return Object(f'((int)string_length({s}))', Type('int'), call_position)
        
        @c_dec(params=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_empty(codegen, call_position: Position, s: Object) -> Object:
            return Object(
                f'({_string_length(codegen, call_position, s)} == 0)',
                Type('bool'), call_position
            )
        
        @c_dec(params=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_char(codegen, call_position: Position, s: Object) -> Object:
            return Object(
                f'({_string_length(codegen, call_position, s)} == 1)',
                Type('bool'), call_position
            )
        
        @c_dec(params=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_digit(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<ctype.h>', codegen)
            
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!isdigit(string_get_char(({s}), {i}))) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(params=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_lower(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<ctype.h>', codegen)
            
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!islower(string_get_char(({s}), {i}))) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(params=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_upper(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<ctype.h>', codegen)

            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!isupper(string_get_char(({s}), {i}))) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(params=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_alpha(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<ctype.h>', codegen)

            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!isalpha(string_get_char(({s}), {i}))) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(params=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_alnum(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<ctype.h>', codegen)
            
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!isalnum(string_get_char(({s}), {i}))) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(params=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_reversed(codegen, call_position: Position, s: Object) -> Object:
            char: TempVar = codegen.create_temp_var(Type('char'), call_position)
            first: TempVar = codegen.create_temp_var(Type('int'), call_position)
            last: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free)
            codegen.prepend_code(f"""string {res} = string_copy({s});
{codegen.c_manager.buf_check(f'string_ptr({res})')}
char {char};
int {first} = 0;
int {last} = {_string_length(codegen, call_position, s)} - 1;
while ({first} < {last}) {{
    {char} = string_get_char({s}, {first});
    string_set_char(&{res}, {first}, string_get_char({s}, {last}));
    string_set_char(&{res}, {last}, {char});
    {first}++;
    {last}--;
}}
""")
            
            return res.OBJECT()
        
        @c_dec(params=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_lower(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<ctype.h>', codegen)
            
            strlen = _string_length(codegen, call_position, s)
            
            temp_free = Free()
            temp_var: TempVar = codegen.create_temp_var(Type('string'), call_position, free=temp_free)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""string {temp_var} = string_empty({strlen});
{codegen.c_manager.buf_check(f'string_ptr({temp_var})')}
for (size_t {i} = 0; {i} < {strlen}; {i}++)
    string_set_char(&{temp_var}, {i}, tolower(string_get_char({s}, {i})));
""")
            
            return Object.STRINGBUF(temp_free, call_position)
        
        @c_dec(params=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_upper(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<ctype.h>', codegen)

            strlen = _string_length(codegen, call_position, s)

            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""string {res} = string_empty({strlen});
{codegen.c_manager.buf_check(f'string_ptr({res})')}
for (size_t {i} = 0; {i} < {strlen}; {i}++)
    string_set_char(&{res}, {i}, toupper(string_get_char({s}, {i})));
""")

            return Object.STRINGBUF(res_free, call_position)
        
        @c_dec(params=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_title(codegen, call_position: Position, s: Object) -> Object:
            codegen.c_manager.include('<ctype.h>', codegen)
            
            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free)
            capitalize: TempVar = codegen.create_temp_var(Type('bool'), call_position,
                                                          default_expr='true')
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""string {res} = string_copy({s});
{codegen.c_manager.buf_check(f'string_ptr({res})')}

for (size_t {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if ({capitalize} && isalpha(string_get_char({s}, {i}))) {{
        {capitalize} = false;
        string_set_char(&{res}, {i}, toupper(string_get_char({s}, {i})));
    }} else if (isspace(string_get_char({s}, {i}))) {{
        {capitalize} = true;
    }} else {{
        string_set_char(&{res}, {i}, tolower(string_get_char({s}, {i})));
    }}
}}
""")
            
            return Object.STRINGBUF(res_free, call_position)
        
        @c_dec(
            params=(Param('s', Type('string')), Param('prefix', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _string_startswith(codegen, call_position: Position, s: Object, prefix: Object) -> Object:
            return Object(
                f'(string_eq_partial({s}, {prefix}, {_string_length(codegen, call_position, prefix)}))',
                Type('bool'), call_position
            )
        
        @c_dec(
            params=(Param('s', Type('string')), Param('suffix', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _string_endswith(codegen, call_position: Position, s: Object, suffix: Object) -> Object:
            slen: TempVar = codegen.create_temp_var(
                Type('int'), call_position,
                default_expr=f'{_string_length(codegen, call_position, s)}'
            )
            
            sulen: TempVar = codegen.create_temp_var(
                Type('int'), call_position,
                default_expr=f'{_string_length(codegen, call_position, suffix)}'
            )
            
            return Object(
                f"""({slen} < {sulen} ? false : (string_eq_partial(
                    ({s}) + {slen} - {sulen}, {suffix}, {sulen})))""",
                Type('bool'), call_position
            )
        
        @c_dec(
            params=(Param('s', Type('string')), Param('index', Type('int'))),
            is_method=True, add_to_class=self
        )
        def _string_at(codegen, call_position: Position, s: Object, index: Object) -> Object:
            strlen = _string_length(codegen, call_position, s)
            code, idx = get_index(codegen, call_position, index, strlen)
            codegen.prepend_code(code)
            return Object(
                f'(string_get({s}, {idx}))',
                Type('string'), call_position
            )
        
        @c_dec(
            params=(Param('s', Type('string')), Param('substr', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _string_has(_, call_position: Position, s: Object, substr: Object) -> Object:
            return Object(
                f'(string_contains({s}, {substr}))',
                Type('bool'), call_position
            )
        
        @c_dec(
            params=(Param('s', Type('string')), Param('arr', Type('array[string]', 'string_array'))),
            is_method=True, add_to_class=self
        )
        def _string_join(codegen, call_position: Position, s: Object, arr: Object) -> Object:
            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free,
                                                   default_expr='NULL')
            i: TempVar = codegen.create_temp_var(Type('size_t'), call_position)
            total_len: TempVar = codegen.create_temp_var(Type('size_t'), call_position)
            delim_len: TempVar = codegen.create_temp_var(Type('size_t'), call_position)
            pos: TempVar = codegen.create_temp_var(Type('size_t'), call_position)
            temp_len: TempVar = codegen.create_temp_var(Type('size_t'), call_position)
            ith_element = Object(f'({arr}).elements[{i}]', Type('string'), call_position)
            codegen.prepend_code(f"""if (({arr}).length == 0) {{
    {res} = string_copy(string_make("")); // string_copy() used to make it able to be freed
}} else if (({arr}).length == 1) {{
    {res} = string_copy(({arr}).elements[0]);
}} else {{
    size_t {total_len} = 0;
    size_t {delim_len} = {_string_length(codegen, call_position, s)};
    for (int {i} = 0; {i} < ({arr}).length; {i}++) {{
        {total_len} += {_string_length(codegen, call_position, ith_element)};
        if ({i} < ({arr}).length - 1) {total_len} += {delim_len};
    }}
    
    string {res} = string_empty({total_len});
    size_t {pos} = 0;
    for (size_t {i} = 0; {i} < ({arr}).length; {i}++) {{
        size_t {temp_len} = {_string_length(codegen, call_position, ith_element)};
        memcpy(string_ptr({res}) + {pos}, string_ptr({ith_element}), {temp_len});
        {pos} += {temp_len};
        if ({i} < ({arr}).length - 1) {{
            memcpy(string_ptr({res}) + {pos}, string_ptr({s}), {delim_len});
            {pos} += {delim_len};
        }}
    }}
}}
""")
            
            return Object.STRINGBUF(res_free, call_position)
        
        @c_dec(params=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_parse_int(codegen, call_position: Position, s: Object) -> Object:
            return codegen.c_manager._string_to_int(codegen, call_position, s)
        
        @c_dec(params=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_parse_float(codegen, call_position: Position, s: Object) -> Object:
            return codegen.c_manager._string_to_float(codegen, call_position, s)
        
        @c_dec(params=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_parse_bool(codegen, call_position: Position, string: Object) -> Object:
            return codegen.c_manager._string_to_bool(codegen, call_position, string)
        
        @c_dec(
            params=(Param('s', Type('string')), Param('substr', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _string_find(codegen, call_position: Position, s: Object, substring: Object) -> Object:
            idx: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('size_t'), call_position)
            codegen.prepend_code(f"""int {idx} = -1;
for (size_t {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (string_eq_partial(
        {s} + {i}, {substring}, {_string_length(codegen, call_position, substring)}
    )) {{
        {idx} = {i};
        break;
    }}
}}
""")
            
            return idx.OBJECT()
        
        @c_dec(
            params=(
                Param('s', Type('string')), Param('start', Type('int')), Param('end', Type('int'))
            ), is_method=True, add_to_class=self
        )
        def _string_slice(codegen, call_position: Position, s: Object, start: Object,
                          end: Object) -> Object:
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free,
                                                   default_expr='string_null')
            start_var: TempVar = codegen.create_temp_var(Type('int'), call_position,
                                                         default_expr=str(start))
            end_var: TempVar = codegen.create_temp_var(Type('int'), call_position,
                                                       default_expr=str(end))
            codegen.prepend_code(f"""if ({start_var} < 0 || {end_var} < 0) {{
    {codegen.c_manager.err('Index out of bounds on string slice')}
}} else if ({start_var} > {end_var}) {{
    {codegen.c_manager.err('Start index must be less than end index')}
}}

{buf} = string_empty({end_var} - {start_var} + 1);
{codegen.c_manager.buf_check(f'string_ptr({buf})')}
memcpy(string_ptr({buf}), string_ptr({s}) + {start_var}, {end_var} - {start_var} + 1);
""")
            
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(
            params=(Param('s', Type('string')), Param('*', Type('*'))),
            is_method=True, add_to_class=self
        )
        def _string_format(codegen, call_position: Position, s: Object, *args: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, f'string_ptr({s})',
                *[str(arg) for arg in args]
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(params=(
            Param('s', Type('string')), Param('index', Type('int')),
            Param('char', Type('string'))
        ), is_method=True, add_to_class=self)
        def _string_set(codegen, call_position: Position, s: Object, index: Object,
                        char: Object) -> Object:
            strlen = _string_length(codegen, call_position, s)
            is_char = _string_is_char(codegen, call_position, char)
            code, idx = get_index(codegen, call_position, index, strlen)
            string_var: TempVar = codegen.create_temp_var(Type('string'), call_position,
                                                          default_expr=str(s))
            codegen.prepend_code(f"""if (!{is_char}) {{
    {codegen.c_manager.err('%s is not a character', str(char))}
}}
{code}
string_set(&{string_var}, {idx}, {char});
""")
            
            return Object.NULL(call_position)
        
        # @c_dec(
        #     params=(Param('s', Type('string')), Param('old', Type('string')),
        #             Param('new', Type('string'))),
        #     is_method=True, add_to_class=self
        # )
        # def _string_replace(_, call_position: Position, s: Object, old: Object,
        #                     new: Object) -> Object:
        #     return Object(
        #         f'(string_replace({s}, {old}, {new}))',
        #         Type('string'), call_position, free=Free()
        #     )
        
        @c_dec(
            params=(Param('s', Type('string')), Param('i', Type('int'))),
            return_type=Type('string'), add_to_class=self
        )
        def _iter_string(codegen, call_position: Position, string: Object, i: Object) -> Object:
            return _string_at(codegen, call_position, string, i)
        
        @c_dec(params=(Param('s', Type('string')), Param('i', Type('int'))), add_to_class=self)
        def _index_string(codegen, call_position: Position, string: Object, i: Object) -> Object:
            return _string_at(codegen, call_position, string, i)
