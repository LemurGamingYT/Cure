from cure.objects import Object, Position, Free
from cure.c_manager import c_dec


BUFFER_SIZE = 1024

class http:
    def __init__(self, compiler) -> None:
        compiler.extra_compile_args.append('-lws2_32')
        compiler.add_toplevel_code("""typedef struct {
    int status_code;
    string headers;
    string body;
    size_t body_size;
    string url;
} HttpResponse;

void init_http_response(HttpResponse* response) {
    response->status_code = 0;
    response->headers = NULL;
    response->body = NULL;
    response->body_size = 0;
    response->url = NULL;
}

void free_http_response(HttpResponse* response) {
    if (response->headers != NULL) {
        free(response->headers);
    }
    
    if (response->body != NULL) {
        free(response->body);
    }
    
    if (response->url != NULL) {
        free(response->url);
    }
}

void init_winsock() {
    WSADATA wsaData;
    int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (result != 0) {
        fprintf(stderr, "WSAStartup failed with error: %d\\n", result);
        exit(1);
    }
}
""")
    
    @c_dec()
    def _HttpResponse_type(self, _, call_position: Position) -> Object:
        return Object('"HttpResponse"', 'string', call_position)
    
    @c_dec(param_types=('HttpResponse',))
    def _HttpResponse_to_string(self, compiler, call_position: Position,
                                response: object) -> Object:
        r = f'({response.code})'
        code, buf_free = compiler.c_manager.fmt_length(
            compiler, call_position,
            'HttpResponse(status_code=%d, url=%s)',
            f'{r}.status_code', f'{r}.url'
        )
        
        compiler.prepend_code(code)
        return Object(buf_free.object_name, 'string', call_position, free=buf_free)
    
    @c_dec(param_types=('string',), can_user_call=True)
    def _get_url(self, compiler, call_position: Position, url: Object) -> Object:
        compiler.c_manager.include('<string.h>', compiler)
        
        sock = compiler.create_temp_var('SOCKET', call_position)
        body_start = compiler.create_temp_var('string', call_position)
        body_size = compiler.create_temp_var('int', call_position)
        buffer_size = compiler.create_temp_var('int', call_position)
        old_body_size = compiler.create_temp_var('int', call_position)
        body = compiler.create_temp_var('string', call_position)
        hints = compiler.create_temp_var('struct addrinfo', call_position)
        res = compiler.create_temp_var('struct addrinfo *', call_position)
        request = compiler.create_temp_var('string', call_position)
        buf = compiler.create_temp_var('string', call_position)
        bytes_recieved = compiler.create_temp_var('int', call_position)
        result = compiler.create_temp_var('int', call_position)
        response_buf = Free(free_name='free_http_response')
        response = compiler.create_temp_var('HttpResponse', call_position, free=response_buf)
        response_buf.object_name = '&' + response
        hostname = compiler.create_temp_var('string', call_position)
        path = compiler.create_temp_var('string', call_position)
        status_line = compiler.create_temp_var('string', call_position)
        compiler.prepend_code(f"""#ifdef OS_WINDOWS
HttpResponse {response};
init_http_response(&{response});

SOCKET {sock};
struct addrinfo {hints}, *{res};
char {request}[{BUFFER_SIZE}];
char {buf}[{BUFFER_SIZE}];
int {bytes_recieved};

init_winsock();

string {hostname} = strdup({url.code});
{compiler.c_manager.buf_check(hostname)}
string {path} = strchr({hostname}, '/');
{compiler.c_manager.buf_check(path)}
if ({path}) {{
    *{path}++ = '\\0';
}} else {{
    {path} = "";
}}

memset(&{hints}, 0, sizeof({hints}));
{hints}.ai_family = AF_INET;
{hints}.ai_socktype = SOCK_STREAM;
{hints}.ai_protocol = IPPROTO_TCP;

int {result} = getaddrinfo({hostname}, "80", &{hints}, &{res});
if ({result} != 0) {{
    free({hostname});
    WSACleanup();
    {compiler.c_manager.err('Could not resolve host: %s', url.code)}
}}

{sock} = socket({res}->ai_family, {res}->ai_socktype, {res}->ai_protocol);
if ({sock} == INVALID_SOCKET) {{
    closesocket({sock});
    freeaddrinfo({res});
    free({hostname});
    WSACleanup();
    {compiler.c_manager.err('Could not create socket: %s', url.code)}
}}

freeaddrinfo({res});

snprintf({request}, sizeof({request}),
        "GET /%s HTTP/1.1\\r\\n"
        "Host: %s\\r\\n"
        "Connection: close\\r\\n"
        "\\r\\n",
        {path}, {hostname});
send({sock}, {request}, (int)strlen({request}), 0);

string {body_start} = NULL;
size_t {body_size} = 0;
size_t {buffer_size} = sizeof({buf});
while (({bytes_recieved} = recv({sock}, {buf}, {buffer_size} - 1, 0)) > 0) {{
    {buf}[{bytes_recieved}] = '\\0';
    if ({body_start} == NULL) {{
        string {body} = strstr({buf}, "\\r\\n\\r\\n");
        if ({body}) {{
            {body_start} = {body} + 4;
            {body_size} = {bytes_recieved} - ({body_start} - {buf});
            {response}.body = (string)malloc({body_size} + 1);
            {compiler.c_manager.buf_check(f'{response}.body')}
            if ({response}.body) {{
                memcpy({response}.body, {body_start}, {body_size});
                {response}.body[{body_size}] = '\\0';
            }}
        }}
    }} else {{
        size_t {old_body_size} = {body_size};
        {body_size} += {bytes_recieved};
        {response}.body = (string)realloc({response}.body, {body_size} + 1);
        {compiler.c_manager.buf_check(f'{response}.body')}
        if ({response}.body) {{
            memcpy({response}.body + {old_body_size}, {buf}, {bytes_recieved});
            {response}.body[{body_size}] = '\\0';
        }}
    }}
}}

{response}.url = strdup({url.code});
{compiler.c_manager.buf_check(f'{response}.url')}
if ({response}.body) {{
    {response}.body_size = {body_size};
}}

string {status_line} = strstr({response}.body, "HTTP/");
if ({status_line}) {{
    {response}.status_code = atoi({status_line} + 9);
}}

closesocket({sock});
WSACleanup();
free({hostname});
#else
#error "OS not supported"
#endif
""")
        
        return Object(response, 'HttpResponse', call_position, free=response_buf)
