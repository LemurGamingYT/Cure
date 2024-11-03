#include "tinycsocket.h"


int tinycsocket_init(void) {
#if _SOCKETS_WINDOWS_
    WSADATA wsaData;
    return WSAStartup(MAKEWORD(2, 2), &wsaData);
#else
    return 0;
#endif
}

int tinycsocket_cleanup(void) {
#if _SOCKETS_WINDOWS_
    return WSACleanup();
#else
    return 0;
#endif
}

int socket_init(socket_t* sock) {
    sock->sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
#if _SOCKETS_WINDOWS_
    if (sock->sock == INVALID_SOCKET)
        return SOCKET_ERROR;
#else
    if (sock->sock < 0)
        return SOCKET_ERROR;
#endif

    return 0;
}

int socket_close(socket_t* sock) {
#if _SOCKETS_WINDOWS_
    return closesocket(sock->sock);
#else
    return close(sock->sock);
#endif
}

int socket_connect(socket_t* sock, const char* ip, const char* port) {
    struct sockaddr_in name;
    name.sin_family = AF_INET;
    name.sin_port = htons(atoi(port));
    inet_pton(AF_INET, ip, &name.sin_addr);
    return connect(sock->sock, (struct sockaddr*)&name, sizeof(name));
}

int socket_send(socket_t* sock, const char* data, int len) {
#if _SOCKETS_WINDOWS_
    return send(sock->sock, data, len, 0);
#else
    return send(sock->sock, data, len, MSG_NOSIGNAL);
#endif
}

int socket_recv(socket_t* sock, char* data, int len) {
    return recv(sock->sock, data, len, 0);
}

int socket_bind(socket_t* sock, const char* ip, const char* port) {
    struct sockaddr_in name;
    name.sin_family = AF_INET;
    name.sin_port = htons(atoi(port));
    inet_pton(AF_INET, ip, &name.sin_addr);
#if !_SOCKETS_WINDOWS_
    int enable = 1;
    setsockopt(sock->sock, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int));
#endif
    return bind(sock->sock, (struct sockaddr*)&name, sizeof(name));
}

int socket_listen(socket_t* sock, int backlog) {
    return listen(sock->sock, backlog);
}

int socket_accept(socket_t* server, socket_t* client) {
    client->sock = accept(server->sock, NULL, NULL);
#if _SOCKETS_WINDOWS_
    return (client->sock == INVALID_SOCKET) ? SOCKET_ERROR : 0;
#else
    return (client->sock < 0) ? SOCKET_ERROR : 0;
#endif
}
