#ifndef CURETUI_H
#define CURETUI_H


#ifdef _WIN32
#include <windows.h>
#include <conio.h>

#define getchar _getch

#undef ENABLE_VIRTUAL_TERMINAL_PROCESSING
#define ENABLE_VIRTUAL_TERMINAL_PROCESSING 0x0004
#endif

#define CLEAR_SCREEN "\033[2J"
#define CURSOR_HOME "\033[H"
#define CURSOR_UP "\033[1A"
#define CURSOR_DOWN "\033[1B"
#define CURSOR_RIGHT "\033[1C"
#define CURSOR_LEFT "\033[1D"

#define COLOR_RESET "\033[0m"
#define COLOR_GREEN "\033[32m"
#define COLOR_BLUE "\033[34m"


void tui_init(void);
void tui_exit(void);
void tui_clear_screen(void);
void tui_draw_box(int width, int height);
void tui_set_cursor_position(int x, int y);

#endif
