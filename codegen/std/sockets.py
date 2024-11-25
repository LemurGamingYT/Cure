from codegen.objects import Object, Position, Type, Param, Free, TempVar
from codegen.c_manager import c_dec, INCLUDES
from codegen.target import Target


TINYCSOCKET_PATH = INCLUDES / 'tinycsocket'

class sockets:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""#ifndef CURE_HTTP_SOCKETS_H
#define CURE_HTTP_SOCKETS_H
""")
        
        codegen.c_manager.include(f'"{TINYCSOCKET_PATH / "tinycsocket.h"}"', codegen)
        codegen.extra_compile_args.append(TINYCSOCKET_PATH / 'tinycsocket.c')
        if codegen.target != Target.WINDOWS:
            codegen.pos.warn_here('sockets have not been tested on this platform')
        else:
            codegen.extra_compile_args.append('-lws2_32')
        
        codegen.type_checker.add_type('Socket')
        
        codegen.add_toplevel_code('typedef socket_t Socket;')
        codegen.add_toplevel_code('#endif')
        
        res: TempVar = codegen.create_temp_var(Type('int'), codegen.pos)
        codegen.main_init_code += f"""int {res} = tinycsocket_init();
if ({res} != 0) {{
    {codegen.c_manager.err('Failed to initialise sockets: error code %d', str(res))}
}}
"""
        codegen.main_end_code += f"""{res} = tinycsocket_cleanup();
if ({res} != 0) {{
    {codegen.c_manager.err('Failed to clean up sockets: error code %d', str(res))}
}}
"""
        
        codegen.c_manager.init_class(self, 'Socket', Type('Socket'))
        
        @c_dec(
            params=(
                Param('sock', Type('Socket')), Param('ip', Type('string')),
                Param('port', Type('string'))
            ), is_method=True, add_to_class=self
        )
        def _Socket_connect(codegen, call_position: Position, sock: Object, ip: Object,
                            port: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {res} = socket_connect(&{sock}, {ip}, {port});
if ({res} == TINYSOCK_CONNECTION_FAILED) {{
    {codegen.c_manager.err('Failed to connect socket: error code %d', str(res))}
}}
""")
            return Object.NULL(call_position)
        
        @c_dec(
            params=(
                Param('sock', Type('Socket')), Param('data', Type('string'))
            ), is_method=True, add_to_class=self
        )
        def _Socket_send(codegen, call_position: Position, sock: Object, data: Object) -> Object:
            length = codegen.c_manager._string_length(codegen, call_position, data)
            res: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {res} = socket_send(&{sock}, {data}, {length});
if ({res} == TINYSOCK_SEND_FAILED) {{
    {codegen.c_manager.err('Failed to send data: error code %d', str(res))}
}}
""")
            return Object.NULL(call_position)
        
        @c_dec(
            params=(
                Param('sock', Type('Socket')), Param('size', Type('int'))
            ), is_method=True, add_to_class=self
        )
        def _Socket_recv(codegen, call_position: Position, sock: Object, size: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('int'), call_position)
            buf: Object = codegen.c_manager._string_new(codegen, call_position, size)
            codegen.prepend_code(f"""int {res} = socket_recv(&{sock}, {buf}, {size});
if ({res} == TINYSOCK_RECV_FAILED) {{
    {codegen.c_manager.err('Failed to receive data: error code %d', str(res))}
}}
""")
            return buf
        
        @c_dec(
            params=(
                Param('sock', Type('Socket')), Param('ip', Type('string')),
                Param('port', Type('string'))
            ), is_method=True, add_to_class=self
        )
        def _Socket_bind(codegen, call_position: Position, sock: Object, ip: Object,
                         port: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {res} = socket_bind(&{sock}, {ip}, {port});
if ({res} != 0) {{
    {codegen.c_manager.err('Failed to bind socket: error code %d', str(res))}
}}
""")
            return Object.NULL(call_position)
        
        @c_dec(
            params=(
                Param('sock', Type('Socket')), Param('backlog', Type('int'))
            ), is_method=True, add_to_class=self
        )
        def _Socket_listen(codegen, call_position: Position, sock: Object, backlog: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {res} = socket_listen(&{sock}, {backlog});
if ({res} != 0) {{
    {codegen.c_manager.err('Failed to listen socket: error code %d', str(res))}
}}
""")
            return Object.NULL(call_position)
        
        @c_dec(
            params=(Param('server', Type('Socket')), Param('client', Type('Socket'))),
            is_method=True, add_to_class=self
        )
        def _Socket_accept(codegen, call_position: Position, server: Object, client: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {res} = socket_accept(&{server}, &{client});
if ({res} != 0) {{
    {codegen.c_manager.err('Failed to accept socket: error code %d', str(res))}
}}
""")
            return Object.NULL(call_position)
        
        @c_dec(params=(Param('sock', Type('Socket')),), is_method=True, add_to_class=self)
        def _Socket_shutdown(codegen, call_position: Position, sock: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {res} = socket_shutdown(&{sock}, SD_BOTH);
if ({res} == TINYSOCK_SHUTDOWN_FAILED) {{
    {codegen.c_manager.err('Failed to shutdown socket: error code %d', str(res))}
}}
""")
            return Object.NULL(call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Socket_new(codegen, call_position: Position) -> Object:
            sock_free = Free(free_name='socket_close')
            sock: TempVar = codegen.create_temp_var(Type('Socket'), call_position, free=sock_free)
            sock_free.object_name = f'&{sock}'
            codegen.prepend_code(f"""Socket {sock};
if (socket_init(&{sock}) == TINYSOCK_INIT_FAILED) {{
    {codegen.c_manager.err('socket creation failed')}
}}
""")
            
            return sock.OBJECT()
        
        
        HOSTNAME_LEN = 1024
        
        @c_dec(can_user_call=True, is_method=True, add_to_class=self)
        def _get_host_name(codegen, call_position: Position) -> Object:
            res: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""char {res}[{HOSTNAME_LEN}];
if (gethostname({res}, {HOSTNAME_LEN})) {{
    {codegen.c_manager.err('Failed to get host name')}
}}
""")
            
            return res.OBJECT()
