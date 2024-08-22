from cure.std.ui.window import Window, EnvItem, Type, Position
from cure.std.ui.button import Button
from cure.std.ui.label import Label
from cure.std.ui.frame import Frame


class ui:
    def __init__(self, compiler) -> None:
        compiler.extra_compile_args.append('-lgdi32')
        
        self.window = Window(compiler)
        
        compiler.add_toplevel_code(f"""#ifdef OS_WINDOWS
typedef struct {{
    HWND hwnd;
    const char* title;
    int width;
    int height;
    void** widgets;
}} Window;

typedef enum {{
    WIDGET_BUTTON, WIDGET_LABEL, WIDGET_FRAME
}} WidgetType;

typedef struct {{
    HWND hwnd;
    WidgetType type;
    const char* text;
    int x, y, width, height;
    COLORREF bg_color;
    void (*on_click)(void);
    struct Widget* next;
}} Widget;

LRESULT CALLBACK {self.window.window_proc}(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {{
    Window* window = (Window*)GetWindowLongPtr(hwnd, GWLP_USERDATA);
    switch (uMsg) {{
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
        case WM_COMMAND:
            if (HIWORD(wParam) == BN_CLICKED) {{
                Widget* widget = (Widget*)GetWindowLongPtr((HWND)lParam, GWLP_USERDATA);
                if (widget && widget->on_click) widget->on_click();
            }}
            break;
        case WM_CTLCOLORBTN:
        case WM_CTLCOLORSTATIC:
            {{
                Widget* widget = (Widget*)GetWindowLongPtr((HWND)lParam, GWLP_USERDATA);
                if (widget) {{
                    SetBkColor((HDC)wParam, widget->bg_color);
                    return (LRESULT)CreateSolidBrush(widget->bg_color);
                }}
            }}
            break;
    }}
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}}

void close_window(Window* window) {{
    Widget* current = (Widget*)window->widgets;
    while (current) {{
        Widget* next = (Widget*)current->next;
        free(current);
        current = next;
    }}
    
    free(window);
}}

#else
#error "OS not supported"
#endif
""")
        
        self.button = Button(compiler)
        self.frame = Frame(compiler)
        self.label = Label(compiler)
        
        compiler.scope.env['close_window'] = EnvItem(
            'close_window', Type('function'),
            Position(0, 0, '')
        )
        
        compiler.c_manager.add_objects(self.window, self)
        compiler.c_manager.add_objects(self.label, self)
        compiler.c_manager.add_objects(self.button, self)
        compiler.c_manager.add_objects(self.frame, self)
