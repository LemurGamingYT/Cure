from codegen.objects import Object, Position, Type, TempVar, Param
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec
from codegen.target import Target


class Process:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code(f"""#ifdef OS_WINDOWS
typedef struct {{
    DWORD pid;
    HANDLE handle;
}} Process;
#else
{codegen.c_manager.symbol_not_supported('process')}
#endif
""")
        
        codegen.c_manager.wrap_struct_properties('proc', Type('Process'), [
            Param('pid', Type('int'))
        ])
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Process_type(_, call_position: Position) -> Object:
            return Object('"Process"', Type('string'), call_position)
        
        @c_dec(param_types=(Param('proc', Type('Process')),), is_method=True, add_to_class=self)
        def _Process_to_string(codegen, call_position: Position, proc: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position,
                '"Process(pid=%d)"', f'({proc}).pid'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        def open_current_process(codegen, call_position: Position) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.warn_here('Processes is only supported on Windows')
            
            proc: TempVar = codegen.create_temp_var(Type('Process'), call_position)
            codegen.prepend_code(f"""Process {proc} = {{
    .pid = GetCurrentProcessId(), .handle = GetCurrentProcess()
}};
if ({proc}.handle == NULL) {{
    {codegen.c_manager.err('Failed to open process, pid=%d', 'GetCurrentProcessId()')}
}}
""")
            
            return proc.OBJECT()
        
        @c_dec(
            param_types=(Param('pid', Type('int')),), is_method=True, is_static=True,
            add_to_class=self, overloads={
                OverloadKey(Type('Process'), ()): OverloadValue(open_current_process)
            }
        )
        def _Process_new(codegen, call_position: Position, pid: Object) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.warn_here('Processes is only supported on Windows')
            
            proc: TempVar = codegen.create_temp_var(Type('Process'), call_position)
            codegen.prepend_code(f"""Process {proc} = {{
    .pid = {pid}, .handle = OpenProcess(PROCESS_ALL_ACCESS, false, {pid})
}};
if ({proc}.handle == NULL) {{
    {codegen.c_manager.err('Failed to open process, pid=%d', str(pid))}
}}
""")
            
            return proc.OBJECT()
        
        @c_dec(
            param_types=(
                Param('proc', Type('Process')), Param('addr', Type('hex')), Param('value', Type('any'))
            ), is_method=True, add_to_class=self
        )
        def _Process_write(codegen, call_position: Position, proc: Object, addr: Object,
                           value: Object) -> Object:
            new_value: TempVar = codegen.create_temp_var(value.type, call_position, free=value.free)
            codegen.prepend_code(f"""{value.type.c_type} {new_value} = {value};
if (!WriteProcessMemory(({proc}).handle, {addr}, &{new_value}, sizeof({value.type.c_type}), NULL)) {{
    {codegen.c_manager.err('Failed to write to process memory')}
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(
                Param('proc', Type('Process')), Param('addr', Type('hex'))
            ), is_method=True, add_to_class=self, generic_params=('T',), return_type=Type('{T}')
        )
        def _Process_read(codegen, call_position: Position, proc: Object, addr: Object,
                          *, T: Type) -> Object:
            new_value: TempVar = codegen.create_temp_var(T, call_position)
            codegen.prepend_code(f"""{new_value.type.c_type} {new_value};
if (!ReadProcessMemory(
    ({proc}).handle, {addr}, &{new_value},
    sizeof({T.c_type}), NULL)
) {{
    {codegen.c_manager.err('Failed to read from process memory')}
}}
""")
            
            return new_value.OBJECT()
        
        @c_dec(param_types=(Param('proc', Type('Process')),), is_method=True, add_to_class=self)
        def _Process_close(codegen, call_position: Position, proc: Object) -> Object:
            codegen.prepend_code(f"""if (!CloseHandle(({proc}).handle)) {{
    {codegen.c_manager.err('Failed to close process handle')}
}}
""")
            
            return Object.NULL(call_position)
