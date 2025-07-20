#include "StringBuilder.h"
#include "Math.h"


StringBuilder StringBuilder_new(void) {
    return StringBuilder_new_0(1024);
}

StringBuilder StringBuilder_new_0(int capacity) {
    StringBuilder sb = {
        .capacity = capacity, .length = 0, .buffer = (u8*)heap_alloc(capacity), .ref = NIL
    };
    
    sb.ref = Ref_new((pointer)sb.buffer, NIL);
    return sb;
}

int StringBuilder_capacity(StringBuilder* self) {
    return self->capacity;
}

int StringBuilder_length(StringBuilder* self) {
    return self->length;
}

nil StringBuilder_add(StringBuilder* self, string s) {
    if (self->length + s.length >= self->capacity) {
        self->capacity = Math_max_3(self->capacity * 2, self->length + s.length);
        self->buffer = (u8*)heap_realloc(self->buffer, self->capacity);
    }

    memcpy(self->buffer + self->length, s.ptr, s.length);
    self->length += s.length;
    return NIL;
}

string StringBuilder_to_string(StringBuilder self) {
    u8* result_buffer = (u8*)heap_alloc(self.length + 1);
    memcpy(result_buffer, self.buffer, self.length);
    result_buffer[self.length] = '\0';
    return string_new(result_buffer, self.length);
}

nil StringBuilder_destroy(StringBuilder* self) {
    if (self->ref == NIL) return NIL;
    Ref_dec(self->ref);
    return NIL;
}
