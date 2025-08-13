#pragma once

#include "builtins/builtins.hpp"
#include "color/color.hpp"

/*
I chose GLFW for it's simplicity and ease of use. Besides, if I'm going to make this a game engine and
a GUI framework in one, the library probably should use OpenGL for drawing.

You may say that it doesn't come with audio but then again, I'll add that in the fstream.SoundFile
class. GLFW is also embeddable which is ideal for this case.
*/
#include <GLFW/glfw3.h>


class Window {
    GLFWwindow* window;
    string _title;
    int _width, _height;
public:
    Window(const string& title, int width, int height) : _title(title), _width(width), _height(height) {
        if (!glfwInit())
            error("Failed to initialize GLFW");
        
        window = glfwCreateWindow(width, height, title.c_str(), nullptr, nullptr);
        if (window == nullptr) {
            glfwTerminate();
            error("Failed to create GLFW window");
        }

        glfwSetWindowAspectRatio(window, 1, 1);
        glfwMakeContextCurrent(window);
        glfwSwapInterval(1);

        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    }

    ~Window() {
        glfwDestroyWindow(window);
        glfwTerminate();
    }

    string title() const { return _title; }
    int width() const { return _width; }
    int height() const { return _height; }
    bool is_running() const { return !glfwWindowShouldClose(window); }
    
    nil line(int x1, int y1, int x2, int y2, const Color& color) {
        glBegin(GL_LINES);
        glColor3f(color.r() / 255.0f, color.g() / 255.0f, color.b() / 255.0f);
        glVertex2i(x1, y1);
        glVertex2i(x2, y2);
        glEnd();
        return nil();
    }

    nil line(int x1, int y1, int x2, int y2) {
        return line(x1, y1, x2, y2, Color{255, 255, 255});
    }

    nil line(const Vector2& start, const Vector2& end, const Color& color) {
        return line(start.x(), start.y(), end.x(), end.y(), color);
    }

    nil line(const Vector2& start, const Vector2& end) {
        return line(start, end, Color{255, 255, 255});
    }

    nil rect(int x, int y, int width, int height, const Color& color) {
        glBegin(GL_QUADS);
        glColor3f(color.r() / 255.0f, color.g() / 255.0f, color.b() / 255.0f);
        glVertex2i(x, y);
        glVertex2i(x + width, y);
        glVertex2i(x + width, y + height);
        glVertex2i(x, y + height);
        glEnd();
        return nil();
    }

    nil set_bg(const Color& color) {
        glClearColor(color.r() / 255.0f, color.g() / 255.0f, color.b() / 255.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        return nil();
    }
    
    nil update() {
        glfwGetFramebufferSize(window, &_width, &_height);
        glViewport(0, 0, _width, _height);

        float aspect_ratio = _height ? _width / (float) _height : 1.f;

        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        glOrtho(-aspect_ratio, aspect_ratio, -1.f, 1.f, 1.f, -1.f);

        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();

        glfwSwapBuffers(window);
        glfwPollEvents();
        return nil();
    }
};

string to_string(const Window& window) { return "Window('" + window.title() + "')"; }
