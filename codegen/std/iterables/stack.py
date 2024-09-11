from codegen.objects import Object, Position, Free, Type, Arg, TempVar
from codegen.c_manager import c_dec


class Stack:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        
        self.defined_types: list[str] = []
    
    def define_stack_type(self, type: Type) -> Type:
        stack_type = Type(f'stack[{type}]', f'{type.c_type}Stack')
        if type.type in self.defined_types:
            return stack_type
        
        self.codegen.add_toplevel_code(f"""typedef struct {{
    {type.c_type}* data;
    size_t size;
    {type.c_type} top;
}} {stack_type.c_type};
""")
        
        c_manager = self.codegen.c_manager
        
        @c_dec(
            param_types=('int',),
            add_to_class=c_manager,
            func_name_override=f'{stack_type.c_type}_create'
        )
        def stack_create(codegen, call_position: Position, size: Object) -> Object:
            stack_free = Free()
            stack: TempVar = codegen.create_temp_var(stack_type, call_position, free=stack_free)
            stack_free.object_name = f'{stack}.data'
            codegen.prepend_code(f"""{stack_type.c_type} {stack} = {{
    .data = ({type.c_type}*)malloc({size} * sizeof({type.c_type})),
    .size = {size},
    .top = -1
}};
""")
            
            return stack.OBJECT()
        
        @c_dec(
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_type',
            is_method=True, is_static=True
        )
        def stack_type_(_, call_position: Position) -> Object:
            return Object(f'"{stack_type}"', Type('string'), call_position)
        
        @c_dec(
            param_types=(stack_type.c_type,),
            add_to_class=c_manager,
            func_name_override=f'{stack_type.c_type}_to_string',
            is_method=True
        )
        def stack_to_string(codegen, call_position: Position, stack: Object) -> Object:
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            elem_buf: TempVar = codegen.create_temp_var(Type('string'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""string {buf} = NULL;
if ({stack_is_empty(
    codegen, call_position, stack
)}) {{
    {buf} = (string)malloc(3 * sizeof(char));
    {codegen.c_manager.buf_check(buf)}
    strcpy({buf}, "[]");
}} else {{
    int {length} = 0;
    for (int {i} = 0; {i} <= ({stack}.top); {i}++) {{
""")
            codegen.prepend_code(f"""{length} += sizeof({c_manager._to_string(
    codegen, call_position,
    Object(f'({stack}).data[{i}]', type, call_position)
)});
    }}
    
    {buf} = malloc((({length} * 2) + 3) * sizeof(char));
    {codegen.c_manager.buf_check(buf)}
    {buf}[0] = '\\0';
    strcat({buf}, "[");
    for (int {i} = 0; {i} <= ({stack}.top); {i}++) {{
""")
            codegen.prepend_code(f"""string {elem_buf} = {c_manager._to_string(
    codegen, call_position,
    Object(f'({stack}).data[{i}]', type, call_position)
)};
        strcat({buf}, {elem_buf});
        if ({i} < {stack}.top) strcat({buf}, ", ");
    }}
    
    strcat({buf}, "]");
}}
""")
            
            return buf.OBJECT()
        
        @c_dec(
            param_types=(stack_type.c_type,),
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_is_empty',
            is_property=True
        )
        def stack_is_empty(_, call_position: Position, stack: Object) -> Object:
            return Object(f'(({stack}).top == -1)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(stack_type.c_type,),
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_is_full',
            is_property=True
        )
        def stack_is_full(_, call_position: Position, stack: Object) -> Object:
            return Object(f'(({stack}).top == ({stack}).size - 1)', Type('bool'),
                          call_position)
        
        @c_dec(
            param_types=(stack_type.c_type, type.c_type),
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_push',
            is_method=True
        )
        def stack_push(codegen, call_position: Position, stack: Object,
                       element: Object) -> Object:
            codegen.prepend_code(f"""if ({stack_is_full(
    codegen, call_position, stack
)}) {{
    {c_manager.err("Stack overflow")}
}}

({stack}).data[++({stack}).top] = {element};
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(stack_type.c_type,),
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_pop',
            is_method=True
        )
        def stack_pop(codegen, call_position: Position, stack: Object) -> Object:
            codegen.prepend_code(f"""if ({stack_is_empty(
    codegen, call_position, stack
)}) {{
    {c_manager.err("Stack underflow")}
}}
""")
            
            return Object(f'(({stack}).data[({stack}).top--])', type, call_position)
        
        @c_dec(
            param_types=(stack_type.c_type,),
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_peek',
            is_method=True
        )
        def stack_peek(codegen, call_position: Position, stack: Object) -> Object:
            codegen.prepend_code(f"""if ({stack_is_empty(
    codegen, call_position, stack
)}) {{
    {c_manager.err("Stack underflow")}
}}
""")

            return Object(f'(({stack}).data[({stack}).top])', type, call_position)
        
        self.defined_types.append(type.type)
        return stack_type
    
    def create_stack(self, codegen, call_position: Position, type: Object, size: Object) -> Object:
        stack_type = self.define_stack_type(Type(str(type)))
        return codegen.call(f'{stack_type.c_type}_create', [Arg(size)], call_position)
