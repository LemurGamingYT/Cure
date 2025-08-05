#pragma once

#include "builtins/builtins.hpp"


class Color {
    int _r;
    int _g;
    int _b;
public:
    Color(int r, int g, int b) : _r(r), _g(g), _b(b) {}
    Color(string hex) {
        if (hex._Starts_with("#")) hex = hex.substr(1);
        _r = std::stoi(hex.substr(1, 2), nullptr, 16);
        _g = std::stoi(hex.substr(3, 2), nullptr, 16);
        _b = std::stoi(hex.substr(5, 2), nullptr, 16);
    }

    int r() const { return _r; }
    int g() const { return _g; }
    int b() const { return _b; }

    string hex() const {
        static char buf[16];
        snprintf(buf, sizeof(buf), "#%02x%02x%02x", _r, _g, _b);
        return buf;
    }

    int h() const {
        float fCMax = std::max(std::max(_r, _g), _b);
        float fCMin = std::min(std::min(_r, _g), _b);
        float fDelta = fCMax - fCMin;
        float res = 0;
        if (fDelta > 0) {
            if (fCMax == _r) {
                res = 60 * (std::fmod(((_g - _b) / fDelta), 6));
            } else if (fCMax == _g) {
                res = 60 * (((_b - _r) / fDelta) + 2);
            } else if (fCMax == _b) {
                res = 60 * (((_r - _g) / fDelta) + 4);
            }
        }
        
        if(res < 0) {
            res = 360 + res;
        }

        return res;
    }

    int s() const {
        float fCMax = std::max(std::max(_r, _g), _b);
        float fCMin = std::min(std::min(_r, _g), _b);
        float fDelta = fCMax - fCMin;
        float res = 0;
        if (fDelta > 0) {
            if (fCMax > 0) {
                res = fDelta / fCMax;
            } else {
                res = 0;
            }
        }

        return res;
    }

    int v() const {
        float fCMax = std::max(std::max(_r, _g), _b);
        float fCMin = std::min(std::min(_r, _g), _b);
        float fDelta = fCMax - fCMin;
        float res = 0;
        if (fDelta > 0) {
            res = fCMax;
        } else {
            res = fCMax;
        }

        return res;
    }
};

string to_string(const Color& color) {
    return "Color(r=" + to_string(color.r()) + ", g=" + to_string(color.g()) + ", b=" +
        to_string(color.b()) + ")";
}
