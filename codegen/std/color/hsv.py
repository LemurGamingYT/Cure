from codegen.objects import Object, Position, Type
from codegen.c_manager import c_dec


class HSV:
    def __init__(self, compiler) -> None:
        compiler.add_toplevel_code("""typedef struct {
    float h;
    float s;
    float v;
} HSV;
""")
    
    @c_dec()
    def _HSV_type(self, _, call_position: Position) -> Object:
        return Object('"HSV"', Type('string'), call_position)
    
    @c_dec(param_types=('int', 'int', 'int'))
    def _HSV_to_string(self, compiler, call_position: Position, hsv: Object) -> Object:
        cls = f'({hsv.code})'
        code, buf_free = compiler.c_manager.fmt_length(
            compiler, call_position,
            'HSV(%f, %f, %f)',
            f'{cls}.h', f'{cls}.s', f'{cls}.v'
        )
        
        compiler.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    
    @c_dec(param_types=('HSV',), is_property=True)
    def _HSV_h(self, _, call_position: Position, hsv: Object) -> Object:
        return Object(f'({hsv.code}).h', Type('float'), call_position)
    
    @c_dec(param_types=('HSV',), is_property=True)
    def _HSV_s(self, _, call_position: Position, hsv: Object) -> Object:
        return Object(f'({hsv.code}).s', Type('float'), call_position)
    
    @c_dec(param_types=('HSV',), is_property=True)
    def _HSV_v(self, _, call_position: Position, hsv: Object) -> Object:
        return Object(f'({hsv.code}).v', Type('float'), call_position)
    
    @c_dec(
        param_types=('HSV',),
        is_property=True
    )
    def _HSV_to_rgb(self, compiler, call_position: Position, hsv: Object) -> Object:
        compiler.c_manager.include('<math.h>', compiler)
        
        cls = f'({hsv.code})'
        h = compiler.create_temp_var(Type('float'), call_position)
        s  = compiler.create_temp_var(Type('float'), call_position)
        v  = compiler.create_temp_var(Type('float'), call_position)
        c = compiler.create_temp_var(Type('float'), call_position)
        x = compiler.create_temp_var(Type('float'), call_position)
        m = compiler.create_temp_var(Type('float'), call_position)
        r1 = compiler.create_temp_var(Type('float'), call_position)
        g1 = compiler.create_temp_var(Type('float'), call_position)
        b1 = compiler.create_temp_var(Type('float'), call_position)
        rgb = compiler.create_temp_var(Type('RGB'), call_position)
        compiler.prepend_code(f"""float {h} = {cls}.h;
float {s} = {cls}.s;
float {v} = {cls}.v;
float {c} = {v} * {s};
float {x} = {c} * (1 - fabs(fmod({h} / 60.0f, 2) - 1));
float {m} = {v} - {c};

float {r1}, {g1}, {b1};
if ({h} >= 0 && {h} < 60) {{
    {r1} = {c}; {g1} = {x}; {b1} = 0;
}} else if ({h} >= 60 && {h} < 120) {{
    {r1} = {x}; {g1} = {c}; {b1} = 0;
}} else if ({h} >= 120 && {h} < 180) {{
    {r1} = 0; {g1} = {c}; {b1} = {x};
}} else if ({h} >= 180 && {h} < 240) {{
    {r1} = 0; {g1} = {x}; {b1} = {c};
}} else if ({h} >= 240 && {h} < 300) {{
    {r1} = {x}; {g1} = 0; {b1} = {c};
}} else {{
    {r1} = {c}; {g1} = 0; {b1} = {x};
}}

RGB {rgb};
{rgb}.r = (unsigned char)(({r1} + {m}) * 255);
{rgb}.g = (unsigned char)(({g1} + {m}) * 255);
{rgb}.b = (unsigned char)(({b1} + {m}) * 255);
""")
        
        return Object(rgb, Type('RGB'), call_position)
