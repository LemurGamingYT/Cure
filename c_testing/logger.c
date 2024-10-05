#include "utils.h"


typedef struct {
    FILE* out;
} Logger;


#define DEFAULT_CAPACITY 10


Logger Logger_new(FILE* out) {
    return (Logger){.out = out};
}

void Logger_dump(Logger* logger) {
    fflush(logger->out);
}

void Logger_log(Logger* logger, string content) {
    fprintf(logger->out, "%s\n", content);
}


int main() {
    FILE* log_file = fopen("c_testing/test.log", "w");
    if (log_file == NULL) {
        printf("failed to open file\n");
        return 1;
    }

    Logger logger = Logger_new(log_file);
    Logger_log(&logger, "Hello world!");
    Logger_log(&logger, "AA");

    fclose(log_file);
    return 0;
}
