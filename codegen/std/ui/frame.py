from codegen.objects import Object, Position, Type
from codegen.c_manager import c_dec


class Frame:
    def __init__(self, compiler) -> None:
        compiler.valid_types.append('Frame')
        compiler.add_toplevel_code("""typedef struct {
    Widget* widget;
} Frame;
""")
        
        def make_255(call_position: Position) -> Object:
            return Object('255', Type('int'), call_position)
    
        @c_dec(add_to_class=self)
        def _Frame_type(_, call_position: Position) -> Object:
            return Object('"Frame"', Type('string'), call_position)
        
        @c_dec(param_types=('Frame',), add_to_class=self)
        def _Frame_to_string(_, call_position: Position, _Frame: Object) -> Object:
            return Object('"class \'Frame\'"', Type('string'), call_position)
        
        
        def only_parent(compiler, call_position: Position, window: Object) -> Object:
            return _Frame_new(
                compiler, call_position, window,
                Object('350', Type('int'), call_position), Object('200', Type('int'), call_position),
                Object('150', Type('int'), call_position), Object('30', Type('int'), call_position),
                compiler.call(
                    'RGB_new',
                    [make_255(call_position), make_255(call_position), make_255(call_position)],
                    call_position
                )
            )
        
        def with_color(compiler, call_position: Position, window: Object,
                    color: Object) -> Object:
            return _Frame_new(
                compiler, call_position, window,
                Object('350', Type('int'), call_position), Object('200', Type('int'), call_position),
                Object('150', Type('int'), call_position), Object('30', Type('int'), call_position),
                color
            )
        
        @c_dec(
            param_types=('Window', 'int', 'int', 'int', 'int', 'RGB'),
            is_method=True, is_static=True,
            overloads={
                (('Window',), 'Frame'): only_parent,
                (('Window', 'RGB'), 'Frame'): with_color
            },
            add_to_class=self
        )
        def _Frame_new(compiler, call_position: Position, window: Object, x: Object, y: Object,
                    width: Object, height: Object, color: Object) -> Object:
            compiler.use('color', call_position)
            
            widget = compiler.create_temp_var(Type('Widget'), call_position)
            frame = compiler.create_temp_var(Type('Frame'), call_position)
            last = compiler.create_temp_var(Type('Widget'), call_position)
            compiler.prepend_code(f"""Widget {widget};
{widget}.type = WIDGET_FRAME;
{widget}.text = NULL;
{widget}.x = {x.code};
{widget}.y = {y.code};
{widget}.width = {width.code};
{widget}.height = {height.code};
{widget}.bg_color = RGB(({color.code}).r, ({color.code}).g, ({color.code}).b);
{widget}.on_click = NULL;
{widget}.next = NULL;

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

Frame {frame};
{frame}.widget = &{widget};
""")
            
            return Object(frame, Type('Frame'), call_position)
