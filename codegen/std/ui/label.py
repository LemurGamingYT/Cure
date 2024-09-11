from codegen.objects import Object, Position, Type, TempVar
from codegen.c_manager import c_dec


class Label:
    def __init__(self, codegen) -> None:
        codegen.valid_types.append('Label')
        codegen.add_toplevel_code("""#ifndef CURE_UI_H
typedef struct {
    Widget* widget;
} Label;
#endif
""")
    
        def make_255(call_position: Position) -> Object:
            return Object('255', Type('int'), call_position)
    
        @c_dec(add_to_class=self, is_method=True, is_static=True)
        def _Label_type(_, call_position: Position) -> Object:
            return Object('"Label"', Type('string'), call_position)
        
        @c_dec(param_types=('Label',), add_to_class=self, is_method=True)
        def _Label_to_string(_, call_position: Position, _Label: Object) -> Object:
            return Object('"class \'Label\'"', Type('string'), call_position)
        
        
        @c_dec(param_types=('Label',), is_property=True, add_to_class=self)
        def _Label_text(_, call_position: Position, label: Object) -> Object:
            return Object(f'(({label}).widget->text)', Type('string'), call_position)
        
        @c_dec(param_types=('Label',), is_property=True, add_to_class=self)
        def _Label_x(_, call_position: Position, label: Object) -> Object:
            return Object(f'(({label}).widget->x)', Type('int'), call_position)
        
        @c_dec(param_types=('Label',), is_property=True, add_to_class=self)
        def _Label_y(_, call_position: Position, label: Object) -> Object:
            return Object(f'(({label}).widget->y)', Type('int'), call_position)
        
        @c_dec(param_types=('Label',), is_property=True, add_to_class=self)
        def _Label_width(_, call_position: Position, label: Object) -> Object:
            return Object(f'(({label}).widget->width)', Type('int'), call_position)
        
        @c_dec(param_types=('Label',), is_property=True, add_to_class=self)
        def _Label_height(_, call_position: Position, label: Object) -> Object:
            return Object(f'(({label}).widget->height)', Type('int'), call_position)
        
        
        @c_dec(
            param_types=('Window', 'int', 'int', 'int', 'int', 'RGB', 'string'),
            is_method=True, is_static=True,
            add_to_class=self
        )
        def _Label_new(codegen, call_position: Position, window: Object, x: Object, y: Object,
                    width: Object, height: Object, color: Object, text: Object) -> Object:
            codegen.use('color', call_position)
            
            widget: TempVar = codegen.create_temp_var(Type('Widget'), call_position)
            label: TempVar = codegen.create_temp_var(Type('Label'), call_position)
            last: TempVar = codegen.create_temp_var(Type('Widget'), call_position)
            codegen.prepend_code(f"""Widget {widget} = {{
    .type = WIDGET_LABEL,
    .text = {text},
    .x = {x},
    .y = {y},
    .width = {width},
    .height = {height},
    .bg_color = RGB(({color}).r, ({color}).g, ({color}).b),
    .on_click = NULL,
    .next = NULL
}};

{widget}.hwnd = CreateWindow(
    "STATIC", {widget}.text, WS_CHILD | WS_VISIBLE | SS_LEFT, {widget}.x, {widget}.y,
    {widget}.width, {widget}.height, ({window}).hwnd, NULL,
    (HINSTANCE)GetWindowLongPtr(({window}).hwnd, GWLP_HINSTANCE), NULL
);

SetWindowLongPtr({widget}.hwnd, GWLP_USERDATA, (LONG_PTR)&{widget});

if (!({window}).widgets) {{
    ({window}).widgets = (void**)&{widget};
}} else {{
    Widget* {last} = (Widget*)({window}).widgets;
    while ({last}->next) {last} = (Widget*){last}->next;
    {last}->next = (struct Widget*)&{widget};
}}

Label {label} = {{ .widget = &{widget} }};
""")
            
            return label.OBJECT()
