#pragma once

#include "builtins.h"

#include <string.h>


typedef struct {
    u8* buffer;
    u64 length;
    u64 capacity;
    Ref* ref;
} StringBuilder;


StringBuilder StringBuilder_new(void);
StringBuilder StringBuilder_new_0(int capacity);
nil StringBuilder_add(StringBuilder* self, string s);
string StringBuilder_to_string(StringBuilder self);
nil StringBuilder_destroy(StringBuilder* self);
