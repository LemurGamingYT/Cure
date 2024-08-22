from cure.objects import Object, Position, Free, Type
from cure.array_manager import DEFAULT_CAPACITY
from cure.c_manager import CManager, c_dec


class DictManager:
    def __init__(self, compiler) -> None:
        self.defined_types = []
        
        self.compiler = compiler
    
    def has_type(self, key_type: str, value_type: str) -> bool:
        for k, v in self.defined_types:
            if k == key_type and v == value_type:
                return True
        
        return False
    
    def define_dict(self, key_type: Type, value_type: Type) -> None:
        if self.has_type(key_type.type, value_type.type):
            return
        
        dict_type = Type(f'dict[{key_type}: {value_type}]', f'{key_type}_{value_type}_dict')
        pair_type = Type(f'pair{{{key_type}, {value_type}}}', f'{key_type}_{value_type}_pair')
        
        self.compiler.add_toplevel_code(f"""typedef struct {{
    {key_type.c_type} key;
    {value_type.c_type} value;
}} {pair_type.c_type};

typedef struct {{
    {pair_type.c_type}* elements;
    size_t length;
    size_t capacity;
}} {dict_type.c_type};
""")
        
        c_manager: CManager = self.compiler.c_manager
        
        @c_dec(
            func_name_override=f'{dict_type.c_type}_make',
            add_to_class=c_manager
        )
        def dict_make(compiler, call_position: Position) -> Object:
            d = compiler.create_temp_var(dict_type, call_position)
            compiler.prepend_code(f"""{dict_type.c_type} {d};
{d}.length = 0;
{d}.capacity = {DEFAULT_CAPACITY};
{d}.elements = ({pair_type.c_type}*)malloc({DEFAULT_CAPACITY} * sizeof({pair_type.c_type}));
{compiler.c_manager.buf_check(f'{d}.elements')}
""")
            
            compiler.add_end_code(f'free({d}.elements);')
            
            return Object(d, dict_type, call_position)
        
        @c_dec(
            param_types=(dict_type.c_type, key_type.c_type),
            func_name_override=f'{dict_type.c_type}_get',
            is_method=True,
            add_to_class=c_manager
        )
        def dict_get(compiler, call_position: Position, dict_obj: Object, key: Object) -> Object:
            value = compiler.create_temp_var(value_type, call_position)
            d = f'({dict_obj.code})'
            i = compiler.create_temp_var(Type('int'), call_position)
            compiler.prepend_code(f"""{value_type.c_type} {value};
for (size_t {i} = 0; {i} < {d}.length; {i}++) {{
    if ({d}.elements[{i}].key == ({key.code})) {{
        {value} = {d}.elements[{i}].value;
        break;
    }}
}}
""")
            
            return Object(value, value_type, call_position)
        
        @c_dec(
            param_types=(dict_type.c_type, key_type.c_type),
            func_name_override=f'{dict_type.c_type}_has',
            is_method=True,
            add_to_class=c_manager
        )
        def dict_has(compiler, call_position: Position, dict_obj: Object, key: Object) -> Object:
            d = f'({dict_obj.code})'
            i = compiler.create_temp_var(Type('int'), call_position)
            has = compiler.create_temp_var(Type('bool'), call_position)
            compiler.prepend_code(f"""bool {has} = false;
for (size_t {i} = 0; {i} < {d}.length; {i}++) {{
    if ({d}.elements[{i}].key == ({key.code})) {{
        {has} = true;
        break;
    }}
}}
""")
            return Object(has, Type('bool'), call_position)
        
        @c_dec(
            param_types=(dict_type.c_type, key_type.c_type, value_type.c_type),
            func_name_override=f'{dict_type.c_type}_set',
            is_method=True,
            add_to_class=c_manager
        )
        def dict_set(compiler, call_position: Position,
                     dict_obj: Object, key: Object, value: Object) -> Object:
            i = compiler.create_temp_var(Type('int'), call_position)
            d = f'({dict_obj.code})'
            compiler.prepend_code(f"""for (size_t {i} = 0; {i} < {d}.length; {i}++) {{
    if ({d}.elements[{i}].key == ({key.code})) {{
        {d}.elements[{i}].value = {value.code};
        break;
    }}
}}
if ({d}.length == {d}.capacity) {{
    {d}.capacity *= 2;
    {d}.elements = ({pair_type.c_type}*)realloc(
        {d}.elements,
        {d}.capacity * sizeof({pair_type.c_type})
    );
    
    {compiler.c_manager.buf_check(f'{d}.elements')}
}}
{d}.elements[{d}.length].key = {key.code};
{d}.elements[{d}.length].value = {value.code};
{d}.length++;
""")
            return Object('NULL', Type('nil'), call_position)
        
        @c_dec(
            param_types=(dict_type.c_type,),
            func_name_override=f'{dict_type.c_type}_to_string',
            add_to_class=c_manager
        )
        def dict_to_string(compiler, call_position: Position, dict_obj: Object) -> Object:
            buf = compiler.create_temp_var(Type('string'), call_position, free=Free())
            pos = compiler.create_temp_var(Type('int'), call_position)
            i = compiler.create_temp_var(Type('int'), call_position)
            d = f'({dict_obj.code})'
            length_calc = f'(({d}.length + 2) * 20 + 3) * sizeof(char)'
            buffer_ = f'{buf} + {pos}'
            buf_count = f'{length_calc} - {pos}'
            key_repr = compiler.create_temp_var(Type('string'), call_position)
            value_repr = compiler.create_temp_var(Type('string'), call_position)
            compiler.prepend_code(f"""string {buf} = (string)malloc({length_calc});
{compiler.c_manager.buf_check(buf)}
memset({buf}, 0, {length_calc});
size_t {pos} = 0;
{pos} += snprintf({buf}, {buf_count}, "{{");
for (size_t {i} = 0; {i} < {d}.length; {i}++) {{""")
            compiler.prepend_code(f"""string {key_repr} = {compiler.call(
    f'{key_type}_to_string',
    [Object(f'{d}.elements[{i}].key', key_type, call_position)],
    call_position
).code};
    string {value_repr} = {compiler.call(
    f'{value_type}_to_string',
    [Object(f'{d}.elements[{i}].value', value_type, call_position)],
    call_position
).code};
{pos} += snprintf({buffer_}, {buf_count}, "{{%s: %s}}", {key_repr}, {value_repr});
if ({i} < {d}.length - 1) {pos} += snprintf({buffer_}, {buf_count}, ", ");
""")
            compiler.prepend_code(f"""}}
strcat({buf}, "}}");""")

            return Object(buf, Type('string'), call_position, free=Free(buf))
        
        @c_dec(
            func_name_override=f'{dict_type.c_type}_type',
            add_to_class=c_manager
        )
        def dict_type_(_, call_position: Position) -> Object:
            return Object(f'"dict[{key_type}: {value_type}]"', Type('string'), call_position)
        
        @c_dec(
            param_types=(dict_type.c_type,),
            func_name_override=f'{dict_type.c_type}_keys',
            is_property=True,
            add_to_class=c_manager
        )
        def dict_keys(compiler, call_position: Position, dict_obj: Object) -> Object:
            key_arr_type = compiler.array_manager.define_array(key_type)
            keys = compiler.create_temp_var(key_arr_type, call_position)
            i = compiler.create_temp_var(Type('int'), call_position)
            d = f'({dict_obj.code})'
            compiler.prepend_code(f"""{key_arr_type.c_type} {keys} = {compiler.call(
    f'{key_arr_type.c_type}_make', [], call_position
).code};
for (size_t {i} = 0; {i} < {d}.length; {i}++) {{
    """)
            compiler.prepend_code(f"""{compiler.call(
        f'{key_arr_type.c_type}_add',
        [
            Object(keys, key_arr_type, call_position),
            Object(f'{d}.elements[{i}].key', key_type, call_position)
        ],
        call_position
    ).code};
}}""")
            
            return Object(keys, key_arr_type, call_position)
        
        @c_dec(
            param_types=(dict_type.c_type,),
            func_name_override=f'{dict_type.c_type}_values',
            is_property=True,
            add_to_class=c_manager
        )
        def dict_values(compiler, call_position: Position, dict_obj: Object) -> Object:
            val_arr_type = compiler.array_manager.define_array(value_type)
            values = compiler.create_temp_var(val_arr_type, call_position)
            i = compiler.create_temp_var(Type('int'), call_position)
            d = f'({dict_obj.code})'
            compiler.prepend_code(f"""{val_arr_type.c_type} {values} = {compiler.call(
    f'{val_arr_type.c_type}_make', [], call_position
).code};
for (size_t {i} = 0; {i} < {d}.length; {i}++) {{
    """)
            compiler.prepend_code(f"""{compiler.call(
        f'{val_arr_type.c_type}_add',
        [
            Object(values, val_arr_type, call_position),
            Object(f'{d}.elements[{i}].value', value_type, call_position)
        ],
        call_position
    ).code};
}}""")
            
            return Object(values, val_arr_type, call_position)
        
        self.defined_types.append((key_type.type, value_type.type))
