from codegen.objects import Object, Position, Type, Param, TempVar, Free
from codegen.c_manager import c_dec


class http:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type('HTTPResponse')
        codegen.add_toplevel_code("""#ifndef CURE_HTTP_H
#define CURE_HTTP_H

typedef struct {
    int status_code;
    StringBuilder *headers, *body, *sb;
} HTTPResponse;

void free_HTTPResponse(HTTPResponse* response) {
    free(response->headers->buf);
    free(response->body->buf);
    free(response->sb->buf);
}
#endif
""")
        
        codegen.c_manager.init_class(self, 'HTTPResponse', Type('HTTPResponse'))
        codegen.c_manager.wrap_struct_properties(
            'response', Type('HTTPResponse'), [Param('status_code', Type('int'))]
        )
        
        @c_dec(
            param_types=(Param('response', Type('HTTPResponse')),),
            is_method=True, add_to_class=self
        )
        def _HTTPResponse_to_string(codegen, call_position: Position, response: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, '"HTTPResponse(status_code=%d)"',
                f'({response}).status_code'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(
            param_types=(Param('response', Type('HTTPResponse')),),
            is_method=True, add_to_class=self
        )
        def _HTTPResponse_to_bool(_, call_position: Position, response: Object) -> Object:
            return Object(f'(({response}).status_code == 200)', Type('bool'), call_position)
        
        @c_dec(
            param_types=(Param('response', Type('HTTPResponse')),),
            is_property=True, add_to_class=self
        )
        def _HTTPResponse_content(codegen, call_position: Position, response: Object) -> Object:
            return codegen.c_manager._StringBuilder_str(
                codegen, call_position,
                Object(f'(*({response}).body)', Type('StringBuilder'), call_position)
            )
        
        @c_dec(
            param_types=(Param('host', Type('string')), Param('path', Type('string'))),
            can_user_call=True, add_to_class=self
        )
        def _get_req(codegen, call_position: Position, host: Object, path: Object) -> Object:
            codegen.dependency_manager.use('http/sockets', call_position)
            
            socket_configs = [
                codegen.c_manager._SocketFamily_AF_INET(codegen, call_position),
                codegen.c_manager._SocketType_SOCK_STREAM(codegen, call_position),
                codegen.c_manager._SocketProtocol_IPPROTO_TCP(codegen, call_position)
            ]
            
            info: Object = codegen.c_manager._AddrInfo_new(
                codegen, call_position, host, Object('"80"', Type('string'), call_position),
                *socket_configs
            )
            response_free = Free(free_name='free_HTTPResponse')
            response: TempVar = codegen.create_temp_var(
                Type('HTTPResponse'), call_position, free=response_free,
                default_expr='{ .headers = NULL, .body = NULL, .sb = NULL }',
            )
            response_free.object_name = f'&{response}'
            
            req: TempVar = codegen.create_temp_var(Type('string'), call_position)
            
            sock: Object = codegen.c_manager._Socket_new(codegen, call_position, *socket_configs)
            ret: Object = codegen.c_manager._Socket_connect(codegen, call_position, sock, info)
            codegen.prepend_code(f"""if ({ret} == SOCKET_ERROR) {{
    {codegen.c_manager.err('connection failed')}
}}

char {req}[1024];
snprintf(
    {req}, sizeof({req}),
    "GET %s HTTP/1.1\\r\\n"
    "Host: %s\\r\\n"
    "Connection: close\\r\\n\\r\\n",
    {path}, {host}
);
""")
            
            ret = codegen.c_manager._Socket_send(
                codegen, call_position, sock, req.OBJECT(),
                codegen.c_manager._string_length(codegen, call_position, req.OBJECT())
            )
            codegen.prepend_code(f"""if ({ret} == SOCKET_ERROR) {{
    {codegen.c_manager.err('send failed')}
}}
""")
            
            sb: Object = codegen.c_manager._StringBuilder_new(
                codegen, call_position, Object('4096', Type('int'), call_position)
            )
            headers: Object = codegen.c_manager._StringBuilder_new(
                codegen, call_position, Object('1024', Type('int'), call_position)
            )
            body: Object = codegen.c_manager._StringBuilder_new(
                codegen, call_position, Object('4096', Type('int'), call_position)
            )
            codegen.scope.remove_free(sb.free)
            codegen.scope.remove_free(headers.free)
            codegen.scope.remove_free(body.free)
            
            res: TempVar = codegen.create_temp_var(Type('string'), call_position)
            bytes_received: TempVar = codegen.create_temp_var(Type('int'), call_position)
            status_code: TempVar = codegen.create_temp_var(Type('int'), call_position)
            temp_status: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""char {res}[4096];
int {bytes_received};
int {status_code} = -1;
""")
            ret = codegen.c_manager._Socket_recv(
                codegen, call_position, sock, res,
                codegen.c_manager._sizeof(codegen, call_position, res)
            )
            codegen.prepend_code(f"""while (({bytes_received} = {ret}) > 0) {{
""")
            codegen.c_manager._StringBuilder_len_add(
                codegen, call_position, 
                sb, res.OBJECT(), bytes_received.OBJECT()
            )
            codegen.prepend_code(f"""if ({status_code} == -1) {{
    int {temp_status};
""")
            double_new_line: TempVar = codegen.create_temp_var(Type('string'), call_position)
            hlen: TempVar = codegen.create_temp_var(Type('int', 'size_t'), call_position)
            sb_str: Object = codegen.c_manager._StringBuilder_str(codegen, call_position, sb)
            codegen.scope.remove_free(sb_str.free)
            codegen.prepend_code(f"""sscanf({sb_str}, "HTTP/1.1 %d", &{temp_status});

{status_code} = {temp_status};
free({sb_str});
}}
}}

const string {double_new_line} = strstr(({sb}).buf, "\\r\\n\\r\\n");
if ({double_new_line}) {{
    size_t {hlen} = {double_new_line} - ({sb}).buf + 4;
""")
            codegen.c_manager._StringBuilder_len_add(
                codegen, call_position,
                headers, Object(f'({sb}).buf', Type('string'), call_position), hlen.OBJECT()
            )
            
            codegen.c_manager._StringBuilder_len_add(
                codegen, call_position,
                body, Object(f'{double_new_line} + 4', Type('string'), call_position),
                Object(f'({sb}).length - {hlen}', Type('int'), call_position)
            )
            
            codegen.prepend_code("""} else {
""")
            
            codegen.c_manager._StringBuilder_len_add(
                codegen, call_position, headers, Object(f'({sb}).buf', Type('string'), call_position),
                Object(f'({sb}).length', Type('int'), call_position)
            )
            
            codegen.prepend_code(f"""}}

{response} = ({response.type.c_type}){{
    .headers = &{headers}, .body = &{body}, .sb = &{sb}, .status_code = {status_code}
}};
""")
            
            return response.OBJECT()
