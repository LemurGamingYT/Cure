from codegen.objects import Object, Position, Type, TempVar, Param, Free
from codegen.c_manager import c_dec


class Window:
    def __init__(self, codegen, widget) -> None:
        codegen.type_checker.add_type('Window')
        codegen.add_toplevel_code("""typedef struct {
    HWND hwnd;
    Widget* head;
    int width, height;
    const string title;
    Color background;
    bool resizable;
} Window;
""")
        
        self.widget = widget
        
        codegen.c_manager.init_class(self, 'Window', Type('Window'))
        codegen.c_manager.wrap_struct_properties('window', Type('Window'), [
            Param('width', Type('int')), Param('height', Type('int')), Param('title', Type('string')),
            Param('background', Type('Color'))
        ])
        
        @c_dec(
            param_types=(Param('window', Type('Window')),), is_method=True, add_to_class=self
        )
        def _Window_run(codegen, call_position: Position, window: Object) -> Object:
            msg: TempVar = codegen.create_temp_var(Type('MSG'), call_position)
            codegen.prepend_code(f"""ShowWindow(({window}).hwnd, SW_SHOW);
MSG {msg} = {{0}};
while (GetMessage(&{msg}, NULL, 0, 0)) {{
    TranslateMessage(&{msg});
    DispatchMessage(&{msg});
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(
                Param('title', Type('string'), default=Object('"Window"', Type('string'))),
                Param('width', Type('int'), default=Object('800', Type('int'))),
                Param('height', Type('int'), default=Object('600', Type('int'))),
                Param('background', Type('Color'), default=Object(
                    '(Color){255, 255, 255}', Type('Color'))),
                Param('resizable', Type('bool'), default=Object('true', Type('bool')))
            ),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Window_new(codegen, call_position: Position, *args) -> Object:
            kwargs = _Window_new.get_kwargs(args)
            title, width, height = kwargs['title'], kwargs['width'], kwargs['height']
            window_destroy: TempVar = codegen.create_temp_var(Type('function'), call_position)
            codegen.add_toplevel_code(f"""void {window_destroy}(Window* window) {{
    if (window != NULL) {{
        for (Widget* widget = window->head; widget != NULL; widget = (Widget*)widget->next) {{
            {self.widget.delete('widget')}
        }}
        
        DestroyWindow(window->hwnd);
    }}
}}
""")
            
            window_proc: TempVar = codegen.create_temp_var(Type('function'), call_position)
            codegen.add_toplevel_code(f"""LRESULT CALLBACK {window_proc}(
    HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam
) {{
    Window* window = (Window*)GetWindowLongPtr(hwnd, GWLP_USERDATA);
    switch (uMsg) {{
    case WM_CTLCOLORSTATIC: {{
            HDC hdc = (HDC)wParam;
            Widget* widget = (Widget*)GetWindowLongPtr((HWND)lParam, GWLP_USERDATA);
            if (widget != NULL) {{
                Color background = widget->bg_color;
                Color text_color = widget->text_color;
                SetBkColor(hdc, RGB(background.r, background.g, background.b));
                SetTextColor(hdc, RGB(text_color.r, text_color.g, text_color.b));
                return (INT_PTR)CreateSolidBrush(RGB(background.r, background.g, background.b));
            }}
        }} break;
    case WM_DRAWITEM: {{
            LPDRAWITEMSTRUCT pdis = (LPDRAWITEMSTRUCT)lParam;
            if (pdis->CtlType == ODT_BUTTON) {{
                Widget* widget = (Widget*)GetWindowLongPtr(pdis->hwndItem, GWLP_USERDATA);
                if (widget != NULL) {{
                    HDC hdc = pdis->hDC;
                    Color bg_color = widget->bg_color;
                    Color text_color = widget->text_color;
                    SetBkColor(hdc, RGB(bg_color.r, bg_color.g, bg_color.b));
                    HBRUSH brush = CreateSolidBrush(RGB(bg_color.r, bg_color.g, bg_color.b));
                    FillRect(hdc, &pdis->rcItem, brush);
                    DeleteObject(brush);
                    
                    SetTextColor(hdc, RGB(text_color.r, text_color.g, text_color.b));
                    int len = GetWindowTextLength(pdis->hwndItem);
                    char* text = (char*)malloc(len + 1);
                    {codegen.c_manager.buf_check('text')}
                    
                    GetWindowText(pdis->hwndItem, text, len + 1);
                    DrawText(hdc, text, len, &pdis->rcItem, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
                    free(text);
                    return TRUE;
                }}
            }}
        }} break;
    case WM_PAINT: {{
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            Color background = window->background;
            SetBkColor(hdc, RGB(background.r, background.g, background.b));
            
            RECT rect;
            GetClientRect(hwnd, &rect);
            ExtTextOut(hdc, 0, 0, ETO_OPAQUE, &rect, NULL, 0, NULL);
            EndPaint(hwnd, &ps);
        }} break;
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    case WM_COMMAND:
        if (HIWORD(wParam) == BN_CLICKED) {{
            Widget* widget = (Widget*)GetWindowLongPtr((HWND)lParam, GWLP_USERDATA);
            if (widget != NULL && widget->clicked != NULL) {{
                widget->clicked();
            }}
        }}
        break;
    }}
    
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}}
""")
            
            wc: TempVar = codegen.create_temp_var(Type('WNDCLASS'), call_position)
            window_free = Free(free_name=str(window_destroy))
            window: TempVar = codegen.create_temp_var(Type('Window'), call_position, free=window_free)
            window_free.object_name = f'&{window}'
            window_style: TempVar = codegen.create_temp_var(Type('int'), call_position)
            
            codegen.prepend_code(f"""WNDCLASS {wc} = {{0}};
{wc}.lpfnWndProc = {window_proc};
{wc}.hInstance = GetModuleHandle(NULL);
{wc}.lpszClassName = "CureUI";
RegisterClass(&{wc});

int {window_style} = WS_OVERLAPPEDWINDOW;
if (!({kwargs['resizable']})) {{
    {window_style} = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX;
}}

Window {window} = {{
    .hwnd = CreateWindow(
        "CureUI", {title}, {window_style}, CW_USEDEFAULT, CW_USEDEFAULT, {width}, {height},
        NULL, NULL, GetModuleHandle(NULL), NULL
    ),
    .head = NULL,
    {', '.join(f'.{p} = {arg}' for p, arg in kwargs.items())}
}};

if ({window}.hwnd == NULL) {{
    {codegen.c_manager.err('Could not create window')}
}}

SetWindowLongPtr({window}.hwnd, GWLP_USERDATA, (LONG_PTR)&{window});
""")
            
            return window.OBJECT()
