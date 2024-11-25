#ifndef BIG_H
#define BIG_H

#include <stddef.h>


typedef struct {
    char *digits;
    size_t length;
} BigInt;

typedef struct {
    BigInt integer_part;
    BigInt fractional_part;
    int exponent;
} BigFloat;


int bigint_init(BigInt* bigint, const char* digits);
void bigint_free(BigInt* bigint);
char* bigint_string(const BigInt* bigint);
int bigint_add(BigInt* result, const BigInt* a, const BigInt* b);
int bigint_sub(BigInt* result, const BigInt* a, const BigInt* b);
int bigint_mul(BigInt* result, const BigInt* a, const BigInt* b);
int bigint_div(BigInt* result, const BigInt* a, const BigInt* b);
int bigint_mod(BigInt* result, const BigInt* a, const BigInt* b);
int bigint_eq(const BigInt* a, const BigInt* b);

int bigfloat_init(BigFloat* bigfloat, const char* digits);
void bigfloat_free(BigFloat* bigfloat);
char* bigfloat_string(const BigFloat* bigfloat);
int bigfloat_add(BigFloat* result, const BigFloat* a, const BigFloat* b);
int bigfloat_sub(BigFloat* result, const BigFloat* a, const BigFloat* b);
int bigfloat_mul(BigFloat* result, const BigFloat* a, const BigFloat* b);
int bigfloat_div(BigFloat* result, const BigFloat* a, const BigFloat* b);
int bigfloat_mod(BigFloat* result, const BigFloat* a, const BigFloat* b);
int bigfloat_eq(const BigFloat* a, const BigFloat* b);


#endif
