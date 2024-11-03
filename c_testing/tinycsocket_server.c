#include "../include/tinycsocket/tinycsocket.h"

#include <stdio.h>


const char* port = "8080";
const char* ip = "127.0.0.1";
#define SEND_BACK "Hello from server!"

int main() {
    if (tinycsocket_init() != 0) {
        fprintf(stderr, "Failed to initialise tinycsocket\n");
        return 1;
    }

    socket_t server;
    if (socket_init(&server) != 0) {
        fprintf(stderr, "Failed to create socket\n");
        goto cleanup;
        return 1;
    }

    char buffer[1024];
    if (socket_bind(&server, ip, port) != 0) {
        fprintf(stderr, "Failed to bind socket to port and ip\n");
        goto cleanup;
        return 1;
    }

    if (socket_listen(&server, SOMAXCONN) != 0) {
        fprintf(stderr, "Failed to listen on socket\n");
        goto cleanup;
        return 1;
    }

    printf("Server listening on port 8080...\n");
    
    socket_t client;
    if (socket_accept(&server, &client) != 0) {
        fprintf(stderr, "Failed to accept client connection\n");
        goto cleanup;
        return 1;
    }

    while (1) {
        int bytes = socket_recv(&client, buffer, sizeof(buffer));
        if (bytes <= 0) continue;

        buffer[bytes] = '\0';
        printf("Received: %s\n", buffer);

        int send_result = socket_send(&client, SEND_BACK, strlen(SEND_BACK));
        if (send_result != strlen(SEND_BACK)) {
            fprintf(stderr, "Failed to send back to the client (error code: %d)\n", WSAGetLastError());
            goto cleanup;
            return 1;
        }

        break;
    }

    goto cleanup;
    return 0;
cleanup:
    if (server.sock != INVALID_SOCKET) {
        if (socket_close(&server) != 0) {
            fprintf(stderr, "Failed to close socket\n");
            return 1;
        }
    }

    if (tinycsocket_cleanup() != 0) {
        fprintf(stderr, "Failed to clean up tinycsocket\n");
        return 1;
    }
}
