#include "utils.h"


#define ARRAY(T) typedef struct { T* elements; size_t length, capacity; } T##_array;\
static T##_array T##_array_new(size_t capacity) {\
    T##_array array = { .capacity = capacity, .length = 0, .elements = malloc(capacity * sizeof(T)) };\
    if (array.elements == NULL) {\
        error("Failed to allocate memory for file array");\
    }\
    return array;\
}\
static void T##_array_add(T##_array* array, T element) {\
    if (array->length == array->capacity) {\
        array->capacity *= 2;\
        array->elements = realloc(array->elements, array->capacity * sizeof(T));\
        if (array->elements == NULL) {\
            error("Failed to reallocate memory for file array");\
            return;\
        }\
    }\
    array->elements[array->length++] = element;\
}\
static void T##_array_free(T##_array* array) {\
    free(array->elements);\
    array->elements = NULL;\
}\
static T T##_array_get(T##_array* array, size_t index) {\
    if (index >= array->length) {\
        error("Index out of bounds");\
    }\
    return array->elements[index];\
}\
static void T##_array_set(T##_array* array, size_t index, T element) {\
    if (index >= array->length) {\
        error("Index out of bounds");\
    }\
    array->elements[index] = element;\
}
