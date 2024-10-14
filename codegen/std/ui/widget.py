from enum import Enum

from codegen.objects import Object, Position, Type, Param, TempVar
from codegen.std.threads.thread import get_function_info
from codegen.c_manager import c_dec


class WidgetType(Enum):
    LABEL = Type('Label')
    BUTTON = Type('Button')
    FRAME = Type('Frame')


class Widget:
    def __init__(self, codegen) -> None:
        codegen.c_manager.reserve('Widget')
        codegen.add_toplevel_code("""typedef struct {
    HWND hwnd;
    unsigned char type;
    const string text;
    int width, height, x, y;
    nil (*clicked)(void);
    struct Window* parent;
    struct Widget* next;
    Color bg_color;
    Color text_color;
    Font* font;
    bool is_placed;
} Widget;
""")
    
    def correct_kwargs(self, kwargs: dict, _: WidgetType) -> None:
        if (font := kwargs.get('font')) is not None:
            kwargs['font'].code = f'&({font})'
    
    def get_create_window_args(self, codegen, type: WidgetType, pos: Position, **kwargs) -> list[str]:
        parent = kwargs['parent']
        x, y, width, height = kwargs['x'], kwargs['y'], kwargs['width'], kwargs['height']
        if type == WidgetType.LABEL:
            return [
                '"STATIC"', str(kwargs['text']),
                'WS_VISIBLE | WS_CHILD | SS_CENTER | SS_CENTERIMAGE',
                f'{x} - ({width}) / 2', f'{y} - ({height}) / 2',
                str(width), str(height),
                f'({parent}).hwnd', 'NULL', 'GetModuleHandle(NULL)', 'NULL'
            ]
        elif type == WidgetType.BUTTON:
            self.validate_clicked_function(kwargs['clicked'], codegen, pos)
            return [
                '"BUTTON"', str(kwargs['text']),
                'WS_CHILD | WS_VISIBLE | BS_OWNERDRAW',
                f'{x} - ({width}) / 2', f'{y} - ({height}) / 2',
                str(width), str(height),
                f'({parent}).hwnd', 'NULL', 'GetModuleHandle(NULL)', 'NULL'
            ]
        elif type == WidgetType.FRAME:
            return [
                '"STATIC"', '""', 'WS_VISIBLE | WS_CHILD | SS_CENTER | SS_CENTERIMAGE',
                f'{x} - ({width}) / 2', f'{y} - ({height}) / 2',
                str(width), str(height),
                f'({parent}).hwnd', 'NULL', 'GetModuleHandle(NULL)', 'NULL'
            ]
        else:
            pos.error_here('Unsupported widget type')
    
    def create_widget(self, codegen, type: WidgetType, pos: Position, **kwargs) -> Object:
        object_type = type.value
        obj: TempVar = codegen.create_temp_var(object_type, pos)
        widget: TempVar = codegen.create_temp_var(Type('Widget'), pos)
        current: TempVar = codegen.create_temp_var(Type('Widget'), pos)
        self.correct_kwargs(kwargs, type)
        parent = kwargs['parent']
        
        object_name = object_type.type.lower()
        fields: list[Param] = []
        for k, v in kwargs.items():
            field_type: Type = v.type
            fields.append(Param(k, field_type))
        
        codegen.c_manager.wrap_struct_properties(
            object_name, object_type, fields, sub_field='widget->'
        )
        
        self.set_widget_attributes(codegen, object_name, object_type, type, **kwargs)
        kwargs['parent'] = f'(struct Window*)&({parent})'
        codegen.prepend_code(f"""Widget {widget} = {{
    .hwnd = NULL, .is_placed = false, .next = NULL,
    {', '.join(f'.{k} = {v}' for k, v in kwargs.items())}
}};

if (({parent}).head == NULL) {{
    ({parent}).head = &{widget};
}} else {{
    Widget* {current} = ({parent}).head;
    while ({current}->next != NULL) {{
        {current} = (Widget*){current}->next;
    }}
    
    {current}->next = (struct Widget*)&{widget};
}}

{object_type} {obj} = {{ .widget = &{widget} }};
""")
        
        return obj.OBJECT()
    
    def validate_clicked_function(self, clicked: Object, codegen, pos: Position) -> None:
        if str(clicked) == 'NULL':
            return
        
        func = get_function_info(str(clicked), codegen, pos)
        if func.return_type != Type('nil'):
            clicked.position.error_here('Button clicked function must return nil')
        
        if len(func.params) > 0:
            clicked.position.error_here('Button clicked function can\'t have any parameters')
        
        if len(func.generic_params) > 0:
            clicked.position.error_here(
                'Button clicked function can\'t have any generic parameters'
            )
    
    def delete(self, widget: Object | str) -> str:
        return f"""DestroyWindow({widget}->hwnd);
if ({widget}->font != NULL) {{
    DeleteObject({widget}->font->hFont);
}}
"""

    def set_widget_attributes(
        self, codegen, widget_name: str, widget_type: Type, type: WidgetType, **kwargs
    ) -> None:
        @c_dec(
            param_types=(
                Param(widget_name, widget_type), Param('x', Type('int')),
                Param('y', Type('int'))
            ), is_method=True, add_to_class=codegen.c_manager,
            func_name_override=f'{widget_type.c_type}_place'
        )
        def place(codegen, call_position: Position, widget: Object, x: Object, y: Object) -> Object:
            CreateWindow_args: list[str] = self.get_create_window_args(
                codegen, type, call_position, **kwargs, x=x, y=y
            )
            
            w = f'({widget}).widget'
            codegen.prepend_code(f"""if (!{w}->is_placed) {{
    {w}->hwnd = CreateWindow({', '.join(CreateWindow_args)});
    if ({w}->hwnd == NULL) {{
        {codegen.c_manager.err('Failed to create widget')}
    }}

    if ({w}->font != NULL) {{
        SendMessage({w}->hwnd, WM_SETFONT, (WPARAM){w}->font->hFont, TRUE);
    }}

    SetWindowLongPtr({w}->hwnd, GWLP_USERDATA, (LONG_PTR){w});
    {w}->is_placed = true;
}}
""")
            
            return Object.NULL(call_position)
