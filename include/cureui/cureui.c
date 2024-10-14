#include "cureui.h"


LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    Window* window = (Window*)GetWindowLongPtr(hwnd, GWLP_USERDATA);
    switch (uMsg) {
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    case WM_COMMAND:
        if (HIWORD(wParam) == BN_CLICKED) {
            Widget* widget = (Widget*)GetWindowLongPtr((HWND)lParam, GWLP_USERDATA);
            if (widget->type == WBUTTON && widget->clicked != NULL) {
                widget->clicked((struct Widget*)widget);
            }
        }
        break;
    }

    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

static void init_window(Window* window, const string title, const int width, const int height) {
    WNDCLASS wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = GetModuleHandle(NULL);
    wc.lpszClassName = "CureUI";
    RegisterClass(&wc);

    window->width = width;
    window->height = height;
    window->head = NULL;
    window->title = title;
    window->hwnd = CreateWindow(
        "CureUI", title, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
        width, height, NULL, NULL, GetModuleHandle(NULL), NULL
    );

    if (window->hwnd == NULL) {
        return;
    }

    SetWindowLongPtr(window->hwnd, GWLP_USERDATA, (LONG_PTR)window);
}

static void add_widget(Window* window, Widget* widget) {
    if (window->head == NULL) {
        window->head = (struct Widget*)widget;
    } else {
        Widget* current = (Widget*)window->head;
        while (current->next != NULL) {
            current = (Widget*)current->next;
        }
        current->next = (struct Widget*)widget;
    }
}

static void run_window(Window* window) {
    ShowWindow(window->hwnd, SW_SHOW);
    MSG msg = {0};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
}

static void destroy_window(Window* window) {
    if (window != NULL) {
        DestroyWindow(window->hwnd);
        if (window->head != NULL) {
            Widget* widget = (Widget*)window->head;
            while (widget != NULL) {
                Widget* next = (Widget*)widget->next;
                free(widget);
                widget = next;
            }
        }
        free(window);
    }
}

static bool is_valid_window(Window* window) {
    return window->hwnd != NULL;
}


static void init_widget(
    Widget* widget, WidgetType type, const string text, const int width, const int height,
    const int x, const int y, void (*clicked)(struct Widget*)
) {
    widget->clicked = clicked;
    widget->height = height;
    widget->width = width;
    widget->text = text;
    widget->type = type;
    widget->next = NULL;
    widget->x = x;
    widget->y = y;

    switch (type) {
    case WLABEL:
        widget->hwnd = CreateWindow(
            "STATIC", text, WS_VISIBLE | WS_CHILD | SS_CENTER | SS_CENTERIMAGE, x, y,
            width, height, NULL, NULL, GetModuleHandle(NULL), NULL
        );
        break;
    default:
        return;
    }

    if (widget->hwnd == NULL) {
        return;
    }

    SetWindowLongPtr(widget->hwnd, GWLP_USERDATA, (LONG_PTR)widget);
}
