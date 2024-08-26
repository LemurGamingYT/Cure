from codegen.objects import Object, Position, Free, Type
from codegen.c_manager import c_dec


class Stack:
    def __init__(self, compiler) -> None:
        self.compiler = compiler
        
        self.defined_types: list[str] = []
    
    def define_stack_type(self, type: Type) -> Type:
        stack_type = Type(f'stack[{type}]', f'{type}Stack')
        if type.type in self.defined_types:
            return stack_type
        
        self.compiler.add_toplevel_code(f"""typedef struct {{
    {type.c_type}* data;
    size_t size;
    {type.c_type} top;
}} {stack_type.c_type};
""")
        
        c_manager = self.compiler.c_manager
        
        @c_dec(
            param_types=('int',),
            add_to_class=c_manager,
            func_name_override=f'{stack_type.c_type}_create'
        )
        def stack_create(compiler, call_position: Position, size: Object) -> Object:
            stack_free = Free()
            stack = compiler.create_temp_var(stack_type, call_position, free=stack_free)
            stack_free.object_name = f'{stack}.data'
            compiler.prepend_code(f"""{stack_type.c_type} {stack};
{stack}.data = ({type.c_type}*)malloc({size.code} * sizeof({type.c_type}));
{stack}.size = {size.code};
{stack}.top = -1;
""")
            
            return Object(stack, stack_type, call_position, free=stack_free)
        
        @c_dec(
            param_types=(stack_type.c_type,),
            add_to_class=c_manager,
            func_name_override=f'{stack_type.c_type}_to_string'
        )
        def stack_to_string(compiler, call_position: Position, stack: Object) -> Object:
            buf_free = Free()
            buf = compiler.create_temp_var(Type('string'), call_position, free=buf_free)
            elem_buf = compiler.create_temp_var(Type('string'), call_position)
            i = compiler.create_temp_var(Type('int'), call_position)
            length = compiler.create_temp_var(Type('int'), call_position)
            compiler.prepend_code(f"""string {buf} = NULL;
if ({stack_is_empty(
    compiler, call_position, stack
).code}) {{
    {buf} = (string)malloc(3 * sizeof(char));
    {compiler.c_manager.buf_check(buf)}
    strcpy({buf}, "[]");
}} else {{
    int {length} = 0;
    for (int {i} = 0; {i} <= ({stack.code}.top); {i}++) {{
""")
            compiler.prepend_code(f"""{length} += sizeof({c_manager._to_string(
    compiler, call_position,
    Object(f'({stack.code}).data[{i}]', type, call_position)
).code});
    }}
    
    {buf} = malloc((({length} * 2) + 3) * sizeof(char));
    {compiler.c_manager.buf_check(buf)}
    {buf}[0] = '\\0';
    strcat({buf}, "[");
    for (int {i} = 0; {i} <= ({stack.code}.top); {i}++) {{
""")
            compiler.prepend_code(f"""string {elem_buf} = {c_manager._to_string(
    compiler, call_position,
    Object(f'({stack.code}).data[{i}]', type, call_position)
).code};
        strcat({buf}, {elem_buf});
        if ({i} < {stack.code}.top) strcat({buf}, ", ");
    }}
    
    strcat({buf}, "]");
}}""")
            
            return Object(buf, Type('string'), call_position, free=buf_free)
        
        @c_dec(
            param_types=(stack_type.c_type,),
            add_to_class=c_manager,
            func_name_override=f'{stack_type.c_type}_is_empty',
            is_property=True
        )
        def stack_is_empty(_, call_position: Position, stack: Object) -> Object:
            return Object(f'({stack.code}).top == -1', Type('bool'), call_position)
        
        @c_dec(
            param_types=(stack_type.c_type,),
            add_to_class=c_manager,
            func_name_override=f'{stack_type.c_type}_is_full',
            is_property=True
        )
        def stack_is_full(_, call_position: Position, stack: Object) -> Object:
            return Object(f'({stack.code}).top == ({stack.code}).size - 1', Type('bool'),
                          call_position)
        
        @c_dec(
            param_types=(stack_type.c_type, type.c_type),
            add_to_class=c_manager,
            func_name_override=f'{stack_type.c_type}_push',
            is_method=True
        )
        def stack_push(compiler, call_position: Position, stack: Object,
                       element: Object) -> Object:
            compiler.prepend_code(f"""if ({stack_is_full(
    compiler, call_position, stack
).code}) {{
    {c_manager.err("Stack overflow")}
}}

({stack.code}).data[++({stack.code}).top] = {element.code};
""")
            
            return Object('NULL', Type('nil'), call_position)
        
        @c_dec(
            param_types=(stack_type.c_type,),
            add_to_class=c_manager,
            func_name_override=f'{stack_type.c_type}_pop',
            is_method=True
        )
        def stack_pop(compiler, call_position: Position, stack: Object) -> Object:
            compiler.prepend_code(f"""if ({stack_is_empty(
    compiler, call_position, stack
).code}) {{
    {c_manager.err("Stack underflow")}
}}
""")
            
            return Object(f'({stack.code}).data[({stack.code}).top--]', type, call_position)
        
        @c_dec(
            param_types=(stack_type.c_type,),
            add_to_class=c_manager,
            func_name_override=f'{stack_type.c_type}_peek',
            is_method=True
        )
        def stack_peek(compiler, call_position: Position, stack: Object) -> Object:
            compiler.prepend_code(f"""if ({stack_is_empty(
    compiler, call_position, stack
).code}) {{
    {c_manager.err("Stack underflow")}
}}
""")

            return Object(f'({stack.code}).data[({stack.code}).top]', type, call_position)
        
        self.defined_types.append(type.type)
        
        return stack_type
    
    def create_stack(self, compiler, call_position: Position, type: Object, size: Object) -> Object:
        stack_type = self.define_stack_type(Type(type.code))
        return compiler.call(f'{stack_type.c_type}_create', [size], call_position)
