#include "./miniui.h"


LRESULT CALLBACK WindowProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    Window* window = (Window*)GetWindowLongPtr(hwnd, GWLP_USERDATA);
    switch (msg) {
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    case WM_SETCURSOR:
        {
            HWND hWnd = (HWND)wParam;
            WORD hitTest = LOWORD(lParam);
            if (hitTest != HTCLIENT) break;

            Widget* widget = (Widget*)GetWindowLongPtr(hWnd, GWLP_USERDATA);
            if (widget != NULL && widget->type == WBUTTON) {
                SetCursor(LoadCursor(NULL, IDC_HAND));
            } else {
                SetCursor(LoadCursor(NULL, IDC_ARROW));
            }

            return TRUE;
        }
        break;
    case WM_COMMAND:
        {
            Widget* widget = (Widget*)GetWindowLongPtr((HWND)lParam, GWLP_USERDATA);
            if (widget != NULL && HIWORD(wParam) == BN_CLICKED) {
                if (widget->type == WBUTTON && widget->on_click != NULL) {
                    widget->on_click(widget);
                }
            }
        } break;
    case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            SetBkColor(hdc, window->bg_color);

            RECT rect;
            GetClientRect(hwnd, &rect);
            ExtTextOut(hdc, 0, 0, ETO_OPAQUE, &rect, NULL, 0, NULL);
            EndPaint(hwnd, &ps);
        } break;
    case WM_CTLCOLORSTATIC:
        {
            HDC hdc = (HDC)wParam;
            Widget* widget = (Widget*)GetWindowLongPtr((HWND)lParam, GWLP_USERDATA);
            if (widget != NULL) {
                SetBkColor(hdc, widget->bg_color);
                SetTextColor(hdc, widget->text_color);
                return (INT_PTR)CreateSolidBrush(widget->bg_color);
            }
        } break;
    case WM_DRAWITEM:
        {
            LPDRAWITEMSTRUCT pdis = (LPDRAWITEMSTRUCT)lParam;
            if (pdis->CtlType != ODT_BUTTON) return FALSE;

            Widget* widget = (Widget*)GetWindowLongPtr(pdis->hwndItem, GWLP_USERDATA);
            if (widget == NULL) return FALSE;

            HDC hdc = pdis->hDC;
            SetBkColor(hdc, widget->bg_color);
            HBRUSH hBrush = CreateSolidBrush(widget->bg_color);
            FillRect(hdc, &pdis->rcItem, hBrush);
            DeleteObject(hBrush);

            SetTextColor(hdc, widget->text_color);
            int len = GetWindowTextLength(pdis->hwndItem);
            string text = (string)malloc(len + 1);
            if (text == NULL) return FALSE;

            GetWindowText(pdis->hwndItem, text, len + 1);
            DrawText(hdc, text, len, &pdis->rcItem, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
            free(text);
            return TRUE;
        } break;
    }

    return DefWindowProc(hwnd, msg, wParam, lParam);
}


bool init_window(
    Window* window, const string title, const int width, const int height,
    const COLORREF bg_color
) {
    if (window == NULL) return false;

    WNDCLASS wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = GetModuleHandle(NULL);
    wc.lpszClassName = CLASS_NAME;
    RegisterClass(&wc);

    window->hwnd = CreateWindow(
        CLASS_NAME, title, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
        width, height, NULL, NULL, GetModuleHandle(NULL), NULL
    );

    if (window->hwnd == NULL) return false;

    window->title = title;
    window->width = width;
    window->height = height;
    window->bg_color = bg_color;
    window->head = NULL;

    SetWindowLongPtr(window->hwnd, GWLP_USERDATA, (LONG_PTR)window);
    return true;
}

bool destroy_window(Window* window) {
    if (window == NULL) return false;
    if (window->hwnd == NULL) return false;

    DestroyWindow(window->hwnd);
    return true;
}

void run_window(Window* window) {
    if (window == NULL) return;
    if (window->hwnd == NULL) return;

    ShowWindow(window->hwnd, SW_SHOW);
    MSG msg = {0};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
}

bool init_widget(
    Widget* widget, WidgetType type, const string text, const int width, const int height,
    const int x, const int y, Window* parent, COLORREF bg_color, COLORREF text_color,
    Font* font, click_callback on_click, int corner_radius
) {
    if (widget == NULL) return false;

    widget->x = x;
    widget->y = y;
    widget->font = font;
    widget->type = type;
    widget->text = text;
    widget->width = width;
    widget->height = height;
    widget->parent = (struct Window*)parent;
    widget->bg_color = bg_color;
    widget->text_color = text_color;
    widget->font = font;
    widget->next = NULL;
    widget->hwnd = NULL;
    widget->on_click = on_click;
    widget->corner_radius = corner_radius;
    return true;
}

bool add_widget(Window* window, Widget* widget) {
    if (window == NULL) return false;
    if (widget == NULL) return false;

    if ((Window*)widget->parent != window) return false;

    switch (widget->type) {
    case WLABEL:
        widget->hwnd = CreateWindow(
            "STATIC", widget->text, WS_CHILD | WS_VISIBLE | SS_CENTER | SS_CENTERIMAGE,
            widget->x - (widget->width / 2), widget->y - (widget->height / 2),
            widget->width, widget->height, window->hwnd, NULL, GetModuleHandle(NULL), NULL
        );
        break;
    case WBUTTON:
        widget->hwnd = CreateWindow(
            "BUTTON", widget->text, WS_CHILD | WS_VISIBLE | BS_DEFPUSHBUTTON | BS_OWNERDRAW,
            widget->x - (widget->width / 2), widget->y - (widget->height / 2),
            widget->width, widget->height, window->hwnd, NULL, GetModuleHandle(NULL), NULL
        );
        break;
    case WFRAME:
        widget->hwnd = CreateWindow(
            "STATIC", "", WS_CHILD | WS_VISIBLE | SS_CENTER | SS_CENTERIMAGE,
            widget->x - (widget->width / 2), widget->y - (widget->height / 2),
            widget->width, widget->height, window->hwnd, NULL, GetModuleHandle(NULL), NULL
        );
    }

    if (widget->hwnd == NULL) return false;
    if (widget->font != NULL) {
        SendMessage(widget->hwnd, WM_SETFONT, (WPARAM)widget->font->font, TRUE);
    }

    SetWindowLongPtr(widget->hwnd, GWLP_USERDATA, (LONG_PTR)widget);

    Widget* current = window->head;
    if (current == NULL) {
        window->head = widget;
    } else {
        while (current->next != NULL) {
            current = (Widget*)current->next;
        }

        current->next = (struct Widget*)widget;
    }

    return true;
}

bool init_font(
    Font* font, const int size, const string family,
    const bool bold, const bool italic, const bool underline, const bool strikeout
) {
    if (font == NULL) return false;

    font->size = size;
    font->bold = bold;
    font->family = family;
    font->italic = italic;
    font->underline = underline;
    font->strikeout = strikeout;
    font->font = CreateFont(
        size, 0, 0, 0,
        bold ? FW_BOLD : FW_NORMAL,
        italic, underline, strikeout,
        DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
        DEFAULT_QUALITY, DEFAULT_PITCH | FF_DONTCARE, family
    );
    return true;
}

bool destroy_font(Font* font) {
    if (font == NULL) return false;
    DeleteObject(font->font);
    return true;
}
