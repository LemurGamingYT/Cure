from codegen.objects import Object, Position, Type
from codegen.c_manager import c_dec


class RGB:
    def __init__(self, compiler) -> None:
        compiler.add_toplevel_code("""typedef struct {
    unsigned char r;
    unsigned char g;
    unsigned char b;
} RGB;
""")
    
    @c_dec()
    def _RGB_type(self, _, call_position: Position) -> Object:
        return Object('"RGB"', Type('string'), call_position)
    
    @c_dec(param_types=('RGB',))
    def _RGB_to_string(self, compiler, call_position: Position, rgb: Object) -> Object:
        cls = f'({rgb.code})'
        code, buf_free = compiler.c_manager.fmt_length(
            compiler, call_position,
            'RGB(%d, %d, %d)',
            f'{cls}.r', f'{cls}.g', f'{cls}.b'
        )
        
        compiler.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    
    @c_dec(param_types=('RGB',), is_property=True)
    def _RGB_r(self, _, call_position: Position, rgb: Object) -> Object:
        return Object(f'({rgb.code}).r', Type('int'), call_position)
    
    @c_dec(param_types=('RGB',), is_property=True)
    def _RGB_g(self, _, call_position: Position, rgb: Object) -> Object:
        return Object(f'({rgb.code}).g', Type('int'), call_position)
    
    @c_dec(param_types=('RGB',), is_property=True)
    def _RGB_b(self, _, call_position: Position, rgb: Object) -> Object:
        return Object(f'({rgb.code}).b', Type('int'), call_position)
    
    @c_dec(
        param_types=('RGB',),
        is_property=True
    )
    def _RGB_to_hsv(self, compiler, call_position: Position, rgb: Object) -> Object:
        compiler.c_manager.include('<math.h>', compiler)
        
        cls = f'({rgb.code})'
        r = compiler.create_temp_var(Type('float'), call_position)
        g = compiler.create_temp_var(Type('float'), call_position)
        b = compiler.create_temp_var(Type('float'), call_position)
        hsv = compiler.create_temp_var(Type('HSV'), call_position)
        delta = compiler.create_temp_var(Type('float'), call_position)
        _max = compiler.create_temp_var(Type('float'), call_position)
        _min = compiler.create_temp_var(Type('float'), call_position)
        compiler.prepend_code(f"""float {r} = {cls}.r / 255.0f;
float {g} = {cls}.g / 255.0f;
float {b} = {cls}.b / 255.0f;
float {_min} = {r} > {g} ? ({r} > {b} ? {r} : {b}) : ({g} > {b} ? {g} : {b});
float {_max} = {r} < {g} ? ({r} < {b} ? {r} : {b}) : ({g} < {b} ? {g} : {b});
float {delta} = {_max} - {_min};
HSV {hsv};
if ({delta} == 0) {{
    {hsv}.h = 0;
}} else if ({_max} == {r}) {{
    {hsv}.h = 60 * fmod((({g} - {b}) / {delta}), 6);
}} else if ({_max} == {g}) {{
    {hsv}.h = 60 * ((({b} - {r}) / {delta}) + 2);
}} else {{
    {hsv}.h = 60 * ((({r} - {g}) / {delta}) + 4);
}}

if ({hsv}.h < 0) {{
    {hsv}.h += 360;
}}

{hsv}.s = {_max} == 0 ? 0 : ({delta} / {_max});
{hsv}.v = {_max};
""")
        
        return Object(hsv, Type('HSV'), call_position)
