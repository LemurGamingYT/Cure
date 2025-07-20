#include "builtins.h"

#include <stdlib.h>

#if WINDOWS
#include <windows.h>
#include <direct.h>
#define sleep(ms) Sleep(ms)
#define getpid GetCurrentProcessId
#define getcwd _getcwd

#define OS_NAME "Windows"
#elif LINUX
#include <unistd.h>
#define sleep(ms) usleep((ms) * 1000)

#define OS_NAME "Linux"
#else
#error Not implemented target.
#endif


string System_os(void) { return string_new(OS_NAME, sizeof(OS_NAME) - 1); }
int System_pid(void) { return getpid(); }
int System_processor_count(void) {
#if WINDOWS
    SYSTEM_INFO si;
    GetSystemInfo(&si);
    return si.dwNumberOfProcessors;
#elif LINUX
    return sysconf(_SC_NPROCESSORS_ONLN);
#endif
}

string System_cwd(void) {
    static u8 buf[1024];
    getcwd(buf, sizeof(buf));
    return string_new(buf, sizeof(buf) - 1);
}

nil System_exit(int code) {
    exit(code);
    return NIL;
}

nil System_exit_0(void) {
    exit(0);
    return NIL;
}

nil System_sleep(int milliseconds) {
    sleep(milliseconds);
    return NIL;
}
