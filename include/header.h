#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#if defined(_WIN32) || defined(_WIN64)
#define OS_WINDOWS 1
#define NOMINMAX
#define WIN32_LEAN_AND_MEAN
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <shlobj.h>
#include <io.h>

#define OS "Windows"
#define IS_ADMIN IsUserAnAdmin()
#elif defined(__APPLE__)
#define OS_MAC 1
#include <unistd.h>

#define OS "Mac"
#define IS_ADMIN geteuid() == 0
#elif defined(__linux__)
#define OS_LINUX 1
#include <unistd.h>

#define OS "Linux"
#define IS_ADMIN geteuid() == 0
#else
#error "Unsupported operating system"
#endif

#if defined(_M_X64)
#define ARCH_x86_64 1
#define ARCH "x86_64"
#elif defined(_M_IX86)
#define ARCH_x86 1
#define ARCH "x86"
#elif defined(_M_ARM64)
#define ARCH_arm64 1
#define ARCH "arm64"
#else
#error "Unsupported architecture"
#endif


typedef void* hex;
typedef char* string;
typedef void* nil;

typedef struct {
  unsigned char _;
} Math;

typedef struct {
  int top;
  int bottom;
} Fraction;

typedef struct {
  float x;
  float y;
} Vector2;

typedef struct {
  unsigned char _;
} System;

typedef struct {
  time_t t;
  struct tm *ti;
} Time;

typedef struct {
  unsigned char _;
} Cure;

typedef struct {
  string buf;
  size_t length;
  size_t capacity;
} StringBuilder;

const int MIN_INT = -2147483648;
const int MAX_INT = 2147483647;
const string DIGITS = "0123456789";
const string PUNCTUATION = "!@#$%^&*()_+-=[]{};:'\"\\|,.<>/?";
const string LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
const string VERSION = "0.0.32";
const float MIN_FLOAT = -1.701411733192644277e+38;
const float MAX_FLOAT = 1.701411733192644277e+38;
const int ONE_BILLION = 1000000000;
const int ONE_MILLION = 1000000;
const int ONE_THOUSAND = 1000;

#ifdef __cplusplus
}
#endif
