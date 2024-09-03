from codegen.std.ui.window import Window, EnvItem, Type, Position
from codegen.std.ui.button import Button
from codegen.std.ui.label import Label
from codegen.std.ui.frame import Frame


# gcc -o glfw_program c_testing/glfw.c -I./include -L./libs -lglfw3 -lopengl32 -lgdi32


class ui:
    def __init__(self, codegen) -> None:
        codegen.extra_compile_args.append('-lgdi32')
        
        self.window = Window(codegen)
        
        codegen.add_toplevel_code(f"""#ifndef CURE_UI_H
#ifdef OS_WINDOWS
typedef struct {{
    HFONT obj;
    const string name;
    int size;
}}

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
    Font font;
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
{codegen.c_manager.symbol_not_supported('ui')}
#endif
#endif
""")
        
        self.button = Button(codegen)
        self.frame = Frame(codegen)
        self.label = Label(codegen)
        
        codegen.add_toplevel_code("""#ifndef CURE_UI_H
#define CURE_UI_H
#endif
""")
        codegen.scope.env['close_window'] = EnvItem(
            'close_window', Type('function'),
            Position(0, 0, '')
        )
        
        codegen.c_manager.add_objects(self.window, self)
        codegen.c_manager.add_objects(self.label, self)
        codegen.c_manager.add_objects(self.button, self)
        codegen.c_manager.add_objects(self.frame, self)
