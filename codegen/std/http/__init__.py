from codegen.objects import Object, Position, Type, Param, TempVar, Free, Arg
from codegen.c_manager import c_dec


class http:
    CAN_USE = False
    
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type('HttpRequest')
        codegen.add_toplevel_code("""#ifndef CURE_HTTP_H
#define CURE_HTTP_H
""")
        codegen.dependency_manager.use('sockets', codegen.pos)
        
        codegen.add_toplevel_code("""typedef struct {
    Socket sock;
    char host[256];
    char path[1024];
    char port[6];
} HttpRequest;
""")
        codegen.add_toplevel_code('#endif')
        
        codegen.c_manager.init_class(self, 'request', Type('HttpRequest'))
        codegen.c_manager.wrap_struct_properties('request', Type('HttpRequest'), [
            Param('sock', Type('Socket')), Param('host', Type('string')),
            Param('path', Type('string')), Param('port', Type('string'))
        ])
        
        
        @c_dec(
            params=(Param('request', Type('HttpRequest')),), is_method=True,
            add_to_class=self
        )
        def _HttpRequest_get(codegen, call_position: Position, request: Object) -> Object:
            request_str: TempVar = codegen.create_temp_var(Type('string'), call_position)
            result: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""char {request_str}[2048];
int {result};

snprintf(
    {request_str}, sizeof({request_str}),
    "GET %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n",
    {request}.path, {request}.host
);
""")
            
            codegen.call('Socket_connect', [
                Arg(request.attr('sock')), Arg(request.attr('host')), Arg(request.attr('port'))
            ], call_position)
            
            codegen.call('Socket_send', [
                Arg(request.attr('sock')), Arg(request_str.OBJECT())
            ], call_position)
            
            total_received: TempVar = codegen.create_temp_var(Type('int'), call_position)
            received: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {total_received} = 0;
int {received};
""")
            codegen.prepend_code(f"""while (({received} = {codegen.call('Socket_recv', [
    Arg(request.attr('sock')), Arg(Object('4096', Type('int'), call_position))
], call_position)})) {{
    
}}
""")
        
        @c_dec(
            params=(Param('host', Type('string')), Param('port', Type('string')),
                    Param('path', Type('string'))),
            is_method=True, is_static=True, add_to_class=self
        )
        def _HttpRequest_new(codegen, call_position: Position, host: Object, port: Object,
                             path: Object) -> Object:
            request_free = Free(free_name='socket_close')
            request: TempVar = codegen.create_temp_var(Type('HttpRequest'), call_position,
                                                       free=request_free)
            request_free.object_name = f'{request}.sock'
            codegen.prepend_code(f"""HttpRequest {request} = {{
    .sock = {codegen.call('Socket_new', [], call_position)},
    .host = {host}, .path = {path}, .port = {port}
}};
""")
            return request.OBJECT()
