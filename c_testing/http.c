#define WIN32_LEAN_AND_MEAN
#include <winsock2.h>
#include <ws2tcpip.h>
#include <string.h>
#include <stdio.h>

#pragma comment(lib, "Ws2_32.lib")  // Link against the Winsock library

#define BUFFER_SIZE 4096

// Initialize Winsock and return the status
int initialize_winsock() {
    WSADATA wsaData;
    int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (result != 0) {
        printf("WSAStartup failed: %d\n", result);
        return result;
    }
    return 0;
}

// Create and return a connected socket to the host
SOCKET create_connection(const char *host, const char *port) {
    struct addrinfo *result = NULL, *ptr = NULL, hints;
    SOCKET sock = INVALID_SOCKET;
    int ret;

    // Set up the hints for getaddrinfo
    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;

    // Resolve the server address and port
    ret = getaddrinfo(host, port, &hints, &result);
    if (ret != 0) {
        printf("getaddrinfo failed: %d\n", ret);
        WSACleanup();
        return INVALID_SOCKET;
    }

    // Attempt to connect to the first available address
    for (ptr = result; ptr != NULL; ptr = ptr->ai_next) {
        sock = socket(ptr->ai_family, ptr->ai_socktype, ptr->ai_protocol);
        if (sock == INVALID_SOCKET) {
            printf("Error at socket(): %ld\n", WSAGetLastError());
            freeaddrinfo(result);
            WSACleanup();
            return INVALID_SOCKET;
        }

        // Connect to the server
        ret = connect(sock, ptr->ai_addr, (int)ptr->ai_addrlen);
        if (ret == SOCKET_ERROR) {
            closesocket(sock);
            sock = INVALID_SOCKET;
            continue;
        }
        break;
    }

    freeaddrinfo(result);

    if (sock == INVALID_SOCKET) {
        printf("Unable to connect to server!\n");
        WSACleanup();
        return INVALID_SOCKET;
    }

    return sock;
}

void http_get(const char *host, const char *path) {
    SOCKET sockfd;
    char send_buffer[BUFFER_SIZE];
    char recv_buffer[BUFFER_SIZE];
    int bytes_received;
    int redirect_limit = 5;  // Prevent infinite redirect loops

    // Ensure that the path starts with a "/"
    if (path == NULL || path[0] != '/') {
        path = "/";
    }

    while (redirect_limit-- > 0) {
        // Connect to the server on port 80 (HTTP)
        sockfd = create_connection(host, "80");
        if (sockfd == INVALID_SOCKET) {
            return;
        }

        // Create the GET request string with HTTP/1.1
        snprintf(send_buffer, sizeof(send_buffer),
                 "GET %s HTTP/1.1\r\n"
                 "Host: %s\r\n"
                 "Connection: close\r\n"
                 "\r\n", path, host);

        // Send the GET request
        if (send(sockfd, send_buffer, (int)strlen(send_buffer), 0) == SOCKET_ERROR) {
            printf("send failed: %d\n", WSAGetLastError());
            closesocket(sockfd);
            WSACleanup();
            return;
        }

        int header_parsed = 0;
        char *location_header = NULL;

        // Receive the response and check for redirect
        do {
            bytes_received = recv(sockfd, recv_buffer, BUFFER_SIZE - 1, 0);
            if (bytes_received > 0) {
                recv_buffer[bytes_received] = '\0';  // Null-terminate the string

                if (!header_parsed) {
                    // Look for the status line
                    if (strstr(recv_buffer, "HTTP/1.1 301") || strstr(recv_buffer, "HTTP/1.1 302")) {
                        // Look for the Location header
                        location_header = strstr(recv_buffer, "Location: ");
                        if (location_header) {
                            location_header += 10;  // Move past "Location: "
                            char *end_of_url = strstr(location_header, "\r\n");
                            if (end_of_url) {
                                *end_of_url = '\0';  // Null-terminate the URL
                                printf("Redirecting to %s\n", location_header);

                                // Parse the new URL
                                if (strncmp(location_header, "http://", 7) == 0) {
                                    location_header += 7;  // Skip "http://"
                                }

                                // Extract new host and path
                                char *new_host = location_header;
                                char *new_path = strchr(location_header, '/');
                                if (new_path) {
                                    *new_path = '\0';  // Null-terminate the host
                                    new_path++;  // Skip '/'
                                } else {
                                    new_path = "";  // Default path
                                }

                                // Set new host and path for the next request
                                host = new_host;
                                path = new_path;

                                // Break to follow the redirect
                                break;
                            }
                        }
                    }

                    header_parsed = 1;  // Header parsed, continue with body
                    printf("%s", recv_buffer);  // Print the current buffer contents
                }
            } else if (bytes_received == 0) {
                printf("\nConnection closed\n");
            } else {
                printf("recv failed: %d\n", WSAGetLastError());
            }
        } while (bytes_received > 0);

        closesocket(sockfd);

        // If no location header was found, break out of the loop
        if (!location_header) {
            break;
        }
    }

    WSACleanup();
}

int main() {
    // Initialize Winsock
    if (initialize_winsock() != 0) {
        return 1;
    }

    // Send a GET request to google.com
    http_get("google.com", "/");

    return 0;
}
