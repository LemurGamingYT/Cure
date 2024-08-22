from cure.objects import Object, Position, Type
from cure.c_manager import c_dec


class Label:
    def __init__(self, compiler) -> None:
        compiler.valid_types.append('Label')
        compiler.add_toplevel_code("""typedef struct {
    Widget* widget;
} Label;
""")
    
        def make_255(call_position: Position) -> Object:
            return Object('255', Type('int'), call_position)
    
        @c_dec(add_to_class=self)
        def _Label_type(_, call_position: Position) -> Object:
            return Object('"Label"', Type('string'), call_position)
        
        @c_dec(param_types=('Label',), add_to_class=self)
        def _Label_to_string(_, call_position: Position, _Label: Object) -> Object:
            return Object('"class \'Label\'"', Type('string'), call_position)
        
        
        def only_parent(compiler, call_position: Position, window: Object) -> Object:
            return self._Label_new(
                compiler, call_position, window,
                Object('350', Type('int'), call_position), Object('200', Type('int'), call_position),
                Object('150', Type('int'), call_position), Object('30', Type('int'), call_position),
                compiler.call('RGB_new', [make_255(call_position), make_255(call_position),
                                          make_255(call_position)], call_position),
                Object('"Label"', 'string', call_position)
            )
        
        def with_text(compiler, call_position: Position, window: Object,
                            text: Object) -> Object:
            return self._Label_new(
                compiler, call_position, window,
                Object('350', Type('int'), call_position), Object('200', Type('int'), call_position),
                Object('150', Type('int'), call_position), Object('30', Type('int'), call_position),
                compiler.call('RGB_new', [make_255(call_position), make_255(call_position),
                                          make_255(call_position)], call_position), text
            )
        
        def text_and_color(compiler, call_position: Position,  window: Object,
                            color: Object, text: Object) -> Object:
            return self._Label_new(
                compiler, call_position, window,
                Object('350', Type('int'), call_position), Object('200', Type('int'), call_position),
                Object('150', Type('int'), call_position), Object('30', Type('int'), call_position),
                color, text
            )
        
        def with_color(compiler, call_position: Position, window: Object,
                    color: Object) -> Object:
            return self._Label_new(
                compiler, call_position, window,
                Object('350', Type('int'), call_position), Object('200', Type('int'), call_position),
                Object('150', Type('int'), call_position), Object('30', Type('int'), call_position),
                color, Object('"Label"', Type('string'), call_position)
            )
        
        @c_dec(
            param_types=('Window', 'int', 'int', 'int', 'int', 'RGB', 'string'),
            is_method=True, is_static=True,
            overloads={
                (('Window',), 'Label'): only_parent,
                (('Window', 'string'), 'Label'): with_text,
                (('Window', 'RGB', 'string'), 'Label'): text_and_color,
                (('Window', 'RGB'), 'Label'): with_color
            },
            add_to_class=self
        )
        def _Label_new(compiler, call_position: Position, window: Object, x: Object, y: Object,
                    width: Object, height: Object, color: Object, text: Object) -> Object:
            compiler.use('color', call_position)
            
            widget = compiler.create_temp_var(Type('Widget'), call_position)
            label = compiler.create_temp_var(Type('Label'), call_position)
            last = compiler.create_temp_var(Type('Widget'), call_position)
            compiler.prepend_code(f"""Widget {widget};
{widget}.type = WIDGET_LABEL;
{widget}.text = {text.code};
{widget}.x = {x.code};
{widget}.y = {y.code};
{widget}.width = {width.code};
{widget}.height = {height.code};
{widget}.bg_color = RGB(({color.code}).r, ({color.code}).g, ({color.code}).b);
{widget}.on_click = NULL;
{widget}.next = NULL;

{widget}.hwnd = CreateWindow(
    "STATIC", {widget}.text, WS_CHILD | WS_VISIBLE | SS_LEFT, {widget}.x, {widget}.y,
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

Label {label};
{label}.widget = &{widget};
""")
            
            return Object(label, Type('Label'), call_position)
        
        @c_dec(param_types=('Label',), is_property=True)
        def _Label_text(_, call_position: Position, label: Object) -> Object:
            return Object(f'({label.code}.widget->text)', Type('string'), call_position)
