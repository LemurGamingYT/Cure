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

    nil line(const Vector2& start, const Vector2& end, const Color& color) {
        if (!SDL_SetRenderDrawColor(renderer, color.r(), color.g(), color.b(), 255))
            error("graphics.Window.line failed: %s", SDL_GetError());

        if (!SDL_RenderLine(renderer, start.x(), start.y(), end.x(), end.y()))
            error("graphics.Window.line failed: %s", SDL_GetError());
        
        return nil();
    }

    nil set_title(const string& title) {
        if (!SDL_SetWindowTitle(window, title.c_str()))
            error("graphics.Window.set_title failed: %s", SDL_GetError());
        
        return nil();
    }

    nil set_width(int width) {
        if (!SDL_SetWindowSize(window, width, height()))
            error("graphics.Window.set_width failed: %s", SDL_GetError());
        
        return nil();
    }

    nil set_height(int height) {
        if (!SDL_SetWindowSize(window, width(), height))
            error("graphics.Window.set_height failed: %s", SDL_GetError());
        
        return nil();
    }

    nil set_size(int width, int height) {
        if (!SDL_SetWindowSize(window, width, height))
            error("graphics.Window.set_size failed: %s", SDL_GetError());
        
        return nil();
    }
};
