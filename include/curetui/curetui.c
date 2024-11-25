#include "curetui.h"

#ifdef _WIN32
#define ENABLE_VIRTUAL_TERMINAL_PROCESSING 0x0004
#endif

#include <string.h>
#include <stdlib.h>
#include <stdio.h>


void tui_init(void) {
#ifdef _WIN32
    // This is handled in the Cure programming language
    // SetConsoleOutputCP(CP_UTF8);
    
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    DWORD dwMode = 0;
    GetConsoleMode(hOut, &dwMode);
    SetConsoleMode(hOut, dwMode | ENABLE_VIRTUAL_TERMINAL_PROCESSING);
#endif
}

void tui_exit(void) {
}

void tui_clear_screen(void) {
    printf(CLEAR_SCREEN);
    printf(CURSOR_HOME);
}

void tui_draw_box(int width, int height) {
    // Top border
    printf("┌");
    for (int i = 0; i < width - 2; i++) printf("─");
    printf("┐\n");
    
    // Sides
    for (int i = 0; i < height - 2; i++) {
        printf("│");
        for (int j = 0; j < width - 2; j++) printf(" ");
        printf("│\n");
    }
    
    // Bottom border
    printf("└");
    for (int i = 0; i < width - 2; i++) printf("─");
    printf("┘\n");
}

void tui_set_cursor_position(int x, int y) {
    printf("\033[%d;%dH", y, x);
}
