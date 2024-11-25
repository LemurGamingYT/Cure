#include "../include/crypto/big/big.h"
#include "../include/crypto/crypto.h"

#include <stdlib.h>
#include <stdio.h>


int main() {
    BigInt a, b, result;
    int ret = bigint_init(&a, "8893490901589876543210");
    if (ret != 0)
        goto error;
    
    ret = bigint_init(&b, "9348681345092348690890");
    if (ret != 0)
        goto error;
    
    ret = bigint_add(&result, &a, &b);
    if (ret != 0)
        goto error;

    char* result_str = bigint_string(&result);
    printf("Addition Result: %s\n", result_str);

    free(result_str);
    bigint_free(&a);
    bigint_free(&b);
    bigint_free(&result);
    return 0;
error:
    fprintf(stderr, "Error code: %d\n", ret);
    return 1;
}
