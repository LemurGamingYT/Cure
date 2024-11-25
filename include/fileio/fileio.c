#include "fileio.h"

#ifdef _WIN32
#include <fileapi.h> // for GetFileAttributes
#include <shlwapi.h> // for PathRelativePathTo

#ifndef bool
#define bool BOOL
#endif

#ifndef true
#define true TRUE
#endif

#ifndef false
#define false FALSE
#endif
#endif

#include <sys/stat.h>
#include <stdlib.h>
#include <string.h>


bool fileio_is_valid(FileIO* fileio) {
    return fileio->filename != NULL;
}

FileIO fileio_open(const char* filename) {
    return (FileIO){.filename = strdup(filename)};
}

FileIO fileio_as_child_of(const char* filename, FileIO* parent) {
    if (parent == NULL) return fileio_open(filename);
    int filename_length = strlen(parent->filename) + strlen(filename) + 2;
    char* path = malloc(filename_length);
    snprintf(path, filename_length, "%s/%s", parent->filename, filename);
    return fileio_open(path);
}

void fileio_free(FileIO* fileio) {
    if (fileio == NULL) return;
    if (fileio->filename != NULL) {
        free(fileio->filename);
        fileio->filename = NULL;
    }
}

size_t fileio_read(FileIO* fileio, char* buf) {
    if (!fileio_exists(fileio) || !fileio_is_valid(fileio) || fileio_is_dir(fileio)) return 0;

    FILE* file = fopen(fileio->filename, "r");
    if (file == NULL)
        return 0;
    
    size_t read = fread(buf, 1, strlen(buf), file);
    fclose(file);
    return read;
}

char* fileio_read_string(FileIO* fileio) {
    if (!fileio_exists(fileio) || !fileio_is_valid(fileio) || fileio_is_dir(fileio)) return NULL;

    FILE* file = fopen(fileio->filename, "r");
    if (file == NULL)
        return NULL;

    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fseek(file, 0, SEEK_SET);
    char* buf = (char*)malloc(size + 1);
    if (buf == NULL) {
        fclose(file);
        return NULL;
    }

    size_t bytes_read = fread((void*)buf, 1, size, file);
    buf[bytes_read] = '\0';

    fclose(file);
    return buf;
}

int fileio_write(FileIO* fileio, const char* data) {
    if (!fileio_is_valid(fileio)) return 0;

    FILE* file = fopen(fileio->filename, "w");
    if (file == NULL)
        return 0;
    
    int written = fprintf(file, data);
    fclose(file);
    return written;
}

long fileio_size(FileIO* fileio) {
    if (!fileio_exists(fileio) || !fileio_is_valid(fileio)) return -1;

    FILE* file = fopen(fileio->filename, "r");
    if (file == NULL)
        return 0;

    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fclose(file);
    return size;
}

bool fileio_exists(FileIO* fileio) {
    if (!fileio_is_valid(fileio)) return false;

    FILE* file = fopen(fileio->filename, "r");
    if (file == NULL)
        return false;
    
    fclose(file);
    return true;
}

bool fileio_delete(FileIO* fileio) {
    if (!fileio_exists(fileio) || !fileio_is_valid(fileio)) return false;
    return remove(fileio->filename) == 0;
}

bool fileio_rename(FileIO* fileio, const char* new_name) {
    if (!fileio_exists(fileio) || !fileio_is_valid(fileio)) return false;
    return rename(fileio->filename, new_name) == 0;
}

char* fileio_suffix(FileIO* fileio) {
    if (!fileio_is_valid(fileio)) return strdup("");
    char* dot = strrchr(fileio->filename, '.');
    if (dot == NULL || dot == fileio->filename) return strdup("");
    return strdup(dot);
}

char* fileio_stem(FileIO* fileio) {
    if (!fileio_is_valid(fileio)) return "";
    char* dot = strrchr(fileio->filename, '.');
    if (dot == NULL)
        return fileio->filename;
    
    size_t len = dot - fileio->filename;
    char* stem = (char*)malloc(len + 1);
    strncpy(stem, fileio->filename, len);
    stem[len] = '\0';
    return stem;
}

bool fileio_is_dir(FileIO* fileio) {
    if (!fileio_is_valid(fileio)) return false;
    struct stat path_stat;
    if (stat(fileio->filename, &path_stat) != 0) return false;
#ifdef _WIN32
    return (path_stat.st_mode & S_IFDIR) != 0;
#else
    return S_ISDIR(path_stat.st_mode);
#endif
}

bool fileio_is_file(FileIO* fileio) {
    if (!fileio_is_valid(fileio)) return false;
    struct stat path_stat;
    if (stat(fileio->filename, &path_stat) != 0) return false;
#ifdef _WIN32
    return (path_stat.st_mode & S_IFREG) != 0;
#else
    return S_ISREG(path_stat.st_mode);
#endif
}

bool fileio_is_link(FileIO* fileio) {
    if (!fileio_is_valid(fileio)) return false;
#ifdef _WIN32
    DWORD attributes = GetFileAttributes(fileio->filename);
    return (attributes != INVALID_FILE_ATTRIBUTES) && (attributes & FILE_ATTRIBUTE_REPARSE_POINT);
#else
    struct stat path_stat;
    if (stat(fileio->filename, &path_stat) != 0) return false;
    return S_ISLNK(path_stat.st_mode);
#endif
}

FileIO fileio_absolute(FileIO* fileio) {
    if (!fileio_is_valid(fileio)) return FILEIO_NULL;
#ifdef _WIN32
    char full_path[MAX_PATH];
    if (GetFullPathName(fileio->filename, MAX_PATH, full_path, NULL) == 0)
        return FILEIO_NULL;
    
    return fileio_open(full_path);
#else
    char* full_path = realpath(fileio->filename, NULL);
    FileIO result = fileio_open(full_path, fileio->mode);
    free(full_path);
    return result;
#endif
}

FileIO fileio_relative(FileIO* fileio, FileIO* to) {
    if (!fileio_is_valid(fileio) || !fileio_is_valid(to)) return FILEIO_NULL;
#ifdef _WIN32
    char path1[MAX_PATH], path2[MAX_PATH];
    if (GetFullPathName(fileio->filename, MAX_PATH, path1, NULL) == 0) return FILEIO_NULL;
    if (GetFullPathName(to->filename, MAX_PATH, path2, NULL) == 0) return FILEIO_NULL;

    char relative_path[MAX_PATH];
    if (PathRelativePathTo(path1, path2, FILE_ATTRIBUTE_DIRECTORY, path1, FILE_ATTRIBUTE_NORMAL) == 0)
        return FILEIO_NULL;
    
    return fileio_open(relative_path);
#else
    char* abs1 = realpath(fileio->filename, NULL);
    char* abs2 = realpath(to->filename, NULL);
    char* relative_path = calculate_relative_path(abs1, abs2);
    FileIO result = fileio_open(relative_path);
    free(abs1);
    free(abs2);
    free(relative_path);
    return result;
#endif
}

bool fileio_touch(FileIO* fileio) {
    if (!fileio_is_valid(fileio)) return false;
#ifdef _WIN32
    HANDLE file = CreateFile(fileio->filename, GENERIC_WRITE, 0, NULL, OPEN_ALWAYS,
        FILE_ATTRIBUTE_NORMAL, NULL);
    if (file == INVALID_HANDLE_VALUE) return false;
    CloseHandle(file);
    return true;
#else
    FILE* file = fopen(fileio->filename, "a");
    if (file == NULL) return false;
    fclose(file);
    return true;
#endif
}

bool fileio_mkdir(FileIO* fileio) {
    if (!fileio_is_valid(fileio)) return false;
#ifdef _WIN32
    return CreateDirectory(fileio->filename, NULL) != 0;
#else
    return mkdir(fileio->filename, 0777) == 0;
#endif
}

bool fileio_rmdir(FileIO* fileio) {
    if (!fileio_is_valid(fileio)) return false;
#ifdef _WIN32
    return RemoveDirectory(fileio->filename) != 0;
#else
    return rmdir(fileio->filename) == 0;
#endif
}
