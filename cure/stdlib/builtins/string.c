#include "builtins.h"

#include <stdlib.h>
#include <string.h>


string string_new(const u8* ptr, u64 length) {
    string s = { .ptr = (u8*)heap_alloc(length + 1), .length = length, .ref = NIL };
    s.ptr = (u8*)heap_alloc(length + 1);
    memcpy(s.ptr, ptr, length);
    s.ptr[length] = (u8)'\0';

    s.ref = Ref_new((pointer)s.ptr, NIL);
    return s;
}

nil string_destroy(string* s) {
    if (s->ref == NIL) return NIL;
    Ref_dec(s->ref);
    return NIL;
}

int string_length(string self) { return (int)self.length; }
string string_clone(string self) { return string_new(self.ptr, self.length); }
nil string_set(string* self, int index, string ch) {
    bound b = bounds_check(index, self->length);
    if (b.out_of_bounds)
        error("string index out of bounds");

    if (ch.length != 1)
        error("ch must be one character");
    
    u8 character = ch.ptr[0];
    self->ptr[b.index] = character;
    return NIL;
}

string string_at(string self, int index) {
    bound b = bounds_check(index, self.length);
    if (b.out_of_bounds)
        error("string index out of bounds");

    u8 ch = self.ptr[index];
    static u8 ptr[2];
    ptr[0] = ch;
    ptr[1] = (u8)'\0';
    return string_new((u8*)ptr, 1);
}
