#ifndef __TINYCSOCKET_H__
#define __TINYCSOCKET_H__

#define _SOCKETS_WINDOWS_ _WIN32
#if _SOCKETS_WINDOWS_
#include <WinSock2.h>
#include <WS2tcpip.h>
#pragma comment(lib, "Ws2_32.lib")
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>

#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
#endif


typedef struct {
#if _SOCKETS_WINDOWS_
    SOCKET sock;
#else
    int sock;
#endif
} socket_t;

int tinycsocket_init(void);
int tinycsocket_cleanup(void);

int socket_init(socket_t* sock);
int socket_close(socket_t* sock);
int socket_connect(socket_t* sock, const char* ip, const char* port);
int socket_send(socket_t* sock, const char* data, int len);
int socket_recv(socket_t* sock, char* data, int len);
int socket_bind(socket_t* sock, const char* ip, const char* port);
int socket_listen(socket_t* sock, int backlog);
int socket_accept(socket_t* server, socket_t* client);

#endif