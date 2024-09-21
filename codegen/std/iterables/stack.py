from codegen.objects import Object, Position, Free, Type, Arg, TempVar, Param
from codegen.c_manager import c_dec


class Stack:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        
        self.defined_types: list[str] = []
        
        @c_dec(
            param_types=(Param('type', Type('type')), Param('size', Type('int'))),
            can_user_call=True, add_to_class=self
        )
        def _create_stack(codegen, call_position: Position, type: Object, size: Object) -> Object:
            stack_type = self.define_stack_type(Type(str(type)))
            return codegen.call(f'{stack_type.c_type}_create', [Arg(size)], call_position)
    
    def define_stack_type(self, type: Type) -> Type:
        stack_type = Type(f'stack[{type}]', f'{type.c_type}Stack')
        if type.type in self.defined_types:
            return stack_type
        
        self.codegen.add_toplevel_code(f"""typedef struct {{
    {type.c_type}* data;
    size_t size;
    size_t length;
}} {stack_type.c_type};
""")
        
        c_manager = self.codegen.c_manager
        
        c_manager.wrap_struct_properties('stack', stack_type, [
            Param('size', Type('int')), Param('length', Type('int'))
        ])
        
        @c_dec(
            param_types=(Param('size', Type('int')),),
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_create'
        )
        def stack_create(codegen, call_position: Position, size: Object) -> Object:
            stack_free = Free()
            stack: TempVar = codegen.create_temp_var(stack_type, call_position, free=stack_free)
            stack_free.object_name = f'{stack}.data'
            codegen.prepend_code(f"""{stack_type.c_type} {stack} = {{
    .data = ({type.c_type}*)malloc({size} * sizeof({type.c_type})),
    .size = {size},
    .length = 0
}};
""")
            
            return stack.OBJECT()
        
        @c_dec(
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_type',
            is_method=True, is_static=True
        )
        def stack_type_(_, call_position: Position) -> Object:
            return Object(f'"Stack[{stack_type}]"', Type('string'), call_position)
        
        @c_dec(
            param_types=(Param('stack', stack_type),), is_method=True,
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_to_string',
        )
        def stack_to_string(codegen, call_position: Position, stack: Object) -> Object:
            builder: Object = codegen.c_manager._StringBuilder_new(codegen, call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('"Stack("', Type('string'), call_position)
)};
for (size_t {i} = 0; {i} < ({stack}).length; {i}++) {{
""")
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, codegen.c_manager._to_string(
        codegen, call_position, Object(f'({stack}).data[{i}]', type, call_position)
    )
)};

if ({i} < ({stack}).length - 1) {{
""")
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('", "', Type('string'), call_position)
)};
}}
}}
""")
            codegen.prepend_code(f"""{codegen.c_manager._StringBuilder_add(
    codegen, call_position, builder, Object('")"', Type('string'), call_position)
)};
""")
            
            return codegen.c_manager._StringBuilder_str(codegen, call_position, builder)
        
        @c_dec(
            param_types=(Param('stack', stack_type),), is_property=True,
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_is_empty',
        )
        def stack_is_empty(_, call_position: Position, stack: Object) -> Object:
            return Object(f'(({stack}).length == 0)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(Param('stack', stack_type),), is_property=True,
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_is_full',
        )
        def stack_is_full(_, call_position: Position, stack: Object) -> Object:
            return Object(f'(({stack}).length == ({stack}).size)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(Param('stack', stack_type), Param('element', type)), is_method=True,
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_push',
        )
        def stack_push(codegen, call_position: Position, stack: Object, element: Object) -> Object:
            codegen.prepend_code(f"""if ({stack_is_full(codegen, call_position, stack)}) {{
    {c_manager.err("Stack overflow")}
}}

({stack}).data[({stack}).length++] = {element};
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('stack', stack_type),), is_method=True,
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_pop',
        )
        def stack_pop(codegen, call_position: Position, stack: Object) -> Object:
            codegen.prepend_code(f"""if ({stack_is_empty(codegen, call_position, stack)}) {{
    {c_manager.err("Stack underflow")}
}}
""")
            
            return Object(f'(({stack}).data[({stack}).length--])', type, call_position)
        
        @c_dec(
            param_types=(Param('stack', stack_type),), is_method=True,
            add_to_class=c_manager, func_name_override=f'{stack_type.c_type}_peek',
        )
        def stack_peek(codegen, call_position: Position, stack: Object) -> Object:
            codegen.prepend_code(f"""if ({stack_is_empty(codegen, call_position, stack)}) {{
    {c_manager.err("Stack underflow")}
}}
""")

            return Object(f'(({stack}).data[({stack}).length])', type, call_position)
        
        self.defined_types.append(type.type)
        return stack_type
