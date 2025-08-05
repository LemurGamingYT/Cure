#pragma once

#include <iostream>
#include <sstream>
#include <limits>
#include <string>
#include <vector>

#define _USE_MATH_DEFINES
#include <math.h>


using nil = std::nullptr_t;


void error(const char* s) {
    std::cerr << "error:" << s << std::endl;
    std::exit(1);
}


class string : public std::string {
public:
    string(std::string s) : std::string(s) {}
    string(char c) : std::string(1, c) {}
    string(const char* s) : std::string(s) {}
    string() : std::string() {}

    string get(int index) {
        if (index < 0)
            index = static_cast<int>(length()) + index;
        
        if (index >= static_cast<int>(length()))
            error("string index out of range");
        
        return (*this)[index];
    }

    nil set(int index, string s) {
        if (s.length() != 1)
            error("set expects a string character");
        
        if (index < 0)
            index = static_cast<int>(length()) + index;
        
        if (index >= static_cast<int>(length()))
            error("string index out of range");
        
        (*this)[index] = s[0];
        return nil();
    }
};


class StringBuilder {
public:
    std::stringstream ss;

    StringBuilder() {}

    string str() const { return string(ss.str()); }

    template<typename T>
    nil add(const T& item) {
        ss << to_string(item);
        return nil();
    }
};

template<typename T>
class array : public std::vector<T> {
public:
    array(std::initializer_list<T> init) : std::vector<T>(init) {}
    array() : std::vector<T>() {}
    
    int length() const { return this->size(); }
    
    nil add(T item) {
        this->push_back(item);
        return nil();
    }
    
    T get(int index) const {
        if (index < 0)
        index = length() + index;
        
        if (index >= length())
        error("index out of range");
        
        return (*this)[index];
    }
    
    nil set(int index, T item) {
        if (index < 0)
        index = length() + index;
        
        if (index >= length())
            error("array index out of range");

        (*this)[index] = item;
        return nil();
    }
};


void error(const string& s) { error(s.c_str()); }


string to_string(int i) { return std::to_string(i); }
string to_string(float f) { return std::to_string(f); }
string to_string(const string& s) { return s; }
string to_string(bool b) { return b ? "true" : "false"; }
string to_string(nil _) { return (string)"nil"; }
string to_string(const StringBuilder& sb) { return sb.ss.str(); }

template<typename T>
string to_string(const array<T>& arr) {
    std::stringstream ss;
    ss << '[';
    for (int i = 0; i < arr.length(); ++i) {
        ss << to_string(arr.get(i));
        if (i < arr.length() - 1)
            ss << ", ";
    }

    ss << ']';
    return ss.str();
}

int int_max(void) { return std::numeric_limits<int>::max(); }
int int_min(void) { return std::numeric_limits<int>::min(); }

float float_max(void) { return std::numeric_limits<float>::max(); }
float float_min(void) { return std::numeric_limits<float>::min(); }
float float_decimal(float x) { return std::fmod(x, 1); }
int float_integer(float x) { return static_cast<int>(x); }

float Math_pi(void) { return M_PI; }
float Math_e(void) { return M_E; }
float Math_abs(float x) { return std::abs(x); }
int Math_abs(int x) { return std::abs(x); }
float Math_sqrt(float x) { return std::sqrtf((int)x); }
int Math_sqrt(int x) { return std::sqrtf((int)x); }
int Math_floor(float x) { return std::floorf(x); }
int Math_ceil(float x) { return std::ceilf(x); }


int int_add_int(int a, int b) {
    if ((b > 0) && (a > std::numeric_limits<int>::max() - b)) error("overflow");
    if ((b < 0) && (a < std::numeric_limits<int>::min() - b)) error("underflow");
    return a + b;
}

int int_sub_int(int a, int b) {
    if ((b < 0) && (a > std::numeric_limits<int>::max() + b)) error("overflow");
    if ((b > 0) && (a < std::numeric_limits<int>::min() + b)) error("underflow");
    return a - b;
}

int int_mul_int(int a, int b) {
    if (a == 0 || b == 0) return 0;
    if ((a == -1 && b == std::numeric_limits<int>::min())
        || (b == -1 && a == std::numeric_limits<int>::min())
        || (a > std::numeric_limits<int>::max() / b) || (a < std::numeric_limits<int>::min() / b))
        error("overflow");
    
    return a * b;
}

int int_div_int(int a, int b) {
    if (b == 0) error("division by zero");
    return a / b;
}

int int_mod_int(int a, int b) {
    if (b == 0) error("modulo by zero");
    return a % b;
}

bool int_eq_int(int a, int b) { return a == b; }
bool int_neq_int(int a, int b) { return a != b; }
bool int_lt_int(int a, int b) { return a < b; }
bool int_gt_int(int a, int b) { return a > b; }
bool int_lte_int(int a, int b) { return a <= b; }
bool int_gte_int(int a, int b) { return a >= b; }

float float_add_float(float a, float b) {
    float c = a + b;
    if (std::isinf(c)) error("overflow");
    return c;
}

float float_sub_float(float a, float b) {
    float c = a - b;
    if (std::isinf(c)) error("underflow");
    return c;
}

float float_mul_float(float a, float b) {
    float c = a * b;
    if (std::isinf(c)) error("overflow");
    return c;
}

float float_div_float(float a, float b) {
    if (b == 0) error("division by zero");
    return a / b;
}

float float_mod_float(float a, float b) {
    if (b == 0) error("modulo by zero");
    return std::fmod(a, b);
}

bool float_eq_float(float a, float b) { return a == b; }
bool float_neq_float(float a, float b) { return a != b; }
bool float_lt_float(float a, float b) { return a < b; }
bool float_gt_float(float a, float b) { return a > b; }
bool float_lte_float(float a, float b) { return a <= b; }
bool float_gte_float(float a, float b) { return a >= b; }

float float_add_int(float a, int b) { return float_add_float(a, (float)b); }
float float_sub_int(float a, int b) { return float_sub_float(a, (float)b); }
float float_mul_int(float a, int b) { return float_mul_float(a, (float)b); }
float float_div_int(float a, int b) { return float_div_float(a, (float)b); }
float float_mod_int(float a, int b) { return float_mod_float(a, (float)b); }
bool float_eq_int(float a, int b) { return float_eq_float(a, (float)b); }
bool float_neq_int(float a, int b) { return float_neq_float(a, (float)b); }
bool float_lt_int(float a, int b) { return float_lt_float(a, (float)b); }
bool float_gt_int(float a, int b) { return float_gt_float(a, (float)b); }
bool float_lte_int(float a, int b) { return float_lte_float(a, (float)b); }
bool float_gte_int(float a, int b) { return float_gte_float(a, (float)b); }

float int_add_float(int a, float b) { return float_add_float((float)a, b); }
float int_sub_float(int a, float b) { return float_sub_float((float)a, b); }
float int_mul_float(int a, float b) { return float_mul_float((float)a, b); }
float int_div_float(int a, float b) { return float_div_float((float)a, b); }
float int_mod_float(int a, float b) { return float_mod_float((float)a, b); }
bool int_eq_float(int a, float b) { return float_eq_float((float)a, b); }
bool int_neq_float(int a, float b) { return float_neq_float((float)a, b); }
bool int_lt_float(int a, float b) { return float_lt_float((float)a, b); }
bool int_gt_float(int a, float b) { return float_gt_float((float)a, b); }
bool int_lte_float(int a, float b) { return float_lte_float((float)a, b); }
bool int_gte_float(int a, float b) { return float_gte_float((float)a, b); }

string string_add_string(const string& a, const string& b) { return a + b; }
bool string_eq_string(const string& a, const string& b) { return a == b; }
bool string_neq_string(const string& a, const string& b) { return a != b; }

bool bool_eq_bool(bool a, bool b) { return a == b; }
bool bool_neq_bool(bool a, bool b) { return a != b; }
bool bool_and_bool(bool a, bool b) { return a && b; }
bool bool_or_bool(bool a, bool b) { return a || b; }
bool not_bool(bool b) { return !b; }

template<typename T>
nil print(const T& s) {
    std::cout << to_string(s) << '\n';
    return nil();
}

nil print_literal(const string& s) {
    std::cout << s;
    return nil();
}

string input(void) {
    std::string s;
    std::getline(std::cin, s);
    return s;
}

string input(const string& prompt) {
    std::cout << prompt;
    return input();
}

nil assert(bool b, const string& msg) {
    if (!b) error(msg);
    return nil();
}

nil assert(bool b) { return assert(b, "assertion failed"); }

array<int> range(int start, int end) {
    array<int> arr;
    for (int i = start; i < end; i++) arr.add(i);
    return arr;
}

array<int> range(int end) {
    array<int> arr;
    for (int i = 0; i < end; i++) arr.add(i);
    return arr;
}

array<int> range(int start, int end, int step) {
    array<int> arr;
    for (int i = start; i < end; i += step) arr.add(i);
    return arr;
}
