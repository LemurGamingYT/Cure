#include <stdbool.h>
#include <stdio.h>


// TODO: Make generators easier to use and less error prone


#define make_gen(type) typedef struct { type state; type (*next)(type); } type##Generator;\
type##Generator make_##type##_gen(type (*next)(type)) {\
    return (type##Generator){ .next = next, .state = 0 };\
}\
type next_##type##_gen(type##Generator* gen) {\
    type next = gen->next(gen->state); gen->state++; return next;\
}

int fib(int n) {
    return n <= 1 ? n : fib(n - 1) + fib(n - 2);
}

bool is_prime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }

    return true;
}

int prime(int n) {
    while (!is_prime(n)) n++;
    return n;
}

int lucas(int n) {
    if (n == 0) return 2;
    if (n == 1) return 1;
    return lucas(n - 1) + lucas(n - 2);
}


make_gen(int)
int main() {
    int n = 25;

    printf("Fibonacci sequence\n");
    intGenerator fibgen = make_int_gen(fib);
    for (int i = 0; i < n; i++) {
        printf("%d\n", next_int_gen(&fibgen));
    }

    /*printf("\nPrime Numbers:\n");
    intGenerator primegen;
    init_int_gen(&primegen, prime);
    for (int i = 0; i < n; i++) {
        printf("%d\n", next_int_gen(&primegen));
    }*/

    printf("\nLucas Numbers:\n");
    intGenerator lucasgen = make_int_gen(lucas);
    for (int i = 0; i < n; i++) {
        printf("%d\n", next_int_gen(&lucasgen));
    }

    return 0;
}
