from codegen.objects import Object, Position, Type
from codegen.c_manager import c_dec


class Button:
    def __init__(self, codegen) -> None:
        codegen.valid_types.append('Button')
        codegen.add_toplevel_code("""#ifndef CURE_UI_H
typedef struct {
    Widget* widget;
} Button;
#endif
""")
        
        def make_255(call_position: Position) -> Object:
            return Object('255', Type('int'), call_position)
    
        @c_dec(add_to_class=self, is_method=True, is_static=True)
        def _Button_type(_, call_position: Position) -> Object:
            return Object('"Button"', Type('string'), call_position)
        
        @c_dec(param_types=('Button',), add_to_class=self, is_method=True)
        def _Button_to_string(_, call_position: Position, _button: Object) -> Object:
            return Object('"class \'Button\'"', Type('string'), call_position)
        
        
        @c_dec(param_types=('Button',), is_property=True, add_to_class=self)
        def _Button_text(_, call_position: Position, button: Object) -> Object:
            return Object(f'(({button}).widget->text)', Type('string'), call_position)
        
        @c_dec(param_types=('Button',), is_property=True, add_to_class=self)
        def _Button_x(_, call_position: Position, button: Object) -> Object:
            return Object(f'(({button}).widget->x)', Type('int'), call_position)
        
        @c_dec(param_types=('Button',), is_property=True, add_to_class=self)
        def _Button_y(_, call_position: Position, button: Object) -> Object:
            return Object(f'(({button}).widget->y)', Type('int'), call_position)
        
        @c_dec(param_types=('Button',), is_property=True, add_to_class=self)
        def _Button_width(_, call_position: Position, button: Object) -> Object:
            return Object(f'(({button}).widget->width)', Type('int'), call_position)
        
        @c_dec(param_types=('Button',), is_property=True, add_to_class=self)
        def _Button_height(_, call_position: Position, button: Object) -> Object:
            return Object(f'(({button}).widget->height)', Type('int'), call_position)
        
        
        @c_dec(
            param_types=('Window', 'int', 'int', 'int', 'int', 'RGB', 'string'),
            is_method=True, is_static=True,
            add_to_class=self
        )
        def _Button_new(codegen, call_position: Position, window: Object, x: Object, y: Object,
                    width: Object, height: Object, color: Object, text: Object) -> Object:
            codegen.use('color', call_position)
            
            widget = codegen.create_temp_var(Type('Widget'), call_position)
            last = codegen.create_temp_var(Type('Widget'), call_position)
            btn = codegen.create_temp_var(Type('Button'), call_position)
            codegen.prepend_code(f"""Widget {widget} = {{
    .type = WIDGET_BUTTON,
    .text = {text.code},
    .x = {x.code},
    .y = {y.code},
    .width = {width.code},
    .height = {height.code},
    .bg_color = RGB(({color.code}).r, ({color.code}).g, ({color.code}).b),
    .on_click = NULL,
    .next = NULL
}};

{widget}.hwnd = CreateWindow(
    "BUTTON", {widget}.text, WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, {widget}.x, {widget}.y,
    {widget}.width, {widget}.height, {window.code}.hwnd, NULL,
    (HINSTANCE)GetWindowLongPtr({window.code}.hwnd, GWLP_HINSTANCE), NULL
);

SetWindowLongPtr({widget}.hwnd, GWLP_USERDATA, (LONG_PTR)&{widget});

if (!{window.code}.widgets) {{
    {window.code}.widgets = (void**)&{widget};
}} else {{
    Widget* {last} = (Widget*){window.code}.widgets;
    while ({last}->next) {last} = (Widget*){last}->next;
    {last}->next = (struct Widget*)&{widget};
}}

Button {btn} = {{ .widget = &{widget} }};
""")
            
            return Object(btn, Type('Button'), call_position)
