#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "../include/tinyregexc/re.h"


/* Fullmatch function */
int re_fullmatchp(re_t pattern, const char* text, int* matchlength)
{
    int result = re_matchp(pattern, text, matchlength);
    if (result != -1 && text[*matchlength] == '\0')
    {
        return result;
    }
    return -1;
}

/* Split function */
char** re_split(const char* pattern, const char* text, int* count)
{
    re_t compiled = re_compile(pattern);
    char** result = NULL;
    int capacity = 10;
    int size = 0;
    const char* start = text;
    int matchlength;

    result = (char**)malloc(capacity * sizeof(char*));
    
    while (*start != '\0')
    {
        int match_start = re_matchp(compiled, start, &matchlength);
        if (match_start == -1)
        {
            break;
        }
        
        int substr_len = start + match_start - text;
        result[size] = (char*)malloc((substr_len + 1) * sizeof(char));
        strncpy(result[size], text, substr_len);
        result[size][substr_len] = '\0';
        size++;
        
        if (size == capacity)
        {
            capacity *= 2;
            result = (char**)realloc(result, capacity * sizeof(char*));
        }
        
        start += match_start + matchlength;
        text = start;
    }
    
    if (*text != '\0')
    {
        result[size] = strdup(text);
        size++;
    }
    
    *count = size;
    return result;
}

/* Replace function */
char* re_replace(const char* pattern, const char* text, const char* replacement)
{
    re_t compiled = re_compile(pattern);
    char* result = NULL;
    int capacity = strlen(text) * 2;
    int size = 0;
    const char* start = text;
    int matchlength;

    result = (char*)malloc(capacity * sizeof(char));
    
    while (*start != '\0')
    {
        int match_start = re_matchp(compiled, start, &matchlength);
        if (match_start == -1)
        {
            break;
        }
        
        int substr_len = match_start;
        if (size + substr_len + strlen(replacement) >= capacity)
        {
            capacity *= 2;
            result = (char*)realloc(result, capacity * sizeof(char));
        }
        
        strncpy(result + size, start, substr_len);
        size += substr_len;
        strcpy(result + size, replacement);
        size += strlen(replacement);
        
        start += match_start + matchlength;
    }
    
    strcpy(result + size, start);
    
    return result;
}

/* Sub function */
char* re_sub(const char* pattern, const char* text, char* (*callback)(const char* match))
{
    re_t compiled = re_compile(pattern);
    char* result = NULL;
    int capacity = strlen(text) * 2;
    int size = 0;
    const char* start = text;
    int matchlength;

    result = (char*)malloc(capacity * sizeof(char));
    
    while (*start != '\0')
    {
        int match_start = re_matchp(compiled, start, &matchlength);
        if (match_start == -1)
        {
            break;
        }
        
        int substr_len = match_start;
        if (size + substr_len >= capacity)
        {
            capacity *= 2;
            result = (char*)realloc(result, capacity * sizeof(char));
        }
        
        strncpy(result + size, start, substr_len);
        size += substr_len;
        
        char* match = (char*)malloc((matchlength + 1) * sizeof(char));
        strncpy(match, start + match_start, matchlength);
        match[matchlength] = '\0';
        
        char* replacement = callback(match);
        int repl_len = strlen(replacement);
        
        if (size + repl_len >= capacity)
        {
            capacity *= 2;
            result = (char*)realloc(result, capacity * sizeof(char));
        }
        
        strcpy(result + size, replacement);
        size += repl_len;
        
        free(match);
        free(replacement);
        
        start += match_start + matchlength;
    }
    
    strcpy(result + size, start);
    
    return result;
}

/* Findall function */
char** re_findall(const char* pattern, const char* text, int* count)
{
    re_t compiled = re_compile(pattern);
    char** result = NULL;
    int capacity = 10;
    int size = 0;
    const char* start = text;
    int matchlength;

    result = (char**)malloc(capacity * sizeof(char*));
    
    while (*start != '\0')
    {
        int match_start = re_matchp(compiled, start, &matchlength);
        if (match_start == -1)
        {
            break;
        }
        
        result[size] = (char*)malloc((matchlength + 1) * sizeof(char));
        strncpy(result[size], start + match_start, matchlength);
        result[size][matchlength] = '\0';
        size++;
        
        if (size == capacity)
        {
            capacity *= 2;
            result = (char**)realloc(result, capacity * sizeof(char*));
        }
        
        start += match_start + matchlength;
    }
    
    *count = size;
    return result;
}


int main() {
    const char* str = "123";
    const char* pattern = "\\d+";
    re_t compiled = re_compile(pattern);
    int match_length;

    printf("%d\n", re_matchp(compiled, str, &match_length));
    return 0;
}
