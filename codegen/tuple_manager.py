from codegen.objects import Object, Position, Type, TempVar, Param, Arg
from codegen.c_manager import c_dec


class TupleManager:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        codegen.metadata.setdefault('tuple_types', [])
    
    def define_tuple(self, types: list[Type]) -> Type:
        tuple_type = Type(
            f'tuple[{", ".join(t.c_type for t in types)}]',
            f'tuple_{"_".join(t.c_type for t in types)}'
        )
        if tuple_type in self.codegen.metadata['tuple_types']:
            return tuple_type
        
        self.codegen.add_toplevel_code(f"""typedef struct {{
    {''.join(f'    {t.c_type} elem{i};' for i, t in enumerate(types))}
    size_t length;
}} {tuple_type.c_type};
""")
        
        c_manager = self.codegen.c_manager
        c_manager.init_class(self, str(tuple_type), tuple_type)
        c_manager.wrap_struct_properties('tuple', tuple_type, [
            Param('length', Type('int'))
        ])
        
        @c_dec(
            param_types=(Param('*', Type('*')),), is_method=True, add_to_class=c_manager,
            func_name_override=f'{tuple_type.c_type}_create'
        )
        def create(codegen, call_position: Position, *args: Object) -> Object:
            tuple: TempVar = codegen.create_temp_var(tuple_type, call_position)
            codegen.prepend_code(f"""{tuple_type.c_type} {tuple} = {{ .length = {len(args)} }};
""")
            for i, arg in enumerate(args):
                codegen.prepend_code(f"""({tuple}).elem{i} = {arg};
""")
                
            return tuple.OBJECT()
        
        @c_dec(
            param_types=(Param('tuple', tuple_type),), is_method=True, add_to_class=c_manager,
            func_name_override=f'{tuple_type.c_type}_to_string'
        )
        def to_string(codegen, call_position: Position, tuple: Object) -> Object:
            builder: Object = codegen.c_manager._StringBuilder_new(codegen, call_position)
            codegen.c_manager._StringBuilder_add(
                codegen, call_position, builder, Object('"("', Type('string'), call_position)
            )
            for i, t in enumerate(types):
                codegen.c_manager._StringBuilder_add(
                    codegen, call_position, builder, codegen.c_manager._to_string(
                        codegen, call_position, Object(f'({tuple}).elem{i}', t, call_position)
                    )
                )
                
                if i != len(types) - 1:
                    codegen.c_manager._StringBuilder_add(
                        codegen, call_position, builder, Object('", "', Type('string'), call_position)
                    )
            
            codegen.c_manager._StringBuilder_add(
                codegen, call_position, builder, Object('")"', Type('string'), call_position)
            )
            
            return codegen.c_manager._StringBuilder_str(codegen, call_position, builder)
        
        @c_dec(
            param_types=(Param('tuple', tuple_type), Param('index', Type('int')),), is_method=True,
            add_to_class=c_manager, func_name_override=f'{tuple_type.c_type}_get'
        )
        def get(codegen, call_position: Position, tuple: Object, index: Object) -> Object:
            if not codegen.is_number_constant(index):
                index.position.error_here('Tuple index must be a constant number')
            
            codegen.prepend_code(f"""if ({index} < 0 || {index} >= ({tuple}).length) {{
    {codegen.c_manager.err('Tuple index out of bounds %d', str(index))}
}}
""")
            
            idx = int(str(index))
            if idx < 0 or idx >= len(types):
                index.position.error_here(f'Tuple index out of bounds {idx}')
            
            type_ = types[idx]
            return Object(f'({tuple}).elem{idx}', type_, call_position)
        
        @c_dec(
            param_types=(Param('a', tuple_type), Param('b', tuple_type)),
            is_method=True, add_to_class=c_manager,
            func_name_override=f'{tuple_type.c_type}_eq_{tuple_type.c_type}'
        )
        def eq(codegen, call_position: Position, a: Object, b: Object) -> Object:
            is_equal: TempVar = codegen.create_temp_var(Type('bool'), call_position,
                                                        default_expr='true')
            for t in types:
                equal = codegen.call_callee(
                    f'{t.c_type}_eq_{t.c_type}', [Arg(a), Arg(b)],
                    f'Cannot compare type {t}', call_position
                )
                codegen.prepend_code(f"""if (!({equal})) {{
    {is_equal} = false;
}}
""")
            
            return is_equal.OBJECT()
        
        @c_dec(
            param_types=(Param('a', tuple_type), Param('b', tuple_type)),
            is_method=True, add_to_class=c_manager,
            func_name_override=f'{tuple_type.c_type}_neq_{tuple_type.c_type}'
        )
        def neq(codegen, call_position: Position, a: Object, b: Object) -> Object:
            is_not_equal: TempVar = codegen.create_temp_var(Type('bool'), call_position,
                                                        default_expr='true')
            for t in types:
                equal = codegen.call_callee(
                    f'{t.c_type}_neq_{t.c_type}', [Arg(a), Arg(b)],
                    f'Cannot compare type {t}', call_position
                )
                codegen.prepend_code(f"""if (!({equal})) {{
    {is_not_equal} = false;
}}
""")
            
            return is_not_equal.OBJECT()
        
        @c_dec(
            param_types=(Param('tuple', tuple_type), Param('index', Type('int'))),
            is_method=True, add_to_class=c_manager, return_type=Type('any'),
            func_name_override=f'index_{tuple_type.c_type}'
        )
        def index_tuple(codegen, call_position: Position, tuple: Object, index: Object) -> Object:
            return get(codegen, call_position, tuple, index)
        
        self.codegen.metadata['tuple_types'].append(tuple_type)
        return tuple_type
