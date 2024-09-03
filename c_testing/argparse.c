#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../include/argparse/argparse.h"


const char* const usages[] = {
    "test [options] [[--] args]",
    "test [options]",
    NULL
};


int main() {
    int age = 0;
    struct argparse_option options[] = {
        OPT_HELP(),
        OPT_INTEGER('a', "age", &age, "Test age", NULL, 0, 0),
        OPT_END()
    };

    struct argparse argp;
    argparse_init(&argp, options, usages, 0);
    argparse_describe(&argp, "\nDescription of program", "Additional description after args");
    argparse_parse(&argp, __argc, (const char**)__argv);
    if (age != 0) {
        printf("Age: %d\n", age);
    }

    return 0;
}
