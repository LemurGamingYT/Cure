from codegen.objects import Object, Position, Type, Param, TempVar
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec
from ir.nodes import TypeNode


class OptionalManager:
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        setattr(codegen.type_checker, 'optional_type', self.optional_type)
    
    def optional_type(self, node: TypeNode) -> Type | None:
        if node.array_type is None:
            return None
        
        return self.define_optional(self.codegen.visit_TypeNode(node.array_type))
    
    def define_optional(self, type: Type) -> Type:
        opt_t = Type(
            f'optional[{type}]', f'{type.c_type}_optional',
            # compatible_types=(type.type, 'nil')
        )
        if self.codegen.type_checker.is_valid_type(opt_t):
            return opt_t
        
        self.codegen.add_toplevel_code(f"""typedef struct {{
    {type.c_type}* value;
}} {opt_t.c_type};
""")
        
        c_manager = self.codegen.c_manager
        c_manager.reserve(opt_t.c_type)
        c_manager.init_class(c_manager, str(opt_t), opt_t)
        
        def is_correct_type(value: Object) -> bool:
            return value.type == type or value.type == Type('nil')
        
        @c_dec(
            is_method=True, is_static=True, add_to_class=c_manager,
            func_name_override=f'_{opt_t.c_type}_type'
        )
        def type_(_, call_position: Position) -> Object:
            return Object(f'"{opt_t}"', Type('string'), call_position)
        
        @c_dec(
            params=(Param('opt', opt_t),), is_method=True, add_to_class=c_manager,
            func_name_override=f'_{opt_t.c_type}_to_string'
        )
        def to_string(_, call_position: Position, _opt: Object) -> Object:
            return Object(f'"optional \'{type}\'"', Type('string'), call_position)
        
        @c_dec(
            params=(Param('value', Type('any')),), add_to_class=c_manager,
            func_name_override=f'_{opt_t.c_type}_new'
        )
        def new(codegen, call_position: Position, value: Object) -> Object:
            if not is_correct_type(value):
                call_position.error_here(f'Expected optional type \'{type}\', got \'{value.type}\'')
            
            opt: TempVar = codegen.create_temp_var(opt_t, call_position)
            temp_value: TempVar = codegen.create_temp_var(value.type, call_position)
            should_point = value.type != Type('nil')
            codegen.prepend_code(f"""{value.type.c_type} {temp_value} = {value};
{opt_t.c_type} {opt} = {{ .value = {'&' if should_point else ''}{temp_value} }};
""")
            
            return opt.OBJECT()
        
        @c_dec(
            params=(Param('opt', opt_t),), is_property=True, add_to_class=c_manager,
            func_name_override=f'_{opt_t.c_type}_is_nil'
        )
        def is_nil(_, call_position: Position, opt: Object) -> Object:
            return Object(f'(({opt}).value == NULL)', Type('bool'), call_position)
        
        @c_dec(
            params=(Param('opt', opt_t),), is_property=True, add_to_class=c_manager,
            func_name_override=f'_{opt_t.c_type}_value'
        )
        def value(codegen, call_position: Position, opt: Object) -> Object:
            codegen.prepend_code(f"""if ({is_nil(codegen, call_position, opt)}) {{
    {codegen.c_manager.err('optional is nil')}
}}
""")
            
            return Object(f'(*(({opt}).value))', type, call_position)
        
        @c_dec(
            params=(Param('opt', opt_t), Param('new_value', Type('any'))), is_method=True,
            add_to_class=c_manager, func_name_override=f'_{opt_t.c_type}_set_value'
        )
        def set_value(codegen, call_position: Position, opt: Object, value: Object) -> Object:
            if not is_correct_type(value):
                call_position.error_here(
                    f'Expected optional value of type \'{type}\', got \'{value.type}\''
                )
            
            temp_value: TempVar = codegen.create_temp_var(value.type, call_position)
            should_point = value.type != Type('nil')
            codegen.prepend_code(f"""{value.type.c_type} {temp_value} = {value};
({opt}).value = {'&' if should_point else ''}{temp_value};
""")
            
            return Object.NULL(call_position)
        
        def unwrap(codegen, call_position: Position, opt: Object) -> Object:
            return value(codegen, call_position, opt)
        
        @c_dec(
            params=(Param('opt', opt_t), Param('default', type),), is_method=True,
            add_to_class=c_manager, overloads={OverloadKey(type, ()): OverloadValue(unwrap)},
            func_name_override=f'{opt_t.c_type}_unwrap'
        )
        def unwrap_default(codegen, call_position: Position, opt: Object, default: Object) -> Object:
            res: TempVar = codegen.create_temp_var(type, call_position)
            codegen.prepend_code(f"""{type.c_type} {res};
if ({is_nil(codegen, call_position, opt)}) {{
    {res} = {default};
}} else {{
    {res} = *(({opt}).value);
}}
""")
            
            return res.OBJECT()
        
        self.codegen.type_checker.add_type(opt_t)
        return opt_t
