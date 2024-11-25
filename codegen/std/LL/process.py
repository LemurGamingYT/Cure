from codegen.objects import Object, Position, Type, TempVar, Param
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec
from codegen.target import Target



class Process:
    def __init__(self, codegen) -> None:
        # Processes are only supported on Windows but are part of the Low Level library so putting
        # a codegen.target != Target.WINDOWS check will cause a compile error if the user tries to
        # use the Low Level library on any other operating system than Windows meaning that it can't
        # be used on any other operating system. Instead check in each of the Process' methods if
        # the target is Windows.
        codegen.add_toplevel_code("""#ifdef OS_WINDOWS
typedef struct {
    DWORD pid;
    HANDLE handle;
} Process;
#endif
""")
        
        codegen.type_checker.add_type('Process')
        codegen.c_manager.init_class(self, 'Process', Type('Process'))
        codegen.c_manager.wrap_struct_properties('proc', Type('Process'), [
            Param('pid', Type('int'))
        ])
        
        @c_dec(params=(Param('proc', Type('Process')),), is_method=True, add_to_class=self)
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
            params=(Param('pid', Type('int')),), is_method=True, is_static=True,
            add_to_class=self, overloads={
                OverloadKey(Type('Process'), ()): OverloadValue(open_current_process)
            }
        )
        def _Process_new(codegen, call_position: Position, pid: Object) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.not_supported_err('Process.new()')
            
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
            params=(
                Param('proc', Type('Process')), Param('addr', Type('hex')), Param('value', Type('any'))
            ), is_method=True, add_to_class=self
        )
        def _Process_write(codegen, call_position: Position, proc: Object, addr: Object,
                           value: Object) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.not_supported_err('Process.write()')
            
            new_value: TempVar = codegen.create_temp_var(value.type, call_position, free=value.free)
            codegen.prepend_code(f"""{value.type.c_type} {new_value} = {value};
if (!WriteProcessMemory(({proc}).handle, {addr}, &{new_value}, sizeof({value.type.c_type}), NULL)) {{
    {codegen.c_manager.err('Failed to write to process memory')}
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            params=(
                Param('proc', Type('Process')), Param('addr', Type('hex'))
            ), is_method=True, add_to_class=self, generic_params=('T',), return_type=Type('{T}')
        )
        def _Process_read(codegen, call_position: Position, proc: Object, addr: Object,
                          *, T: Type) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.not_supported_err('Process.read()')
            
            new_value: TempVar = codegen.create_temp_var(T, call_position)
            codegen.prepend_code(f"""{new_value.type.c_type} {new_value};
if (!ReadProcessMemory(({proc}).handle, {addr}, &{new_value}, sizeof({T.c_type}), NULL)) {{
    {codegen.c_manager.err('Failed to read from process memory')}
}}
""")
            
            return new_value.OBJECT()
        
        @c_dec(params=(Param('proc', Type('Process')),), is_method=True, add_to_class=self)
        def _Process_close(codegen, call_position: Position, proc: Object) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.not_supported_err('Process.close()')
            
            codegen.prepend_code(f"""if (!CloseHandle(({proc}).handle)) {{
    {codegen.c_manager.err('Failed to close process handle')}
}}
""")
            
            return Object.NULL(call_position)
