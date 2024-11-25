#include "../include/fileio/fileio.h"

#include <stdlib.h>
#include <stdio.h>


int main() {
    // Create and write to a file
    FileIO file = fileio_open("test.txt");
    fileio_write(&file, "Hello, World!");

    // Read the file contents
    char* content = fileio_read_string(&file);
    if (content) {
        printf("File contents: %s\n", content);
        free(content);  // Free the allocated string
    }

    // Get file information
    printf("File size: %ld bytes\n", fileio_size(&file));
    printf("File extension: %s\n", fileio_suffix(&file));
    printf("File stem: %s\n", fileio_stem(&file));

    // File operations
    FileIO new_file = fileio_open("renamed.txt");
    fileio_rename(&file, new_file.filename);
    fileio_free(&new_file);

    // Directory operations
    FileIO dir = fileio_open("test_dir");
    if (fileio_mkdir(&dir)) {
        printf("Directory created\n");
    }

    // Create a file in that directory
    FileIO dir_file = fileio_open("test_dir/test.txt");
    fileio_touch(&dir_file);

    // Cleanup
    fileio_free(&dir_file);
    fileio_free(&file);
    fileio_free(&dir);

    return 0;
}
