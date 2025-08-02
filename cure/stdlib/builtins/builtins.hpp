#pragma once

#include <iostream>
#include <sstream>
#include <limits>
#include <string>
#include <vector>


using nil = std::nullptr_t;


class string : public std::string {
public:
    string(std::string s) : std::string(s) {}
    string(char c) : std::string(1, c) {}
    string(const char* s) : std::string(s) {}
    string() : std::string() {}

    // Custom iterator
    class iterator {
        std::string::iterator it;
    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = string;
        using difference_type = std::ptrdiff_t;
        using pointer = string*;

        iterator(std::string::iterator i) : it(i) {}

        string operator*() const {
            return string(*it);  // return a string of length 1
        }

        iterator& operator++() {
            ++it;
            return *this;
        }

        iterator operator++(int) {
            iterator tmp = *this;
            ++(*this);
            return tmp;
        }

        bool operator==(const iterator& other) const {
            return it == other.it;
        }

        bool operator!=(const iterator& other) const {
            return it != other.it;
        }
    };

    iterator begin() {
        return iterator(std::string::begin());
    }

    iterator end() {
        return iterator(std::string::end());
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
    template<typename... Args>
    array(Args... args) : std::vector<T>{std::forward<Args>(args)...} {}

    int length() const { return this->size(); }

    nil add(T item) {
        this->push_back(item);
        return nil();
    }

    T get(int index) {
        return this->at(index);
    }

    nil set(int index, T item) {
        this->at(index) = item;
        return nil();
    }
};


void error(const string& s) {
    std::cerr << "error: " << s << std::endl;
    std::exit(1);
}

string to_string(int i) { return std::to_string(i); }
string to_string(float f) { return std::to_string(f); }
string to_string(const string& s) { return s; }
string to_string(bool b) { return b ? "true" : "false"; }
string to_string(nil _) { return (string)"nil"; }
string to_string(const StringBuilder& sb) {
    return sb.ss.str();
}

template<typename T>
string to_string(const array<T>& arr) {
    std::stringstream ss;
    ss << '[';
    for (size_t i = 0; i < static_cast<size_t>(arr.length()); ++i) {
        ss << arr.get(i);
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

nil assert(bool b, const string& msg) {
    if (!b) error(msg);
    return nil();
}

nil assert(bool b) { return assert(b, "assertion failed"); }
