#ifndef OS_CHECK_H
#define OS_CHECK_H


#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>


#if defined(_WIN32) || defined(_WIN64) || defined(_MSC_VER) || defined(WIN32)
#define OS_WINDOWS true
#elif defined(__APPLE__)
#define OS_MAC true
#elif defined(__linux__)
#define OS_LINUX true
#else
#error "Unsupported operating system"
#endif

#if defined(_M_X64) || defined(__x86_64__)
#define ARCH_x86_64 true
#elif defined(_M_IX86) || defined(__i386__)
#define ARCH_x86 true
#elif defined(_M_ARM64) || defined(__aarch64__)
#define ARCH_arm64 true
#else
#error "Unsupported architecture"
#endif


#ifdef __cplusplus
}
#endif


#endif
