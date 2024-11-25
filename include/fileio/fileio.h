#ifndef FILEIO_H
#define FILEIO_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>
#include <stdio.h>

typedef struct {
    char* filename;
} FileIO;

#define FILEIO_NULL ((FileIO){.filename = NULL})

bool fileio_is_valid(FileIO* fileio);
FileIO fileio_open(const char* filename);
FileIO fileio_as_child_of(const char* filename, FileIO* parent);
void fileio_free(FileIO* fileio);
size_t fileio_read(FileIO* fileio, char* buf);
char* fileio_read_string(FileIO* fileio);
int fileio_write(FileIO* fileio, const char* data);
long fileio_size(FileIO* fileio);
bool fileio_exists(FileIO* fileio);
bool fileio_delete(FileIO* fileio);
bool fileio_rename(FileIO* fileio, const char* new_name);
char* fileio_suffix(FileIO* fileio);
char* fileio_stem(FileIO* fileio);
bool fileio_is_dir(FileIO* fileio);
bool fileio_is_file(FileIO* fileio);
bool fileio_is_link(FileIO* fileio);
FileIO fileio_absolute(FileIO* fileio);
FileIO fileio_relative(FileIO* fileio, FileIO* to);
bool fileio_touch(FileIO* fileio);
bool fileio_mkdir(FileIO* fileio);
bool fileio_rmdir(FileIO* fileio);

#ifdef __cplusplus
}
#endif

#endif
