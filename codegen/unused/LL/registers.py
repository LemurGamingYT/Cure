from codegen.objects import Object, Position, Type
from codegen.c_manager import c_dec


class Registers:
    REGISTER_ENUM = {
        'cr0': '0',
        'cr2': '1',
        'cr3': '2',
        'cr4': '3',
        'EFLAGS': '4',
        'CS': '5',
        'DS': '6',
        'ES': '7',
        'FS': '8',
        'GS': '9',
        'SS': '10',
    }
    
    def __init__(self, compiler) -> None:
        compiler.valid_types.append('Register')
        compiler.c_manager.RESERVED_NAMES.append('Register_name')
        
        compiler.add_toplevel_code(f"""typedef struct {{
    int register_name;
}} Register;

char* Register_name(int register_name) {{
    switch (register_name) {{
        {'\n'.join([f'case {i}: return "{name}";' for name, i in self.REGISTER_ENUM.items()])}
    }}
}}
""")
    
    
    @c_dec()
    def _Register_type(self, _, call_position: Position) -> Object:
        return Object('"Register"', Type('string'), call_position)
    
    @c_dec(params=('Register',))
    def _Register_to_string(self, _, call_position: Position, _register: Object) -> Object:
        return Object('"class \'Register\'"', Type('string'), call_position)
    
    
    @c_dec(params=('Register',), is_method=True)
    def _Register_read(self, _, call_position: Position, _register: Object) -> Object:
        return Object('', Type('nil'), call_position)
