#include "big.h"

#include <stdlib.h>
#include <string.h>


int bigint_init(BigInt* bigint, const char* digits) {
    bigint->digits = strdup(digits);
    bigint->length = strlen(digits);
    return 0;
}

void bigint_free(BigInt* bigint) {
    free(bigint->digits);
}

char* bigint_string(const BigInt* bigint) {
    return strdup(bigint->digits);
}

int bigint_add(BigInt* result, const BigInt* a, const BigInt* b) {
    int max_len = (a->length > b->length) ? a->length : b->length;
    char* sum = (char*)malloc(max_len + 2); // +2 for potential carry and null terminator
    if (sum == NULL)
        return 1;
    
    int carry = 0;
    int i = a->length - 1;
    int j = b->length - 1;
    int k = max_len;
    
    sum[max_len + 1] = '\0';
    
    while (i >= 0 || j >= 0 || carry) {
        int digit_a = (i >= 0) ? a->digits[i] - '0' : 0;
        int digit_b = (j >= 0) ? b->digits[j] - '0' : 0;
        int total = digit_a + digit_b + carry;
        
        carry = total / 10;
        sum[k] = (total % 10) + '0';
        
        i--; j--; k--;
    }
    
    // Skip leading zeros
    char* final_result = sum + k + 1;
    result->digits = strdup(final_result);
    result->length = strlen(result->digits);
    
    free(sum);
    return 0;
}

int bigint_sub(BigInt* result, const BigInt* a, const BigInt* b) {
    int max_len = a->length;
    char* diff = (char*)malloc(max_len + 1);
    if (diff == NULL)
        return 1;
    
    int borrow = 0;
    int i = a->length - 1;
    int j = b->length - 1;
    int k = max_len - 1;
    
    diff[max_len] = '\0';
    
    while (i >= 0) {
        int digit_a = a->digits[i] - '0';
        int digit_b = (j >= 0) ? b->digits[j] - '0' : 0;
        
        digit_a -= borrow;
        if (digit_a < digit_b) {
            digit_a += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }
        
        diff[k] = (digit_a - digit_b) + '0';
        i--; j--; k--;
    }
    
    // Skip leading zeros
    char* start = diff;
    while (*start == '0' && *(start + 1) != '\0') start++;
    
    result->digits = strdup(start);
    result->length = strlen(result->digits);
    
    free(diff);
    return 0;
}

int bigint_mul(BigInt* result, const BigInt* a, const BigInt* b) {
    int len = a->length + b->length;
    char* product = (char*)calloc(len + 1, sizeof(char));
    if (product == NULL)
        return 1;
    
    for (int i = a->length - 1; i >= 0; i--) {
        for (int j = b->length - 1; j >= 0; j--) {
            int digit_a = a->digits[i] - '0';
            int digit_b = b->digits[j] - '0';
            int pos1 = i + j;
            int pos2 = i + j + 1;
            
            int mul = digit_a * digit_b;
            int sum = mul + (product[pos2] - '0');
            
            product[pos2] = (sum % 10) + '0';
            product[pos1] += sum / 10;
        }
    }
    
    // Skip leading zeros
    char* start = product;
    while (*start == '0' && *(start + 1) != '\0') start++;
    
    result->digits = strdup(start);
    result->length = strlen(result->digits);
    
    free(product);
    return 0;
}

int bigint_div(BigInt* result, const BigInt* a, const BigInt* b) {
    // Simple implementation - can be optimized
    BigInt current;
    int ret;
    ret = bigint_init(&current, "0");
    if (ret != 0)
        return ret;
    
    while (bigint_sub(result, a, &current) >= 0) {
        BigInt temp;
        ret = bigint_add(&temp, &current, b);
        if (ret != 0)
            return ret;
        
        bigint_free(&current);
        current = temp;
    }
    
    bigint_free(&current);
    return 0;
}

int bigint_mod(BigInt* result, const BigInt* a, const BigInt* b) {
    BigInt div_result;
    int ret;
    ret = bigint_div(&div_result, a, b);
    if (ret != 0)
        return ret;
    
    BigInt mul_result;
    ret = bigint_mul(&mul_result, &div_result, b);
    if (ret != 0)
        return ret;
    
    ret = bigint_sub(result, a, &mul_result);
    if (ret != 0)
        return ret;
    
    bigint_free(&div_result);
    bigint_free(&mul_result);
    return 0;
}

int bigint_eq(const BigInt* a, const BigInt* b) {
    if (a->length != b->length)
        return 1;
    
    return strcmp(a->digits, b->digits) == 0;
}
