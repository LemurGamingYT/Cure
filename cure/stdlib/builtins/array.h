#pragma once

#include "builtins.h"


#define array(T)\
typedef struct {\
    T* elements;\
    u64 length;\
    u64 capacity;\
    Ref* ref;\
} array_##T;\
\
array_##T array_##T##_new(int capacity) {\
    array_##T arr = (array_##T){\
        .elements = (T*)heap_alloc(capacity * sizeof(T)), .length = 0, .capacity = capacity,\
        .ref = NIL\
    };\
    arr.ref = Ref_new((pointer)arr.elements, NIL);\
    \
    return arr;\
}\
\
string array_##T##_to_string(array_##T arr) {\
    StringBuilder sb = StringBuilder_new();\
    StringBuilder_add(&sb, string_new((u8*)"[", 1));\
    for (u64 i = 0; i < arr.length; i++) {\
        StringBuilder_add(&sb, T##_to_string(arr.elements[i]));\
        if (i != arr.length - 1)\
            StringBuilder_add(&sb, string_new((u8*)", ", 2));\
    }\
    \
    StringBuilder_add(&sb, string_new((u8*)"]", 1));\
    return StringBuilder_to_string(sb);\
}\
\
int array_##T##_length(array_##T* arr) {\
    return arr->length;\
}\
\
nil array_##T##_add(array_##T* arr, T elem) {\
    if (arr->length == arr->capacity) {\
        arr->capacity *= 2;\
        arr->elements = (T*)heap_realloc(arr->elements, arr->capacity * sizeof(T));\
    }\
    \
    arr->elements[arr->length++] = elem;\
    return NIL;\
}\
\
T array_##T##_get(array_##T* arr, int index) {\
    bound b = bounds_check(index, arr->length);\
    if (b.out_of_bounds)\
        error("array index out of bounds");\
    \
    return arr->elements[b.index];\
}\
\
nil array_##T##_destroy(array_##T* arr) {\
    if (arr->ref == NIL) return NIL;\
    Ref_dec(arr->ref);\
    return NIL;\
}\
\
array_##T array_##T##_from_array(T* arr, u64 length) {\
    array_##T a = array_##T##_new(length);\
    for (u64 i = 0; i < length; i++)\
        array_##T##_add(&a, arr[i]);\
    \
    return a;\
}
