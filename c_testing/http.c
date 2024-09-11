#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdio.h>

#pragma comment(lib, "ws2_32.lib")


int main() {
    WSADATA wsaData;
    SOCKET ConnectSocket = INVALID_SOCKET;
    struct addrinfo hints, *result = NULL;
    char recvbuf[1024];
    int iResult;

    // Initialize Winsock
    WSAStartup(MAKEWORD(2, 2), &wsaData);

    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;

    // Resolve the server address and port
    getaddrinfo("http://openweathermap.org", "443", &hints, &result);

    // Create a SOCKET for connecting to server
    ConnectSocket = WSASocket(result->ai_family, result->ai_socktype, result->ai_protocol, NULL, 0, 0);

    // Connect to server.
    iResult = connect(ConnectSocket, result->ai_addr, (int)result->ai_addrlen);

    if (iResult == SOCKET_ERROR) {
        printf("connect failed with error: %d\n", WSAGetLastError());
        closesocket(ConnectSocket);
        WSACleanup();
        return 1;
    }

    // Send an HTTP GET request
    char* request = "GET / HTTP/1.1\r\nHost: http://openweathermap.org\r\n\r\n";
    send(ConnectSocket, request, strlen(request), 0);

    // Receive the response
    int bytesReceived = 0;
    do {
        iResult = recv(ConnectSocket, recvbuf, 1024, 0);
        if (iResult > 0) {
            bytesReceived += iResult;
            printf("%.*s", iResult, recvbuf);
        } else if (iResult == 0) {
            printf("Received %d bytes before connection was closed\n", bytesReceived);
        } else {
            printf("recv failed with error: %d\n", WSAGetLastError());
        }
    } while (iResult > 0);

    // shutdown the send half of the connection since no more data will be sent
    shutdown(ConnectSocket, SD_SEND);

    printf("%d bytes received\n", bytesReceived);

    // cleanup
    closesocket(ConnectSocket);
    WSACleanup();

    return 0;
}
