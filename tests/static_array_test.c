#include "static_array.h"

static_array(u8, 10)
print(int)


int main(void) {
    array_u8_10 arr = array_u8_10_new();
    array_u8_10_set(&arr, 0, 1);
    array_u8_10_set(&arr, 1, 2);
    array_u8_10_set(&arr, 2, 3);
    array_u8_10_set(&arr, 3, 4);
    array_u8_10_set(&arr, 4, 5);
    array_u8_10_set(&arr, 5, 6);
    array_u8_10_set(&arr, 6, 7);
    array_u8_10_set(&arr, 7, 8);

    print_int(array_u8_10_get(&arr, 0));
    print_int(array_u8_10_get(&arr, 1));

    // No destroy method! It's on the stack!
    return 0;
}
