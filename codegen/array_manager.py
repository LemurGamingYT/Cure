from codegen.objects import Position, Object, Free, Type, Arg, TempVar
from codegen.c_manager import CManager, c_dec

DEFAULT_CAPACITY = 10


class ArrayManager:
    def __init__(self, codegen) -> None:
        self.defined_types: list[str] = []
        
        self.codegen = codegen
    
    def define_array(self, type: Type) -> Type:
        array_type = Type(f'array[{type}]', f'{type.c_type}_array')
        if type.type in self.defined_types:
            return array_type
        
        self.codegen.add_toplevel_code(f"""typedef struct {{
    {type.c_type}* elements;
    size_t length;
    size_t capacity;
}} {array_type.c_type};
""")
        
        c_manager: CManager = self.codegen.c_manager
        
        @c_dec(
            param_types=(array_type.c_type,),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_to_string',
            is_method=True
        )
        def array_string(codegen, call_position: Position, arr: Object) -> Object:
            size: TempVar = codegen.create_temp_var(Type('int', 'size_t'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int', 'size_t'), call_position)
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            remaining: TempVar = codegen.create_temp_var(Type('int', 'size_t'), call_position)
            a = f'({arr})'
            get_element = Arg(Object(f'{a}.elements[{i}]', type, call_position))
            elem: TempVar = codegen.create_temp_var(Type('string'), call_position)
            
            codegen.prepend_code(f"""string {buf} = NULL;
size_t {size} = 3; // '{{', '}}' and '\\0'
for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            codegen.prepend_code(f"""
    {size} += strlen({codegen.call(f'{type.c_type}_to_string', [get_element], call_position)});
    if ({i} < {a}.length - 1) {size} += 2; // ',' and ' '
}}

{buf} = (string)malloc({size});
{codegen.c_manager.buf_check(buf)}
snprintf({buf}, {size}, "{{");
size_t {remaining} = {size} - 1;

for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            codegen.prepend_code(f"""
    string {elem} = {codegen.call(
    f'{type.c_type}_to_string', [get_element], call_position
)};
strncat({buf}, {elem}, {remaining});
    {remaining} -= strlen({elem});
    if ({i} < {a}.length - 1) {{
        strncat({buf}, ", ", {remaining});
        {remaining} -= 2;
    }}
}}
strncat({buf}, "}}", {remaining});
""")
            
            return buf.OBJECT()
        
        @c_dec(add_to_class=c_manager, func_name_override=f'{array_type.c_type}_make')
        def array_make(codegen, call_position: Position) -> Object:
            arr_free = Free()
            arr: TempVar = codegen.create_temp_var(array_type, call_position, free=arr_free)
            arr_free.object_name = f'{arr}.elements'
            codegen.prepend_code(f"""{array_type.c_type} {arr} = {{
    .length = 0, .capacity = {DEFAULT_CAPACITY},
    .elements = ({type.c_type}*)malloc(sizeof({type.c_type}) * {DEFAULT_CAPACITY}),
}};
{codegen.c_manager.buf_check(f'{arr}.elements')}
""")
            
            return arr.OBJECT()
        
        @c_dec(
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_type', 
            is_method=True, is_static=True
        )
        def array_type_(_, call_position: Position) -> Object:
            return Object(f'"array[{type}]"', Type('string'), call_position)
        
        def array_insert(codegen, call_position: Position,
                         arr: Object, index: Object, element: Object) -> Object:
            a = f'({arr})'
            i = f'({index})'
            codegen.prepend_code(f"""if ({i} < 0 || {i} >= {a}.length) {{
    {codegen.c_manager.err('Index out of bounds')}
}}

{a}.elements[{i}] = {element};
""")
            
            return Object.NULL(call_position)
        
        def array_add_range(codegen, call_position: Position,
                            arr: Object, elements: Object) -> Object:
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            elems = f'({elements})'
            codegen.prepend_code(f"""for (size_t {i} = 0; {i} < {elems}.length; {i}++) {{
""")
            codegen.prepend_code(f"""{array_add(
    codegen, call_position, arr,
    Object(f'{elems}.elements[{i}]', type, call_position)
)};
}}
""")
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(array_type.c_type, type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_add',
            is_method=True,
            overloads={
                ((array_type.c_type, 'int', type.c_type), 'nil'): array_insert,
                ((array_type.c_type, array_type.c_type), 'nil'): array_add_range
            },
        )
        def array_add(codegen, call_position: Position, arr: Object, element: Object) -> Object:
            a = f'({arr})'
            codegen.prepend_code(f"""if ({a}.length == {a}.capacity) {{
    {a}.capacity *= 2;
    {a}.elements = ({type.c_type}*)realloc({a}.elements, sizeof({type.c_type}) * {a}.capacity);
    {codegen.c_manager.buf_check(f'{a}.elements')}
}}

{a}.elements[{a}.length++] = {element};
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(array_type.c_type, 'int', type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_set',
            is_method=True,
        )
        def array_set(codegen, call_position: Position, arr: Object, index: Object,
                      element: Object) -> Object:
            a = f'({arr})'
            i = f'({index})'
            codegen.prepend_code(f"""if ({i} < 0 || {i} >= {a}.length) {{
    {codegen.c_manager.err('Index out of bounds')}
}}
{a}.elements[{i}] = {element};
""")
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(array_type.c_type, 'int'),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_get',
            is_method=True,
        )
        def array_get(codegen, call_position: Position, arr: Object, index: Object) -> Object:
            a = f'({arr})'
            i = f'({index})'
            idx: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {idx} = {i};
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
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_length',
            is_property=True,
        )
        def array_length(_, call_position: Position, arr: Object) -> Object:
            return Object(f'(({arr}).length)', Type('int'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type,),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_capacity',
            is_property=True,
        )
        def array_capacity(_, call_position: Position, arr: Object) -> Object:
            return Object(f'(({arr}).capacity)', Type('int'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type, type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_has',
            is_method=True,
        )
        def array_has(codegen, call_position: Position, arr: Object, element: Object) -> Object:
            return Object(
                f'(({array_find(codegen, call_position, arr, element)}) != -1)',
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(array_type.c_type, type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_add_{type.c_type}',
            is_method=True,
        )
        def array_add_type(codegen, call_position: Position, arr: Object, element: Object) -> Object:
            return array_add(codegen, call_position, arr, element)
        
        @c_dec(
            param_types=(array_type.c_type,),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_reverse',
            is_method=True,
        )
        def array_reverse(codegen, call_position: Position, arr: Object) -> Object:
            a = f'({arr})'
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            temp: TempVar = codegen.create_temp_var(type, call_position)
            codegen.prepend_code(f"""for (size_t {i} = 0; {i} < {a}.length / 2; {i}++) {{
    {type} {temp} = {a}.elements[{i}];
    {a}.elements[{i}] = {a}.elements[{a}.length - {i} - 1];
    {a}.elements[{a}.length - {i} - 1] = {temp};
}}
""")

            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(array_type.c_type,),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_sort',
            is_method=True,
        )
        def array_sort(codegen, call_position: Position, arr: Object) -> Object:
            a = f'({arr})'
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            j: TempVar = codegen.create_temp_var(Type('int'), call_position)
            temp: TempVar = codegen.create_temp_var(type, call_position)
            codegen.prepend_code(f"""for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
    for (size_t {j} = 0; {j} < {a}.length - 1; {j}++) {{
        if ({a}.elements[{j}] > {a}.elements[{j} + 1]) {{
            {type.c_type} {temp} = {a}.elements[{j}];
            {a}.elements[{j}] = {a}.elements[{j} + 1];
            {a}.elements[{j} + 1] = {temp};
        }}
    }}
}}
""")
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(array_type.c_type, type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_remove',
            is_method=True,
        )
        def array_remove(codegen, call_position: Position, arr: Object, element: Object) -> Object:
            a = f'({arr})'
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            j: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
    if ({a}.elements[{i}] == ({element})) {{
        for (size_t {j} = {i}; {j} < {a}.length - 1; {j}++) {{
            {a}.elements[{j}] = {a}.elements[{j} + 1];
        }}
        {a}.length--;
    }}
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(array_type.c_type, 'int'),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_remove_at',
            is_method=True,
        )
        def array_remove_at(codegen, call_position: Position,
                            arr: Object, index: Object) -> Object:
            a = f'({arr})'
            i = f'({index})'
            j: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""if ({i} >= {a}.length || {i} < 0) {{
    {c_manager.err('Index out of range')}
}}
for (size_t {j} = {i}; {j} < {a}.length - 1; {j}++) {{
    {a}.elements[{j}] = {a}.elements[{j} + 1];
    {a}.length--;
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(array_type.c_type, type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_pop',
            is_method=True,
        )
        def array_pop(codegen, call_position: Position, arr: Object, elem: Object) -> Object:
            a = f'({arr})'
            popped: TempVar = codegen.create_temp_var(type, call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            j: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""if ({a}.length == 0) {{
    {c_manager.err('Array is empty')}
}}
{type.c_type} {popped} = {{0}};
for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
    if ({a}.elements[{i}] == ({elem})) {{
        {popped} = {a}.elements[{i}];
        for (size_t {j} = {i}; {j} < {a}.length - 1; {j}++) {{
            {a}.elements[{j}] = {a}.elements[{j} + 1];
        }}
        {a}.length--;
        break;
    }}
}}

if (!{popped}) {{
    {c_manager.err('Element not found')}
}}
""")
            
            return popped.OBJECT()
        
        @c_dec(
            param_types=(array_type.c_type, 'int'),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_pop_at',
            is_method=True,
        )
        def array_pop_at(codegen, call_position: Position, arr: Object, index: Object) -> Object:
            a = f'({arr})'
            i = f'({index})'
            popped: TempVar = codegen.create_temp_var(type, call_position)
            j: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""if ({i} >= {a}.length || {i} < 0) {{
    {c_manager.err('Index out of range')}
}}
{type.c_type} {popped} = {{0}};
{popped} = {a}.elements[{i}];
for (size_t {j} = {i}; {j} < {a}.length - 1; {j}++) {{
    {a}.elements[{j}] = {a}.elements[{j} + 1];
    {a}.length--;
}}
""")
            
            return popped.OBJECT()
        
        @c_dec(
            param_types=(array_type.c_type,),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_clear',
            is_method=True,
        )
        def array_clear(codegen, call_position: Position, arr: Object) -> Object:
            a = f'({arr})'
            codegen.prepend_code(f"""free({a}.elements);
{a}.length = 0;
{a}.capacity = {DEFAULT_CAPACITY};
{a}.elements = ({type.c_type}*)malloc(sizeof({type.c_type}) * {DEFAULT_CAPACITY});
{c_manager.buf_check(f'{a}.elements')}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(array_type.c_type,),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_any',
            is_method=True,
        )
        def array_any(codegen, call_position: Position, arr: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            a = f'({arr})'
            codegen.prepend_code(f"""bool {res} = false;
for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            codegen.prepend_code(f"""if ({codegen.call(
    f'{type}_to_bool', [Arg(Object(f'{a}.elements[{i}]', type, call_position))],
    call_position
).code}) {{
    {res} = true;
    break;
}}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(
            param_types=(array_type.c_type,),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_all',
            is_method=True,
        )
        def array_all(codegen, call_position: Position, arr: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            a = f'({arr})'
            codegen.prepend_code(f"""bool {res} = true;
for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            codegen.prepend_code(f"""if (!({codegen.call(
    f'{type}_to_bool', [Arg(Object(f'{a}.elements[{i}]', type, call_position))],
    call_position
).code})) {{
    {res} = false;
    break;
}}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(
            param_types=(array_type.c_type,),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_pick_random',
            is_method=True
        )
        def array_pick_random(codegen, call_position: Position, arr: Object) -> Object:
            a = f'({arr})'
            return Object(f'({a}.elements[{codegen.call(
    'Math_random', [Arg(Object(f'{a}.length', Type('int'), call_position))], call_position
).code}])', type, call_position)
        
        @c_dec(
            param_types=(array_type.c_type, type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_find',
            is_method=True
        )
        def array_find(codegen, call_position: Position, arr: Object, value: Object) -> Object:
            a = f'({arr})'
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            idx: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {idx} = -1;
for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            codegen.prepend_code(f"""if ({codegen.call(
    f'{type.c_type}_eq_{type.c_type}',
    [Arg(Object(f'{a}.elements[{i}]', type, call_position)), Arg(value)], call_position
)}) {{
        {idx} = {i};
        break;
    }}
}}
""")
            return idx.OBJECT()
        
        @c_dec(
            param_types=(array_type.c_type, array_type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_eq_{array_type.c_type}'
        )
        def array_eq_array(codegen, call_position: Position, arr1: Object, arr2: Object) -> Object:
            a1 = f'({arr1})'
            a2 = f'({arr2})'
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (size_t {i} = 0; {i} < {a1}.length; {i}++) {{
    if ({a1}.elements[{i}] != {a2}.elements[{i}]) {{
        {res} = false;
        break;
    }}
}}
""")

            return res.OBJECT()
        
        @c_dec(
            param_types=(array_type.c_type, array_type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_neq_{array_type.c_type}',
        )
        def array_neq_array(codegen, call_position: Position, arr1: Object, arr2: Object) -> Object:
            a1 = f'({arr1})'
            a2 = f'({arr2})'
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (size_t {i} = 0; {i} < {a1}.length; {i}++) {{
    if ({a1}.elements[{i}] != {a2}.elements[{i}]) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(
            param_types=(array_type.c_type, array_type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_lt_{array_type.c_type}'
        )
        def array_lt_array(_, call_position: Position, arr1: Object, arr2: Object) -> Object:
            return Object(f'(({arr1}).length < ({arr2}).length)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type, array_type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_lte_{array_type.c_type}'
        )
        def array_lte_array(_, call_position: Position, arr1: Object, arr2: Object) -> Object:
            return Object(f'(({arr1}).length <= ({arr2}).length)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type, array_type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_gt_{array_type.c_type}'
        )
        def array_gt_array(_, call_position: Position, arr1: Object, arr2: Object) -> Object:
            return Object(f'(({arr1}).length > ({arr2}).length)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type, array_type.c_type),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_gte_{array_type.c_type}'
        )
        def array_gte_array(_, call_position: Position, arr1: Object, arr2: Object) -> Object:
            return Object(f'(({arr1}).length >= ({arr2}).length)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(array_type.c_type, 'int'),
            return_type=type,
            add_to_class=c_manager,
            func_name_override=f'iter_{array_type.c_type}'
        )
        def iter_array(codegen, call_position: Position, arr: Object, index: Object) -> Object:
            return array_get(codegen, call_position, arr, index)
        
        @c_dec(
            param_types=(array_type.c_type, 'int'),
            add_to_class=c_manager,
            func_name_override=f'index_{array_type.c_type}'
        )
        def index_array(codegen, call_position: Position, arr: Object, index: Object) -> Object:
            return array_get(codegen, call_position, arr, index)
        
        self.defined_types.append(type.type)
        
        return array_type
