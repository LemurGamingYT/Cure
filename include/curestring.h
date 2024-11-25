#ifndef STRING_H
#define STRING_H

// this file serves as a placeholder for what's to come for the string type
// planning on making a string struct that holds a char* and a size_t length
// this is instead of a null terminated char*

#ifndef __cplusplus
#include <stdbool.h>
#endif


#ifdef __cplusplus
extern "C" {
#endif

#include <stdlib.h>
#include <string.h>

typedef char* string;

#define string_null NULL

string string_make(char* str) { return str; }
string string_empty(size_t len) {
    string str = (string)malloc(len + 1);
    str[len] = '\0';
    return str;
}
string string_new(size_t len) {
    string str = string_empty(len);
    for (size_t i = 0; i < len; i++)
        str[i] = ' ';
    return str;
}
size_t string_length(string str) { return strlen(str); }
string string_copy(string str) { return string_make(strdup(str)); }
bool string_contains(string str, string substr) { return strstr(str, substr) != NULL; }
char* string_ptr(string str) { return str; }
void string_set_char(string* str, size_t index, char c) { (*str)[index] = c; }
void string_set(string* str, size_t index, string c) { (*str)[index] = *string_ptr(c); }
char string_start(string str) { return *str; }
char string_get_char(string str, size_t index) { return str[index]; }
bool string_eq(string str, string str2) { return strcmp(str, str2) == 0; }
bool string_eq_partial(string str, string str2, size_t len) { return strncmp(str, str2, len) == 0; }
bool string_neq(string str, string str2) { return strcmp(str, str2) != 0; }
bool string_neq_partial(string str, string str2, size_t len) { return strncmp(str, str2, len) != 0; }
string string_get(string str, size_t index) {
    static char temp[2];
    temp[0] = string_get_char(str, index);
    temp[1] = '\0';
    return string_make(temp);
}
string string_concat(string a, string b) {
    size_t alen = string_length(a);
    size_t blen = string_length(b);
    size_t len = alen + blen;
    string str = (string)malloc(len + 1);
    if (str == NULL)
        return NULL;
    
    memcpy(str, a, alen);
    memcpy(str + alen, b, blen);
    str[len] = '\0';
    return str;
}

string string_replace(string str, string old, string new) {
    size_t oldlen = string_length(old);
    size_t newlen = string_length(new);
    size_t len = string_length(str);

    size_t count = 0;
    string pos = str;
    while ((pos = strstr(pos, old)) != NULL) {
        count++;
        pos += oldlen;
    }

    size_t final_len = len + count * (newlen - oldlen);
    string res = string_empty(final_len);
    if (!res)
        return NULL;
    
    string current_pos = str;
    string write_pos = res;
    while ((pos = strstr(current_pos, old)) != NULL) {
        size_t prefix_len = pos - current_pos;
        memcpy(write_pos, current_pos, prefix_len);
        write_pos += prefix_len;

        memcpy(write_pos, new, newlen);
        write_pos += newlen;

        current_pos = pos + oldlen;
    }

    strncpy(write_pos, current_pos, len - (current_pos - str));
    return res;
}

#ifdef __cplusplus
}
#endif

#endif
