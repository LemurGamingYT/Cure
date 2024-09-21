#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#include <stdlib.h>
#include <stdarg.h>
#include <stdio.h>
#include <time.h>


#define TIME_FUNC(func){\
    clock_t start = clock();\
    func;\
    clock_t end = clock();\
    printf("%s took %fs\n", #func, ((double)(end - start)) / CLOCKS_PER_SEC);\
}

static char* allocate_fmt(const char* fmt, ...) {
    va_list args;
    va_start(args, fmt);
    size_t length = vsnprintf(NULL, 0, fmt, args);
    char* buf = (char*)malloc(length + 1);
    if (buf == NULL) {
        return NULL;
    }

    vsnprintf(buf, length + 1, fmt, args);
    va_end(args);
    return buf;
}

#ifdef __cplusplus
}
#endif
