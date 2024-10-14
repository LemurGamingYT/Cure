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
        
        
        @c_dec(
            param_types=(Param('color', Type('Color')),), is_method=True, add_to_class=self
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
    {codegen.c_manager.err('Invalid hex string %s', hexvar.OBJECT())}
}}

static char {r}[3];
{r}[0] = {hexvar}[0];
{r}[1] = {hexvar}[1];
{r}[2] = '\\0';
static char {g}[3];
{g}[0] = {hexvar}[2];
{g}[1] = {hexvar}[3];
{g}[2] = '\\0';
static char {b}[3];
{b}[0] = {hexvar}[4];
{b}[1] = {hexvar}[5];
{b}[2] = '\\0';

Color {color} = {{
    .r = (unsigned char)strtol({r}), .g = (unsigned char)strtol({g}), .g = (unsigned char)strtol({b})
}};
""")
            
            return color.OBJECT()
    
        @c_dec(
            param_types=(Param('r', Type('int')), Param('g', Type('int')), Param('b', Type('int'))),
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
