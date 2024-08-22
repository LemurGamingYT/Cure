from cure.objects import Object, Position, Type
from cure.c_manager import c_dec


class Button:
    def __init__(self, compiler) -> None:
        compiler.valid_types.append('Button')
        compiler.add_toplevel_code("""typedef struct {
    Widget* widget;
} Button;
""")
        
        def make_255(call_position: Position) -> Object:
            return Object('255', Type('int'), call_position)
    
        @c_dec(add_to_class=self)
        def _Button_type(_, call_position: Position) -> Object:
            return Object('"Button"', Type('string'), call_position)
        
        @c_dec(param_types=('Button',), add_to_class=self)
        def _Button_to_string(_, call_position: Position, _button: Object) -> Object:
            return Object('"class \'Button\'"', Type('string'), call_position)
        
        
        def only_parent(compiler, call_position: Position, window: Object) -> Object:
            return self._Button_new(
                compiler, call_position, window,
                Object('350', Type('int'), call_position), Object('200', Type('int'), call_position),
                Object('150', Type('int'), call_position), Object('30', Type('int'), call_position),
                compiler.call('RGB_new', [make_255(call_position), make_255(call_position),
                                          make_255(call_position)], call_position),
                Object('"Button"', 'string', call_position)
            )
        
        def with_text(compiler, call_position: Position, window: Object,
                            text: Object) -> Object:
            return self._Button_new(
                compiler, call_position, window,
                Object('350', Type('int'), call_position), Object('200', Type('int'), call_position),
                Object('150', Type('int'), call_position), Object('30', Type('int'), call_position),
                compiler.call('RGB_new', [make_255(call_position), make_255(call_position),
                                          make_255(call_position)], call_position), text
            )
        
        def text_and_color(compiler, call_position: Position,  window: Object,
                            color: Object, text: Object) -> Object:
            return self._Button_new(
                compiler, call_position, window,
                Object('350', Type('int'), call_position), Object('200', Type('int'), call_position),
                Object('150', Type('int'), call_position), Object('30', Type('int'), call_position),
                color, text
            )
        
        def with_color(compiler, call_position: Position, window: Object,
                    color: Object) -> Object:
            return self._Button_new(
                compiler, call_position, window,
                Object('350', Type('int'), call_position), Object('200', Type('int'), call_position),
                Object('150', Type('int'), call_position), Object('30', Type('int'), call_position),
                color, Object('"Button"', Type('string'), call_position)
            )
        
        @c_dec(
            param_types=('Window', 'int', 'int', 'int', 'int', 'RGB', 'string'),
            is_method=True, is_static=True,
            overloads={
                (('Window',), 'Button'): only_parent,
                (('Window', 'string'), 'Button'): with_text,
                (('Window', 'RGB', 'string'), 'Button'): text_and_color,
                (('Window', 'RGB'), 'Button'): with_color
            },
            add_to_class=self
        )
        def _Button_new(compiler, call_position: Position, window: Object, x: Object, y: Object,
                    width: Object, height: Object, color: Object, text: Object) -> Object:
            compiler.use('color', call_position)
            
            widget = compiler.create_temp_var(Type('Widget'), call_position)
            button = compiler.create_temp_var(Type('Button'), call_position)
            last = compiler.create_temp_var(Type('Widget'), call_position)
            compiler.prepend_code(f"""Widget {widget};
{widget}.type = WIDGET_BUTTON;
{widget}.text = {text.code};
{widget}.x = {x.code};
{widget}.y = {y.code};
{widget}.width = {width.code};
{widget}.height = {height.code};
{widget}.bg_color = RGB(({color.code}).r, ({color.code}).g, ({color.code}).b);
{widget}.on_click = NULL;
{widget}.next = NULL;

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

Button {button};
{button}.widget = &{widget};
""")
            
            return Object(button, Type('Button'), call_position)
