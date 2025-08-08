#pragma once

/*https://www.lua.org/
Copyright © 1994–2025 Lua.org, PUC-Rio.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. */

#include "builtins/builtins.hpp"
#include "lib/lua.h"
#include "lib/lualib.h"
#include "lib/lauxlib.h"


// TODO: look at https://www.lua.org/pil/contents.html

class Lua {
    lua_State* state;
public:
    Lua() {
        state = luaL_newstate();
        luaL_openlibs(state);
    }

    ~Lua() {
        lua_close(state);
    }

    int get_global(string name) {
        return lua_getglobal(state, name.c_str());
    }

    nil push_number(int n) {
        lua_pushnumber(state, n);
        return nil();
    }

    nil push_number(float n) {
        lua_pushnumber(state, n);
        return nil();
    }

    nil push_boolean(bool b) {
        lua_pushboolean(state, b);
        return nil();
    }

    nil push_string(string s) {
        lua_pushstring(state, s.c_str());
        return nil();
    }

    nil push_nil() {
        lua_pushnil(state);
        return nil();
    }

    bool is_number(int index) { return lua_isnumber(state, index); }
    bool is_string(int index) { return lua_isstring(state, index); }
    bool is_boolean(int index) { return lua_isboolean(state, index); }
    bool is_nil(int index) { return lua_isnil(state, index); }
};

string to_string(const Lua& lua) { return "Lua()"; }
