#pragma once

#include "builtins/builtins.hpp"


class Color {
    int _r;
    int _g;
    int _b;
public:
    Color(int r, int g, int b) : _r(r), _g(g), _b(b) {}

    // TODO: Color(string hex)

    int r() const { return _r; }
    int g() const { return _g; }
    int b() const { return _b; }

    string hex() const {
        static char buf[16];
        snprintf(buf, sizeof(buf), "#%02x%02x%02x", _r, _g, _b);
        return buf;
    }

    // TODO: .h, .s, .v

    bool operator==(const Color& other) const {
        return _r == other._r && _g == other._g && _b == other._b;
    }

    bool operator!=(const Color& other) const {
        return _r != other._r || _g != other._g || _b != other._b;
    }
};

string to_string(const Color& color) {
    return "Color(r=" + to_string(color.r()) + ", g=" + to_string(color.g()) + ", b=" +
        to_string(color.b()) + ")";
}
