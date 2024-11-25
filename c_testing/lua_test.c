#include "../include/lua/lua.h"
#include "../include/lua/lualib.h"
#include "../include/lua/lauxlib.h"


// Based on https://www.cs.usfca.edu/~galles/cs420/lecture/LuaLectures/LuaAndC.html
// gcc c_testing/lua_test.c include/lua/lapi.c include/lua/lauxlib.c include/lua/lbaselib.c include/lua/lcode.c include/lua/lcorolib.c include/lua/lctype.c include/lua/ldblib.c include/lua/ldebug.c include/lua/ldo.c include/lua/ldump.c include/lua/lfunc.c include/lua/lgc.c include/lua/linit.c include/lua/liolib.c include/lua/llex.c include/lua/lmathlib.c include/lua/lmem.c include/lua/loadlib.c include/lua/lobject.c include/lua/lopcodes.c include/lua/loslib.c include/lua/lparser.c include/lua/lstate.c include/lua/lstring.c include/lua/lstrlib.c include/lua/ltable.c include/lua/ltablib.c include/lua/ltm.c include/lua/lundump.c include/lua/lutf8lib.c include/lua/lvm.c include/lua/lzio.c -o c_testing/lua_test.exe -I./include/lua


int add(lua_State* L) {
    double n1 = lua_tonumber(L, 1);
    double n2 = lua_tonumber(L, 2);

    double sum = n1 + n2;
    lua_pushnumber(L, sum);

    return 1;
}


int main(int argc, char* argv[]) {
    lua_State* L = luaL_newstate();
    luaL_openlibs(L);

    double a = 10;
    double b = 50;

    lua_register(L, "add", add);

    lua_getglobal(L, "add");
    lua_pushnumber(L, a);
    lua_pushnumber(L, b);

    lua_call(L, 2, 1);

    int sum = (int)lua_tointeger(L, -1);
    lua_pop(L, 1);
    printf("Sum: %d\n", sum);

    lua_close(L);
    return 0;
}
