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
srand(time(NULL));
#if OS_WINDOWS
    SetConsoleOutputCP(CP_UTF8);
#else
    setlocale(LC_ALL, "en_US.UTF-8");
#endif
}

void deinit() {
    free(args.elements);
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
