#include <curetui/curetui.h>
#include <stdio.h>


int main() {
    tui_init();

    printf(COLOR_GREEN "Simple CureTUI Demo\n" COLOR_RESET);
    tui_draw_box(40, 10);

    printf(COLOR_BLUE "\nPress 'q' to quit\n" COLOR_RESET);

    char c;
    while ((c = getchar()) != 'q') {
        printf("Pressed: %c\n", c);
    }

    tui_clear_screen();
    tui_exit();
    return 0;
}
