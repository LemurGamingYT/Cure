#include "fstream.h"


File File_new(string filename) {
    return (File){ .filename = filename };
}

string File_filename(File* file) { return file->filename; }
string File_contents(File* file) {
    FILE* fp;
    if (fopen_s(&fp, (char*)(file->filename.ptr), "r"))
        error("cannot open file '%s': no such file or directory", (char*)(file->filename.ptr));

    fseek(fp, 0, SEEK_END);
    long size = ftell(fp);
    rewind(fp);

    u8* ptr = (u8*)heap_alloc(size + 1);
    fread(ptr, 1, size, fp);
    ptr[size] = (u8)'\0';

    fclose(fp);
    return string_new(ptr, size);
}

nil File_write(File* file, string contents) {
    FILE* fp;
    if (!fopen_s(&fp, (char*)(file->filename.ptr), "w"))
        error("cannot open file '%s': no such file or directory", (char*)(file->filename.ptr));
    
    fprintf(fp, "%s", (char*)(contents.ptr));
    fclose(fp);
    return NIL;
}
