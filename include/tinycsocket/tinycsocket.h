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
#endif


typedef struct {
#if _SOCKETS_WINDOWS_
    SOCKET sock;
#else
    int sock;
#endif
} socket_t;

#define TINYSOCK_SUCCESS 0
#define TINYSOCK_INIT_FAILED -1
#define TINYSOCK_INVALID_PARAM -2
#define TINYSOCK_CONNECTION_FAILED -3
#define TINYSOCK_SEND_FAILED -4
#define TINYSOCK_RECV_FAILED -5
#define TINYSOCK_HOSTNAME_GET_FAILED -6
#define TINYSOCK_SHUTDOWN_FAILED -7

int tinycsocket_init(void);
int tinycsocket_cleanup(void);

int tinycsocket_gethostname(char* buf, int len);

int socket_init(socket_t* sock);
int socket_close(socket_t* sock);
int socket_connect(socket_t* sock, const char* ip, const char* port);
int socket_send(socket_t* sock, const char* data, int len);
int socket_recv(socket_t* sock, char* data, int len);
int socket_bind(socket_t* sock, const char* ip, const char* port);
int socket_listen(socket_t* sock, int backlog);
int socket_accept(socket_t* server, socket_t* client);
int socket_shutdown(socket_t* sock, int how);

#endif
