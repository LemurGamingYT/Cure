#include "../include/cwalk/cwalk.h"

#include <stdlib.h>
#include <string.h>
#include <stdio.h>


typedef struct {
    char* path;
} File;


int main() {
    const char* path = "examples/";
    const char* ext;
    if (cwk_path_get_extension(path, &ext, NULL)) {
        printf("%s\n", ext);
    } else {
        printf("No extension\n");
    }

    const char* basename;
    cwk_path_get_basename(path, &basename, NULL);
    printf("%s\n", basename);

    char* dirname;
    size_t dirname_length;
    cwk_path_get_dirname(path, &dirname_length);
    if (dirname_length > 0) {
        dirname = malloc(dirname_length + 1);
        memcpy(dirname, path, dirname_length);
        dirname[dirname_length] = '\0';
        printf("%s\n", dirname);
        free(dirname);
    } else {
        printf("No dirname\n");
    }

    bool is_absolute = cwk_path_is_absolute(path);
    printf("%d\n", is_absolute);

    struct cwk_segment first;
    cwk_path_get_first_segment(path, &first);
    printf("%s\n", first.end);

    struct cwk_segment last;
    cwk_path_get_last_segment(path, &last);
    printf("%s\n", last.end);
    return 0;
}
