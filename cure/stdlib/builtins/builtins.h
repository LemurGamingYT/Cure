#pragma once

#include <stdbool.h>
#include <stdio.h> // for puts


typedef void* nil;
typedef void* pointer;
typedef unsigned char u8;
typedef unsigned long long u64;

typedef nil (*RefFunction)(pointer);

#define NIL ((nil)0)


typedef struct {
    pointer data;
    u64 ref_count;
    RefFunction destroy_fn;
} Ref;

typedef struct {
    u8* ptr;
    u64 length;
    Ref* ref;
} string;

typedef struct {
    int index;
    u64 length;
    bool out_of_bounds;
} bound;


void error(const char* message, ...);
bound bounds_check(int index, u64 length);
pointer heap_alloc(u64 size);
void heap_free(pointer ptr);
pointer heap_zero_alloc(u64 count, u64 size);
pointer heap_realloc(pointer ptr, u64 size);


Ref* Ref_new(pointer data, RefFunction destroy_fn);
nil Ref_inc(Ref* ref);
nil Ref_dec(Ref* ref);

int int_min(void);
int int_max(void);

float float_min(void);
float float_max(void);

string string_new(const u8* ptr, u64 length);
int string_length(string self);
nil string_destroy(string* s);
string string_clone(string self);
nil string_set(string* self, int index, string ch);
string string_at(string self, int index);


string int_to_string(int i);
string float_to_string(float f);
string string_to_string(string s);
string bool_to_string(bool b);
string nil_to_string(nil n);


#define print(T)\
    nil print_##T(T x) {\
        string x_str = T##_to_string(x);\
        puts((char*)x_str.ptr);\
        string_destroy(&x_str);\
        return NIL;\
    }

nil print_literal(string s);
string input(void);
string input_0(string prompt);
nil assert(bool condition, string error_message);


int int_add_int(int a, int b);
float float_add_float(float a, float b);
string string_add_string(string a, string b);
int int_sub_int(int a, int b);
float float_sub_float(float a, float b);
int int_mul_int(int a, int b);
float float_mul_float(float a, float b);
int int_div_int(int a, int b);
float float_div_float(float a, float b);
int int_mod_int(int a, int b);
float float_mod_float(float a, float b);
bool int_eq_int(int a, int b);
bool float_eq_float(float a, float b);
bool string_eq_string(string a, string b);
bool bool_eq_bool(bool a, bool b);
bool int_neq_int(int a, int b);
bool float_neq_float(float a, float b);
bool string_neq_string(string a, string b);
bool bool_neq_bool(bool a, bool b);
int int_lt_int(int a, int b);
float float_lt_float(float a, float b);
int int_gt_int(int a, int b);
float float_gt_float(float a, float b);
int int_lte_int(int a, int b);
float float_lte_float(float a, float b);
int int_gte_int(int a, int b);
float float_gte_float(float a, float b);
bool bool_and_bool(bool a, bool b);
bool bool_or_bool(bool a, bool b);
bool not_bool(bool a);
