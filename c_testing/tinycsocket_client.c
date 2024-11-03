#include "../include/tinycsocket/tinycsocket.h"

#include <stdio.h>


const char* port = "8080";
const char* ip = "127.0.0.1";
#define SEND_TO_SERVER "Hello from the client!"

int main() {
    if (tinycsocket_init() != 0) {
        fprintf(stderr, "Failed to initialise tinycsocket\n");
        return 1;
    }

    socket_t client;
    if (socket_init(&client) != 0) {
        fprintf(stderr, "Failed to initialise socket\n");
        goto cleanup;
        return 1;
    }

    if (socket_connect(&client, ip, port) != 0) {
        fprintf(stderr, "Failed to connect client to the server\n");
        goto cleanup;
        return 1;
    }

    printf("Connected to the server!\n");

    int send_result = socket_send(&client, SEND_TO_SERVER, strlen(SEND_TO_SERVER));
    if (send_result != strlen(SEND_TO_SERVER)) {
        fprintf(stderr, "Failed to send message to server\n");
        goto cleanup;
        return 1;
    }

    char buffer[1024];
    int bytes = socket_recv(&client, buffer, sizeof(buffer));
    if (bytes < 0) {
        fprintf(stderr, "Failed to receive message\n");
        goto cleanup;
        return 1;
    }

    buffer[bytes] = '\0';
    printf("Server says: %s\n", buffer);

    goto cleanup;
    return 0;
cleanup:
    if (client.sock != INVALID_SOCKET)
        socket_close(&client);

    if (tinycsocket_cleanup() != 0) {
        fprintf(stderr, "Failed to clean up tinycsocket\n");
        return 1;
    }
}
