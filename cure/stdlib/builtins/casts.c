#include "builtins.h"


string int_to_string(int i) {
    int len = snprintf(NIL, 0, "%d", i);
    u8* buf = (u8*)heap_alloc(len + 1);
    snprintf((char*)buf, len + 1, "%d", i);
    return string_new(buf, len);
}

string float_to_string(float f) {
    int len = snprintf(NIL, 0, "%f", f);
    u8* buf = (u8*)heap_alloc(len + 1);
    snprintf((char*)buf, len + 1, "%f", f);
    return string_new((u8*)buf, len);
}

string string_to_string(string s) { return string_clone(s); }
string bool_to_string(bool b) { return string_new((u8*)(b ? "true" : "false"), b ? 4 : 5); }
string nil_to_string(nil _) { return string_new((u8*)"nil", 3); }
