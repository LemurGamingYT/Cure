#include <stdio.h>

typedef unsigned char byte;
typedef byte* bytes;

int main() {
    byte a[] = {'a', 'b', 'c', '\0'};
    printf("%s\n", a);
    return 0;
}
