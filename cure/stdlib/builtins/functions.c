#include "builtins.h"

#include <stdlib.h>
#include <stdarg.h>
#include <string.h>


#define INPUT_BUF_SIZE 256


void error(const char* message, ...) {
    va_list args;
    va_start(args, message);

    fprintf(stderr, "error: ");
    vfprintf(stderr, message, args);
    fprintf(stderr, "\n");

    va_end(args);

    exit(1);
}

bound bounds_check(int index, u64 length) {
    bound b = { .length = length, .index = index, .out_of_bounds = false };
    if (b.index < 0)
        b.index = b.length + b.index;

    if ((u64)(b.index) >= b.length) {
        b.out_of_bounds = true;
    }

    return b;
}


nil print_literal(string s) {
    printf("%s", (char*)s.ptr);
    return NIL;
}

string input(void) {
    static u8 buf[INPUT_BUF_SIZE];
    fgets((char*)buf, INPUT_BUF_SIZE, stdin);
    return string_new((u8*)buf, strlen((char*)buf));
}

string input_0(string prompt) {
    printf("%s", prompt.ptr);
    return input();
}

nil assert(bool condition, string error_message) {
    if (condition) return NIL;

    error("%s", (char*)error_message.ptr);
    return NIL;
}


pointer heap_alloc(u64 size) {
    pointer ptr = (pointer)malloc(size);
    if (ptr == NIL) error("out of memory");

    return ptr;
}

void heap_free(pointer ptr) {
    if (ptr == NIL) return;
    free(ptr);
    return;
}

pointer heap_zero_alloc(u64 count, u64 size) {
    pointer ptr = (pointer)calloc(count, size);
    if (ptr == NIL) error("out of memory");

    return ptr;
}

pointer heap_realloc(pointer ptr, u64 size) {
    pointer reallocated_ptr = (pointer)realloc(ptr, size);
    if (reallocated_ptr == NIL) error("out of memory");

    return reallocated_ptr;
}
