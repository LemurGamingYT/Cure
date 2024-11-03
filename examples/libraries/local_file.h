#pragma once
#ifdef __cplusplus
extern "C" {
#endif
#include <stdbool.h>

#include <stdlib.h>

#include <stdio.h>

#include <time.h>

#ifndef __CURE_INIT__
#define __CURE_INIT__


#define OS_WINDOWS true
#define NOMINMAX
#define WIN32_LEAN_AND_MEAN
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <shlobj.h>
#include <fcntl.h>
#include <io.h>

#define OS "Windows"
#define IS_ADMIN IsUserAnAdmin()


#if defined(_M_X64) || defined(__x86_64__)
#define ARCH_x86_64 1
#define ARCH "x86_64"
#elif defined(_M_IX86) || defined(__i386__)
#define ARCH_x86 1
#define ARCH "x86"
#elif defined(_M_ARM64) || defined(__aarch64__)
#define ARCH_arm64 1
#define ARCH "arm64"
#else
#error "Unsupported architecture"
#endif


typedef void* hex;
typedef char* string;
typedef void* nil;
typedef unsigned char byte;

const int MIN_INT = -2147483648;
const int MAX_INT = 2147483647;
const string DIGITS = "0123456789";
const string PUNCTUATION = "!@#$%^&*()_+-=[]{};:'\"\\|,.<>/?";
const string LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
const string VERSION = "0.0.51";
const float MIN_FLOAT = -1.701411733192644277e+38;
const float MAX_FLOAT = 1.701411733192644277e+38;
const int ONE_BILLION = 1000000000;
const int ONE_MILLION = 1000000;
const int ONE_THOUSAND = 1000;


typedef struct {
    byte _;
} Math;

typedef struct {
    int top, bottom;
} Fraction;

typedef struct {
    float x, y;
} Vector2;


typedef struct {
    byte _;
} Cure;


typedef struct {
    FILE* out;
    string path;
} Logger;


typedef struct {
    byte _;
} System;

typedef struct {
    time_t t;
    struct tm *ti;
} Time;


typedef struct {
    string buf;
    size_t length, capacity;
    int saved_stdout_fd;
    HANDLE hRead, hWrite;
} StringBuilder;


typedef struct {
    LARGE_INTEGER start, end, frequency;
    bool is_running;
} Timer;


#endif

typedef int (*__temp67)();



int test1(void) {



return 10;
}
;
int test2(int x) {



return ((x) + (test1()));
}
;
#ifdef __cplusplus
}
#endif
