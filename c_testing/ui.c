#include <windows.h>
#include <stdbool.h>


typedef enum {
    WIDGET_BUTTON, WIDGET_LABEL, WIDGET_FRAME
} WidgetType;

typedef struct {
    HWND hwnd;
    WidgetType type;
    const char* text;
    int x, y, width, height;
    COLORREF bg_color;
    void (*on_click)(void);
    struct Widget* next;
} Widget;

typedef struct {
    HWND hwnd;
    const char* title;
    int width;
    int height;
    void** widgets;
} Window;


LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    Window* window = (Window*)GetWindowLongPtr(hwnd, GWLP_USERDATA);
    switch (uMsg) {
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
        case WM_COMMAND:
            if (HIWORD(wParam) == BN_CLICKED) {
                Widget* widget = (Widget*)GetWindowLongPtr((HWND)lParam, GWLP_USERDATA);
                if (widget && widget->on_click) widget->on_click();
            }
            break;
        case WM_CTLCOLORBTN:
        case WM_CTLCOLORSTATIC:
            {
                Widget* widget = (Widget*)GetWindowLongPtr((HWND)lParam, GWLP_USERDATA);
                if (widget) {
                    SetBkColor((HDC)wParam, widget->bg_color);
                    return (LRESULT)CreateSolidBrush(widget->bg_color);
                }
            }
            break;
    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

Window* create_window(const char* title, int width, int height) {
    Window* window = malloc(sizeof(Window));
    window->title = title;
    window->width = width;
    window->height = height;
    window->widgets = NULL;

    WNDCLASS wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = GetModuleHandle(NULL);
    wc.lpszClassName = "SimpleUIWindowClass";
    RegisterClass(&wc);

    window->hwnd = CreateWindowEx(0, wc.lpszClassName, title, WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, width, height, NULL, NULL, wc.hInstance, NULL);
    
    SetWindowLongPtr(window->hwnd, GWLP_USERDATA, (LONG_PTR)window);
    return window;
}

Widget* create_widget(Window* parent, WidgetType type, const char* text,
                      int x, int y, int width, int height,
                      void (*on_click)(void), COLORREF bg_color) {
    Widget* widget = malloc(sizeof(Widget));
    widget->type = type;
    widget->text = text;
    widget->x = x;
    widget->y = y;
    widget->width = width;
    widget->height = height;
    widget->on_click = on_click;
    widget->bg_color = bg_color;
    widget->next = NULL;

    const char* class_name;
    DWORD style = WS_CHILD | WS_VISIBLE;
    switch (type) {
        case WIDGET_BUTTON:
            class_name = "BUTTON";
            style |= BS_PUSHBUTTON;
            break;
        case WIDGET_LABEL:
            class_name = "STATIC";
            style |= SS_LEFT;
            break;
        case WIDGET_FRAME:
            class_name = "BUTTON";
            style |= BS_GROUPBOX;
            break;
        default:
            class_name = "STATIC";
            style |= SS_LEFT;
    }

    widget->hwnd = CreateWindow(class_name, text, style, x, y, width, height,
        parent->hwnd, NULL, (HINSTANCE)GetWindowLongPtr(parent->hwnd, GWLP_HINSTANCE), NULL);

    SetWindowLongPtr(widget->hwnd, GWLP_USERDATA, (LONG_PTR)widget);

    // Add widget to the window's linked list
    if (!parent->widgets) {
        parent->widgets = (void**)widget;
    } else {
        Widget* last = (Widget*)parent->widgets;
        while (last->next) last = (Widget*)last->next;
        last->next = (struct Widget*)widget;
    }

    return widget;
}

void show_window(Window* window) {
    ShowWindow(window->hwnd, SW_SHOW);
}

void close_window(Window* window) {
    Widget* current = (Widget*)window->widgets;
    while (current) {
        Widget* next = (Widget*)current->next;
        free(current);
        current = next;
    }
    free(window);
}

int main() {
    Window* window = create_window("Simplified UI", 800, 600);
    create_widget(window, WIDGET_BUTTON, "Test Button", 350, 250, 150, 30, NULL, RGB(24, 24, 24));
    create_widget(window, WIDGET_LABEL, "Hello, World!", 350, 200, 150, 30, NULL, RGB(240, 240, 240));
    show_window(window);

    MSG msg = {0};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    close_window(window);
    return 0;
}
