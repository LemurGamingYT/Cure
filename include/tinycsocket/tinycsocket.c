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

int tinycsocket_gethostname(char* buf, int len) {
    if (gethostname(buf, len) == SOCKET_ERROR)
        return TINYSOCK_HOSTNAME_GET_FAILED;
    
    return 0;
}

int socket_init(socket_t* sock) {
    sock->sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
#if _SOCKETS_WINDOWS_
    if (sock->sock == INVALID_SOCKET)
        return TINYSOCK_INIT_FAILED;
#else
    if (sock->sock < 0)
        return TINYSOCK_INIT_FAILED;
#endif

    return 0;
}

int socket_close(socket_t* sock) {
    if (sock == NULL)
        return TINYSOCK_INVALID_PARAM;
#if _SOCKETS_WINDOWS_
    return closesocket(sock->sock);
#else
    return close(sock->sock);
#endif
}

int socket_connect(socket_t* sock, const char* ip, const char* port) {
    if (sock == NULL || ip == NULL || port == NULL)
        return TINYSOCK_INVALID_PARAM;

    struct sockaddr_in name;
    name.sin_family = AF_INET;
    name.sin_port = htons(atoi(port));
    if (inet_pton(AF_INET, ip, &name.sin_addr) != 1)
        return TINYSOCK_INVALID_PARAM;
    
    int ret = connect(sock->sock, (struct sockaddr*)&name, sizeof(name));
    return ret == 0 ? 0 : TINYSOCK_CONNECTION_FAILED;
}

int socket_send(socket_t* sock, const char* data, int len) {
    if (sock == NULL || data == NULL)
        return TINYSOCK_INVALID_PARAM;

#if _SOCKETS_WINDOWS_
    if (send(sock->sock, data, len, 0) != len)
        return TINYSOCK_SEND_FAILED;
    
    return 0;
#else
    return send(sock->sock, data, len, MSG_NOSIGNAL);
#endif
}

int socket_recv(socket_t* sock, char* data, int len) {
    if (sock == NULL || data == NULL)
        return TINYSOCK_INVALID_PARAM;
    
    return recv(sock->sock, data, len, 0);
}

int socket_bind(socket_t* sock, const char* ip, const char* port) {
    if (sock == NULL || ip == NULL || port == NULL)
        return TINYSOCK_INVALID_PARAM;

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

int socket_shutdown(socket_t* sock, int how) {
    if (shutdown(sock->sock, how) == SOCKET_ERROR)
        return TINYSOCK_SHUTDOWN_FAILED;
    
    return 0;
}
