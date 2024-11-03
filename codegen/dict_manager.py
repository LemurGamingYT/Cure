from codegen.objects import Object, Position, Free, Type, TempVar, Param, Arg
from codegen.array_manager import DEFAULT_CAPACITY
from codegen.c_manager import CManager, c_dec
from ir.nodes import TypeNode


class DictManager:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        
        setattr(codegen.type_checker, 'dict_type', self.dict_type)
        codegen.metadata.setdefault('dict_types', {})
    
    def dict_type(self, node: TypeNode) -> Type | None:
        if node.dict_types is None:
            return None
        
        return self.codegen.dict_manager.define_dict(
            self.codegen.visit_TypeNode(node.dict_types[0]),
            self.codegen.visit_TypeNode(node.dict_types[1])
        )
    
    def has_type(self, key_type: Type, value_type: Type) -> bool:
        for k, v in self.codegen.metadata['dict_types'].items():
            if k == key_type and v == value_type:
                return True
        
        return False
    
    def define_dict(self, key_type: Type, value_type: Type) -> Type:
        dict_type = Type(
            f'dict[{key_type}: {value_type}]',
            f'{key_type.c_type}_{value_type.c_type}_dict'
        )
        
        if self.has_type(key_type, value_type):
            return dict_type
        
        pair_type = Type(
            f'dict_pair[{key_type}, {value_type}]',
            f'{key_type.c_type}_{value_type.c_type}_pair'
        )
        
        self.codegen.add_toplevel_code(f"""typedef struct {{
    {key_type.c_type} key;
    {value_type.c_type} value;
}} {pair_type.c_type};

typedef struct {{
    {pair_type.c_type}* elements;
    size_t length;
    size_t capacity;
}} {dict_type.c_type};
""")
        
        c_manager: CManager = self.codegen.c_manager
        
        c_manager.init_class(c_manager, str(pair_type), pair_type)
        c_manager.init_class(c_manager, str(dict_type), dict_type)
        c_manager.wrap_struct_properties('pair', pair_type, [
            Param('key', key_type), Param('value', value_type)
        ])
        
        c_manager.wrap_struct_properties('dict', dict_type, [
            Param('length', Type('int')), Param('capacity', Type('int'))
        ])
        
        @c_dec(func_name_override=f'{pair_type.c_type}_type', add_to_class=c_manager, is_property=True)
        def pair_type_(_, call_position: Position) -> Object:
            return Object(f'"{pair_type}"', Type('string'), call_position)
        
        @c_dec(
            param_types=(Param('pair', pair_type),), is_method=True,
            func_name_override=f'{pair_type.c_type}_to_string', add_to_class=c_manager
        )
        def pair_to_string(codegen, call_position: Position, pair_obj: Object) -> Object:
            code, buf_free = codegen.fmt_length(
                codegen, call_position,
                'dict_pair[key=%s, value=%s]',
                str(codegen.call(
                    f'{key_type}_to_string',
                    [Arg(Object(f'(({pair_obj}).key)', key_type, call_position))],
                    call_position
                )),
                str(codegen.call(
                    f'{value_type}_to_string',
                    [Arg(Object(f'(({pair_obj}).value)', value_type, call_position))],
                    call_position
                ))
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(
            param_types=(Param('a', pair_type), Param('b', pair_type)),
            func_name_override=f'{pair_type.c_type}_eq_{pair_type.c_type}', add_to_class=c_manager
        )
        def pair_eq(codegen, call_position: Position, a: Object, b: Object) -> Object:
            keys_are_equal = codegen.call(
                f'{key_type.c_type}_eq_{key_type.c_type}', [
                    Arg(Object(f'({a}).key', key_type, call_position)),
                    Arg(Object(f'({b}).key', key_type, call_position))
                ], call_position
            )
            
            values_are_equal = codegen.call(
                f'{value_type.c_type}_eq_{value_type.c_type}', [
                    Arg(Object(f'({a}).value', value_type, call_position)),
                    Arg(Object(f'({b}).value', value_type, call_position))
                ], call_position
            )
            
            return Object(f'({keys_are_equal}) && ({values_are_equal})', Type('bool'), call_position)
        
        @c_dec(
            param_types=(Param('a', pair_type), Param('b', pair_type)),
            func_name_override=f'{pair_type.c_type}_neq_{pair_type.c_type}', add_to_class=c_manager
        )
        def pair_neq(codegen, call_position: Position, a: Object, b: Object) -> Object:
            keys_are_equal = codegen.call(
                f'{key_type.c_type}_neq_{key_type.c_type}', [
                    Arg(Object(f'({a}).key', key_type, call_position)),
                    Arg(Object(f'({b}).key', key_type, call_position))
                ], call_position
            )
            
            values_are_equal = codegen.call(
                f'{value_type.c_type}_neq_{value_type.c_type}', [
                    Arg(Object(f'({a}).value', value_type, call_position)),
                    Arg(Object(f'({b}).value', value_type, call_position))
                ], call_position
            )
            
            return Object(f'({keys_are_equal}) && ({values_are_equal})', Type('bool'), call_position)
        
        @c_dec(func_name_override=f'{dict_type.c_type}_make', add_to_class=c_manager)
        def dict_make(codegen, call_position: Position) -> Object:
            dict_free = Free()
            d: TempVar = codegen.create_temp_var(dict_type, call_position, free=dict_free)
            dict_free.object_name = f'{d}.elements'
            
            codegen.prepend_code(f"""{dict_type.c_type} {d} = {{
    .length = 0, .capacity = {DEFAULT_CAPACITY},
    .elements = ({pair_type.c_type}*)malloc({DEFAULT_CAPACITY} * sizeof({pair_type.c_type}))
}};
{codegen.c_manager.buf_check(f'{d}.elements')}
""")
            
            return d.OBJECT()
        
        @c_dec(
            param_types=(Param('dict', dict_type), Param('key', key_type)),
            func_name_override=f'{dict_type.c_type}_get', add_to_class=c_manager, is_method=True,
        )
        def dict_get(codegen, call_position: Position, dict_obj: Object, key: Object) -> Object:
            value: TempVar = codegen.create_temp_var(value_type, call_position)
            d = f'({dict_obj})'
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            found: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""{value_type.c_type} {value};
bool {found} = false;
for (size_t {i} = 0; {i} < {d}.length; {i}++) {{
""")
            codegen.prepend_code(f"""if ({codegen.call(
    f'{key_type.c_type}_eq_{key_type.c_type}',
    [Arg(Object(f'{d}.elements[{i}].key', key_type, call_position)), Arg(key)],
    call_position
)}) {{
        {value} = {d}.elements[{i}].value;
        {found} = true;
        break;
    }}
}}

if (!{found}) {{
    {codegen.c_manager.err('Key not found')}
}}
""")
            
            return value.OBJECT()
        
        @c_dec(
            param_types=(Param('dict', dict_type), Param('key', key_type)),
            func_name_override=f'{dict_type.c_type}_has', add_to_class=c_manager, is_method=True,
        )
        def dict_has(codegen, call_position: Position, dict_obj: Object, key: Object) -> Object:
            d = f'({dict_obj})'
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            has: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {has} = false;
for (size_t {i} = 0; {i} < {d}.length; {i}++) {{
""")
            codegen.prepend_code(f"""if ({codegen.call(
    f'{key_type.c_type}_eq_{key_type.c_type}',
    [Arg(Object(f'{d}.elements[{i}].key', key_type, call_position)), Arg(key)],
    call_position
)}) {{
        {has} = true;
        break;
    }}
}}
""")
            return has.OBJECT()
        
        @c_dec(
            param_types=(Param('dict', dict_type), Param('key', key_type), Param('value', value_type)),
            func_name_override=f'{dict_type.c_type}_set', add_to_class=c_manager, is_method=True,
        )
        def dict_set(codegen, call_position: Position, dict_obj: Object, key: Object,
                     value: Object) -> Object:
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            d = f'({dict_obj})'
            codegen.prepend_code(f"""if ({dict_has(codegen, call_position, dict_obj, key)}) {{
    for (size_t {i} = 0; {i} < {d}.length; {i}++) {{
""")
            codegen.prepend_code(f"""if ({codegen.call(
    f'{key_type.c_type}_eq_{key_type.c_type}',
    [Arg(Object(f'{d}.elements[{i}].key', key_type, call_position)), Arg(key)],
    call_position
)}) {{
            {d}.elements[{i}].value = {value};
            break;
        }}
    }}
}} else {{
    if ({d}.length == {d}.capacity) {{
        {d}.capacity *= 2;
        {d}.elements = ({pair_type.c_type}*)realloc(
            {d}.elements,
            {d}.capacity * sizeof({pair_type.c_type})
        );
        
        {codegen.c_manager.buf_check(f'{d}.elements')}
    }}
    {d}.elements[{d}.length].key = {key};
    {d}.elements[{d}.length].value = {value};
    {d}.length++;
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('dict', dict_type),),
            func_name_override=f'{dict_type.c_type}_to_string', add_to_class=c_manager, is_method=True
        )
        def dict_to_string(codegen, call_position: Position, dict_obj: Object) -> Object:
            builder: Object = codegen.c_manager._StringBuilder_new(codegen, call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            d = f'({dict_obj})'
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('"{"', Type('string'), call_position)
)};
for (size_t {i} = 0; {i} < {d}.length; {i}++) {{
""")
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, codegen.c_manager._to_string(
        codegen, call_position, Object(f'{d}.elements[{i}].key', key_type, call_position)
    )
)};
{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('": "', Type('string'), call_position)
)};
{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, codegen.c_manager._to_string(
        codegen, call_position, Object(f'{d}.elements[{i}].value', value_type, call_position)
    )
)};

if ({i} < {d}.length - 1) {{
""")
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('", "', Type('string'), call_position)
)};
}}
}}
""")
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('"}"', Type('string'), call_position)
)};
""")
            
            return codegen.c_manager._StringBuilder_str(codegen, call_position, builder)
        
        @c_dec(
            func_name_override=f'{dict_type.c_type}_type', add_to_class=c_manager,
            is_method=True, is_static=True
        )
        def dict_type_(_, call_position: Position) -> Object:
            return Object(f'"dict[{key_type}: {value_type}]"', Type('string'), call_position)
        
        @c_dec(
            param_types=(Param('dict', dict_type),),
            func_name_override=f'{dict_type.c_type}_keys', add_to_class=c_manager, is_property=True,
        )
        def dict_keys(codegen, call_position: Position, dict_obj: Object) -> Object:
            key_arr_type: Type = codegen.array_manager.define_array(key_type)
            keys: TempVar = codegen.create_temp_var(key_arr_type, call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            d = f'({dict_obj})'
            codegen.prepend_code(f"""{key_arr_type.c_type} {keys} = {codegen.call(
    f'{key_arr_type.c_type}_make', [], call_position
)};
for (size_t {i} = 0; {i} < {d}.length; {i}++) {{
    """)
            codegen.prepend_code(f"""{codegen.call(
    f'{key_arr_type.c_type}_add', [
        Arg(keys.OBJECT()),
        Arg(Object(f'{d}.elements[{i}].key', key_type, call_position))
    ], call_position
)};
}}""")
            
            return keys.OBJECT()
        
        @c_dec(
            param_types=(Param('dict', dict_type),),
            func_name_override=f'{dict_type.c_type}_values', add_to_class=c_manager, is_property=True,
        )
        def dict_values(codegen, call_position: Position, dict_obj: Object) -> Object:
            val_arr_type: Type = codegen.array_manager.define_array(value_type)
            values: TempVar = codegen.create_temp_var(val_arr_type, call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            d = f'({dict_obj})'
            codegen.prepend_code(f"""{val_arr_type.c_type} {values} = {codegen.call(
    f'{val_arr_type.c_type}_make', [], call_position
)};
for (size_t {i} = 0; {i} < {d}.length; {i}++) {{
    """)
            codegen.prepend_code(f"""{codegen.call(
    f'{val_arr_type.c_type}_add', [
        Arg(values.OBJECT()),
        Arg(Object(f'{d}.elements[{i}].value', value_type, call_position))
    ], call_position
)};
}}""")
            
            return values.OBJECT()
        
        @c_dec(
            param_types=(Param('a', dict_type), Param('b', dict_type)),
            func_name_override=f'{dict_type.c_type}_eq_{dict_type.c_type}', add_to_class=c_manager
        )
        def dict_eq_dict(codegen, call_position: Position, a: Object, b: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (size_t {i} = 0; {i} < ({a}).length; {i}++) {{
""")
            codegen.prepend_code(f"""if ({pair_neq(
    codegen, call_position,
    Object(f'({a}).elements[{i}]', pair_type, call_position),
    Object(f'({b}).elements[{i}]', pair_type, call_position)
)}) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(
            param_types=(Param('a', dict_type), Param('b', dict_type)),
            func_name_override=f'{dict_type.c_type}_neq_{dict_type.c_type}', add_to_class=c_manager
        )
        def dict_neq_dict(codegen, call_position: Position, a: Object, b: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""bool {res} = false;
for (size_t {i} = 0; {i} < ({a}).length; {i}++) {{
""")
            codegen.prepend_code(f"""if ({pair_eq(
    codegen, call_position,
    Object(f'({a}).elements[{i}]', pair_type, call_position),
    Object(f'({b}).elements[{i}]', pair_type, call_position)
)}) {{
        {res} = true;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(
            param_types=(Param('dict', dict_type), Param('key', key_type)),
            func_name_override=f'index_{dict_type.c_type}', add_to_class=c_manager
        )
        def index_dict(codegen, call_position: Position, dict_obj: Object, key: Object) -> Object:
            return dict_get(codegen, call_position, dict_obj, key)
        
        @c_dec(
            param_types=(Param('dict', dict_type), Param('i', Type('int'))),
            func_name_override=f'iter_{dict_type.c_type}', add_to_class=c_manager,
            return_type=pair_type,
        )
        def iter_dict(_, call_position: Position, dict_obj: Object, i: Object) -> Object:
            return Object(f'(({dict_obj}).elements[{i}])', pair_type, call_position)
        
        self.codegen.metadata[key_type] = value_type
        return dict_type
