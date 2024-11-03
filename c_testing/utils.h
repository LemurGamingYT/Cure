#ifndef CURE_UTILS_TESTING_H
#define CURE_UTILS_TESTING_H

#ifdef __cplusplus
extern "C" {
#endif

#include <assert.h>
#include <stdint.h>
#include <stddef.h>
#include <stdarg.h>


void error(const char* msg, ...) {
    va_list args;
    va_start(args, msg);
    printf("Error: ");
    vprintf(msg, args);
    printf("\n");
    va_end(args);
    exit(1);
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

#endif
