#ifndef CUREUI_DRAW_H
#define CUREUI_DRAW_H

#ifdef __cplusplus
extern "C" {
#endif

#include "./cureui.h"


typedef struct {
    Window* window;
    COLORREF color;
} Brush;


Brush new_brush(Window* window, COLORREF* color);
void destroy_brush(Brush* brush);


void draw_ellipse(Brush* brush, int left, int top, int right, int bottom);
void draw_line(Brush* brush, int xStart, int yStart, int xEnd, int yEnd);
void draw_round_rectangle(
    Brush* brush, int left, int top, int right, int bottom, int width, int height);
void draw_rectangle(Brush* brush, int left, int top, int right, int bottom);
void draw_text(Brush* brush, int left, int top, int right, int bottom, string text);



#ifdef __cplusplus
}
#endif

#endif
