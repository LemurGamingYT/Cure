#include "../include/iniparser/iniparser.h"
#include "utils.h"


int main() {
    char *ini_file = "c_testing/test.ini";
    dictionary* ini = iniparser_load(ini_file);
    if (ini == NULL) {
        error("cannot parse file: %s\n", ini_file);
    }

    iniparser_dump(ini, stdout);

    int i = iniparser_getint(ini, "a:b", -1);
    printf("a:b = %d\n", i);

    iniparser_freedict(ini);
    return 0;
}
