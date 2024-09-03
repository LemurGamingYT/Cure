from codegen.objects import Object, Position, Type
from codegen.c_manager import c_dec


class Frame:
    def __init__(self, codegen) -> None:
        codegen.valid_types.append('Frame')
        codegen.add_toplevel_code("""#ifndef CURE_UI_H
typedef struct {
    Widget* widget;
} Frame;
#endif
""")
        
        def make_255(call_position: Position) -> Object:
            return Object('255', Type('int'), call_position)
    
        @c_dec(add_to_class=self, is_method=True, is_static=True)
        def _Frame_type(_, call_position: Position) -> Object:
            return Object('"Frame"', Type('string'), call_position)
        
        @c_dec(param_types=('Frame',), add_to_class=self, is_method=True)
        def _Frame_to_string(_, call_position: Position, _Frame: Object) -> Object:
            return Object('"class \'Frame\'"', Type('string'), call_position)

        
        @c_dec(param_types=('Frame',), is_property=True, add_to_class=self)
        def _Frame_x(_, call_position: Position, frame: Object) -> Object:
            return Object(f'(({frame}).widget->x)', Type('int'), call_position)
        
        @c_dec(param_types=('Frame',), is_property=True, add_to_class=self)
        def _Frame_y(_, call_position: Position, frame: Object) -> Object:
            return Object(f'(({frame}).widget->y)', Type('int'), call_position)
        
        @c_dec(param_types=('Frame',), is_property=True, add_to_class=self)
        def _Frame_width(_, call_position: Position, frame: Object) -> Object:
            return Object(f'(({frame}).widget->width)', Type('int'), call_position)
        
        @c_dec(param_types=('Frame',), is_property=True, add_to_class=self)
        def _Frame_height(_, call_position: Position, frame: Object) -> Object:
            return Object(f'(({frame}).widget->height)', Type('int'), call_position)

        
        @c_dec(
            param_types=('Window', 'int', 'int', 'int', 'int', 'RGB'),
            is_method=True, is_static=True,
            add_to_class=self
        )
        def _Frame_new(codegen, call_position: Position, window: Object, x: Object, y: Object,
                    width: Object, height: Object, color: Object) -> Object:
            codegen.use('color', call_position)
            
            widget = codegen.create_temp_var(Type('Widget'), call_position)
            frame = codegen.create_temp_var(Type('Frame'), call_position)
            last = codegen.create_temp_var(Type('Widget'), call_position)
            codegen.prepend_code(f"""Widget {widget} = {{
    .type = WIDGET_FRAME,
    .text = NULL,
    .x = {x.code},
    .y = {y.code},
    .width = {width.code},
    .height = {height.code},
    .bg_color = RGB(({color.code}).r, ({color.code}).g, ({color.code}).b);
    .on_click = NULL,
    .next = NULL
}};

{widget}.hwnd = CreateWindow(
    "BUTTON", {widget}.text, WS_CHILD | WS_VISIBLE | BS_GROUPBOX, {widget}.x, {widget}.y,
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

Frame {frame} = {{ .widget = &{widget} }};
""")
            
            return Object(frame, Type('Frame'), call_position)
