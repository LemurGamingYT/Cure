#include "builtins.h"

#include <string.h>
#include <limits.h>
#include <math.h>


int int_add_int(int a, int b) {
    if ((b > 0 && a > INT_MAX - b) || (b < 0 && a < INT_MIN - b)) error("integer overflow");
    return a + b;
}

float float_add_float(float a, float b) {
    float res = a + b;
    if (isinf(res)) error("float overflow");
    return res;
}

string string_add_string(string a, string b) {
    u64 length = a.length + b.length;
    u8* ptr = (u8*)heap_alloc(length + 1);
    memcpy(ptr, a.ptr, a.length);
    memcpy(ptr + a.length, b.ptr, b.length);
    ptr[length] = (u8)'\0';
    
    return string_new(ptr, length);
}

int int_sub_int(int a, int b) {
    if ((b > 0 && a < INT_MIN + b) || (b < 0 && a > INT_MAX + b)) error("integer overflow");
    return a - b;
}

float float_sub_float(float a, float b) {
    float res = a - b;
    if (isinf(res)) error("float overflow");
    return res;
}

int int_mul_int(int a, int b) {
    if (a > 0) {
        if (b > 0 && a > INT_MAX / b) error("integer overflow");
        if (b < INT_MIN / a) error("integer overflow");
    } else {
        if (b > 0 && a < INT_MIN / b) error("integer overflow");
        if (a != 0 && b < INT_MAX / a) error("integer overflow");
    }
    
    return a * b;
}

float float_mul_float(float a, float b) {
    float res = a * b;
    if (isinf(res)) error("float overflow");

    return res;
}

int int_div_int(int a, int b) {
    if (b == 0) error("integer division by zero");
    return a / b;
}

float float_div_float(float a, float b) {
    if (b == 0.0f) error("float division by zero");
    return a / b;
}

int int_mod_int(int a, int b) {
    if (b == 0) error("integer modulo by zero");
    return a % b;
}

float float_mod_float(float a, float b) {
    if (b == 0.0f) error("float modulo by zero");
    return fmod(a, b);
}

int int_post_inc(int* a) { return (*a)++; }
int int_pre_inc(int* a) { return ++(*a); }

bool int_eq_int(int a, int b) { return a == b; }
bool float_eq_float(float a, float b) { return a == b; }
bool string_eq_string(string a, string b) { return memcmp(a.ptr, b.ptr, a.length > b.length ? a.length : b.length) == 0; }
bool bool_eq_bool(bool a, bool b) { return a == b; }
bool int_neq_int(int a, int b) { return a != b; }
bool float_neq_float(float a, float b) { return a != b; }
bool string_neq_string(string a, string b) { return memcmp(a.ptr, b.ptr, a.length > b.length ? a.length : b.length) != 0; }
bool bool_neq_bool(bool a, bool b) { return a != b; }
int int_lt_int(int a, int b) { return a < b; }
float float_lt_float(float a, float b) { return a < b; }
int int_gt_int(int a, int b) { return a > b; }
float float_gt_float(float a, float b) { return a > b; }
int int_lte_int(int a, int b) { return a <= b; }
float float_lte_float(float a, float b) { return a <= b; }
int int_gte_int(int a, int b) { return a >= b; }
float float_gte_float(float a, float b) { return a >= b; }
bool bool_and_bool(bool a, bool b) { return a && b; }
bool bool_or_bool(bool a, bool b) { return a || b; }
bool not_bool(bool a) { return !a; }
