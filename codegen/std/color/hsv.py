from codegen.objects import Object, Position, Type, TempVar
from codegen.c_manager import c_dec


class HSV:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""#ifndef CURE_COLOR_H
typedef struct {
    float h;
    float s;
    float v;
} HSV;
#endif
""")
    
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _HSV_type(_, call_position: Position) -> Object:
            return Object('"HSV"', Type('string'), call_position)
        
        @c_dec(param_types=('int', 'int', 'int'), is_method=True, add_to_class=self)
        def _HSV_to_string(codegen, call_position: Position, hsv: Object) -> Object:
            cls = f'({hsv})'
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, '"HSV(%f, %f, %f)"', f'{cls}.h', f'{cls}.s', f'{cls}.v'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        
        @c_dec(param_types=('HSV',), is_property=True, add_to_class=self)
        def _HSV_h(_, call_position: Position, hsv: Object) -> Object:
            return Object(f'(({hsv}).h)', Type('float'), call_position)
        
        @c_dec(param_types=('HSV',), is_property=True, add_to_class=self)
        def _HSV_s(_, call_position: Position, hsv: Object) -> Object:
            return Object(f'(({hsv}).s)', Type('float'), call_position)
        
        @c_dec(param_types=('HSV',), is_property=True, add_to_class=self)
        def _HSV_v(_, call_position: Position, hsv: Object) -> Object:
            return Object(f'(({hsv}).v)', Type('float'), call_position)
        
        @c_dec(param_types=('HSV',), is_property=True, add_to_class=self)
        def _HSV_to_rgb(codegen, call_position: Position, hsv: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            
            cls = f'({hsv})'
            h: TempVar = codegen.create_temp_var(Type('float'), call_position)
            s: TempVar = codegen.create_temp_var(Type('float'), call_position)
            v: TempVar = codegen.create_temp_var(Type('float'), call_position)
            c: TempVar = codegen.create_temp_var(Type('float'), call_position)
            x: TempVar = codegen.create_temp_var(Type('float'), call_position)
            m: TempVar = codegen.create_temp_var(Type('float'), call_position)
            r1: TempVar = codegen.create_temp_var(Type('float'), call_position)
            g1: TempVar = codegen.create_temp_var(Type('float'), call_position)
            b1: TempVar = codegen.create_temp_var(Type('float'), call_position)
            rgb: TempVar = codegen.create_temp_var(Type('RGB'), call_position)
            codegen.prepend_code(f"""float {h} = {cls}.h;
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

RGB {rgb} = {{
    .r = (unsigned char)(({r1} + {m}) * 255), .g = (unsigned char)(({g1} + {m}) * 255),
    .b = (unsigned char)(({b1} + {m}) * 255)
}};
""")
            
            return rgb.OBJECT()
