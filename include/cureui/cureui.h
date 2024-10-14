#ifndef CUREUI_H
#define CUREUI_H

#ifdef __cplusplus
extern "C" {
#endif

#include "../../c_testing/utils.h"


#ifndef OS_WINDOWS
// TODO: Support Linux and MacOS. Use XCB/Xlib for Linux
#error "CureUI is only available on Windows currently"
#endif


typedef struct {
    HWND hwnd;
    struct Widget* head;
    int width, height;
    string title;
} Window;

typedef enum {
    WLABEL, WBUTTON, WFRAME
} WidgetType;

typedef struct {
    HWND hwnd;
    WidgetType type;
    string text;
    int width, height, x, y;
    void (*clicked)(struct Widget*);
    struct Widget* next;
} Widget;


LRESULT CALLBACK WindowProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);


static void init_window(Window* window, const string title, const int width, const int height);
static void add_widget(Window* window, Widget* widget);
static void destroy_window(Window* window);
static void run_window(Window* window);
static bool is_valid_window(Window* window);

static void init_widget(
    Widget* widget, WidgetType type, const string text, const int width, const int height,
    const int x, const int y, void (*clicked)(struct Widget*)
);

static void show_widget(Widget* widget);
static void hide_widget(Widget* widget);
static void set_focus(Widget* widget);
static void set_text(Widget* widget);
static void set_widget_position(Widget* widget);
static void set_widget_size(Widget* widget, const int width, const int height);


#ifdef __cplusplus
}
#endif

#endif
