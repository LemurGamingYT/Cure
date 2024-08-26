#pragma once


#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#if defined(_WIN32) || defined(_WIN64)
#define OS_WINDOWS
#define OS "Windows"
#define NOMINMAX
#include <io.h>
#include <windows.h>
#elif defined(__APPLE__)
#define OS_MAC
#define OS "Mac"
#include <unistd.h>
#elif defined(__linux__)
#define OS_LINUX
#define OS "Linux"
#include <unistd.h>
#else
#error "Unsupported operating system"
#endif

#if defined(_M_X64)
#define ARCH_x86_64
#define ARCH "x86_64"
#elif defined(_M_IX86)
#define ARCH_x86
#define ARCH "x86"
#elif defined(_M_ARM64)
#define ARCH_arm64
#define ARCH "arm64"
#else
#error "Unsupported architecture"
#endif

typedef struct {
  unsigned char _;
} Math;
typedef struct {
  unsigned char _;
} System;
typedef struct {
  time_t t;
  struct tm *ti;
} Time;

typedef char* string;
typedef void* nil;
const int MIN_INT = -2147483648;
const int MAX_INT = 2147483647;
const string DIGITS = "0123456789";
const string PUNCTUATION = "!@#$%^&*()_+-=[]{};:'\"\\|,.<>/?";
const string LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
const string VERSION = "0.0.21";
const float MIN_FLOAT = -1.701411733192644277e+38;
const float MAX_FLOAT = 1.701411733192644277e+38;
const int ONE_BILLION = 1000000000;
const int ONE_MILLION = 1000000;
const int ONE_THOUSAND = 1000;
