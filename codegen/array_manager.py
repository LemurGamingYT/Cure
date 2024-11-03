from codegen.objects import Position, Object, Free, Type, Arg, TempVar, Param, Stringable
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import CManager, c_dec
from ir.nodes import TypeNode


DEFAULT_CAPACITY = 10

def element_index(
    iterable: Stringable, index: Stringable, iterable_type: Type,
    pos: Position
) -> Object:
    return Object(f'({iterable}).elements[{index}]', iterable_type, pos)

def get_index(codegen, call_position: Position, index: Stringable, max_length: Stringable):
    idx: TempVar = codegen.create_temp_var(Type('int'), call_position)
    return f"""int {idx} = {index};
if ({idx} < 0) {{
    {idx} = ({max_length}) + {idx};
    if (abs({idx}) > ({max_length})) {{
        {codegen.c_manager.err('Index out of range')}
    }}
}} else if ({idx} >= ({max_length})) {{
    {codegen.c_manager.err('Index out of range')}
}}
""", idx

class ArrayManager:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        
        setattr(codegen.type_checker, 'array_type', self.array_type)
        codegen.metadata.setdefault('array_types', [])
    
    def array_type(self, node: TypeNode) -> Type | None:
        if node.array_type is None:
            return None
        
        return self.codegen.array_manager.define_array(self.codegen.visit_TypeNode(node.array_type))
    
    def define_array(self, type: Type) -> Type:
        array_type = Type(f'array[{type}]', f'{type.c_type}_array')
        if type in self.codegen.metadata['array_types']:
            return array_type
        
        self.codegen.add_toplevel_code(f"""typedef struct {{
    {type.c_type}* elements;
    size_t length;
    size_t capacity;
}} {array_type.c_type};
""")
        
        c_manager: CManager = self.codegen.c_manager
        c_manager.reserve(array_type.c_type)
        
        c_manager.init_class(self, str(array_type), array_type)
        c_manager.wrap_struct_properties('arr', array_type, [
            Param('length', Type('int')), Param('capacity', Type('int'))
        ])
        
        @c_dec(
            param_types=(Param('arr', array_type),), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_to_string',
        )
        def array_string(codegen, call_position: Position, arr: Object) -> Object:
            i: TempVar = codegen.create_temp_var(Type('size_t'), call_position)
            builder: Object = codegen.c_manager._StringBuilder_new(codegen, call_position)
            a = f'({arr})'
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('"{"', Type('string'), call_position)
)};
for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            value: Object = codegen.c_manager._to_string(
                codegen, call_position, Object(f'{a}.elements[{i}]', type, call_position)
            )
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
codegen, call_position, builder, value
)};
if ({i} < {a}.length - 1) {{
""")
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
codegen, call_position, builder, Object('", "', Type('string'), call_position)
)};
}}
{value.free.code if value.free is not None else ''}
}}
""")
            if value.free is not None:
                codegen.scope.remove_free(value.free)
            
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('"}"', Type('string'), call_position)
)};
""")
            
            obj: Object = codegen.c_manager._StringBuilder_str(codegen, call_position, builder)
            # StringBuilder_str duplicates the builder's buffer and so now the builder is not needed
            if builder.free is not None:
                codegen.prepend_code(builder.free.code)
                codegen.scope.remove_free(builder.free)
            
            return obj
        
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
            is_method=True, is_static=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_type', 
        )
        def array_type_(_, call_position: Position) -> Object:
            return Object(f'"array[{type}]"', Type('string'), call_position)
        
        def array_insert(codegen, call_position: Position,
                         arr: Object, index: Object, element: Object) -> Object:
            a = f'({arr})'
            code, idx = get_index(codegen, call_position, index, f'{a}.length')
            codegen.prepend_code(f"""{code}
{a}.elements[{idx}] = {element};
""")
            
            return Object.NULL(call_position)
        
        def array_add_range(codegen, call_position: Position, arr: Object, elements: Object) -> Object:
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
            param_types=(Param('arr', array_type), Param('element', type)), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_add',
            overloads={
                OverloadKey(Type('nil'), (
                    Param('arr', array_type), Param('index', Type('int')),
                    Param('element', type)
                )): OverloadValue(array_insert),
                OverloadKey(
                    Type('nil'), (Param('arr', array_type), Param('arr2', array_type))
                ): OverloadValue(array_add_range)
            }
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
            param_types=(Param('arr', array_type), Param('index', Type('int')), Param('element', type)),
            is_method=True, add_to_class=c_manager, func_name_override=f'{array_type.c_type}_set',
        )
        def array_set(codegen, call_position: Position, arr: Object, index: Object,
                      element: Object) -> Object:
            a = f'({arr})'
            code, idx = get_index(codegen, call_position, index, f'{a}.length')
            codegen.prepend_code(f"""{code}
{a}.elements[{idx}] = {element};
""")
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('arr', array_type), Param('index', Type('int'))), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_get',
        )
        def array_get(codegen, call_position: Position, arr: Object, index: Object) -> Object:
            a = f'({arr})'
            code, idx = get_index(codegen, call_position, index, f'{a}.length')
            codegen.prepend_code(code)
            return element_index(arr, idx, type, call_position)
        
        @c_dec(
            param_types=(Param('arr', array_type), Param('element', type)), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_has',
        )
        def array_has(codegen, call_position: Position, arr: Object, element: Object) -> Object:
            return Object(
                f'(({array_find(codegen, call_position, arr, element)}) != -1)',
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(Param('arr', array_type), Param('element', type)), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_add_{type.c_type}',
        )
        def array_add_type(codegen, call_position: Position, arr: Object, element: Object) -> Object:
            return array_add(codegen, call_position, arr, element)
        
        @c_dec(
            param_types=(Param('arr', array_type),), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_reverse',
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
        
        # TODO: change all of the array.elements[index] == element to use the eq method for each of
        # the types, e.g. int_eq_int by using the codegen.c_manager, same with the lt and gt
        
        @c_dec(
            param_types=(Param('arr', array_type),), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_sort',
        )
        def array_sort(codegen, call_position: Position, arr: Object) -> Object:
            a = f'({arr})'
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            j: TempVar = codegen.create_temp_var(Type('int'), call_position)
            temp: TempVar = codegen.create_temp_var(type, call_position)
            codegen.prepend_code(f"""for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
    for (size_t {j} = 0; {j} < {a}.length - 1; {j}++) {{
""")
            codegen.prepend_code(f"""if ({codegen.call(
    f'{type.c_type}_gt_{type.c_type}', [
        Arg(element_index(arr, j, type, call_position)),
        Arg(element_index(arr, f'{j} + 1', type, call_position))
    ], call_position
)}) {{
            {type.c_type} {temp} = {a}.elements[{j}];
            {a}.elements[{j}] = {a}.elements[{j} + 1];
            {a}.elements[{j} + 1] = {temp};
        }}
    }}
}}
""")
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('arr', array_type), Param('element', type)), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_remove',
        )
        def array_remove(codegen, call_position: Position, arr: Object, element: Object) -> Object:
            a = f'({arr})'
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            j: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            codegen.prepend_code(f"""if ({codegen.call(
    f'{type.c_type}_eq_{type.c_type}', [
        Arg(element_index(arr, i, type, call_position)), Arg(element)
    ], call_position
)}) {{
        for (size_t {j} = {i}; {j} < {a}.length - 1; {j}++) {{
            {a}.elements[{j}] = {a}.elements[{j} + 1];
        }}
        {a}.length--;
    }}
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('arr', array_type), Param('index', Type('int'))), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_remove_at',
        )
        def array_remove_at(codegen, call_position: Position,
                            arr: Object, index: Object) -> Object:
            a = f'({arr})'
            code, idx = get_index(codegen, call_position, index, f'{a}.length')
            j: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""{code}
for (size_t {j} = {idx}; {j} < {a}.length - 1; {j}++) {{
    {a}.elements[{j}] = {a}.elements[{j} + 1];
    {a}.length--;
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('arr', array_type), Param('elem', type)), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_pop',
        )
        def array_pop(codegen, call_position: Position, arr: Object, elem: Object) -> Object:
            a = f'({arr})'
            temp: TempVar = codegen.create_temp_var(type, call_position)
            popped: TempVar = codegen.create_temp_var(type, call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            j: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""if ({a}.length == 0) {{
    {codegen.c_manager.err('Array is empty')}
}}
{type.c_type}* {temp} = NULL;
for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            codegen.prepend_code(f"""if ({codegen.call(
    f'{type.c_type}_eq_{type.c_type}',
    [Arg(element_index(arr, i, type, call_position), Arg(elem))],
    call_position
)}) {{
        *{temp} = {a}.elements[{i}];
        for (size_t {j} = {i}; {j} < {a}.length - 1; {j}++) {{
            {a}.elements[{j}] = {a}.elements[{j} + 1];
        }}
        {a}.length--;
        break;
    }}
}}

if (!{temp}) {{
    {codegen.c_manager.err('Element not found')}
}}
{popped} = *{temp};
""")
            
            return popped.OBJECT()
        
        @c_dec(
            param_types=(Param('arr', array_type), Param('index', Type('int'))), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_pop_at',
        )
        def array_pop_at(codegen, call_position: Position, arr: Object, index: Object) -> Object:
            a = f'({arr})'
            code, idx = get_index(codegen, call_position, index, f'{a}.length')
            popped: TempVar = codegen.create_temp_var(type, call_position)
            j: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""{code}
{type.c_type} {popped};
{popped} = {a}.elements[{idx}];
for (size_t {j} = {idx}; {j} < {a}.length - 1; {j}++) {{
    {a}.elements[{j}] = {a}.elements[{j} + 1];
}}

{a}.length--;
""")
            
            return popped.OBJECT()
        
        @c_dec(
            param_types=(Param('arr', array_type),), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_clear',
        )
        def array_clear(codegen, call_position: Position, arr: Object) -> Object:
            a = f'({arr})'
            codegen.prepend_code(f"""free({a}.elements);
{a}.length = 0;
{a}.capacity = {DEFAULT_CAPACITY};
{a}.elements = ({type.c_type}*)malloc(sizeof({type.c_type}) * {DEFAULT_CAPACITY});
{codegen.c_manager.buf_check(f'{a}.elements')}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('arr', array_type),), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_any',
        )
        def array_any(codegen, call_position: Position, arr: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            a = f'({arr})'
            codegen.prepend_code(f"""bool {res} = false;
for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            codegen.prepend_code(f"""if ({codegen.c_manager._to_bool(
    codegen, call_position, element_index(a, i, type, call_position)
)}) {{
    {res} = true;
    break;
}}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(
            param_types=(Param('arr', array_type),), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_all',
        )
        def array_all(codegen, call_position: Position, arr: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            a = f'({arr})'
            codegen.prepend_code(f"""bool {res} = true;
for (size_t {i} = 0; {i} < {a}.length; {i}++) {{
""")
            codegen.prepend_code(f"""if (!({codegen.c_manager._to_bool(
    codegen, call_position, element_index(a, i, type, call_position)
)})) {{
    {res} = false;
    break;
}}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(
            param_types=(Param('arr', array_type),), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_pick_random',
        )
        def array_pick_random(codegen, call_position: Position, arr: Object) -> Object:
            a = f'({arr})'
            return Object(f'({a}.elements[{codegen.c_manager._Math_random(
    codegen, call_position,
    Object('0', Type('int'), call_position), Object(f'{a}.length', Type('int'), call_position)
)}])', type, call_position)
        
        @c_dec(
            param_types=(Param('arr', array_type), Param('value', type)), is_method=True,
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_find',
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
    [Arg(element_index(arr, i, type, call_position)), Arg(value)], call_position
)}) {{
        {idx} = {i};
        break;
    }}
}}
""")
            return idx.OBJECT()
        
        @c_dec(
            param_types=(
                Param('arr', array_type), Param('start', Type('int')), Param('to', Type('int'))
            ), is_method=True, add_to_class=c_manager,
            func_name_override=f'{array_type.c_type}_slice'
        )
        def array_slice(codegen, call_position: Position, arr: Object, start: Object,
                        to: Object) -> Object:
            res: Object = array_make(codegen, call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""size_t {i} = 0;
{res}.elements = ({type.c_type}*)malloc(sizeof({type.c_type}) * (({to}) - ({start})));
{codegen.c_manager.buf_check(f'{res}.elements')}
for (size_t {i} = ({start}); {i} < ({to}); {i}++) {{
    {res}.elements[{i} - ({start})] = {res}.elements[{i}];
}}
{res}.length = ({to}) - ({start});
""")

            return Object(f'({res})', array_type, call_position)
        
        @c_dec(
            param_types=(Param('b', array_type), Param('a', array_type)),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_eq_{array_type.c_type}'
        )
        def array_eq_array(codegen, call_position: Position, a: Object, b: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (size_t {i} = 0; {i} < ({a}).length; {i}++) {{
""")
            codegen.prepend_code(f"""if ({codegen.call(
    f'{type.c_type}_neq_{type.c_type}', [
        Arg(element_index(a, i, type, call_position)),
        Arg(element_index(b, i, type, call_position))
    ], call_position
)}) {{
        {res} = false;
        break;
    }}
}}
""")

            return res.OBJECT()
        
        @c_dec(
            param_types=(Param('a', array_type), Param('b', array_type)),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_neq_{array_type.c_type}',
        )
        def array_neq_array(codegen, call_position: Position, a: Object, b: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (size_t {i} = 0; {i} < ({a}).length; {i}++) {{
""")
            codegen.prepend_code(f"""if ({codegen.call(
    f'{type.c_type}_eq_{type.c_type}', [
        Arg(element_index(a, i, type, call_position)),
        Arg(element_index(b, i, type, call_position))
    ], call_position
)}) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(
            param_types=(Param('b', array_type), Param('b', array_type)),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_lt_{array_type.c_type}'
        )
        def array_lt_array(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}).length < ({b}).length)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(Param('a', array_type), Param('b', array_type)),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_lte_{array_type.c_type}'
        )
        def array_lte_array(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}).length <= ({b}).length)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(Param('a', array_type), Param('b', array_type)),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_gt_{array_type.c_type}'
        )
        def array_gt_array(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}).length > ({b}).length)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(Param('a', array_type), Param('b', array_type)),
            add_to_class=c_manager, func_name_override=f'{array_type.c_type}_gte_{array_type.c_type}'
        )
        def array_gte_array(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}).length >= ({b}).length)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(Param('arr', array_type), Param('index', Type('int'))), return_type=type,
            add_to_class=c_manager, func_name_override=f'iter_{array_type.c_type}'
        )
        def iter_array(_, call_position: Position, arr: Object, index: Object) -> Object:
            return element_index(arr, index, type, call_position)
        
        @c_dec(
            param_types=(Param('arr', array_type), Param('index', Type('int'))),
            add_to_class=c_manager, func_name_override=f'index_{array_type.c_type}'
        )
        def index_array(codegen, call_position: Position, arr: Object, index: Object) -> Object:
            return array_get(codegen, call_position, arr, index)
        
        self.codegen.metadata['array_types'].append(type)
        return array_type
