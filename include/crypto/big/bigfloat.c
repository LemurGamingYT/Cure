#include "big.h"
#include <stdlib.h>
#include <string.h>

int bigfloat_init(BigFloat* bigfloat, const char* int_part, const char* frac_part, int exp) {
    bigint_init(&bigfloat->integer_part, int_part);
    bigint_init(&bigfloat->fractional_part, frac_part);
    bigfloat->exponent = exp;
    return 0;
}

void bigfloat_free(BigFloat* bigfloat) {
    bigint_free(&bigfloat->integer_part);
    bigint_free(&bigfloat->fractional_part);
}

char* bigfloat_string(const BigFloat* bigfloat) {
    char* int_part = bigint_string(&bigfloat->integer_part);
    char* frac_part = bigint_string(&bigfloat->fractional_part);
    char* result = (char*)malloc(strlen(int_part) + strlen(frac_part) + 2); // +2 for decimal point and null terminator
    if (result == NULL)
        return NULL;

    strcpy(result, int_part);
    strcat(result, ".");
    strcat(result, frac_part);

    free(int_part);
    free(frac_part);
    return result;
}

int bigfloat_add(BigFloat* result, const BigFloat* a, const BigFloat* b) {
    // Add integer parts
    bigint_add(&result->integer_part, &a->integer_part, &b->integer_part);
    
    // Add fractional parts
    bigint_add(&result->fractional_part, &a->fractional_part, &b->fractional_part);
    
    // Handle carry from fractional to integer part
    if (result->fractional_part.length > a->fractional_part.length) {
        BigInt carry;
        char carry_digit[] = "1";
        bigint_init(&carry, carry_digit);
        bigint_add(&result->integer_part, &result->integer_part, &carry);
        bigint_free(&carry);
    }
    
    // Adjust exponent
    result->exponent = (a->exponent > b->exponent) ? a->exponent : b->exponent;
    return 0;
}

int bigfloat_mul(BigFloat* result, const BigFloat* a, const BigFloat* b) {
    // Multiply integer parts
    bigint_mul(&result->integer_part, &a->integer_part, &b->integer_part);
    
    // Handle fractional multiplication
    BigInt temp1, temp2, temp3;
    
    // Integer * fractional
    bigint_mul(&temp1, &a->integer_part, &b->fractional_part);
    bigint_mul(&temp2, &b->integer_part, &a->fractional_part);
    
    // Fractional * fractional
    bigint_mul(&temp3, &a->fractional_part, &b->fractional_part);
    
    // Combine results
    bigint_add(&result->fractional_part, &temp1, &temp2);
    bigint_add(&result->fractional_part, &result->fractional_part, &temp3);
    
    // Clean up
    bigint_free(&temp1);
    bigint_free(&temp2);
    bigint_free(&temp3);
    
    // Set exponent
    result->exponent = a->exponent + b->exponent;
    return 0;
}

int bigfloat_div(BigFloat* result, const BigFloat* a, const BigFloat* b) {
    const int PRECISION = 100;
    
    // Convert to scaled integers for division
    BigInt scaled_a, scaled_b;
    
    // Scale a
    char* scaled_str_a = malloc(a->integer_part.length + a->fractional_part.length + PRECISION + 1);
    sprintf(scaled_str_a, "%s%s", a->integer_part.digits, a->fractional_part.digits);
    bigint_init(&scaled_a, scaled_str_a);
    
    // Scale b
    char* scaled_str_b = malloc(b->integer_part.length + b->fractional_part.length + 1);
    sprintf(scaled_str_b, "%s%s", b->integer_part.digits, b->fractional_part.digits);
    bigint_init(&scaled_b, scaled_str_b);
    
    // Perform division
    BigInt quotient;
    bigint_div(&quotient, &scaled_a, &scaled_b);
    
    // Split result into integer and fractional parts
    int split_point = quotient.length - PRECISION;
    char* int_part = malloc(split_point + 1);
    char* frac_part = malloc(PRECISION + 1);
    
    strncpy(int_part, quotient.digits, split_point);
    int_part[split_point] = '\0';
    
    strncpy(frac_part, quotient.digits + split_point, PRECISION);
    frac_part[PRECISION] = '\0';
    
    bigint_init(&result->integer_part, int_part);
    bigint_init(&result->fractional_part, frac_part);
    
    // Clean up
    free(int_part);
    free(frac_part);
    free(scaled_str_a);
    free(scaled_str_b);
    bigint_free(&scaled_a);
    bigint_free(&scaled_b);
    bigint_free(&quotient);
    
    // Set exponent
    result->exponent = a->exponent - b->exponent;
    return 0;
}

int bigfloat_eq(const BigFloat* a, const BigFloat* b) {
    return bigint_eq(&a->integer_part, &b->integer_part) &&
           bigint_eq(&a->fractional_part, &b->fractional_part) &&
           a->exponent == b->exponent;
}
