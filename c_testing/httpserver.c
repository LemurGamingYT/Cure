#include <tinycsocket/tinycsocket.h>
#include <process.h>
#include <string.h>
#include <stdio.h>


#define HTTP_BUFFER_SIZE 4096
#define HTTP_MAX_HEADERS 100

typedef struct {
  char method[16], path[256], version[16], headers[HTTP_MAX_HEADERS], *body;
  int header_count;
} http_request_t;

typedef struct {
  int status_code, header_count;
  char status_text[32], headers[HTTP_MAX_HEADERS], *body;
} http_response_t;


int http_server_start(const char* ip, const char* port) {
  socket_t server_sock;
  if (socket_init(&server_sock) != TINYSOCK_SUCCESS)
    return -1;
  
  if (socket_bind(&server_sock, ip, port) != TINYSOCK_SUCCESS) {
    socket_close(&server_sock);
    return -1;
  }
  
  if (socket_listen(&server_sock, 10) != TINYSOCK_SUCCESS) {
    socket_close(&server_sock);
    return -1;
  }

  printf("HTTP Server listening on %s:%s\n", ip, port);
  while (1) {
    socket_t client_sock;
    if (socket_accept(&server_sock, &client_sock) == 0) {
      unsigned threadId;
      _beginthreadex(NULL, 0, client_handler, &client_sock, 0, &threadId);
    }
  }

  return 0;
}

void http_parse_request(const char* raw_request, http_request_t* request) {
  char* line = strdup(raw_request), *saveptr, *context = NULL;
  char* token = strtok_s(line, " ", &context);
  if (token) strncpy(request->method, token, sizeof(request->method) - 1);

  token = strtok_s(NULL, " ", &context);
  if (token) strncpy(request->path, token, sizeof(request->path) - 1);

  token = strtok_s(NULL, "\r\n", &context);
  if (token) strncpy(request->version, token, sizeof(request->version) - 1);

  request->header_count = 0;
  while ((token = strtok_s(NULL, "\r\n", &context)) != NULL && request->header_count < HTTP_MAX_HEADERS) {
    if (strlen(token) == 0) break;
    strncpy(request->headers[request->header_count++], token, 255);
  }

  free(line);
}

void http_send_response(socket_t* client_sock, http_response_t* response) {
  char buffer[HTTP_BUFFER_SIZE];
  int len = 0;

  len += sprintf(buffer + len, "HTTP/1.1 %d %s\r\n", response->status_code, response->status_text);
  for (int i = 0; i < response->header_count; i++)
    len += sprintf(buffer + len, "%s\r\n", response->headers[i]);
  
  len += sprintf(buffer + len, "\r\n%s", response->body);
  socket_send(client_sock, buffer, len);
}


unsigned __stdcall client_handler(void* arg) {
  socket_t* client_sock = (socket_t*)arg;
  handle_client(client_sock);

  _endthreadex(0);
  return 0;
}


int main(void) {
  http_server_start("97.1.32", "8080");
  return 0;
}
