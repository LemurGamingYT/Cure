from cure.objects import Object, Position, Free, Type, EnvItem
from cure.c_manager import c_dec


class Window:
    def __init__(self, compiler) -> None:
        compiler.valid_types.append('Window')
        
        self.window_proc = compiler.get_unique_name()
        compiler.scope.env[self.window_proc] = EnvItem(
            self.window_proc, Type('function'),
            Position(0, 0, '')
        )
    
    
    @c_dec()
    def _Window_type(self, _, call_position: Position, _window: Object) -> Object:
        return Object('"Window"', Type('string'), call_position)
    
    @c_dec(param_types=('Window',))
    def _Window_to_string(self, _, call_position: Position, _window: Object) -> Object:
        return Object('"class \'Window\'"', Type('string'), call_position)
    
    
    @c_dec(param_types=('string', 'int', 'int'), is_method=True, is_static=True)
    def _Window_new(self, compiler, call_position: Position, title: Object, width: Object,
                    height: Object) -> Object:
        window_free = Free()
        window = compiler.create_temp_var(Type('Window'), call_position, free=window_free)
        window_free.object_name = '&' + window
        window_free.free_name = 'close_window'
        wc = compiler.create_temp_var(Type('WNDCLASS'), call_position)
        compiler.prepend_code(f"""Window {window};
{window}.title = {title.code};
{window}.width = {width.code};
{window}.height = {height.code};
{window}.widgets = NULL;

WNDCLASS {wc} = {{0}};
{wc}.lpfnWndProc = {self.window_proc};
{wc}.hInstance = GetModuleHandle(NULL);
{wc}.lpszClassName = "Window";
RegisterClass(&{wc});

{window}.hwnd = CreateWindowEx(
    0, {wc}.lpszClassName, {window}.title, WS_OVERLAPPEDWINDOW,
    CW_USEDEFAULT, CW_USEDEFAULT, {window}.width, {window}.height,
    NULL, NULL, {wc}.hInstance, NULL
);

SetWindowLongPtr({window}.hwnd, GWLP_USERDATA, (LONG_PTR)(&{window}));
""")
        
        return Object(window, Type('Window'), call_position, free=window_free)
    
    @c_dec(param_types=('Window',), is_method=True)
    def _Window_run(self, compiler, call_position: Position, window: Object) -> Object:
        msg = compiler.create_temp_var(Type('MSG'), call_position)
        compiler.prepend_code(f"""ShowWindow({window.code}.hwnd, SW_SHOW);
MSG {msg} = {{0}};
while (GetMessage(&{msg}, NULL, 0, 0)) {{
    TranslateMessage(&{msg});
    DispatchMessage(&{msg});
}}
""")
        
        return Object('NULL', Type('nil'), call_position)
