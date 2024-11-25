from codegen.objects import Object, Position, Type, Param, Arg, Free, TempVar
from codegen.c_manager import c_dec
from ir.nodes import TypeNode


class Queue:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        codegen.type_checker.add_type('Queue')
        setattr(codegen.type_checker, 'Queue_type', self.queue_type)
        
        @c_dec(
            params=(Param('size', Type('int')),),
            add_to_class=self, is_method=True, is_static=True, generic_params=('T',),
            return_type=Type('Queue[{T}]')
        )
        def _Queue_new(codegen, call_position: Position, size: Object, *, T: Type) -> Object:
            queue_type = self.define_queue_type(T)
            return codegen.call(f'{queue_type.c_type}_make', [Arg(size)], call_position)
    
    def queue_type(self, node: TypeNode) -> Type | None:
        if node.array_type is None:
            return None
        
        return self.define_queue_type(self.codegen.visit_TypeNode(node.array_type))
    
    def define_queue_type(self, type: Type) -> Type:
        queue_type = Type(f'Queue[{type}]', f'{type.c_type}_queue')
        if self.codegen.type_checker.is_valid_type(queue_type):
            return queue_type
        
        self.codegen.add_toplevel_code(f"""typedef struct {{
    {type.c_type}* data;
    int rear;
    int front;
    size_t capacity;
    size_t length;
}} {queue_type.c_type};
""")
        
        c_manager = self.codegen.c_manager
        
        c_manager.init_class(self, str(queue_type), queue_type)
        c_manager.wrap_struct_properties('queue', queue_type, [
            Param('capacity', Type('int')), Param('length', Type('int')),
            Param('front', Type('int')), Param('rear', Type('int'))
        ])
        
        @c_dec(
            params=(Param('size', Type('int')),),
            add_to_class=c_manager, func_name_override=f'{queue_type.c_type}_make'
        )
        def queue_make(codegen, call_position: Position, size: Object) -> Object:
            queue_free = Free()
            queue: TempVar = codegen.create_temp_var(queue_type, call_position, free=queue_free)
            queue_free.object_name = f'{queue}.data'
            
            codegen.prepend_code(f"""{queue_type.c_type} {queue} = {{
    .data = ({type.c_type}*)malloc(sizeof({type.c_type}) * {size}),
    .rear = {size} - 1, .front = 0, .capacity = {size}, .length = 0
}};
{c_manager.buf_check(f'{queue}.data')}
""")
            
            return queue.OBJECT()
        
        @c_dec(
            params=(Param('queue', queue_type),),
            add_to_class=c_manager, func_name_override=f'{queue_type.c_type}_to_string',
            is_method=True
        )
        def queue_to_string(codegen, call_position: Position, queue: Object) -> Object:
            builder: Object = c_manager._StringBuilder_new(codegen, call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""{c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('"Queue("', Type('string'), call_position)
)};

for (size_t {i} = 0; {i} < ({queue}).length; {i}++) {{
""")
            codegen.prepend_code(f"""{c_manager._StringBuilder_add(
    codegen, call_position, builder, c_manager._to_string(
        codegen, call_position, Object(f'({queue}).data[{i}]', type, call_position)
    )
)};

if ({i} < ({queue}).length - 1) {{
""")
            codegen.prepend_code(f"""{c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('", "', Type('string'), call_position)
)};
}}
}}
""")
            codegen.prepend_code(f"""{c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('")"', Type('string'), call_position)
)};
""")
            
            return c_manager._StringBuilder_str(codegen, call_position, builder)
        
        @c_dec(
            params=(Param('queue', queue_type),),
            is_property=True, add_to_class=c_manager, func_name_override=f'{queue_type.c_type}_is_full'
        )
        def queue_is_full(_, call_position: Position, queue: Object) -> Object:
            return Object(f'(({queue}).length == ({queue}).capacity)', Type('string'), call_position)
        
        @c_dec(
            params=(Param('queue', queue_type),),
            is_property=True, add_to_class=c_manager,
            func_name_override=f'{queue_type}_is_empty'
        )
        def queue_is_empty(_, call_position: Position, queue: Object) -> Object:
            return Object(f'(({queue}).length == 0)', Type('string'), call_position)
        
        @c_dec(
            params=(Param('queue', queue_type), Param('item', type)),
            is_method=True, add_to_class=c_manager, func_name_override=f'{queue_type.c_type}_enqueue'
        )
        def enqueue(codegen, call_position: Position, queue: Object, item: Object) -> Object:
            codegen.prepend_code(f"""if ({queue_is_full(codegen, call_position, queue)}) {{
    {c_manager.err('Queue overflow')}
}}

({queue}).rear = (({queue}).rear + 1) % ({queue}).capacity;
({queue}).data[({queue}).rear] = {item};
({queue}).length++;
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            params=(Param('queue', queue_type),),
            is_method=True, add_to_class=c_manager, func_name_override=f'{queue_type.c_type}_dequeue'
        )
        def dequeue(codegen, call_position: Position, queue: Object) -> Object:
            item: TempVar = codegen.create_temp_var(type, call_position)
            
            codegen.prepend_code(f"""if ({queue_is_empty(codegen, call_position, queue)}) {{
    {c_manager.err('Queue underflow')}
}}

{type.c_type} {item} = ({queue}).data[({queue}).front];
({queue}).front = (({queue}).front + 1) % ({queue}).capacity;
({queue}).length--;
""")
            
            return item.OBJECT()

        self.codegen.type_checker.add_type(queue_type)
        return queue_type
