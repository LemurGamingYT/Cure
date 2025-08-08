#pragma once

#include "builtins/builtins.hpp"
#include "color/color.hpp"

#include "SDL3/include/SDL3/SDL.h"


class Window {
    SDL_Window* window;
    SDL_Renderer* renderer;
    string _title;
    int _width, _height;
public:
    Window(const string& title = "Window", int width = 800, int height = 600) :
        _title(title), _width(width), _height(height) {
        if (!SDL_Init(SDL_INIT_VIDEO))
            error("graphics.Window failed: %s", SDL_GetError());
        
        if (!SDL_CreateWindowAndRenderer(title.c_str(), width, height, 0, &window, &renderer)) {
            SDL_Quit();
            error("graphics.Window failed: %s", SDL_GetError());
        }
    }

    string title() const { return _title; }
    int width() const { return _width; }
    int height() const { return _height; }

    nil line(int x1, int y1, int x2, int y2, const Color& color) {
        SDL_SetRenderDrawColor(renderer, color.r(), color.g(), color.b(), 255);
        if (!SDL_RenderLine(renderer, x1, y1, x2, y2))
            error("graphics.Window.line failed: %s", SDL_GetError());
        
        return nil();
    }

    nil set_title(const string& title) {
        SDL_SetWindowTitle(window, title.c_str());
        return nil();
    }

    nil set_width(int width) {
        SDL_SetWindowSize(window, width, height());
        return nil();
    }

    nil set_height(int height) {
        SDL_SetWindowSize(window, width(), height);
        return nil();
    }

    nil set_size(int width, int height) {
        SDL_SetWindowSize(window, width, height);
        return nil();
    }
};
