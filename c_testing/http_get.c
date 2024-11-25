#include "../include/tinycsocket/tinycsocket.h"

#include <stdlib.h>
#include <string.h>
#include <stdio.h>


char* http_get(const char* url) {
    char* buffer = NULL;
    size_t total_size = 0;
    size_t buffer_size = 0;
    const int chunk_size = 1024;

    socket_t sock;
    if (socket_init(&sock) == TINYSOCK_INIT_FAILED) {
        fprintf(stderr, "Failed to initialize socket\n");
        return NULL;
    }

    char* request = (char*)malloc(strlen(url) + 64);
    if (request == NULL) {
        fprintf(stderr, "out of memory\n");
        return NULL;
    }

    snprintf(request, strlen(url) + 64,
        "GET / HTTP/1.1\r\n"
        "Host: %s\r\n"
        "Connection: close\r\n"
        "\r\n", url
    );

    if (socket_connect(&sock, "93.184.216.34", "80") == TINYSOCK_CONNECTION_FAILED) {
        fprintf(stderr, "Failed to connect to %s\n", url);
        return NULL;
    }

    if (socket_send(&sock, request, strlen(request)) == TINYSOCK_SEND_FAILED) {
        fprintf(stderr, "Failed to send a request to %s\n", url);
        return NULL;
    }

    buffer = (char*)malloc(chunk_size);
    if (buffer == NULL)
        return NULL;
    
    buffer_size = chunk_size;

    int bytes;
    while ((bytes = socket_recv(&sock, buffer + total_size, chunk_size)) > 0) {
        total_size += bytes;
        if (total_size + chunk_size > buffer_size) {
            while (buffer_size < total_size + chunk_size) {
                buffer_size *= 2;
                buffer = realloc(buffer, buffer_size);
                if (buffer == NULL) {
                    fprintf(stderr, "out of memory\n");
                    return NULL;
                }
            }
        }
    }

    buffer[total_size] = '\0';
    socket_close(&sock);
    return buffer;
}


int main() {
    tinycsocket_init();

    char* buffer = http_get("https://example.com");
    if (buffer == NULL) {
        fprintf(stderr, "Failed to get a response from example.com\n");
        tinycsocket_cleanup();
        return 1;
    }

    printf("%s\n", buffer);

    free(buffer);

    tinycsocket_cleanup();
    return 0;
}
