#pragma once

#include "builtins/builtins.hpp"
#include "color/color.hpp"

#include <SDL3/SDL.h>


class Window {
    SDL_Window* _window;
    SDL_Renderer* _renderer;
    string _title;
    int _width, _height;
public:
    Window(
        const string& title, int width, int height
    ) : _title(title), _width(width), _height(height) {
        if (!SDL_Init(SDL_INIT_VIDEO))
            error("SDL failed to initialise");
        
        if (!SDL_CreateWindowAndRenderer(title.c_str(), width, height, 0, &_window, &_renderer)) {
            close();
            error("SDL failed to create window");
        }
    }

    ~Window() {
        close();
    }

    string title() const { return _title; }
    int width() const { return _width; }
    int height() const { return _height; }
    bool is_running() const {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_EVENT_QUIT)
                return false;
        }

        return true;
    }

    nil close() const {
        if (_window != nullptr)
            SDL_DestroyWindow(_window);
        
        if (_renderer != nullptr)
            SDL_DestroyRenderer(_renderer);
        
        SDL_Quit();
        return nil();
    }

    nil set_bg(const Color& color) const {
        return nil();
    }

    nil update() const {
        return nil();
    }
};

string to_string(const Window& window) {
    return "Window(title='" + window.title() + "', width=" + to_string(window.width()) +
        ", height=" + to_string(window.height()) + ")";
}
