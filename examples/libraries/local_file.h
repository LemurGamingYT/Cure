#pragma once
#ifdef __cplusplus
extern "C" {
#endif
#include "C:/Programming/Python/Cure/include/header.h"
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#ifndef _CURE_INITIALISED

typedef struct {
    string* elements;
    size_t length;
    size_t capacity;
} string_array;

string_array args;
void init() {
string_array __temp0 = {
    .length = 0, .capacity = 10,
    .elements = (string*)malloc(sizeof(string) * 10)
};
int __temp2 = __argc;
if (__temp2 > 0) {
    for (int __temp1 = 0; __temp1 <= __temp2; __temp1++) {
        if (__temp0.length == __temp0.capacity) {
            __temp0.capacity *= 2;
            __temp0.elements = (string*)realloc(
                __temp0.elements, sizeof(string) * __temp0.capacity
            );
        }
        
        __temp0.elements[__temp1] = __argv[__temp1];
        __temp0.length++;
    }
}

args = __temp0;
srand(time(NULL));
}

#define _CURE_INITIALISED
#endif

int test() {




return 10;
}
;
int test2(int x) {




return ((x) + (test()));
}
;
#ifdef __cplusplus
}
#endif
