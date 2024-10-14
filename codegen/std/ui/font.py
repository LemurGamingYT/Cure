from codegen.objects import Object, Position, Type, Param, TempVar
from codegen.c_manager import c_dec


class Font:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""typedef struct {
    HFONT hFont;
    string name;
    int size;
    int weight;
} Font;
""")
        
        codegen.type_checker.add_type('Font')
        codegen.c_manager.init_class(self, 'Font', Type('Font'))
        codegen.c_manager.wrap_struct_properties('font', Type('Font'), [
            Param('name', Type('string')), Param('size', Type('int')), Param('weight', Type('int'))
        ])
        
        @c_dec(
            param_types=(
                Param('name', Type('string'), default=Object('"Segoe UI"', Type('string'))),
                Param('size', Type('int'), default=Object('12', Type('int'))),
                Param('is_bold', Type('bool'), default=Object('false', Type('bool')))
            ), is_method=True, is_static=True, add_to_class=self
        )
        def _Font_new(codegen, call_position: Position, name: Object, size: Object,
                      is_bold: Object) -> Object:
            font: TempVar = codegen.create_temp_var(Type('Font'), call_position)
            codegen.prepend_code(f"""Font {font} = {{
    .hFont = CreateFont(
        {size}, 0, 0, 0, {is_bold} ? FW_BOLD : FW_NORMAL, FALSE, FALSE, FALSE, ANSI_CHARSET,
        OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY, DEFAULT_PITCH | FF_DONTCARE,
        {name}
    ), .name = {name}, .size = {size}, .weight = {is_bold} ? FW_BOLD : FW_NORMAL
}};
""")
            
            return font.OBJECT()
