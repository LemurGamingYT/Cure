#ifndef MINIUI_H
#define MINIUI_H


#ifdef __cplusplus
extern "C" {
#endif


#include "../osarch_check.h"

#if OS_WINDOWS
#include <windows.h>
#else
// TODO: Support Linux and MacOS. Use XCB/Xlib for Linux
#error "MiniUI is only supported on Windows"
#endif

#include <stdbool.h>

typedef char* string;
typedef void (*click_callback)();

#define CLASS_NAME "MiniUI"


typedef struct {
    HFONT font;
    int size;
    string family;
    bool bold, italic, underline, strikeout;
} Font;

typedef enum {
    WLABEL, WBUTTON, WFRAME
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
    Widget* widget, WidgetType type, const string text, const int width, const int height,
    const int x, const int y, Window* parent, COLORREF bg_color, COLORREF text_color,
    Font* font, click_callback on_click, int corner_radius
);
bool add_widget(Window* window, Widget* widget);

bool init_font(
    Font* font, const int size, const string family,
    const bool bold, const bool italic, const bool underline, const bool strikeout
);
bool destroy_font(Font* font);


#ifdef __cplusplus
}
#endif


#endif
