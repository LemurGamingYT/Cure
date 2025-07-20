#include "builtins/builtins.h"

#include <string.h>


typedef struct {
    pointer ptr;
    u64 size;
} Pointer;

Pointer Pointer_new(u64 size) { return (Pointer){ .ptr = heap_alloc(size), .size = size }; }
pointer Pointer_read(Pointer* self) { return self->ptr; }

nil Pointer_free(Pointer* self) {
    heap_free(self->ptr);
    return NIL;
}

nil Pointer_write(Pointer* self, pointer data) {
    memcpy(self->ptr, data, self->size);
    return NIL;
}

int main(void) {
    Pointer ptr = Pointer_new(10);
    
    int x = 5;
    Pointer_write(&ptr, (pointer)&x);

    int read_ptr = *(int*)Pointer_read(&ptr);
    printf("%d\n", read_ptr); // 5

    Pointer_free(&ptr);
    return 0;
}
