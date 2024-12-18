#ifndef MINIUI_H
#define MINIUI_H


#ifdef __cplusplus
extern "C" {
#endif


#define bool int
#define true 1
#define false 0

#if defined(_WIN32) || defined(_WIN64) || defined(_MSC_VER) || defined(WIN32)
#define OS_WINDOWS 1
#elif defined(__APPLE__)
#define OS_MAC 1
#elif defined(__linux__)
#define OS_LINUX 1
#else
#error "Unsupported operating system"
#endif

#if OS_WINDOWS
#include <windows.h>
#else
// TODO: Support Linux and MacOS. Use XCB/Xlib for Linux
#error "MiniUI is only supported on Windows"
#endif

typedef char* string;
typedef void (*click_callback)();
typedef void (*text_changed_callback)(string new_text);

#define CLASS_NAME "MiniUI"


typedef struct {
    HFONT font;
    int size;
    string family;
    bool bold, italic, underline, strikeout;
} Font;

typedef enum {
    WLABEL, WBUTTON, WFRAME, WTEXTBOX
} WidgetType;

typedef struct {
    HWND hwnd;
    string text;
    int width, height, x, y;
    COLORREF bg_color, text_color;
    struct Widget* next;
    struct Window* parent;
    WidgetType type;
    Font* font;
    click_callback on_click;
    int corner_radius;
    float relx, rely, relwidth, relheight;
    text_changed_callback on_text_changed;
} Widget;

typedef struct {
    HWND hwnd;
    string title;
    int width, height;
    COLORREF bg_color;
    Widget* head;
} Window;

LRESULT CALLBACK WindowProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);

bool init_window(
    Window* window, const string title, const int width, const int height,
    const COLORREF bg_color
);
bool destroy_window(Window* window);
void run_window(Window* window);

bool init_widget(
    Widget* widget, WidgetType type, const string text, int width, int height,
    int x, int y, Window* parent, COLORREF bg_color, COLORREF text_color,
    Font* font, click_callback on_click, int corner_radius, float relx, float rely,
    float relwidth, float relheight, text_changed_callback on_text_changed
);
bool add_widget(Window* window, Widget* widget);
string get_textbox_text(Widget* widget);

bool init_font(
    Font* font, const int size, const string family,
    const bool bold, const bool italic, const bool underline, const bool strikeout
);
bool destroy_font(Font* font);


#ifdef __cplusplus
}
#endif


#endif
