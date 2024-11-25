#include <stdio.h>
#include <stdlib.h>
#include <locale.h>


int main(void) {
    wchar_t *s;
    s = (wchar_t *) malloc(sizeof(wchar_t) * 2);
    s[0] = 0xC389;
    s[1] = 0;

    setlocale(LC_ALL, "");

    if (printf("%ls\n", s) < 0) {
        perror("printf");
    }

    free(s);
    return 0;
}
