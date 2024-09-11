from codegen.objects import Object, Position, Free, Type, EnvItem, TempVar
from codegen.c_manager import c_dec


class Window:
    def __init__(self, codegen) -> None:
        codegen.valid_types.append('Window')
        
        self.window_proc = codegen.get_unique_name()
        codegen.scope.env[self.window_proc] = EnvItem(
            self.window_proc, Type('function'),
            Position(0, 0, '')
        )
    
    
    @c_dec(is_method=True, is_static=True)
    def _Window_type(self, _, call_position: Position, _window: Object) -> Object:
        return Object('"Window"', Type('string'), call_position)
    
    @c_dec(param_types=('Window',), is_method=True)
    def _Window_to_string(self, _, call_position: Position, _window: Object) -> Object:
        return Object('"class \'Window\'"', Type('string'), call_position)
    
    
    @c_dec(param_types=('Window',), is_property=True)
    def _Window_width(self, _, call_position: Position, window: Object) -> Object:
        return Object(f'(({window}).width)', Type('int'), call_position)
    
    @c_dec(param_types=('Window',), is_property=True)
    def _Window_height(self, _, call_position: Position, window: Object) -> Object:
        return Object(f'(({window}).height)', Type('int'), call_position)
    
    @c_dec(param_types=('Window',), is_property=True)
    def _Window_title(self, _, call_position: Position, window: Object) -> Object:
        return Object(f'(({window}).title)', Type('string'), call_position)
    
    @c_dec(param_types=('string', 'int', 'int'), is_method=True, is_static=True)
    def _Window_new(self, codegen, call_position: Position, title: Object, width: Object,
                    height: Object) -> Object:
        window_free = Free(free_name='close_window')
        window: TempVar = codegen.create_temp_var(Type('Window'), call_position, free=window_free)
        window_free.object_name = f'&{window}'
        wc: TempVar = codegen.create_temp_var(Type('WNDCLASS'), call_position)
        codegen.prepend_code(f"""Window {window} = {{
    .title = {title},
    .width = {width},
    .height = {height},
    .widgets = NULL
}};

WNDCLASS {wc} = {{0}};
{wc}.lpfnWndProc = {self.window_proc};
{wc}.hInstance = GetModuleHandle(NULL);
{wc}.lpszClassName = "Window";
RegisterClass(&{wc});

({window}).hwnd = CreateWindowEx(
    0, {wc}.lpszClassName, ({window}).title, WS_OVERLAPPEDWINDOW,
    CW_USEDEFAULT, CW_USEDEFAULT, ({window}).width, ({window}).height,
    NULL, NULL, {wc}.hInstance, NULL
);

SetWindowLongPtr(({window}).hwnd, GWLP_USERDATA, (LONG_PTR)&({window}));
""")
        
        return window.OBJECT()
    
    @c_dec(param_types=('Window',), is_method=True)
    def _Window_run(self, codegen, call_position: Position, window: Object) -> Object:
        msg: TempVar = codegen.create_temp_var(Type('MSG'), call_position)
        codegen.prepend_code(f"""ShowWindow({window.code}.hwnd, SW_SHOW);
MSG {msg} = {{0}};
while (GetMessage(&{msg}, NULL, 0, 0)) {{
    TranslateMessage(&{msg});
    DispatchMessage(&{msg});
}}
""")
        
        return Object.NULL(call_position)
