from codegen.objects import Object, Position, Type, Param, Free, TempVar
from codegen.c_manager import c_dec
from codegen.target import Target


class sockets:
    CAN_USE = False
    
    def __init__(self, codegen) -> None:
        if codegen.target != Target.WINDOWS:
            codegen.pos.warn_here('sockets is only supported on Windows')
        else:
            codegen.extra_compile_args.append('-lws2_32')
        
        codegen.valid_types.extend(('Socket', 'AddrInfo'))
        
        codegen.c_enum(
            'SocketFamily', [
                'AF_UNSPEC', 'AF_INET', 'AF_IPX', 'AF_APPLETALK', 'AF_NETBIOS', 'AF_INET6', 'AF_IRDA',
                'AF_BTH'
            ], codegen.pos
        )
        
        codegen.c_enum(
            'SocketType', ['SOCK_STREAM', 'SOCK_DGRAM', 'SOCK_RAW', 'SOCK_RDM', 'SOCK_SQPACKET'],
            codegen.pos
        )
        
        codegen.c_enum(
            'SocketProtocol', [
                'IPPROTO_ICMP', 'IPPROTO_IGMP', 'BTHPROTO_RFCOMM', 'IPPROTO_TCP', 'IPPROTO_UDP',
                'IPPROTO_ICMPV6', 'IPPROTO_RM'
            ], codegen.pos
        )
        
        codegen.add_toplevel_code("""typedef struct {
    SocketFamily family;
    SocketType type;
    SocketProtocol protocol;
    SOCKET sock;
} Socket;

typedef struct {
    const char *port, *host;
    struct addrinfo *result, hints;
} AddrInfo;
""")
        
        startup_res: TempVar = codegen.create_temp_var(Type('int'), codegen.pos)
        wsa_data: TempVar = codegen.create_temp_var(Type('WSADATA'), codegen.pos)
        codegen.main_init_code += f"""WSADATA {wsa_data} = {{0}};
int {startup_res} = WSAStartup(MAKEWORD(2, 2), &{wsa_data});
if ({startup_res} != 0) {{
    {codegen.c_manager.err('WSAStartup failed: error code %d', str(startup_res))}
}}
"""
        codegen.main_end_code += 'WSACleanup();'
        
        codegen.c_manager.wrap_struct_properties('socket', Type('Socket'), [
            Param('family', Type('SocketFamily')), Param('type', Type('SocketType')),
            Param('protocol', Type('SocketProtocol'))
        ])
        
        codegen.c_manager.wrap_struct_properties('info', Type('AddrInfo'), [
            Param('port', Type('string')), Param('host', Type('string'))
        ])

        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Socket_type(_, call_position: Position) -> Object:
            return Object('"Socket"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        
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
                Param('family', Type('SocketFamily')), Param('type', Type('SocketType')),
                Param('protocol', Type('SocketProtocol'))
            ), is_method=True, is_static=True, add_to_class=self
        )
        def _Socket_new(codegen, call_position: Position, family: Object, type: Object,
                        protocol: Object) -> Object:
            socket_free = Free(free_name='closesocket')
            socket: TempVar = codegen.create_temp_var(Type('Socket'), call_position, free=socket_free)
            socket_free.object_name = f'{socket}.sock'
            codegen.prepend_code(f"""Socket {socket} = {{
    .sock = socket((int){family}, (int){type}, (int){protocol}), .family = {family}, .type = {type},
    .protocol = {protocol}
}};
if ({socket}.sock == INVALID_SOCKET) {{
    {codegen.c_manager.err('socket function failed with error: %ld', 'WSAGetLastError()')}
}}
""")
            
            return socket.OBJECT()
        
        
        @c_dec(
            param_types=(
                Param('socket', Type('Socket')), Param('host', Type('string')),
                Param('port', Type('string'))
            ), is_method=True, is_static=True, add_to_class=self
        )
        def _AddrInfo_new(codegen, call_position: Position, socket: Object, host: Object,
                          port: Object) -> Object:
            result: TempVar = codegen.create_temp_var(Type('struct addrinfo'), call_position)
            hints: TempVar = codegen.create_temp_var(Type('struct addrinfo'), call_position)
            ret: TempVar = codegen.create_temp_var(Type('int'), call_position)
            info_free = Free(free_name='freeaddrinfo')
            info: TempVar = codegen.create_temp_var(Type('AddrInfo'), call_position, free=info_free)
            info_free.object_name = f'{info}.result'
            codegen.prepend_code(f"""struct addrinfo *{result} = NULL, {hints};
AddrInfo {info} = {{ .host = {host}, .port = {port}, .hints = {hints}, .result = {result} }};
int {ret};

ZeroMemory(&{hints}, sizeof({hints}));
{hints}.ai_family = (int)(({socket}).family);
{hints}.ai_socktype = (int)(({socket}).type);
{hints}.ai_protocol = (int)(({socket}).protocol);

{ret} = getaddrinfo({host}, {port}, &{hints}, &{result});
if ({ret} != 0) {{
    {codegen.c_manager.err('getaddrinfo failed: %d', str(ret))}
}}
""")
            
            return info.OBJECT()
