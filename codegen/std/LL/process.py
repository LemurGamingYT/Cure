from codegen.objects import Object, Position, Type, TempVar
from codegen.c_manager import c_dec


class Process:
    def __init__(self, codegen) -> None:
        codegen.valid_types.append('Process')
        codegen.add_toplevel_code(f"""#ifdef OS_WINDOWS
typedef struct {{
    DWORD pid;
    HANDLE handle;
}} Process;
#else
{codegen.c_manager.symbol_not_supported('process')}
#endif
""")
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Process_type(_, call_position: Position) -> Object:
            return Object('"Process"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Process_to_string(codegen, call_position: Position, process: Object) -> Object:
            proc = f'({process})'
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position,
                '"Process(pid=%d)"', f'{proc}.pid'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        def open_current_process(codegen, call_position: Position) -> Object:
            proc: TempVar = codegen.create_temp_var(Type('Process'), call_position)
            codegen.prepend_code(f"""Process {proc} = {{
    .pid = GetCurrentProcessId(), .handle = GetCurrentProcess()
}};
if ({proc}.handle == NULL) {{
    {codegen.c_manager.err('Failed to open process, pid=%d', 'GetCurrentProcessId()')}
}}
""")
            
            return proc.OBJECT()
        
        @c_dec(param_types=('int',), is_method=True, is_static=True, add_to_class=self, overloads={
            ((), 'Process'): open_current_process
        })
        def _Process_new(codegen, call_position: Position, pid: Object) -> Object:
            proc: TempVar = codegen.create_temp_var(Type('Process'), call_position)
            codegen.prepend_code(f"""Process {proc} = {{
    .pid = {pid}, .handle = OpenProcess(PROCESS_ALL_ACCESS, false, {pid})
}};
if ({proc}.handle == NULL) {{
    {codegen.c_manager.err('Failed to open process, pid=%d', str(pid))}
}}
""")
            
            return proc.OBJECT()
        
        @c_dec(param_types=('Process',), is_property=True, add_to_class=self)
        def _Process_pid(_, call_position: Position, process: Object) -> Object:
            return Object(f'((int)(({process}).pid))', Type('int'), call_position)
        
        @c_dec(param_types=('Process', 'hex', 'any'), is_method=True, add_to_class=self)
        def _Process_write(codegen, call_position: Position, process: Object, addr: Object,
                           value: Object) -> Object:
            new_value: TempVar = codegen.create_temp_var(value.type, call_position, free=value.free)
            codegen.prepend_code(f"""{value.type.c_type} {new_value} = {value};
if (!WriteProcessMemory(({process}).handle, {addr}, &{new_value}, sizeof({value.type.c_type}), NULL)) {{
    {codegen.c_manager.err('Failed to write to process memory')}
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(param_types=('Process', 'hex', 'type'), is_method=True, add_to_class=self)
        def _Process_read(codegen, call_position: Position, process: Object, addr: Object,
                          type_: Object) -> Object:
            new_value: TempVar = codegen.create_temp_var(Type(type_.code), call_position)
            codegen.prepend_code(f"""{new_value.type.c_type} {new_value};
if (!ReadProcessMemory(
    ({process}).handle, {addr}, &{new_value},
    sizeof({new_value.type.c_type}), NULL)
) {{
    {codegen.c_manager.err('Failed to read from process memory')}
}}
""")
            
            return new_value.OBJECT()
        
        @c_dec(param_types=('Process',), is_method=True, add_to_class=self)
        def _Process_close(codegen, call_position: Position, process: Object) -> Object:
            codegen.prepend_code(f"""if (!CloseHandle(({process}).handle)) {{
    {codegen.c_manager.err('Failed to close process handle')}
}}
""")
            
            return Object.NULL(call_position)
