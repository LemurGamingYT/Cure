from cure.objects import Object, Position, Type
from cure.std.color.rgb import RGB
from cure.std.color.hsv import HSV
from cure.c_manager import c_dec


class color:
    def __init__(self, compiler) -> None:
        self.rgb = RGB(compiler)
        self.hsv = HSV(compiler)
        
        compiler.valid_types.extend(('RGB', 'HSV'))
        
        compiler.c_manager.add_objects(self.rgb, self)
        compiler.c_manager.add_objects(self.hsv, self)
    
    @c_dec(
        param_types=('int', 'int', 'int'),
        is_method=True,
        is_static=True
    )
    def _RGB_new(self, compiler, call_position: Position,
             r: Object, g: Object, b: Object) -> Object:
        _r = f'({r.code})'
        _g = f'({g.code})'
        _b = f'({b.code})'
        
        cls = compiler.create_temp_var(Type('RGB'), call_position)
        compiler.prepend_code(f"""if ({_r} > 255 || {_r} < 0) {{
    {compiler.c_manager.err('\'r\' must be between 0 and 255')}
}}

if ({_g} > 255 || {_g} < 0) {{
    {compiler.c_manager.err('\'g\' must be between 0 and 255')}
}}

if ({_b} > 255 || {_b} < 0) {{
    {compiler.c_manager.err('\'b\' must be between 0 and 255')}
}}

RGB {cls};
{cls}.r = {_r};
{cls}.g = {_g};
{cls}.b = {_b};
""")

        return Object(cls, Type('RGB'), call_position)
    
    @c_dec(
        param_types=('int', 'int', 'int'),
        is_method=True,
        is_static=True
    )
    def _HSV_new(self, compiler, call_position: Position,
             h: Object, s: Object, v: Object) -> Object:
        _h = f'({h.code})'
        _s = f'({s.code})'
        _v = f'({v.code})'

        cls = compiler.create_temp_var(Type('HSV'), call_position)
        compiler.prepend_code(f"""if ({_h} > 360 || {_h} < 0) {{
    {compiler.c_manager.err('\'h\' must be between 0 and 360')}
}}

if ({_s} > 1 || {_s} < 0) {{
    {compiler.c_manager.err('\'s\' must be between 0 and 1')}
}}

if ({_v} > 1 || {_v} < 0) {{
    {compiler.c_manager.err('\'v\' must be between 0 and 1')}
}}

HSV {cls};
{cls}.h = {_h};
{cls}.s = {_s};
{cls}.v = {_v};
""")
        
        return Object(cls, Type('HSV'), call_position)
