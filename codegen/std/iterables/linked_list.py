from codegen.objects import Object, Position, Free, Type
from codegen.c_manager import c_dec


class LinkedList:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        
        self.defined_types: list[str] = []
    
    def define_linked_list_type(self, type: Type) -> Type:
        node_type = Type(f'LinkedList[{type}]', f'{str(type).title()}LinkedListNode')
        list_type = Type(f'LinkedList[{type}]', f'{str(type).title()}LinkedList')
        
        if type.type in self.defined_types:
            return list_type
    
        self.codegen.add_toplevel_code(f"""typedef struct {{
    {type.c_type} data;
    struct {node_type.c_type}* next;
}} {node_type.c_type};

typedef struct {{
    {node_type.c_type}* head;
}} {list_type.c_type};
""")
        
        c_manager = self.codegen.c_manager
        
        @c_dec(add_to_class=c_manager, func_name_override=f'{list_type.c_type}_make')
        def make_ll(codegen, call_position: Position) -> Object:
            ll_free = Free(free_name=f'{list_type.c_type}_free')
            ll = codegen.create_temp_var(list_type, call_position, free=ll_free)
            free(codegen, call_position, ll)

            codegen.prepend_code(f'{list_type.c_type} {ll} = {{ .head = NULL }};')
            return Object(ll, list_type, call_position, free=ll_free)
        
        @c_dec(
            add_to_class=c_manager, func_name_override=f'{list_type.c_type}_type',
            is_method=True, is_static=True
        )
        def type_(_, call_position: Position) -> Object:
            return Object(f'"{list_type}"', Type('string'), call_position)
        
        @c_dec(
            add_to_class=c_manager,
            func_name_override=f'{list_type.c_type}_to_string',
            param_types=(list_type.c_type,),
            is_method=True
        )
        def to_string(codegen, call_position: Position, ll: Object) -> Object:
            ll_code = f'({ll.code})'
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position,
                '"LinkedList(head=%p)"',
                f'{ll_code}.head'
            )
            
            codegen.prepend_code(code)
            return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
        
        @c_dec(
            add_to_class=c_manager,
            func_name_override=f'{list_type.c_type}_count',
            param_types=(list_type.c_type,),
            is_property=True
        )
        def count(codegen, call_position: Position, ll: Object) -> Object:
            i = codegen.create_temp_var(Type('int'), call_position)
            node = codegen.create_temp_var(node_type, call_position)
            list_ = f'({ll.code})'
            codegen.prepend_code(f"""int {i} = 1;
{node_type.c_type}* {node} = {list_}.head;
while ({node} != NULL) {{
    {i}++;
    {node} = ({node_type.c_type}*){node}->next;
}}
""")
            
            return Object(i, Type('int'), call_position)
        
        @c_dec(
            add_to_class=c_manager,
            func_name_override=f'{list_type.c_type}_first',
            param_types=(list_type.c_type,),
            is_property=True
        )
        def first(codegen, call_position: Position, ll: Object) -> Object:
            list_ = f'({ll.code})'
            codegen.prepend_code(f"""if ({list_}.head == NULL) {{
    {c_manager.err('Index out of range')}
}}
""")
            return Object(f'({list_}.head)', type, call_position)
        
        @c_dec(
            add_to_class=c_manager,
            func_name_override=f'{list_type.c_type}_last',
            param_types=(list_type.c_type,),
            is_property=True
        )
        def last(codegen, call_position: Position, ll: Object) -> Object:
            node = codegen.create_temp_var(node_type, call_position)
            first_node = first(codegen, call_position, ll)
            codegen.prepend_code(f"""{node_type.c_type}* {node} = {first_node.code};
while ({node}->next != NULL) {{
    {node} = ({node_type.c_type}*){node}->next;
}}
""")

            return Object(node, node_type, call_position)
        
        @c_dec(
            add_to_class=c_manager,
            func_name_override=f'{list_type.c_type}_insert_begin',
            param_types=(list_type.c_type, type.c_type),
            is_method=True
        )
        def insert_begin(codegen, call_position: Position,
                            ll: Object, value: Object) -> Object:
            new_node = codegen.create_temp_var(node_type, call_position)
            list_ = f'({ll.code})'
            codegen.prepend_code(f"""{node_type.c_type} {new_node} = {{
    .data = {value.code}, .next = {list_}.head
}};
{list_}.head = &{new_node};
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            add_to_class=c_manager,
            func_name_override=f'{list_type.c_type}_insert_at_index',
            param_types=(list_type.c_type, 'int', type.c_type),
            is_method=True
        )
        def insert_at_index(codegen, call_position: Position,
                          ll: Object, index: Object, value: Object) -> Object:
            new_node = codegen.create_temp_var(node_type, call_position)
            current = codegen.create_temp_var(node_type, call_position)
            i = codegen.create_temp_var(Type('int'), call_position)
            list_ = f'({ll.code})'
            codegen.prepend_code(f"""{node_type.c_type} {new_node};
{new_node}.data = {value.code};
if (({index.code}) == 0 || {list_}.head == NULL) {{
    {new_node}.next = {list_}.head;
    {list_}.head = &{new_node};
}} else {{
    {node_type}* {current} = {list_}.head;
    for (int {i} = 0; {i} < ({index.code}) - 1 && {current}->next != NULL; {i}++) {{
        {current} = ({node_type}*){current}->next;
    }}
    
    {new_node}.next = {current}->next;
    {current}->next = &{new_node};
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            add_to_class=c_manager,
            func_name_override=f'{list_type.c_type}_insert_end',
            param_types=(list_type.c_type, type.c_type),
            is_method=True
        )
        def insert_end(codegen, call_position: Position, ll: Object, value: Object) -> Object:
            new_node = codegen.create_temp_var(node_type, call_position)
            last_node = codegen.create_temp_var(node_type, call_position)
            list_ = f'({ll.code})'
            codegen.prepend_code(f"""{node_type.c_type} {new_node};
{new_node}.data = {value.code};
{new_node}.next = NULL;
if ({list_}.head == NULL) {{
    {list_}.head = &{new_node};
}} else {{
    {node_type.c_type}* {last_node} = {list_}.head;
    while ({last_node}->next != NULL) {{
        {last_node} = ({node_type.c_type}*){last_node}->next;
    }}
    
    {last_node}->next = (struct {node_type.c_type}*)&{new_node};
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            add_to_class=c_manager,
            func_name_override=f'{list_type.c_type}_remove',
            param_types=(list_type.c_type, type.c_type),
            is_method=True
        )
        def remove(codegen, call_position: Position, ll: Object, value: Object) -> Object:
            current = codegen.create_temp_var(node_type, call_position)
            prev = codegen.create_temp_var(node_type, call_position)
            list_ = f'({ll.code})'
            codegen.prepend_code(f"""{node_type.c_type}* {current} = {list_}.head;
{node_type.c_type}* {prev} = NULL;
while ({current} != NULL && {current}->data != ({value.code})) {{
    {prev} = {current};
    {current} = ({node_type.c_type}*){current}->next;
}}

if ({current} != NULL) {{
    if ({prev} == NULL) {{
        {list_}.head = ({node_type.c_type}*){current}->next;
    }} else {{
        {prev}->next = {current}->next;
    }}
}}
""")
            
            return Object.NULL(call_position)
        
        def free(codegen, call_position: Position, ll: str) -> Object:
            node = codegen.create_temp_var(node_type, call_position)
            temp = codegen.create_temp_var(node_type, call_position)
            list_ = f'({ll})'
            codegen.c_manager.RESERVED_NAMES.append(f'{list_type.c_type}_free')
            codegen.add_toplevel_code(f"""void {list_type.c_type}_free({list_type.c_type} {ll}) {{
    {node_type.c_type}* {node} = {list_}.head;
    while ({node} != NULL) {{
        {node_type.c_type}* {temp} = ({node_type.c_type}*){node}->next;
        free({node});
        {node} = {temp};
    }}
}}
""")
            
            return Object.NULL(call_position)
        
        self.defined_types.append(type.type)
        
        return list_type
    
    def create_linked_list(self, codegen, call_position: Position, type: Object) -> Object:
        ll_type = self.define_linked_list_type(Type(type.code))
        return codegen.call(f'{ll_type.c_type}_make', [], call_position)
