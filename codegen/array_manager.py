from codegen.objects import Position, Object, Free, Type
from codegen.c_manager import CManager, c_dec

DEFAULT_CAPACITY = 10


class ArrayManager:
    def __init__(self, compiler) -> None:
        self.defined_types: list[str] = []
        
        self.compiler = compiler
    
    def define_array(self, type: Type) -> Type:
        array_type = Type(f'array[{type}]', f'{type}_array')
        if type.type in self.defined_types:
            return array_type
        
        self.compiler.add_toplevel_code(f"""typedef struct {{
    {type.c_type}* elements;
    size_t length;
    size_t capacity;
}} {array_type.c_type};
""")
        
        c_manager: CManager = self.compiler.c_manager
        
        @c_dec(
            param_types=(array_type.c_type,),
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_to_string'
        )
        def array_string(compiler, call_position: Position, arr: Object) -> Object:
            size = compiler.create_temp_var(Type('int', 'size_t'), call_position)
            i = compiler.create_temp_var(Type('int', 'size_t'), call_position)
            buf_free = Free()
            buf = compiler.create_temp_var(Type('string'), call_position, free=buf_free)
            remaining = compiler.create_temp_var(Type('int', 'size_t'), call_position)
            a = f'({arr.code})'
            get_element = Object(f'{a}.elements[{i}]', type, call_position)
            elem = compiler.create_temp_var(Type('string'), call_position)
            
            compiler.prepend_code(f"""size_t {size} = 3; // '{{', '}}' and \\0
for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            compiler.prepend_code(f"""
    {size} += strlen({compiler.call(f'{type}_to_string', [get_element], call_position).code});
    if ({i} < {a}.length - 1) {size} += 2; // ',' and ' '
}}

string {buf} = (string)malloc({size});
{compiler.c_manager.buf_check(buf)}
snprintf({buf}, {size}, "{{");
size_t {remaining} = {size} - 1;

for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            compiler.prepend_code(f"""
    string {elem} = {compiler.call(
    f'{type}_to_string', [get_element], call_position
).code};
strncat({buf}, {elem}, {remaining});
    {remaining} -= strlen({elem});
    if ({i} < {a}.length - 1) {{
        strncat({buf}, ", ", {remaining});
        {remaining} -= 2;
    }}
}}
strncat({buf}, "}}", {remaining});
""")
            
            return Object(buf, Type('string'), call_position, free=buf_free)
        
        @c_dec(add_to_class=c_manager, func_name_override=f'{array_type.c_type}_make')
        def array_make(compiler, call_position: Position) -> Object:
            arr_free = Free()
            arr = compiler.create_temp_var(array_type, call_position, free=arr_free)
            arr_free.object_name = f'{arr}.elements'
            compiler.prepend_code(f"""{array_type.c_type} {arr};
{arr}.length = 0;
{arr}.capacity = {DEFAULT_CAPACITY};
{arr}.elements = ({type.c_type}*)malloc(sizeof({type.c_type}) * {DEFAULT_CAPACITY});
{compiler.c_manager.buf_check(f'{arr}.elements')}
""")
            
            return Object(arr, array_type, call_position, free=arr_free)
        
        @c_dec(add_to_class=c_manager, func_name_override=f'{array_type.c_type}_type')
        def array_type_(_, call_position: Position) -> Object:
            return Object(f'"array[{type}]"', Type('string'), call_position)
        
        def array_insert(compiler, call_position: Position,
                         arr: Object, index: Object, element: Object) -> Object:
            a = f'({arr.code})'
            i = f'({index.code})'
            compiler.prepend_code(f"""if ({i} < 0 || {i} >= {a}.length) {{
    {compiler.c_manager.err('Index out of bounds')}
}}

{a}.elements[{i}] = {element.code};
""")
            
            return Object('NULL', Type('nil'), call_position)
        
        def array_add_range(compiler, call_position: Position,
                            arr: Object, elements: Object) -> Object:
            i = compiler.create_temp_var(Type('int'), call_position)
            elems = f'({elements.code})'
            compiler.prepend_code(f"""for (size_t {i} = 0; {i} < {elems}.length; {i}++) {{
""")
            compiler.prepend_code(f"""{array_add(
    compiler, call_position, arr,
    Object(f'{elems}.elements[{i}]', type, call_position)
).code};
}}
""")
            return Object('NULL', Type('nil'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type, type.c_type),
            is_method=True,
            overloads={
                ((array_type.c_type, 'int', type.c_type), 'nil'): array_insert,
                ((array_type.c_type, array_type.c_type), 'nil'): array_add_range
            },
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_add'
        )
        def array_add(compiler, call_position: Position, arr: Object, element: Object) -> Object:
            a = f'({arr.code})'
            compiler.prepend_code(f"""if ({a}.length == {a}.capacity) {{
    {a}.capacity *= 2;
    {a}.elements = ({type.c_type}*)realloc({a}.elements, sizeof({type.c_type}) * {a}.capacity);
    {compiler.c_manager.buf_check(f'{a}.elements')}
}}

{a}.elements[{a}.length++] = {element.code};
""")
            
            return Object('NULL', Type('nil'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type, 'int'),
            is_method=True,
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_get'
        )
        def array_get(compiler, call_position: Position, arr: Object, index: Object) -> Object:
            a = f'({arr.code})'
            i = f'({index.code})'
            idx = compiler.create_temp_var(Type('int'), call_position)
            compiler.prepend_code(f"""int {idx} = {i};
if ({idx} < 0) {{
    {idx} = {a}.length + {idx};
    if (abs({idx}) > {a}.length) {{
        {c_manager.err('Index out of range')}
    }}
}} else if ({idx} >= {a}.length) {{
    {c_manager.err('Index out of range')}
}}
""")
            
            return Object(f'{a}.elements[{idx}]', type, call_position)
        
        @c_dec(
            param_types=(array_type.c_type,),
            is_property=True,
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_length'
        )
        def array_length(_, call_position: Position, arr: Object) -> Object:
            return Object(f'(({arr.code}).length)', Type('int'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type,),
            is_property=True,
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_capacity'
        )
        def array_capacity(_, call_position: Position, arr: Object) -> Object:
            return Object(f'(({arr.code}).capacity)', Type('int'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type, type.c_type),
            is_method=True,
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_has'
        )
        def array_has(compiler, call_position: Position, arr: Object, element: Object) -> Object:
            has_var = compiler.create_temp_var(Type('bool'), call_position)
            i = compiler.create_temp_var(Type('int'), call_position)
            compiler.prepend_code(f"""bool {has_var} = false;
for (size_t {i} = 0; {i} < ({arr.code}).length; {i}++) {{
    if ((({arr.code}).elements[{i}]) == ({element.code})) {has_var} = true;
}}
""")
            
            return Object(has_var, Type('bool'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type, type.c_type),
            is_method=True,
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_add_{type.c_type}'
        )
        def array_add_type(compiler, call_position: Position, arr: Object, element: Object) -> Object:
            return array_add(compiler, call_position, arr, element)
        
        @c_dec(
            param_types=(array_type.c_type,),
            is_method=True,
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_reverse'
        )
        def array_reverse(compiler, call_position: Position, arr: Object) -> Object:
            a = f'({arr.code})'
            i = compiler.create_temp_var(Type('int'), call_position)
            temp = compiler.create_temp_var(type, call_position)
            compiler.prepend_code(f"""for (size_t {i} = 0; {i} < {a}.length / 2; {i}++) {{
    {type} {temp} = {a}.elements[{i}];
    {a}.elements[{i}] = {a}.elements[{a}.length - {i} - 1];
    {a}.elements[{a}.length - {i} - 1] = {temp};
}}
""")

            return Object('NULL', Type('nil'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type,),
            is_method=True,
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_sort'
        )
        def array_sort(compiler, call_position: Position, arr: Object) -> Object:
            a = f'({arr.code})'
            i = compiler.create_temp_var(Type('int'), call_position)
            j = compiler.create_temp_var(Type('int'), call_position)
            temp = compiler.create_temp_var(type, call_position)
            compiler.prepend_code(f"""for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
    for (size_t {j} = 0; {j} < {a}.length - 1; {j}++) {{
        if ({a}.elements[{j}] > {a}.elements[{j} + 1]) {{
            {type} {temp} = {a}.elements[{j}];
            {a}.elements[{j}] = {a}.elements[{j} + 1];
            {a}.elements[{j} + 1] = {temp};
        }}
    }}
}}
""")
            return Object('NULL', Type('nil'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type, type.c_type),
            is_method=True,
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_remove'
        )
        def array_remove(compiler, call_position: Position, arr: Object, element: Object) -> Object:
            a = f'({arr.code})'
            i = compiler.create_temp_var(Type('int'), call_position)
            j = compiler.create_temp_var(Type('int'), call_position)
            compiler.prepend_code(f"""for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
    if ({a}.elements[{i}] == ({element.code})) {{
        for (size_t {j} = {i}; {j} < {a}.length - 1; {j}++) {{
            {a}.elements[{j}] = {a}.elements[{j} + 1];
        }}
        {a}.length--;
    }}
}}
""")
            
            return Object('NULL', Type('nil'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type, 'int'),
            is_method=True,
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_remove_at'
        )
        def array_remove_at(compiler, call_position: Position,
                            arr: Object, index: Object) -> Object:
            a = f'({arr.code})'
            i = f'({index.code})'
            j = compiler.create_temp_var(Type('int'), call_position)
            compiler.prepend_code(f"""if ({i} >= {a}.length || {i} < 0) {{
    {c_manager.err('Index out of range')}
}}
for (size_t {j} = {i}; {j} < {a}.length - 1; {j}++) {{
    {a}.elements[{j}] = {a}.elements[{j} + 1];
    {a}.length--;
}}
""")
            
            return Object('NULL', Type('nil'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type,),
            is_method=True,
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_clear'
        )
        def array_clear(compiler, call_position: Position, arr: Object) -> Object:
            a = f'({arr.code})'
            compiler.prepend_code(f"""free({a}.elements);
{a}.length = 0;
{a}.capacity = {DEFAULT_CAPACITY};
{a}.elements = ({type.c_type}*)malloc(sizeof({type.c_type}) * {DEFAULT_CAPACITY});
{compiler.c_manager.buf_check(f'{a}.elements')}
""")
            return Object('NULL', Type('nil'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type,),
            is_method=True,
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_any'
        )
        def array_any(compiler, call_position: Position, arr: Object) -> Object:
            res = compiler.create_temp_var(Type('bool'), call_position)
            i = compiler.create_temp_var(Type('int'), call_position)
            a = f'({arr.code})'
            compiler.prepend_code(f"""bool {res} = false;
for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            compiler.prepend_code(f"""if ({compiler.call(
    f'{type}_to_bool', [Object(f'{a}.elements[{i}]', Type('bool'), call_position)],
    call_position
).code}) {{
    {res} = true;
    break;
}}
}}
""")
            
            return Object(res, Type('bool'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type,),
            is_method=True,
            add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_all'
        )
        def array_all(compiler, call_position: Position, arr: Object) -> Object:
            res = compiler.create_temp_var(Type('bool'), call_position)
            i = compiler.create_temp_var(Type('int'), call_position)
            a = f'({arr.code})'
            compiler.prepend_code(f"""bool {res} = true;
for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            compiler.prepend_code(f"""if (!({compiler.call(
    f'{type}_to_bool', [Object(f'{a}.elements[{i}]', Type('bool'))],
    call_position
)})) {{
    {res} = false;
    break;
}}
}}
""")
            
            return Object(res, Type('bool'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type, 'int'),
            return_type=type,
            add_to_class=c_manager,
            func_name_override=f'iter_{array_type.c_type}'
        )
        def iter_array(compiler, call_position: Position, arr: Object, index: Object) -> Object:
            return array_get(compiler, call_position, arr, index)
        
        @c_dec(
            param_types=(array_type.c_type, 'int'),
            add_to_class=c_manager,
            func_name_override=f'index_{array_type.c_type}'
        )
        def index_array(compiler, call_position: Position, arr: Object, index: Object) -> Object:
            return array_get(compiler, call_position, arr, index)
        
        self.defined_types.append(type.type)
        
        return array_type
