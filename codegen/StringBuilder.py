from codegen.objects import Object, Type, Param, Position, TempVar, Free
from codegen.c_manager import c_dec


STRINGBUILDER_CAPACITY = 50


class StringBuilder:
    def __init__(self, c_manager) -> None:
        c_manager.wrap_struct_properties('builder', Type('StringBuilder'), [
            Param('length', Type('int')), Param('capacity', Type('int'))
        ])
        
        @c_dec(
            param_types=(Param('builder', Type('StringBuilder')),),
            is_property=True, add_to_class=self
        )
        def _StringBuilder_str(codegen, call_position: Position, obj: Object) -> Object:
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            codegen.prepend_code(f"""string {buf} = strdup(({obj}).buf);
{buf}[({obj}).length] = '\\0';
""")
            
            return buf.OBJECT()
        
        # TODO: make this StringBuilder.len_add an overload of StringBuilder.add
        @c_dec(
            param_types=(
                Param('builder', Type('StringBuilder')), Param('s', Type('string')),
                Param('len', Type('int'))
            ), is_method=True, add_to_class=self
        )
        def _StringBuilder_len_add(codegen, call_position: Position, builder: Object, s: Object,
                       len: Object) -> Object:
            lvar: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""size_t {lvar} = {len};
if (({builder}).capacity - ({builder}).length < {lvar}) {{
    while (({builder}).capacity < ({builder}).length + {lvar}) {{
        ({builder}).capacity *= 2;
    }}
    
    ({builder}).buf = (string)realloc(({builder}).buf, ({builder}).capacity);
    {codegen.c_manager.buf_check(f'({builder}).buf')}
}}

memcpy(({builder}).buf + ({builder}).length, {s}, {lvar});
({builder}).length += {lvar};
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('builder', Type('StringBuilder')), Param('s', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _StringBuilder_add(codegen, call_position: Position, builder: Object, s: Object) -> Object:
            return _StringBuilder_len_add(
                codegen, call_position, builder, s,
                codegen.c_manager._string_length(codegen, call_position, s)
            )
        
        @c_dec(
            param_types=(Param('builder', Type('StringBuilder')),), is_method=True,
            add_to_class=self
        )
        def _StringBuilder_capture_stdout(codegen, call_position: Position,
                                          builder: Object) -> Object:
            pipe_write_fd: TempVar = codegen.create_temp_var(Type('int'), call_position)
            hwrite: TempVar = codegen.create_temp_var(Type('HANDLE'), call_position)
            hread: TempVar = codegen.create_temp_var(Type('HANDLE'), call_position)
            codegen.prepend_code(f"""#if OS_WINDOWS
HANDLE {hwrite}, {hread};
if (!CreatePipe(&{hread}, &{hwrite}, NULL, 0)) {{
    {codegen.c_manager.err('Failed to create pipe')}
}}

({builder}).saved_stdout_fd = _dup(_fileno(stdout));
int {pipe_write_fd} = _open_osfhandle((intptr_t){hwrite}, _O_WRONLY);
_dup2({pipe_write_fd}, _fileno(stdout));

({builder}).hRead = {hread};
({builder}).hWrite = {hwrite};
#endif
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('builder', Type('StringBuilder')),), is_method=True,
            add_to_class=self
        )
        def _StringBuilder_release_stdout(codegen, call_position: Position,
                                          builder: Object) -> Object:
            bytes_read: TempVar = codegen.create_temp_var(Type('DWORD'), call_position)
            codegen.prepend_code(f"""#if OS_WINDOWS
fflush(stdout);
_dup2(({builder}).saved_stdout_fd, _fileno(stdout));
close(({builder}).saved_stdout_fd);

DWORD {bytes_read};
if (!ReadFile(({builder}).hRead, ({builder}).buf, ({builder}).capacity, &{bytes_read}, NULL)) {{
    {codegen.c_manager.err('Failed to read from pipe')}
}}

({builder}).length += {bytes_read};

CloseHandle(({builder}).hRead);
CloseHandle(({builder}).hWrite);
({builder}).saved_stdout_fd = 0;
({builder}).hRead = NULL;
({builder}).hWrite = NULL;
#endif
""")
            
            return Object.NULL(call_position)
        
        default_capacity = Object(str(STRINGBUILDER_CAPACITY), Type('int'))
        @c_dec(
            param_types=(Param(
                'capacity', Type('int'),
                default=default_capacity
            ),), is_method=True, is_static=True, add_to_class=self
        )
        def _StringBuilder_new(
            codegen, call_position: Position, capacity: Object = default_capacity
        ) -> Object:
            obj_free = Free()
            obj: TempVar = codegen.create_temp_var(Type('StringBuilder'), call_position, free=obj_free)
            obj_free.object_name = f'{obj}.buf'
            
            codegen.prepend_code(f"""StringBuilder {obj} = {{
    .buf = (string)malloc({capacity}), .capacity = {capacity},
    .length = 0
}};
{codegen.c_manager.buf_check(f'{obj}.buf')}
""")
            
            return obj.OBJECT()
