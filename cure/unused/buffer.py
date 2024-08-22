from cure.objects import Object, Position, Free
from cure.parser.CureParser import CureParser
from cure.std.LL import READ_REGEX


class buffer:
    LIB_WIP = True
    
    def __init__(self, compiler) -> None:
        self.defined_types = []
        
        self.compiler = compiler
    
    def get_type(self, ctx: CureParser.TypeContext) -> str | None:
        name = ctx.ID().getText()
        if name == 'buffer':
            buf_type = self.compiler.visitType(ctx.type_())
            self.define_buf_type(self.compiler, f'"{buf_type}"', Position(0, 0, ''))
            return f'{buf_type.title()}Buffer'
    
    def define_buf_type(self, compiler, type: str, pos: Position) -> str:
        if (_type := READ_REGEX.match(type)) is not None:
            ident = _type.group(1)
            
            buf_type = f'{ident.title()}Buffer'
            if ident in self.defined_types:
                return buf_type
            
            
            self.defined_types.append(ident)
            
            compiler.add_toplevel_code(f"""typedef struct {{
    {ident}* elements;
    bool* free_elements;
    size_t length;
}} {buf_type};
""")
            compiler.valid_types.append(buf_type)
            
            def type_func(_, call_position: Position) -> Object:
                return Object(f'"{buf_type}"', 'string', call_position)
            
            def to_string(_, call_position: Position, buf: Object) -> Object:
                buf_name = compiler.create_temp_var('string', call_position, free=Free())
                i = compiler.create_temp_var('int', call_position)
                pos = compiler.create_temp_var('int', call_position)
                b = f'({buf.code})'
                
                length_calc = f'(({b}.length + 2) * 20 + 1) * sizeof(char)'
                buf_count = f'{length_calc} - {pos}'
                buffer_ = f'{buf_name} + {pos}'
                compiler.prepend_code(f"""string {buf_name} = (string)malloc({length_calc});
memset({buf_name}, 0, {length_calc});
size_t {pos} = 0;
for (size_t {i} = 0; {i} < {b}.length; {i}++) {{
    if ({b}.free_elements[{i}]) {{
        {pos} += snprintf({buf_name} + {pos}, {length_calc} - {pos}, "nil");
        if ({i} < {b}.length - 1) {pos} += snprintf({buffer_}, {buf_count}, ", ");
        continue;
    }}""")
                compiler.prepend_code(f"""{pos} += snprintf({buffer_}, {buf_count}, {compiler.call(
    f'{ident}_to_string',
    [Object(f'{b}.elements[{i}]', ident, call_position)],
    call_position
).code});
if ({i} < {b}.length - 1) {pos} += snprintf({buffer_}, {buf_count}, ", ");
}}
{buf_name}[{length_calc}] = '\\0';
""")
                
                return Object(buf_name, 'string', call_position, free=Free(buf_name))
            to_string.param_types = [buf_type]
            to_string.is_property = True
            
            def length(_, call_position: Position, buf: Object) -> Object:
                return Object(f'(({buf.code}).length)', 'int', call_position)
            length.param_types = [buf_type]
            length.is_property = True
            
            def set_value(_, call_position: Position,
                          buf: Object, i: Object, value: Object) -> Object:
                compiler.prepend_code(f"""({buf.code}).elements[{i.code}] = {value.code};
({buf.code}).free_elements[{i.code}] = false;""")
                return Object('NULL', 'nil', call_position)
            set_value.param_types = [buf_type, 'int', ident]
            set_value.is_method = True
            
            def get(_, call_position: Position, buf: Object, i: Object) -> Object:
                b = f'({buf.code})'
                compiler.prepend_code(f"""if (({i.code}) >= {b}.length || {i.code} < 0) {{
    {compiler.c_manager.err('Index out of range')}
}}

if (({b}.free_elements[{i.code}])) {{
    {compiler.c_manager.err('index %d is nil', i.code)}
}}
""")
                
                return Object(f'({b}.elements[{i.code}])', ident, call_position)
            get.param_types = [buf_type, 'int']
            get.is_method = True
            
            setattr(compiler.c_manager, f'_{buf_type}_type', type_func)
            setattr(compiler.c_manager, f'_{buf_type}_length', length)
            setattr(compiler.c_manager, f'_{buf_type}_to_string', to_string)
            setattr(compiler.c_manager, f'_{buf_type}_set', set_value)
            setattr(compiler.c_manager, f'_{buf_type}_get', get)
            
            return buf_type
        else:
            pos.error_here(f'Cannot create type \'{type}\' as a buffer')
    
    def _create_buf(self, compiler, call_position: Position, type: Object, size: Object) -> Object:
        buf_type = self.define_buf_type(compiler, type.code, call_position)
        ident = type.code[1:-1]
        buffer_name = compiler.create_temp_var(buf_type, call_position)
        elements = compiler.create_temp_var('int_array', call_position)
        free_elements = compiler.create_temp_var('static_bool_array', call_position)
        i = compiler.create_temp_var('int', call_position)
        length_calc = f'{size.code} * sizeof({ident})'
        compiler.add_end_code(f"""free({buffer_name}.elements);
free({buffer_name}.free_elements);""")
        compiler.prepend_code(f"""{ident}* {elements} = ({ident}*)malloc({length_calc});
{buf_type} {buffer_name};
{buffer_name}.length = {size.code};
{buffer_name}.elements = {elements};
bool* {free_elements} = (bool*)malloc({length_calc});
for (size_t {i} = 0; {i} < {length_calc}; {i}++) {{
    {free_elements}[{i}] = true;
}}
{buffer_name}.free_elements = {free_elements}""")
        return Object(buffer_name, buf_type, call_position, free=Free(buffer_name))
    _create_buf.param_types = ['string', 'int']
    _create_buf.can_user_call = True
