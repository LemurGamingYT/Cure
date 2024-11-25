from codegen.objects import Object, Position, Type, TempVar, Param
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec


class color:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type('Color')
        codegen.add_toplevel_code("""#ifndef CURE_COLOR_H
#define CURE_COLOR_H

typedef struct {
    unsigned char r, g, b;
} Color;
#endif
""")
        
        codegen.c_manager.init_class(self, 'Color', Type('Color'))
        codegen.c_manager.wrap_struct_properties('color', Type('Color'), [
            Param('r', Type('int')), Param('g', Type('int')), Param('b', Type('int'))
        ])
        
        
        def create_from_ints(codegen, pos: Position, r: int, g: int, b: int) -> Object:
            return _Color_new(
                codegen, pos, Object(str(r), Type('int'), pos), Object(str(g), Type('int'), pos),
                Object(str(b), Type('int'), pos)
            )
        
        def define_color(name: str, r: int, g: int, b: int) -> None:
            @c_dec(
                is_property=True, is_static=True, add_to_class=self,
                func_name_override=f'Color_{name.upper()}'
            )
            def _(codegen, call_position: Position, r=r, g=g, b=b) -> Object:
                return create_from_ints(codegen, call_position, r, g, b)
        
        
        @c_dec(
            params=(Param('color', Type('Color')),), is_method=True, add_to_class=self
        )
        def _Color_to_string(codegen, call_position: Position, color: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, '"Color(r=%d, g=%d, b=%d)"',
                f'({color}).r', f'({color}).g', f'({color}).b'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        def Color_hex(codegen, call_position: Position, hex: Object) -> Object:
            hexvar: TempVar = codegen.create_temp_var(Type('string'), call_position)
            color: TempVar = codegen.create_temp_var(Type('Color'), call_position)
            r: TempVar = codegen.create_temp_var(Type('string'), call_position)
            g: TempVar = codegen.create_temp_var(Type('string'), call_position)
            b: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""string {hexvar} = {hex};
if (*{hexvar} == '#') {hexvar}++;
if ({codegen.c_manager._string_length(codegen, call_position, hexvar.OBJECT())} != 6) {{
    {codegen.c_manager.err('Invalid hex string %s', str(hexvar.OBJECT()))}
}}

char {r}[] = {{{hexvar}[0], {hexvar}[1], '\\0'}};
char {g}[] = {{{hexvar}[2], {hexvar}[3], '\\0'}};
char {b}[] = {{{hexvar}[4], {hexvar}[5], '\\0'}};

Color {color} = {{.r = atoi({r}), .g = atoi({g}), .b = atoi({b})}};
""")
            
            return color.OBJECT()
    
        @c_dec(
            params=(Param('r', Type('int')), Param('g', Type('int')), Param('b', Type('int'))),
            is_method=True, is_static=True, add_to_class=self, overloads={
                OverloadKey(Type('Color'), (Param('hex', Type('string')),)): OverloadValue(Color_hex)
            }
        )
        def _Color_new(codegen, call_position: Position, r: Object, g: Object, b: Object) -> Object:
            _r, _g, _b = f'({r})', f'({g})', f'({b})'
            color: TempVar = codegen.create_temp_var(Type('Color'), call_position)
            codegen.prepend_code(f"""if ({_r} > 255 || {_r} < 0) {{
    {codegen.c_manager.err('\'r\' must be between 0 and 255')}
}}

if ({_g} > 255 || {_g} < 0) {{
    {codegen.c_manager.err('\'g\' must be between 0 and 255')}
}}

if ({_b} > 255 || {_b} < 0) {{
    {codegen.c_manager.err('\'b\' must be between 0 and 255')}
}}

Color {color} = {{ .r = {_r}, .g = {_g}, .b = {_b} }};
""")

            return color.OBJECT()

        define_color('white', 255, 255, 255)
        define_color('black', 0, 0, 0)
        define_color('blue', 0, 0, 255)
        define_color('red', 255, 0, 0)
        define_color('green', 0, 255, 0)
        define_color('yellow', 255, 255, 0)
        define_color('cyan', 0, 255, 255)
        define_color('magenta', 255, 0, 255)
        define_color('gray', 128, 128, 128)
        define_color('dark_gray', 64, 64, 64)
        define_color('light_gray', 192, 192, 192)
        define_color('orange', 255, 165, 0)
        define_color('purple', 128, 0, 128)
        define_color('brown', 165, 42, 42)
        define_color('pink', 255, 192, 203)
        define_color('maroon', 128, 0, 0)
        define_color('navy', 0, 0, 128)
