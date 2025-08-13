#pragma once

#include <filesystem>
#include <functional> // used for std::function types (not in this file)
#include <algorithm>
#include <iostream>
#include <sstream>
#include <thread>
#include <limits>
#include <string>
#include <vector>
#include <cctype>

#define _USE_MATH_DEFINES
#include <stdarg.h>
#include <math.h>


using nil = std::nullptr_t;


void error(const char* s, ...) {
    va_list args;
    va_start(args, s);
    
    std::cerr << "error: ";
    vfprintf(stderr, s, args);
    std::cerr << std::endl;
    
    va_end(args);
    std::exit(1);
}


template<typename T>
class array : public std::vector<T> {
    public:
    array(std::initializer_list<T> init) : std::vector<T>(init) {}
    array() : std::vector<T>() {}
    
    nil add(T item) {
        this->push_back(item);
        return nil();
    }
    
    nil add_all(array<T> items) {
        this->insert(this->end(), items.begin(), items.end());
        return nil();
    }
    
    int remove_first(T value) {
        auto it = std::find(this->begin(), this->end(), value);
        if (it == this->end())
        return -1;
        
        this->erase(it);
        return it - this->begin();
    }
    
    array<int> remove_all(T value) {
        array<int> indexes;
        auto it = std::find(this->begin(), this->end(), value);
        while (it != this->end()) {
            indexes.add(it - this->begin());
            this->erase(it);
            it = std::find(this->begin(), this->end(), value);
        }

        return indexes;
    }
    
    T remove_at(int index) {
        if (index < 0)
            index = length() + index;
            
            if (index >= length())
            error("array index out of range");
            
            T item = (*this)[index];
            this->erase(this->begin() + index);
            return item;
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
        
        bool contains(T item) const {
            return std::find(this->begin(), this->end(), item) != this->end();
        }
        
        int index_of(T item) const {
            auto it = std::find(this->begin(), this->end(), item);
            if (it == this->end())
            return -1;
        
            return it - this->begin();
        }

        nil clear() const {
            this->clear();
            return nil();
        }
        
        nil reserve(int size) const {
            this->reserve(size);
            return nil();
        }
        
        nil reverse() const {
            std::reverse(this->begin(), this->end());
        return nil();
    }

    nil sort() const {
        std::sort(this->begin(), this->end());
        return nil();
    }
    
    array<T> map(std::function<T(T)> func) const {
        array<T> result;
        result.insert(result.end(), this->begin(), this->end());
        std::transform(result.begin(), result.end(), result.begin(), func);
        return result;
    }

    array<T> filter(std::function<bool(T)> func) const {
        array<T> result;
        std::copy_if(this->begin(), this->end(), std::back_inserter(result), func);
        return result;
    }
    
    
    int length() const { return this->size(); }
    bool is_empty() const { return length() == 0; }
    array<T> reversed() const {
        array<T> result;
        result.insert(result.end(), this->rbegin(), this->rend());
        return result;
    }
    
    array<T> sorted() const {
        array<T> result;
        result.insert(result.end(), this->begin(), this->end());
        std::sort(result.begin(), result.end());
        return result;
    }

    
    array<T> operator+(const array<T>& other) const {
        array<T> result;
        result.insert(result.end(), this->begin(), this->end());
        result.insert(result.end(), other.begin(), other.end());
        return result;
    }
    
    bool operator==(const array<T>& other) const {
        return this->size() == other.size() && std::equal(
            this->begin(), this->end(), other.begin()
        );
    }
    
    bool operator!=(const array<T>& other) const {
        return this->size() != other.size() || !std::equal(
            this->begin(), this->end(), other.begin()
        );
    }
};

class string : public std::string {
    public:
    string(std::string s) : std::string(s) {}
    string(char c) : std::string(1, c) {}
    string(const char* s) : std::string(s) {}
    string() : std::string() {}
    
    string get(int index) const {
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
    
    bool contains(const string& substring) const {
        return this->find(substring) != std::string::npos;
    }

    bool startswith(const string& prefix) const {
        return this->find(prefix) == 0;
    }

    bool endswith(const string& suffix) const {
        return this->find(suffix) == this->length() - suffix.length();
    }

    string repeat(int times) const {
        string result;
        for (int i = 0; i < times; i++)
            result += *this;
        
        return result;
    }

    int index_of(const string& substring) const { return this->find(substring); }
    

    string lowercase() const {
        std::string result;
        std::transform(this->begin(), this->end(), result.begin(), ::tolower);
        return result;
    }

    string uppercase() const {
        std::string result;
        std::transform(this->begin(), this->end(), result.begin(), ::toupper);
        return result;
    }
    
    bool is_alpha() const {
        return std::all_of(this->begin(), this->end(), ::isalpha);
    }
    
    bool is_empty() const {
        return length() == static_cast<size_t>(0);
    }
    
    bool is_digit() const {
        return std::all_of(this->begin(), this->end(), ::isdigit);
    }
    
    bool is_alphanumeric() const {
        return std::all_of(this->begin(), this->end(), ::isalnum);
    }
    
    bool is_whitespace() const {
        return std::all_of(this->begin(), this->end(), ::isspace);
    }
    
    string reversed() const {
        std::string result = *this;
        std::reverse(result.begin(), result.end());
        return result;
    }
    
    string join(const array<string>& strings) const {
        if (strings.is_empty()) return "";

        string result;
        result.reserve(strings.size() * (this->length() + 8));

        result += strings[0];
        for (size_t i = 1; i < static_cast<size_t>(strings.length()); ++i) {
            result += *this;
            result += strings[i];
        }

        return result;
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

    nil clear() {
        ss.clear();
        return nil();
    }

    bool operator==(const StringBuilder& other) const { return str() == other.str(); }
    bool operator!=(const StringBuilder& other) const { return str() != other.str(); }
};

class Vector2 {
    float _x, _y;
    public:
    Vector2(float x, float y) : _x(x), _y(y) {}
    
    float x() const { return _x; }
    float y() const { return _y; }

    int length() const { return std::sqrt(_x * _x + _y * _y); }
    int length_squared() const { return _x * _x + _y * _y; }
    Vector2 normalized() const { return Vector2(_x / length(), _y / length()); }
    int distance(const Vector2& other) const {
        return std::sqrt((_x - other.x()) * (_x - other.x()) + (_y - other.y()) * (_y - other.y()));
    }

    int distance_squared(const Vector2& other) const {
        return (_x - other.x()) * (_x - other.x()) + (_y - other.y()) * (_y - other.y());
    }

    Vector2 operator+(const Vector2& other) const { return Vector2(_x + other.x(), _y + other.y()); }
    Vector2 operator-(const Vector2& other) const { return Vector2(_x - other.x(), _y - other.y()); }
    Vector2 operator*(const Vector2& other) const { return Vector2(_x * other.x(), _y * other.y()); }
    Vector2 operator/(const Vector2& other) const { return Vector2(_x / other.x(), _y / other.y()); }

    bool operator==(const Vector2& other) const { return _x == other.x() && _y == other.y(); }
    bool operator!=(const Vector2& other) const { return _x != other.x() || _y != other.y(); }
};


void error(const string s, ...) {
    va_list args;
    va_start(args, s);
    
    std::cerr << "error: ";
    vfprintf(stderr, s.c_str(), args);
    std::cerr << std::endl;
    
    va_end(args);
    std::exit(1);
}


string to_string(int i) { return std::to_string(i); }
string to_string(float f) { return std::to_string(f); }
string to_string(const string& s) { return s; }
string to_string(bool b) { return b ? "true" : "false"; }
string to_string(nil _) { return (string)"nil"; }
string to_string(const StringBuilder& sb) { return sb.ss.str(); }
string to_string(const Vector2& v) {
    return "Vector2(x=" + to_string(v.x()) + ", y=" + to_string(v.y()) + ")";
}

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


string System_cwd(void) { return std::filesystem::current_path().string(); }
int System_pid(void) { // TODO: test if this works on all the target platforms
#if WINDOWS
    return _getpid();
#else
    return getpid();
#endif
}

nil System_exit(int code = 0) {
    std::exit(code);
    return nil();
}

nil System_sleep(int ms) {
    std::this_thread::sleep_for(std::chrono::milliseconds(ms));
    return nil();
}


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

float float_add_int(float a, int b) { return float_add_float(a, (float)b); }
float float_sub_int(float a, int b) { return float_sub_float(a, (float)b); }
float float_mul_int(float a, int b) { return float_mul_float(a, (float)b); }
float float_div_int(float a, int b) { return float_div_float(a, (float)b); }
float float_mod_int(float a, int b) { return float_mod_float(a, (float)b); }

float int_add_float(int a, float b) { return float_add_float((float)a, b); }
float int_sub_float(int a, float b) { return float_sub_float((float)a, b); }
float int_mul_float(int a, float b) { return float_mul_float((float)a, b); }
float int_div_float(int a, float b) { return float_div_float((float)a, b); }
float int_mod_float(int a, float b) { return float_mod_float((float)a, b); }

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

array<int> range(int end) {
    array<int> arr;
    for (int i = 0; i < end; i++) arr.add(i);
    return arr;
}

array<int> range(int start, int end) {
    array<int> arr;
    for (int i = start; i < end; i++) arr.add(i);
    return arr;
}

array<int> range(int start, int end, int step) {
    array<int> arr;
    for (int i = start; i < end; i += step) arr.add(i);
    return arr;
}
