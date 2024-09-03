#ifndef _WIN32
#error "ui.c can only be ran on Windows"
#endif

#include <windows.h>
#include <stdbool.h>
#include <stdio.h>


typedef struct {
    HFONT obj;
    const char* name;
    int size;
} Font;

typedef struct {
    HWND hwnd;
    const char* title;
    int width;
    int height;
    void** widgets;
} Window;

typedef enum {
    WIDGET_BUTTON, WIDGET_LABEL, WIDGET_FRAME
} WidgetType;

typedef struct {
    HWND hwnd;
    WidgetType type;
    const char* text;
    int x, y, width, height;
    Font* font;
    void (*on_click)(Window*);
    struct Widget* next;
} Widget;


void close_window(Window* window);


LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    Window* window = (Window*)GetWindowLongPtr(hwnd, GWLP_USERDATA);
    static BOOL isMouseTracking = FALSE;
    static BOOL isButtonPressed = FALSE;

    switch (uMsg) {
        case WM_DESTROY:
            PostQuitMessage(0);
            close_window(window);
            return 0;
        case WM_COMMAND:
            if (HIWORD(wParam) == BN_CLICKED) {
                Widget* widget = (Widget*)GetWindowLongPtr((HWND)lParam, GWLP_USERDATA);
                if (widget && widget->on_click) widget->on_click(window);
            }
            break;
        case WM_CTLCOLORBTN:
        case WM_CTLCOLORSTATIC:
            {
                Widget* widget = (Widget*)GetWindowLongPtr((HWND)lParam, GWLP_USERDATA);
                if (widget && widget->font) {
                    HDC hdc = (HDC)wParam;
                    SelectObject(hdc, widget->font->obj);
                }
            }
            break;
    }
    
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

Font* create_font(const char* name, int size) {
    Font* font = (Font*)malloc(sizeof(Font));
    if (!font) {
        printf("Failed to allocate memory for font.\n");
        return NULL;
    }

    font->obj = CreateFont(
        size, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE, DEFAULT_CHARSET,
        OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY,
        DEFAULT_PITCH | FF_DONTCARE, name
    );
    font->name = name;
    font->size = size;
    return font;
}

Window* create_window(const char* title, int width, int height) {
    Window* window = malloc(sizeof(Window));
    if (!window) {
        printf("Failed to allocate memory for window.\n");
        return NULL;
    }

    window->title = title;
    window->width = width;
    window->height = height;
    window->widgets = NULL;

    WNDCLASS wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = GetModuleHandle(NULL);
    wc.lpszClassName = "CureUIWindowClass";
    RegisterClass(&wc);

    window->hwnd = CreateWindowEx(0, wc.lpszClassName, title, WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, width, height, NULL, NULL, wc.hInstance, NULL);
    
    SetWindowLongPtr(window->hwnd, GWLP_USERDATA, (LONG_PTR)window);
    return window;
}

Widget* create_widget(Window* parent, WidgetType type, const char* text,
                      int x, int y, int width, int height,
                      void (*on_click)(Window*), Font* font) {
    Widget* widget = calloc(1, sizeof(Widget));
    if (!widget) {
        printf("Failed to allocate memory for widget.\n");
        return NULL;
    }

    widget->type = type;
    widget->text = text;
    widget->x = x;
    widget->y = y;
    widget->width = width;
    widget->height = height;
    widget->on_click = on_click;
    if (type != WIDGET_FRAME) {
        widget->font = font;
        SendMessage(widget->hwnd, WM_SETFONT, (WPARAM)font->obj, TRUE);
    } else {
        widget->font = NULL;
    }

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

void close_window(Window* window) {
    if (window != NULL && window->widgets != NULL) {
        Widget* current = (Widget*)window->widgets;
        while (current) {
            Widget* next = (Widget*)current->next;
            DestroyWindow(current->hwnd);
            if (current->type != WIDGET_FRAME) {
                DeleteObject(current->font->obj);
                free(current->font);
            }

            free(current);
            current = next;
        }
        DestroyWindow(window->hwnd);
        free(window);
    }
}

void test_on_click(Window* window) {
    MessageBox(window->hwnd, "Button clicked!", "Information", MB_OK | MB_ICONINFORMATION);
}

int main() {
    Window* window = create_window("Cure UI", 800, 600);
    Widget* label = create_widget(
        window, WIDGET_LABEL, "Cure UI", 400, 50, 75, 25, NULL, create_font("Segoe UI", 24)
    );
    Widget* btn = create_widget(
        window, WIDGET_BUTTON, "Test Button", 350, 250, 150, 30, test_on_click,
        create_font("Segoe UI", 24)
    );

    Widget* frame = create_widget(window, WIDGET_FRAME, NULL, 10, 10, 765, 535, NULL, NULL);

    ShowWindow(window->hwnd, SW_SHOW);

    MSG msg = {0};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    close_window(window);
    return 0;
}
