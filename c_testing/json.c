#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

#include "../include/cJSON/cJSON.h"


char* get_file_contents(const char* filename) {
    FILE* fp = fopen(filename, "rb");
    if (fp == NULL) {
        return NULL;
    }

    fseek(fp, 0, SEEK_END);
    size_t filesize = ftell(fp);
    fseek(fp, 0, SEEK_SET);

    char* contents = (char*)malloc(filesize + 1);
    if (contents == NULL) {
        fclose(fp);
        return NULL;
    }

    size_t read = fread(contents, 1, filesize, fp);
    if (read != filesize) {
        free(contents);
        fclose(fp);
        return NULL;
    }

    fclose(fp);
    contents[filesize] = '\0';
    return contents;
}


int main() {
    char* contents = get_file_contents("examples/libraries/test.json");
    cJSON* json = cJSON_Parse(contents);
    if (json == NULL) {
        const char* eptr = cJSON_GetErrorPtr();
        if (eptr != NULL) {
            printf("JSON parsing error: %s\n", eptr);
            return 1;
        }
        
        printf("JSON parsing error\n");
        return 1;
    }

    cJSON_AddStringToObject(json, "surname", "Crockford");

    printf("%s\n", cJSON_Print(json));

    cJSON_Delete(json);
    free(contents);
    return 0;
}
