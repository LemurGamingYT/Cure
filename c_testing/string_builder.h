#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#include <stdlib.h>
#include <string.h>

#include "utils.h"


typedef struct {
    char* buf;
    size_t length;
    size_t capacity;
} StringBuilder;


StringBuilder sb_new(size_t capacity) {
    return (StringBuilder){ .capacity = capacity, .length = 0, .buf = (char*)malloc(capacity) };
}

void sb_add(StringBuilder* sb, const char* str) {
    size_t len = strlen(str);
    if (sb->capacity - sb->length < len) {
        sb->capacity *= 2;
        sb->buf = (char*)realloc(sb->buf, sb->capacity);
    }

    memcpy(sb->buf + sb->length, str, len);
    sb->length += len;
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


void benchmark(StringBuilder* sb) {
    for (int i = 0; i < 10000000; i++) {
        sb_add(sb, "hello");
    }
}


/*int main() {
    StringBuilder sb = sb_new(100000000);
    if (sb.buf == NULL) {
        printf("error: out of memory\n");
        return 1;
    }

    TIME_FUNC(benchmark(&sb));

    printf("Length: %zu\n", sb.length);
    sb_destroy(&sb);
    return 0;
}*/

#ifdef __cplusplus
}
#endif
