#include <stdlib.h>
#include <stdio.h>

#include "../include/binn/binn.h"


int main() {
    binn* b = binn_object();

    binn_object_set_int32(b, "test", 12);
    binn_object_set_str(b, "test2", "test");
    
    void* buf = binn_ptr(b);
    int size = binn_size(b);
    FILE* f = fopen("test.binn", "wb");
    if (f == NULL) {
        binn_free(b);
        return 1;
    }

    printf("%d\n", size);
    fwrite(buf, 1, size, f);

    fclose(f);

    FILE* f2 = fopen("test.binn", "rb");
    if (f2 == NULL) {
        binn_free(b);
        return 1;
    }

    fseek(f2, 0, SEEK_END);
    size = ftell(f2);
    fseek(f2, 0, SEEK_SET);
    void* buf2 = malloc(size);
    if (buf2 == NULL) {
        free(buf2);
        fclose(f2);
        binn_free(b);
        return 1;
    }

    fread(buf2, 1, size, f2);
    binn* b2 = binn_open(buf2);
    int value2;
    binn_object_get_int32(b2, "test", &value2);
    printf("%d\n", value2);

    free(buf2);
    fclose(f2);
    binn_free(b);
    binn_free(b2);
    return 0;
}
