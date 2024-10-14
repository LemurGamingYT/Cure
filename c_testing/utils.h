#ifndef CURE_UTILS_TESTING_H
#define CURE_UTILS_TESTING_H

#ifdef __cplusplus
extern "C" {
#endif

#include <assert.h>
#include <stdint.h>
#include <stddef.h>
#include <stdarg.h>

#include "../include/header.h"


void timer_start(Timer* timer) {
#if OS_WINDOWS
    QueryPerformanceFrequency(&timer->frequency);
    QueryPerformanceCounter(&timer->start);
#elif OS_LINUX
    clock_gettime(CLOCK_MONOTONIC, &timer->start);
#endif
}

void timer_stop(Timer* timer) {
#if OS_WINDOWS
    QueryPerformanceCounter(&timer->end);
#elif OS_LINUX
    clock_gettime(CLOCK_MONOTONIC, &timer->end);
#endif
}

double timer_get_elapsed_ns(const Timer* timer) {
#if OS_WINDOWS
    LARGE_INTEGER elapsed;
    elapsed.QuadPart = timer->end.QuadPart - timer->start.QuadPart;
    return (double)elapsed.QuadPart * 1e9 / timer->frequency.QuadPart;
#elif OS_LINUX
    return (timer->end.tv_sec - timer->start.tv_sec) * 1e9 +
        (timer->end.tv_nsec - timer->start.tv_nsec);
#endif
}

double timer_get_elapsed_us(const Timer* timer) {
    return timer_get_elapsed_ns(timer) / 1e3;
}

double timer_get_elapsed_ms(const Timer* timer) {
    return timer_get_elapsed_ns(timer) / 1e6;
}

double timer_get_elapsed_s(const Timer* timer) {
    return timer_get_elapsed_ns(timer) / 1e9;
}

void error(const char* msg, ...) {
    va_list args;
    va_start(args, msg);
    printf("Error: ");
    vprintf(msg, args);
    printf("\n");
    va_end(args);
    exit(1);
}

#define TIME_FUNC(func){\
    Timer timer;\
    timer_start(&timer);\
    func;\
    timer_end(&timer);\
    printf("%s took %fms\n", #func, timer_get_elapsed_ms(&timer));\
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
