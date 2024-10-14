#ifndef CURE_HEADER_H
#define CURE_HEADER_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include "./osarch_check.h"

#if OS_WINDOWS
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
#elif OS_MAC
#include <unistd.h>

#define OS "Mac"
#define IS_ADMIN geteuid() == 0
#elif OS_LINUX
#include <unistd.h>

#define OS "Linux"
#define IS_ADMIN geteuid() == 0
#else
#error "Unsupported operating system"
#endif

#if ARCH_x86_64
#define ARCH "x86_64"
#elif ARCH_x86
#define ARCH "x86"
#elif ARCH_arm64
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
  int top, bottom;
} Fraction;

typedef struct {
  float x, y;
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

  int saved_stdout_fd;
  HANDLE hRead;
  HANDLE hWrite;
} StringBuilder;

typedef struct {
#if OS_WINDOWS
  LARGE_INTEGER start;
  LARGE_INTEGER end;
  LARGE_INTEGER frequency;
#elif OS_LINUX
  struct timespec start;
  struct timespec end;
#endif
  bool is_running;
} Timer;

typedef struct {
  FILE* out;
  string path;
} Logger;

const int MIN_INT = -2147483648;
const int MAX_INT = 2147483647;
const string DIGITS = "0123456789";
const string PUNCTUATION = "!@#$%^&*()_+-=[]{};:'\"\\|,.<>/?";
const string LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
const string VERSION = "0.0.4";
const float MIN_FLOAT = -1.701411733192644277e+38;
const float MAX_FLOAT = 1.701411733192644277e+38;
const int ONE_BILLION = 1000000000;
const int ONE_MILLION = 1000000;
const int ONE_THOUSAND = 1000;

#ifdef __cplusplus
}
#endif

#endif
