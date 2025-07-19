#pragma once

#include "builtins/builtins.h"


typedef struct {
    string filename;
} File;


File File_new(string filename);
string File_filename(File* file);
string File_contents(File* file);
nil File_write(File* file, string contents);
