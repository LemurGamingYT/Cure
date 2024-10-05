from codegen.objects import Object, Position, Type, Arg, TempVar, Param
from codegen.std.color.hex_triplet import HexTriplet
from codegen.std.color.rgb import RGB
from codegen.std.color.hsv import HSV
from codegen.c_manager import c_dec


class color:
    def __init__(self, codegen) -> None:
        codegen.add_type(('RGB', 'HSV', 'HexTriplet'))
        codegen.c_manager.reserve(('RGB', 'HSV', 'HexTriplet'))
        codegen.c_manager.add_objects(HexTriplet(codegen), self)
        codegen.c_manager.add_objects(RGB(codegen), self)
        codegen.c_manager.add_objects(HSV(codegen), self)
        codegen.add_toplevel_code("""#ifndef CURE_COLOR_H
#define CURE_COLOR_H
#endif
""")
    
        @c_dec(
            param_types=(Param('r', Type('int')), Param('g', Type('int')), Param('b', Type('int'))),
            is_method=True, is_static=True, add_to_class=self
        )
        def _RGB_new(codegen, call_position: Position,
                r: Object, g: Object, b: Object) -> Object:
            _r, _g, _b = f'({r})', f'({g})', f'({b})'
            rgb: TempVar = codegen.create_temp_var(Type('RGB'), call_position)
            codegen.prepend_code(f"""if ({_r} > 255 || {_r} < 0) {{
    {codegen.c_manager.err('\'r\' must be between 0 and 255')}
}}

if ({_g} > 255 || {_g} < 0) {{
    {codegen.c_manager.err('\'g\' must be between 0 and 255')}
}}

if ({_b} > 255 || {_b} < 0) {{
    {codegen.c_manager.err('\'b\' must be between 0 and 255')}
}}

RGB {rgb} = {{ .r = {_r}, .g = {_g}, .b = {_b} }};
""")

            return rgb.OBJECT()
        
        @c_dec(
            param_types=(Param('h', Type('int')), Param('s', Type('int')), Param('v', Type('int'))),
            is_method=True, is_static=True, add_to_class=self
        )
        def _HSV_new(codegen, call_position: Position,
                h: Object, s: Object, v: Object) -> Object:
            _h, _s, _v = f'({h})', f'({s})', f'({v})'
            hsv: TempVar = codegen.create_temp_var(Type('HSV'), call_position)

            codegen.prepend_code(f"""if ({_h} > 360 || {_h} < 0) {{
    {codegen.c_manager.err('\'h\' must be between 0 and 360')}
}}

if ({_s} > 1 || {_s} < 0) {{
    {codegen.c_manager.err('\'s\' must be between 0 and 1')}
}}

if ({_v} > 1 || {_v} < 0) {{
    {codegen.c_manager.err('\'v\' must be between 0 and 1')}
}}

HSV {hsv} = {{ .h = {_h}, .s = {_s}, .v = {_v} }};
""")
            
            return hsv.OBJECT()
        
        @c_dec(
            param_types=(Param('s', Type('string')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _HexTriplet_new(codegen, call_position: Position, s: Object) -> Object:
            strvar: TempVar = codegen.create_temp_var(Type('string'), call_position)
            hex: TempVar = codegen.create_temp_var(Type('HexTriplet'), call_position)
            codegen.prepend_code(f"""string {strvar} = {s};
if (*{strvar} == '#') {strvar}++;
if ({codegen.call('string_length', [Arg(strvar.OBJECT())], call_position)} != 6) {{
    {codegen.c_manager.err('\'hex\' must be a 6 character string')}
}}

HexTriplet {hex} = {{ .hex = {strvar} }};
""")
            
            return hex.OBJECT()
