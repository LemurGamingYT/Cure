#include "string_builder.h"
#include "utils.h"

#pragma comment(lib, "Ws2_32.lib")


typedef struct {
    SOCKET sock;
} Socket;

typedef struct {
    const string host, port;
    struct addrinfo* hints, *result;
    int return_code;
} AddrInfo;

typedef struct {
    int status_code;
    StringBuilder* headers, *body, *sb;
} HTTPResponse;


void HTTPResponse_free(HTTPResponse* response) {
    sb_destroy(response->headers);
    sb_destroy(response->body);
    sb_destroy(response->sb);
}


int init_winsock() {
    WSADATA wsaData;
    int res = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (res != 0) {
        error("WSAStartup failed: error code %d", res);
    }

    return 0;
}

int deinit_winsock() {
    int res = WSACleanup();
    if (res != 0) {
        error("WSACleanup failed: error code %d", res);
    }

    return 0;
}


AddrInfo AddrInfo_new(
    const string host, const string port, const int family, const int type, const int protocol
) {
    struct addrinfo *result, hints;
    
    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = family;
    hints.ai_socktype = type;
    hints.ai_protocol = protocol;

    int ret = getaddrinfo(host, port, &hints, &result);
    return (AddrInfo){
        .return_code = ret, .host = host, .port = port, .hints = &hints, .result = result
    };
}

void AddrInfo_free(AddrInfo* info) {
    if (info->result) {
        freeaddrinfo(info->result);
    }
}


bool Socket_is_invalid(const Socket sock) {
    return sock.sock == INVALID_SOCKET;
}

Socket Socket_new(const int family, const int type, const int protocol) {
    return (Socket){ .sock = socket(family, type, protocol) };
}

void Socket_free(Socket* sock) {
    if (!Socket_is_invalid(*sock)) {
        closesocket(sock->sock);
    }
}

int Socket_connect(Socket* sock, AddrInfo* info) {
    return connect(sock->sock, info->result->ai_addr, (int)info->result->ai_addrlen);
}

int Socket_send(Socket* sock, const string data, int length) {
    return send(sock->sock, data, length, 0);
}

int Socket_recv(Socket* sock, string buf, int buf_size) {
    return recv(sock->sock, buf, buf_size, 0);
}


void parse_headers(StringBuilder* sb, StringBuilder* headers, StringBuilder* body) {
    const string double_newline = strstr(sb->buf, "\r\n\r\n");
    if (double_newline) {
        size_t hlen = double_newline - sb->buf + 4;
        sb_add_len(headers, sb->buf, hlen);
        sb_add_len(body, double_newline + 4, sb->length - hlen);
    } else {
        sb_add_len(headers, sb->buf, sb->length);
    }
}

int parse_status_code(const string response) {
    int status_code;
    if (sscanf(response, "HTTP/1.1 %d", &status_code) != 1) {
        error("failed to parse status code");
    }

    return status_code;
}

HTTPResponse GET_request(const string host, const string path) {
    AddrInfo addr_info = AddrInfo_new(host, "80", AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (addr_info.return_code != 0) {
        deinit_winsock();
        error("getaddrinfo failed: error code %d", addr_info.return_code);
    }

    Socket sock = Socket_new(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (Socket_is_invalid(sock)) {
        AddrInfo_free(&addr_info);
        error("socket creation failed");
    }

    if (Socket_connect(&sock, &addr_info) == SOCKET_ERROR) {
        Socket_free(&sock);
        AddrInfo_free(&addr_info);
        error("connection failed");
    }

    char req[1024];
    snprintf(
        req, sizeof(req),
        "GET %s HTTP/1.1\r\n"
        "Host: %s\r\n"
        "Connection: close\r\n\r\n",
        path, host
    );

    if (Socket_send(&sock, req, strlen(req)) == SOCKET_ERROR) {
        Socket_free(&sock);
        AddrInfo_free(&addr_info);
        error("send failed");
    }

    StringBuilder headers = sb_new(1024);
    StringBuilder body = sb_new(4096);
    StringBuilder sb = sb_new(4096);

    char res[4096];
    int bytes_received;
    int status_code = -1;
    while ((bytes_received = Socket_recv(&sock, res, sizeof(res))) > 0) {
        sb_add_len(&sb, res, bytes_received);
        if (status_code == -1) {
            status_code = parse_status_code(sb.buf);
        }
    }

    parse_headers(&sb, &headers, &body);

    Socket_free(&sock);
    AddrInfo_free(&addr_info);
    return (HTTPResponse){.headers = &headers, .body = &body, .sb = &sb, .status_code = status_code};
}


int main() {
    init_winsock();

    HTTPResponse response = GET_request("example.com", "/");
    printf("Headers:\n%s\n", sb_str(response.headers));
    printf("Body:\n%s\n", sb_str(response.body));
    printf("Status code: %d\n", response.status_code);

    HTTPResponse_free(&response);
    deinit_winsock();
    return 0;
}
