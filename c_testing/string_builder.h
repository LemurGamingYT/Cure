#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#include <stdlib.h>
#include <string.h>

#include "../include/header.h"
#include "utils.h"

#if OS_WINDOWS
    #include <io.h>
    #include <fcntl.h>
#endif


StringBuilder sb_new(size_t capacity) {
    return (StringBuilder){ .capacity = capacity, .length = 0, .buf = (char*)malloc(capacity) };
}

void sb_add_len(StringBuilder* sb, const char* str, size_t len) {
    if (sb->capacity - sb->length < len) {
        while (sb->capacity + len > sb->capacity) {
            sb->capacity *= 2;
        }

        sb->buf = (char*)realloc(sb->buf, sb->capacity);
    }

    memcpy(sb->buf + sb->length, str, len);
    sb->length += len;
}

void sb_add(StringBuilder* sb, const char* str) {
    sb_add_len(sb, str, strlen(str));
}

char* sb_str(StringBuilder* sb) {
    sb->buf[sb->length] = '\0';
    return sb->buf;
}

void sb_destroy(StringBuilder* sb) {
    sb->capacity = 0;
    sb->length = 0;

    free(sb->buf);
    sb->buf = NULL;
}

void sb_capture_stdout(StringBuilder* sb) {
#if OS_WINDOWS
    HANDLE hRead, hWrite;

    if (!CreatePipe(&hRead, &hWrite, NULL, 0)) {
        error("CreatePipe failed");
    }

    int saved_stdout_fd = _dup(_fileno(stdout));
    int pipe_write_fd = _open_osfhandle((intptr_t)hWrite, _O_WRONLY);
    _dup2(pipe_write_fd, _fileno(stdout));

    sb->saved_stdout_fd = saved_stdout_fd;
    sb->hRead = hRead;
    sb->hWrite = hWrite;
#endif
}

void sb_release_stdout(StringBuilder* sb) {
#if OS_WINDOWS
    fflush(stdout);
    _dup2(sb->saved_stdout_fd, _fileno(stdout));
    close(sb->saved_stdout_fd);

    DWORD bytes_read;
    if (!ReadFile(sb->hRead, sb->buf, sb->capacity, &bytes_read, NULL)) {
        error("ReadFile failed");
    }

    sb->length += bytes_read;

    CloseHandle(sb->hRead);
    CloseHandle(sb->hWrite);
    sb->saved_stdout_fd = 0;
    sb->hRead = NULL;
    sb->hWrite = NULL;
#endif
}


#ifdef __cplusplus
}
#endif
