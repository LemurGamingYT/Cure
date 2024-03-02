#pragma once

#include <stdbool.h>
#include <Windows.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <time.h>

// The basic int type
typedef long long Int;

// The basic float type
typedef double Float;

// The string type, needs to be freed using free()
typedef char* String;

// The boolean type
typedef bool Bool;

// The nil type, can be any type but use just void
typedef void* Nil;

// The Math class
typedef struct {
    void* _; // Empty field, don't use this
} Math;

// The System class
typedef struct {
    void* _; // Empty field, don't use this
} System;

// The Timer class, used in the System class
typedef struct {
    // timeinfo stores the time information
    struct tm* timeinfo;
} Timer;

// The File class, used in the System class
typedef struct {
    // path stores the path to the file as a String type
    String path;

    // Use this to read from the file or any other basic operation, e.g. exists
    FILE* r;

    // Use this to write to the file
    FILE* w;
} File;

// The LogLevel enum, used in the Logger class
typedef enum {
    LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERROR
} LogLevel;

// The Log class, used in the Logger class
typedef struct {
    // level stores the log level of which it actually logs out a message
    LogLevel level;
    
    // logFile stores a File object which stores the log file
    File logFile;
} Log;

// The Logger class
typedef struct {
    void* _; // Empty field, don't use this
} Logger;

// The Mem class
typedef struct {
    void* _; // Empty field, don't use this
} Mem;

// The Pointer class, used in the Mem class
typedef struct {
    void* val;
} Pointer;


// Hardcoded PI
#define PI 3.14159265358979323846

// Hardcoded E
#define E 2.71828182845904523536


// Use this to raise an error and end the program
void error(String name, String msg) {
    printf("%sError: %s\n", name, msg);
    exit(1);
}


// Add two strings
String String_add_String(String a, String b);


// Return the type of an int
String Int_type() {
    return "int";
}

// Return the type of a float
String Float_type() {
    return "float";
}

// Return the type of a string
String String_type() {
    return "string";
}

// Return the type of a boolean
String Bool_type() {
    return "bool";
}

// Return the type of a nil
String Nil_type() {
    return "nil";
}

// Return the type of the Math class
String Math_type() {
    return "Math";
}

// Return the type of the System class
String System_type() {
    return "System";
}

// Return the type of the Timer class
String Timer_type() {
    return "Timer";
}

// Return the type of the File class
String File_type() {
    return "File";
}

// Return the type of the LogLevel enum
String LogLevel_type() {
    return "LogLevel";
}

// Return the type of the Log class
String Log_type() {
    return "Log";
}

// Return the type of the Logger class
String Logger_type() {
    return "Logger";
}

// Return the type of the Mem class
String Mem_type() {
    return "Mem";
}

// Return the type of the Pointer class
String Pointer_type() {
    return "Ptr";
}


// Get the string representation of an int, simply converts it to a string
String Int_repr(Int i) {
    String buf = (String)malloc(21);
    snprintf(buf, 21, "%lld", i);
    return buf;
}

// Get the string representation of a float, simply converts it to a string
String Float_repr(Float f) {
    String buf = (String)malloc(21);
    snprintf(buf, 21, "%f", f);
    return buf;
}

// Get the string representation of a string, don't use this it's only used for compiler simplicity
String String_repr(String s) {
    return s;
}

// Get the string representation of a boolean, checks if it's true or false
String Bool_repr(Bool b) {
    return b ? "true" : "false";
}

// Get the string representation of a nil
String Nil_repr(Nil n) {
    return "nil";
}

// Get the string representation of the Math class
String Math_repr(Math m) {
    return "Class 'Math'";
}

// Get the string representation of the System class
String System_repr(System s) {
    return "Class 'System'";
}

// Get the string representation of the Timer class, prints the time info
String Timer_repr(Timer t) {
    String buf = (String)malloc(21);
    snprintf(
        buf, 21, "Timer(\"%s:%s:%s\")",
        t.timeinfo->tm_hour, t.timeinfo->tm_min, t.timeinfo->tm_sec
    );
    return buf;
}

// Get the string representation of the File class, prints the path
String File_repr(File f) {
    String buf = (String)malloc(21);
    snprintf(buf, 21, "File(\"%s\")", f.path);
    return buf;
}

// Get the string representation of the LogLevel enum
String LogLevel_repr(LogLevel l) {
    switch (l) {
        case LOG_DEBUG:
            return "DEBUG";
        case LOG_INFO:
            return "INFO";
        case LOG_WARNING:
            return "WARNING";
        case LOG_ERROR:
            return "ERROR";
        default:
            return "UNKNOWNLOGLEVEL";
    }
}

// Get the string representation of the Log class, prints the level
String Log_repr(Log l) {
    String buf = (String)malloc(21);
    snprintf(buf, 21, "Log(\"%s\")", LogLevel_repr(l.level));
    return buf;
}

// Get the string representation of the Logger class
String Logger_repr(Logger l) {
    return "Class 'Logger'";
}

// Get the string representation of the Mem class
String Mem_repr(Mem m) {
    return "Class 'Mem'";
}

// Get the string representation of the Pointer class, prints the pointer
String Pointer_repr(Pointer p) {
    String buf = (String)malloc(21);
    snprintf(buf, 21, "Ptr(%p)", p.val);
    return buf;
}


// Convert an int to a boolean, checks if it's greater than 0
Bool Int_bool(Int i) {
    return i > 0;
}

// Convert a float to a boolean, checks if it's greater than 0
Bool Float_bool(Float f) {
    return f > 0;
}

// Convert a string to a boolean, checks if it's length is greater than 0
Bool String_bool(String s) {
    return strlen(s) > 0;
}

// Convert a boolean to a boolean, don't use this it's only used for the compiler simplicity
Bool Bool_bool(Bool b) {
    return b;
}

// Convert a nil to a boolean
Bool Nil_bool(Nil n) {
    return false;
}

// Convert the Math class to a boolean
Bool Math_bool(Math m) {
    return true;
}

// Convert the System class to a boolean
Bool System_bool(System s) {
    return true;
}

// Convert the Timer class to a boolean
Bool Timer_bool(Timer t) {
    return true;
}

// Convert the File class to a boolean
Bool File_bool(File f) {
    return f.r != NULL;
}

// Convert the LogLevel enum to a boolean
Bool Log_bool(Log l) {
    return l.logFile.r != NULL;
}

// Convert the Logger class to a boolean
Bool Logger_bool(Logger l) {
    return true;
}

// Convert the Mem class to a boolean
Bool Mem_bool(Mem m) {
    return true;
}

// Convert the Pointer class to a boolean
Bool Pointer_bool(Pointer p) {
    return p.val != NULL;
}


// Convert a float to an int
Int Float_to_Int(Float f) {
    Int* i = (Int*)malloc(sizeof(Int));
    *i = (Int)f;
    return *i;
}

// Convert a string to an int
Int String_to_Int(String s) {
    return atoll(s);
}

// Convert a boolean to an int
Int Bool_to_Int(Bool b) {
    return b ? 1 : 0;
}


// Convert an int to a float
Float Int_to_Float(Int i) {
    Float* f = (Float*)malloc(sizeof(Float));
    *f = (Float)i;
    return *f;
}

// Convert a string to a float
Float String_to_Float(String s) {
    return atof(s);
}


// Add two ints
Int Int_add_Int(Int a, Int b) {
    return a + b;
}

// Add an int and a float
Float Float_add_Int(Int a, Float b) {
    return a + b;
}

// Add a float and an int
Float Int_add_Float(Int a, Float b) {
    return a + b;
}

// Add two floats
Float Float_add_Float(Float a, Float b) {
    return a + b;
}

// Add two strings
String String_add_String(String a, String b) {
    String res = (String)malloc(strlen(a) + strlen(b) + 1);
    strcpy(res, a);
    strcat(res, b);
    return res;
}


// Subtract two ints
Int Int_sub_Int(Int a, Int b) {
    return a - b;
}

// Subtract an int and a float
Float Float_sub_Int(Int a, Float b) {
    return a - b;
}

// Subtract a float and an int
Float Int_sub_Float(Int a, Float b) {
    return a - b;
}

// Subtract two floats
Float Float_sub_Float(Float a, Float b) {
    return a - b;
}


// Multiply two ints
Int Int_mul_Int(Int a, Int b) {
    return a * b;
}

// Multiply a float and an int
Float Float_mul_Int(Int a, Float b) {
    return a * b;
}

// Multiply an int and a float
Float Int_mul_Float(Int a, Float b) {
    return a * b;
}

// Multiply two floats
Float Float_mul_Float(Float a, Float b) {
    return a * b;
}


// Divide two ints
Float Int_div_Int(Int a, Int b) {
    return a / b;
}

// Divide a float and an int
Float Float_div_Int(Int a, Float b) {
    return a / b;
}

// Divide an int and a float
Float Int_div_Float(Int a, Float b) {
    return a / b;
}

// Divide two floats
Float Float_div_Float(Float a, Float b) {
    return a / b;
}


// Modulo two ints
Int Int_mod_Int(Int a, Int b) {
    return a % b;
}


// Compare two ints
Bool Int_eq_Int(Int a, Int b) {
    return a == b;
}

// Compare two floats
Bool Float_eq_Float(Float a, Float b) {
    return a == b;
}

// Compare two strings
Bool String_eq_String(String a, String b) {
    return strcmp(a, b) == 0;
}

// Compare two booleans
Bool Bool_eq_Bool(Bool a, Bool b) {
    return a == b;
}

// Compare nil
Bool Nil_eq_Nil(Nil a, Nil b) {
    return false;
}


// Compare two ints
Bool Int_neq_Int(Int a, Int b) {
    return a != b;
}

// Compare two floats
Bool Float_neq_Float(Float a, Float b) {
    return a != b;
}

// Compare two strings
Bool String_neq_String(String a, String b) {
    return strcmp(a, b) != 0;
}

// Compare two booleans
Bool Bool_neq_Bool(Bool a, Bool b) {
    return a != b;
}

// Compare nil
Bool Nil_neq_Nil(Nil a, Nil b) {
    return true;
}


// Compare two ints
Bool Int_lt_Int(Int a, Int b) {
    return a < b;
}

// Compare two floats
Bool Float_lt_Float(Float a, Float b) {
    return a < b;
}

// Compare two strings
Bool String_lt_String(String a, String b) {
    return strlen(a) < strlen(b);
}


// Compare two ints
Bool Int_lte_Int(Int a, Int b) {
    return a <= b;
}

// Compare two floats
Bool Float_lte_Float(Float a, Float b) {
    return a <= b;
}

// Compare two strings
Bool String_lte_String(String a, String b) {
    return strlen(a) <= strlen(b);
}


// Compare two ints
Bool Int_gt_Int(Int a, Int b) {
    return a > b;
}

// Compare two floats
Bool Float_gt_Float(Float a, Float b) {
    return a > b;
}

// Compare two strings
Bool String_gt_String(String a, String b) {
    return strlen(a) > strlen(b);
}


// Compare two ints
Bool Int_gte_Int(Int a, Int b) {
    return a >= b;
}

// Compare two floats
Bool Float_gte_Float(Float a, Float b) {
    return a >= b;
}

// Compare two strings
Bool String_gte_String(String a, String b) {
    return strlen(a) >= strlen(b);
}


// Check a boolean and a boolean
Bool Bool_and_Bool(Bool a, Bool b) {
    return a && b;
}


// Check a boolean or a boolean
Bool Bool_or_Bool(Bool a, Bool b) {
    return a || b;
}


// Invert a boolean value
Bool not_Bool(Bool a) {
    return !a;
}


// Get the length of a string
Int String_length(String s) {
    return (Int)strlen(s);
}


// Get PI (used by the compiler)
Float Math_PI() {
    return PI;
}

// Get E (used by the compiler)
Float Math_E() {
    return E;
}

// Get the sine value of x
Float Math_sin(Float x) {
    return sin(x);
}

// Get the cosine value of x
Float Math_cos(Float x) {
    return cos(x);
}

// Get the tangent value of x
Float Math_tan(Float x) {
    return tan(x);
}

// Get the arc sine value of x
Float Math_asin(Float x) {
    return asin(x);
}

// Get the arc cosine value of x
Float Math_acos(Float x) {
    return acos(x);
}

// Get the arc tangent value of x
Float Math_atan(Float x) {
    return atan(x);
}

// Get the square root value of x
Float Math_sqrt(Float x) {
    return sqrt(x);
}

// Get the absolute value of x
Float Math_abs(Float x) {
    return fabs(x);
}

// Get x rounded down
Int Math_floor(Float x) {
    return floor(x);
}

// Get x rounded up
Int Math_ceil(Float x) {
    return ceil(x);
}

// Get the natural logarithm of x
Float Math_log(Float x) {
    return log(x);
}


// Exit the program
Nil System_exit(Int x) {
    exit(x);
}

// Execute a shell command
Int System_shell(String code) {
    return system(code);
}

// Get an environment variable
String System_getenv(String x) {
    String value;
    if ((value = getenv(x)) != NULL) {
        return value;
    } else {
        return "";
    }
}

// Get the current time
Timer System_current_time() {
    Timer timer;
    time_t t;
    time(&t);
    timer.timeinfo = localtime(&t);
    return timer;
}

// Get the total memory usage
Float System_total_memory_usage() {
    MEMORYSTATUS memoryStatus;
    GlobalMemoryStatus(&memoryStatus);

    return memoryStatus.dwTotalPhys / 1024;
}

// Get the free memory usage
Float System_free_memory_usage() {
    MEMORYSTATUS memoryStatus;
    GlobalMemoryStatus(&memoryStatus);

    return memoryStatus.dwAvailPhys / 1024;
}

// Set the console color
Nil System_console_color(Int color) {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color);
}

// Reset the console color
Nil System_reset_console_color() {
    SetConsoleTextAttribute(
        GetStdHandle(STD_OUTPUT_HANDLE),
        FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE
    );
}

// Foreground red color (used for System_console_color)
Int System_fg_red() {
    return FOREGROUND_RED;
}

// Foreground green color (used for System_console_color)
Int System_fg_green() {
    return FOREGROUND_GREEN;
}

// Foreground blue color (used for System_console_color)
Int System_fg_blue() {
    return FOREGROUND_BLUE;
}

// Foreground yellow color (used for System_console_color)
Int System_fg_yellow() {
    return FOREGROUND_RED | FOREGROUND_GREEN;
}

// Foreground magenta color (used for System_console_color)
Int System_fg_magenta() {
    return FOREGROUND_RED | FOREGROUND_BLUE;
}

// Foreground cyan color (used for System_console_color)
Int System_fg_cyan() {
    return FOREGROUND_BLUE | FOREGROUND_GREEN;
}

// Foreground white color (used for System_console_color)
Int System_fg_white() {
    return FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE;
}

// Background red color (used for System_console_color)
Int System_bg_red() {
    return BACKGROUND_RED;
}

// Background green color (used for System_console_color)
Int System_bg_green() {
    return BACKGROUND_GREEN;
}

// Background blue color (used for System_console_color)
Int System_bg_blue() {
    return BACKGROUND_BLUE;
}

// Background yellow color (used for System_console_color)
Int System_bg_yellow() {
    return BACKGROUND_RED | BACKGROUND_GREEN;
}

// Background magenta color (used for System_console_color)
Int System_bg_magenta() {
    return BACKGROUND_RED | BACKGROUND_BLUE;
}

// Background cyan color (used for System_console_color)
Int System_bg_cyan() {
    return BACKGROUND_BLUE | BACKGROUND_GREEN;
}

// Background white color (used for System_console_color)
Int System_bg_white() {
    return BACKGROUND_RED | BACKGROUND_GREEN | BACKGROUND_BLUE;
}

// Clear the console
Nil System_clear_console() {
    system("cls");
}

// Open a file
File System_open_file(String path) {
    File file;
    file.path = path;
    file.r = fopen(path, "r");
    file.w = fopen(path, "w");
    return file;
}


// Get the path of the file
String File_path(File f) {
    return f.path;
}

// Check if the file exists
Bool File_exists(File f) {
    return f.r != NULL;
}

// Get the size of the file
Int File_size(File f) {
    if (!File_exists(f)) {
        error("File", "Cannot read from file, it does not exist");
        return -1;
    }

    fseek(f.r, 0, SEEK_END);
    Int size = ftell(f.r);
    fseek(f.r, 0, SEEK_SET);
    return size;
}

// Read from the file
String File_read(File f) {
    if (!File_exists(f)) {
        error("File", "Cannot read from file, it does not exist");
        return "";
    }

    Int size = File_size(f);
    char* buffer = (char*)malloc(size + 1);
    fread(buffer, size, 1, f.r);
    buffer[size] = '\0';
    return buffer;
}

// Write to the file
Nil File_write(File f, String s) {
    if (!File_exists(f)) {
        error("File", "Cannot write to file, it does not exist");
    }

    Int size = String_length(s);
    fwrite(s, size, 1, f.w);
}

// Create the file
Nil File_create(File f) {
    f.w = fopen(f.path, "w");
    f.r = fopen(f.path, "r");
}

// Copy the file
Nil File_copy(File f, String path) {
    if (!File_exists(f)) {
        error("File", "Cannot copy file, it does not exist");
    }

    FILE* dest = fopen(path, "wb");
    if (dest == NULL) {
        error("File", "Cannot copy file, failed to open destination");
    }

    fseek(f.r, 0, SEEK_SET);
    Int size = File_size(f);
    char* buffer = (char*)malloc(size + 1);
    fread(buffer, size, 1, f.r);
    fwrite(buffer, size, 1, dest);
    fclose(dest);
    free(buffer);
}

// Delete the file
Nil File_delete(File f) {
    if (!File_exists(f)) {
        error("File", "Cannot delete file, it does not exist");
    }

    fclose(f.r);
    fclose(f.w);
    remove(f.path);
}

// Move the file
Nil File_move(File f, String path) {
    if (!File_exists(f)) {
        error("File", "Cannot move file, it does not exist");
    }

    File_copy(f, path);
    File_delete(f);
}


// set_level wrapper
Nil Log_set_level(Log l, LogLevel level) {
    l.level = level;
}

// Log a message
Nil Log_log(Log l, LogLevel level, String msg) {
    if (level >= l.level) {
        if (File_exists(l.logFile)) {
            File_write(l.logFile, msg);
        } else {
            printf("%s\n", msg);
        }
    }
}

// Wrapper for LOG_DEBUG (used by the compiler)
LogLevel Logger_debug() {
    return LOG_DEBUG;
}

// Wrapper for LOG_INFO (used by the compiler)
LogLevel Logger_info() {
    return LOG_INFO;
}

// Wrapper for LOG_WARNING (used by the compiler)
LogLevel Logger_warn() {
    return LOG_WARNING;
}

// Wrapper for LOG_ERROR (used by the compiler)
LogLevel Logger_error() {
    return LOG_ERROR;
}

// Open the log file
Log Logger_open(String path) {
    Log l;
    l.logFile = System_open_file(path);
    return l;
}


// Wrapper for free()
Nil Mem_free(Pointer obj) {
    free(obj.val);
}

// Wrapper for sizeof()
Int Mem_sizeof(Pointer obj) {
    return sizeof(obj.val);
}

// Wrapper for pointers
Pointer Mem_point(void* obj) {
    Pointer p = { .val = obj };
    return p;
}

// Wrapper for malloc
Pointer Mem_alloc(Int size) {
    Pointer p = { .val = malloc(size) };
    return p;
}

// Wrapper for memcpy
Pointer Mem_copy(Pointer p) {
    return Mem_point(memcpy(p.val, p.val, Mem_sizeof(p)));
}

// Wrapper for clone
Pointer Mem_clone(Pointer p) {
    return Mem_point(memcpy(Mem_alloc(Mem_sizeof(p)).val, p.val, Mem_sizeof(p)));
}
