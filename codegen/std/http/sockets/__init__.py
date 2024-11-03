from codegen.objects import Object, Position, Type, Param, Free, TempVar
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec
from codegen.target import Target


class sockets:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""#ifndef CURE_HTTP_SOCKETS_H
#define CURE_HTTP_SOCKETS_H
""")
        
        if codegen.target != Target.WINDOWS:
            codegen.pos.not_supported_err('sockets')
        
        codegen.extra_compile_args.append('-lws2_32')
        codegen.add_toplevel_code("""#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "Ws2_32.lib")
""")
        
        codegen.type_checker.add_type(('Socket', 'AddrInfo'))
        
        codegen.c_enum(
            'SocketFamily', [
                ('AF_UNSPEC', 0), ('AF_INET', 2), ('AF_IPX', 6), ('AF_APPLETALK', 16),
                ('AF_NETBIOS', 17), ('AF_INET6', 23), ('AF_IRDA', 26), ('AF_BTH', 32)
            ], codegen.pos
        )
        
        codegen.c_enum(
            'SocketType', ['SOCK_STREAM', 'SOCK_DGRAM', 'SOCK_RAW', 'SOCK_RDM'],
            codegen.pos, start=1
        )
        
        codegen.c_enum(
            'SocketProtocol', [
                'IPPROTO_ICMP', 'IPPROTO_IGMP', ('IPPROTO_TCP', 6), ('IPPROTO_UDP', 17),
                ('IPPROTO_ICMPV6', 58)
            ], codegen.pos, start=1
        )
        
        codegen.add_toplevel_code("""typedef struct {
    SocketFamily family;
    SocketType type;
    SocketProtocol protocol;
    SOCKET sock;
} Socket;

typedef struct {
    string host, port;
    struct addrinfo* hints, *result;
    int return_code;
} AddrInfo;
""")
        
        codegen.add_toplevel_code('#endif')
        
        res: TempVar = codegen.create_temp_var(Type('int'), codegen.pos)
        wsa_data: TempVar = codegen.create_temp_var(Type('WSADATA'), codegen.pos)
        codegen.main_init_code += f"""WSADATA {wsa_data} = {{0}};
int {res} = WSAStartup(MAKEWORD(2, 2), &{wsa_data});
if ({res} != 0) {{
    {codegen.c_manager.err('WSAStartup failed: error code %d', str(res))}
}}
"""
        codegen.main_end_code += f"""{res} = WSACleanup();
if ({res} != 0) {{
    {codegen.c_manager.err('WSACleanup failed: error code %d', str(res))}
}}
"""
        
        codegen.c_manager.init_class(self, 'Socket', Type('Socket'))
        codegen.c_manager.wrap_struct_properties('socket', Type('Socket'), [
            Param('family', Type('SocketFamily')), Param('type', Type('SocketType')),
            Param('protocol', Type('SocketProtocol'))
        ])
        
        codegen.c_manager.init_class(self, 'AddrInfo', Type('AddrInfo'))
        codegen.c_manager.wrap_struct_properties('info', Type('AddrInfo'), [
            Param('port', Type('string')), Param('host', Type('string'))
        ])
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _SocketFamily_type(_, call_position: Position) -> Object:
            return Object('"SocketFamily"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _SocketType_type(_, call_position: Position) -> Object:
            return Object('"SocketType"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _SocketProtocol_type(_, call_position: Position) -> Object:
            return Object('"SocketProtocol"', Type('string'), call_position)
        
        @c_dec(param_types=(Param('family', Type('SocketFamily')),), is_method=True, add_to_class=self)
        def _SocketFamily_to_string(codegen, call_position: Position, family: Object) -> Object:
            return Object(codegen.c_manager._int_to_string(
                    codegen, call_position, Object(f'((int)({family}))', Type('int'), call_position)
                ), Type('string'), call_position
            )
        
        @c_dec(param_types=(Param('type', Type('SocketType')),), is_method=True, add_to_class=self)
        def _SocketType_to_string(codegen, call_position: Position, type: Object) -> Object:
            return Object(codegen.c_manager._int_to_string(
                    codegen, call_position, Object(f'((int)({type}))', Type('int'), call_position)
                ), Type('string'), call_position
            )
        
        @c_dec(
            param_types=(Param('protocol', Type('SocketProtocol')),),
            is_method=True, add_to_class=self
        )
        def _SocketProtocol_to_string(codegen, call_position: Position, protocol: Object) -> Object:
            return Object(codegen.c_manager._int_to_string(
                    codegen, call_position, Object(f'((int)({protocol}))', Type('int'), call_position)
                ), Type('string'), call_position
            )
        
        @c_dec(param_types=(Param('socket', Type('Socket')),), is_method=True, add_to_class=self)
        def _Socket_to_string(codegen, call_position: Position, socket: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, '"Socket(family=%d, type=%d, protocol=%d)"',
                f'({socket}).family', f'({socket}).type', f'({socket}).protocol'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(param_types=(Param('info', Type('AddrInfo')),), is_method=True, add_to_class=self)
        def _AddrInfo_to_string(codegen, call_position: Position, info: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, '"AddrInfo(port=%s, host=%s)"',
                f'({info}).port', f'({info}).host'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        
        @c_dec(
            param_types=(
                Param('host', Type('string')), Param('port', Type('string')),
                Param('family', Type('SocketFamily')), Param('type', Type('SocketType')),
                Param('protocol', Type('SocketProtocol'))
            ), is_method=True, is_static=True, add_to_class=self
        )
        def _AddrInfo_new(codegen, call_position: Position, host: Object, port: Object,
                          family: Object, type: Object, protocol: Object) -> Object:
            info_free = Free(free_name='freeaddrinfo')
            info: TempVar = codegen.create_temp_var(Type('AddrInfo'), call_position, free=info_free,
                                                    default_expr='{ .result = NULL }')
            info_free.object_name = f'{info}.result'
            result: TempVar = codegen.create_temp_var(Type('struct addrinfo*'), call_position)
            hints: TempVar = codegen.create_temp_var(Type('struct addrinfo'), call_position)
            ret: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""struct addrinfo *{result}, {hints};

ZeroMemory(&{hints}, sizeof({hints}));
{hints}.ai_family = {family.cast(Type('int'))};
{hints}.ai_socktype = {type.cast(Type('int'))};
{hints}.ai_protocol = {protocol.cast(Type('int'))};

int {ret} = getaddrinfo({host}, {port}, &{hints}, &{result});
if ({ret} != 0) {{
    {codegen.c_manager.err('getaddrinfo failed: error code %d', str(ret))}
}}

{info} = ({info.type.c_type}){{
    .return_code = {ret}, .host = {host}, .port = {port}, .hints = &{hints}, .result = {result}
}};
""")
            
            return info.OBJECT()
        
        
        @c_dec(
            param_types=(Param('sock', Type('Socket')),), is_property=True, add_to_class=self
        )
        def _Socket_is_invalid(_, call_position: Position, sock: Object) -> Object:
            return Object(f'(({sock}).sock == INVALID_SOCKET)', Type('bool'), call_position)
        
        def connect_socket_int(codegen, call_position: Position, sock: Object, host: Object,
                               port: Object) -> Object:
            return _Socket_connect(
                codegen, call_position, sock, host,
                codegen.c_manager._int_to_string(codegen, call_position, port)
            )
        
        @c_dec(
            param_types=(
                Param('sock', Type('Socket')), Param('host', Type('string')),
                Param('port', Type('string'))
            ), is_method=True, add_to_class=self, overloads={
                OverloadKey(Type('int'), (
                    Param('sock', Type('Socket')), Param('host', Type('string')),
                    Param('port', Type('int'))
                )): OverloadValue(connect_socket_int)
            }
        )
        def _Socket_connect(codegen, call_position: Position, sock: Object, host: Object,
                            port: Object) -> Object:
            info = _AddrInfo_new(
                codegen, call_position, host, port,
                sock.attr('family'), sock.attr('type'), sock.attr('protocol')
            )
            
            return Object(
                f"""(connect(
                    {sock.attr('sock')}, {info.attr('result').attr('ai_addr', True)},
                    {info.attr('result').attr('ai_addrlen', True).cast(Type('int'))}
                ))""",
                Type('int'), call_position
            )
        
        @c_dec(
            param_types=(
                Param('sock', Type('Socket')), Param('data', Type('string'))
            ), is_method=True, add_to_class=self
        )
        def _Socket_send(codegen, call_position: Position, sock: Object, data: Object) -> Object:
            length = codegen.c_manager._string_length(codegen, call_position, data)
            return Object(
                f'(send(({sock}).sock, {data}, {length}, 0))',
                Type('int'), call_position
            )
        
        @c_dec(
            param_types=(
                Param('sock', Type('Socket')), Param('buffer', Type('string')),
                Param('size', Type('int'))
            ), is_method=True, add_to_class=self
        )
        def _Socket_recv(_, call_position: Position, sock: Object, buffer: Object,
                         size: Object) -> Object:
            return Object(f'(recv(({sock}).sock, {buffer}, {size}, 0))', Type('int'), call_position)
        
        @c_dec(
            param_types=(
                Param('family', Type('SocketFamily')), Param('type', Type('SocketType')),
                Param('protocol', Type('SocketProtocol'))
            ), is_method=True, is_static=True, add_to_class=self
        )
        def _Socket_new(
            codegen, call_position: Position, family: Object, type: Object, protocol: Object
        ) -> Object:
            sock_free = Free(free_name='closesocket')
            sock: TempVar = codegen.create_temp_var(Type('Socket'), call_position, free=sock_free)
            sock_free.object_name = f'{sock}.sock'
            codegen.prepend_code(f"""Socket {sock} = {{
    .family = {family}, .type = {type}, .protocol = {protocol},
    .sock = socket((int){family}, (int){type}, (int){protocol})
}};

if ({_Socket_is_invalid(codegen, call_position, sock.OBJECT())}) {{
    {codegen.c_manager.err('socket creation failed')}
}}
""")
            
            return sock.OBJECT()
