#pragma once

#include "builtins/builtins.h"


#define static_array(T, size)\
typedef struct {\
    T elements[size];\
} array_##T##_##size;\
\
array_##T##_##size array_##T##_##size##_new(void) {\
    array_##T##_##size arr;\
    return arr;\
}\
\
nil array_##T##_##size##_set(array_##T##_##size##* arr, int index, T element) {\
    bound b = bounds_check(index, size);\
    if (b.out_of_bounds)\
        error("array index out of bounds");\
    \
    arr->elements[b.index] = element;\
    return NIL;\
}\
\
T array_##T##_##size##_get(array_##T##_##size* arr, int index) {\
    bound b = bounds_check(index, size);\
    if (b.out_of_bounds)\
        error("array index out of bounds");\
    \
    return arr->elements[b.index];\
}
