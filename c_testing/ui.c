#include "utils.h"
#ifndef OS_WINDOWS
#error "This file is only for Windows"
#endif

#include <windows.h>
#include <stdlib.h>
#include <stdio.h>

typedef void (*ButtonCallback)(HWND);

typedef struct {
    int width, height;
} Rect;

typedef struct {
    int x, y;
} Vector2int;

typedef struct {
    HWND hwnd;
    ButtonCallback callback;
} Button;

typedef struct {
    HWND hwnd;
} Label;

typedef struct {
    HWND hwnd;
} Frame;

typedef struct {
    HWND hwnd;
    Button** buttons;
    size_t button_count;
    Label** labels;
    size_t label_count;
    Frame** frames;
    size_t frame_count;
} Window;


static LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    Window* window = (Window*)GetWindowLongPtr(hwnd, GWLP_USERDATA);
    switch (uMsg) {
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
        case WM_COMMAND:
            if (HIWORD(wParam) == BN_CLICKED) {
                Button* button = (Button*)GetWindowLongPtr((HWND)lParam, GWLP_USERDATA);
                if (button && button->callback) {
                    button->callback(button->hwnd);
                }
            }
            break;
    }

    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

static Window Window_new(const char* title, const Rect size) {
    WNDCLASS wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = GetModuleHandle(NULL);
    wc.lpszClassName = "CureUI";
    RegisterClass(&wc);

    Window window = { .button_count = 0, .buttons = NULL, .hwnd = CreateWindowEx(
        0, "CureUI", title, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, size.width,
        size.height, NULL, NULL, GetModuleHandle(NULL), NULL
    ) };

    if (window.hwnd == NULL) {
        error("Failed to create window.");
    }

    SetWindowLongPtr(window.hwnd, GWLP_USERDATA, (LONG_PTR)&window);
    return window;
}

static void Window_destroy(Window* window) {
    if (window != NULL) {
        DestroyWindow(window->hwnd);
        if (window->buttons != NULL) {
            for (int i = 0; i < window->button_count; ++i) {
                free(window->buttons[i]);
            }
            free(window->buttons);
        }
        window->buttons = NULL;

        if (window->labels != NULL) {
            for (int i = 0; i < window->label_count; ++i) {
                free(window->labels[i]);
            }
            free(window->labels);
        }
        window->labels = NULL;

        if (window->frames != NULL) {
            for (int i = 0; i < window->frame_count; ++i) {
                free(window->frames[i]);
            }
            free(window->frames);
        }
        window->frames = NULL;
    }
}

static Frame* Window_add_frame(
    Window* window, const Vector2int pos, const Rect size
) {
    Frame* frame = (Frame*)malloc(sizeof(Frame));
    if (frame == NULL) {
        Window_destroy(window);
        error("Failed to allocate memory for frame");
    }

    frame->hwnd = CreateWindow(
        "STATIC", "", WS_VISIBLE | WS_CHILD | SS_CENTER | SS_CENTERIMAGE, pos.x, pos.y,
        size.width, size.height, window->hwnd, NULL, GetModuleHandle(NULL), NULL
    );

    if (frame->hwnd == NULL) {
        free(frame);
        Window_destroy(window);
        error("Failed to create frame");
    }

    window->frames = realloc(window->frames, (window->frame_count + 1) * sizeof(Frame*));
    window->frames[window->frame_count++] = frame;
    return frame;
}

static Label* Window_add_label(
    Window* window, const char* text, const Vector2int pos, const Rect size
) {
    Label* label = (Label*)malloc(sizeof(Label));
    if (label == NULL) {
        Window_destroy(window);
        error("Failed to allocate memory for label");
    }

    label->hwnd = CreateWindow(
        "STATIC", text, WS_VISIBLE | WS_CHILD | SS_CENTER | SS_CENTERIMAGE, pos.x, pos.y,
        size.width, size.height, window->hwnd, NULL, GetModuleHandle(NULL), NULL
    );

    if (label->hwnd == NULL) {
        free(label);
        Window_destroy(window);
        error("Failed to create label");
    }

    window->labels = realloc(window->labels, (window->label_count + 1) * sizeof(Label*));
    if (window->labels == NULL) {
        free(label);
        Window_destroy(window);
        error("Failed to allocate memory for labels");
    }

    window->labels[window->label_count++] = label;
    return label;
}

static Button* Window_add_button(
    Window* window, const char* text, const Vector2int pos, const Rect size,
    ButtonCallback callback
) {
    Button* button = (Button*)malloc(sizeof(Button));
    if (button == NULL) {
        Window_destroy(window);
        error("Failed to allocate memory for button");
    }

    button->hwnd = CreateWindow(
        "BUTTON", text, WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON, pos.x, pos.y,
        size.width, size.height, window->hwnd, NULL, GetModuleHandle(NULL), NULL
    );

    if (button->hwnd == NULL) {
        free(button);
        Window_destroy(window);
        error("Failed to create button");
    }

    button->callback = callback;

    window->buttons = realloc(window->buttons, (window->button_count + 1) * sizeof(Button*));
    if (window->buttons == NULL) {
        free(button);
        Window_destroy(window);
        error("Failed to allocate memory for button list");
    }

    window->buttons[window->button_count++] = button;
    SetWindowLongPtr(button->hwnd, GWLP_USERDATA, (LONG_PTR)button);
    return button;
}

void btn_callback(HWND hwnd) {
    MessageBox(hwnd, "Button clicked!", "Button Clicked", MB_OK);
}

int main() {
    Window window = Window_new("Test Window", (Rect){ 800, 600 });
    Window_add_frame(&window, (Vector2int){ 0, 0 }, (Rect){ 400, 300 });
    Window_add_button(&window, "Button", (Vector2int){ 10, 10 }, (Rect){ 100, 30 }, btn_callback);
    Window_add_label(&window, "Label", (Vector2int){ 10, 50 }, (Rect){ 50, 20 });
    ShowWindow(window.hwnd, SW_SHOW);
    MSG msg = {0};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    Window_destroy(&window);
    return 0;
}
