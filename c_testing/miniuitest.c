#include "../include/miniui/miniui.h"

#include <stdio.h>


void on_button_click() {
    printf("You clicked the button!\n");
}


int main() {
    Window window;
    if (!init_window(&window, "Mini UI", 800, 600, RGB(24, 24, 24))) {
        printf("Failed to initialize window.\n");
        return 1;
    }

    Font labelFont;
    if (!init_font(&labelFont, 40, "Arial", true, false, false, false)) {
        printf("Failed to initialize font.\n");
        return 1;
    }

    Widget label;
    if (!init_widget(
        &label, WLABEL, "MiniUI Test", 225, 50, 400, 50, &window,
        RGB(35, 35, 35), RGB(255, 255, 255), &labelFont, NULL, 25
    )) {
        printf("Failed to initialize label.\n");
        return 1;
    }

    if (!add_widget(&window, &label)) {
        printf("Failed to add label to window.\n");
        return 1;
    }

    Font btnFont;
    if (!init_font(&btnFont, 30, "Arial", false, false, false, false)) {
        printf("Failed to initialize font.\n");
        return 1;
    }

    Widget button;
    if (!init_widget(
        &button, WBUTTON, "Click Me!", 150, 50, 400, 150, &window,
        RGB(35, 35, 35), RGB(255, 255, 255), &btnFont, on_button_click, 10
    )) {
        printf("Failed to initialize button.\n");
        return 1;
    }

    if (!add_widget(&window, &button)) {
        printf("Failed to add button to window.\n");
        return 1;
    }

    Widget frame;
    if (!init_widget(
        &frame, WFRAME, "", 400, 300, 0, 0, &window,
        RGB(255, 255, 255), RGB(0, 0, 0), NULL, NULL, 0
    ))

    if (!add_widget(&window, &frame)) {
        printf("Failed to add frame to window.\n");
        return 1;
    }

    run_window(&window);
    if (!destroy_window(&window)) {
        printf("Failed to destroy window.\n");
        return 1;
    }

    if (!destroy_font(&labelFont)) {
        printf("Failed to destroy font.\n");
        return 1;
    }

    if (!destroy_font(&btnFont)) {
        printf("Failed to destroy font.\n");
        return 1;
    }

    return 0;
}
