from codegen.objects import Object, Position, EnvItem, Free, Type
from codegen.c_manager import c_dec


class Thread:
    def __init__(self, codegen) -> None:
        codegen.valid_types.append('Thread')
        codegen.c_manager.RESERVED_NAMES.append('thread_close')
        
        codegen.add_toplevel_code(f"""#ifndef CURE_THREADS_H
#ifdef OS_WINDOWS
typedef struct {{
    HANDLE handle;
}} Thread;

void thread_close(Thread* t) {{
#ifdef OS_WINDOWS
    if (t->handle != NULL) {{
        CloseHandle(t->handle);
        t->handle = NULL;
    }}
#endif
}}
#else
{codegen.c_manager.symbol_not_supported('threads')}
#endif
#endif
""")
    
    
    @c_dec(is_method=True, is_static=True)
    def _Thread_type(self, _, call_position: Position) -> Object:
        return Object('"Thread"', Type('string'), call_position)
    
    @c_dec(param_types=('Thread',), is_method=True)
    def _Thread_to_string(self, _, call_position: Position, _thread: Object) -> Object:
        return Object('"class \'Thread\'"', Type('string'), call_position)
    
    
    def create_thread(self, codegen, call_position: Position, func: Object,
                       *args: Object) -> Object:
        if codegen.scope.env.get(func.code) is None:
            call_position.error_here(f'Function \'{func.code}\' not found')
        
        fn = codegen.scope.env[func.code].func
        
        thread_fn = codegen.get_unique_name()
        codegen.scope.env[thread_fn] = EnvItem(thread_fn, Type('function'), call_position,
                                                reserved=True)
        
        args_str = ', '.join(arg.code for arg in args)
        codegen.add_toplevel_code(f"""#ifdef OS_WINDOWS
{fn.returns.c_type} {fn.name}({", ".join(str(param) for param in fn.params)});
DWORD WINAPI {thread_fn}(void* _) {{
    {func}({args_str});
}}
#else
{codegen.c_manager.symbol_not_supported('Thread.new()')}
#endif
""")
        
        thread_close = Free(free_name='thread_close')
        thread = codegen.create_temp_var(
            Type('Thread'), call_position,
            free=thread_close
        )
        thread_close.object_name = '&' + thread
        
        codegen.prepend_code(f"""#ifdef OS_WINDOWS
Thread {thread} = {{ .handle = CreateThread(NULL, 0, {thread_fn}, NULL, CREATE_SUSPENDED, NULL) }};
if ({thread}.handle == NULL) {{
    {codegen.c_manager.err('Threading failed: %d', 'GetLastError()')}
}}
#else
{codegen.c_manager.symbol_not_supported('Thread.new()')}
#endif
""")
        
        return Object(thread, Type('Thread'), call_position, free=thread_close)
    
    
    @c_dec(param_types=('Thread',), is_property=True)
    def _Thread_id(self, codegen, call_position: Position, thread: Object) -> Object:
        id = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""#ifdef OS_WINDOWS
int {id} = GetThreadId(({thread.code}).handle);
#else
{codegen.c_manager.symbol_not_supported('Thread.id')}
#endif
""")
        return Object(id, Type('int'), call_position)
    
    @c_dec(param_types=('Thread',), is_method=True)
    def _Thread_start(self, codegen, call_position: Position, thread: Object) -> Object:
        codegen.prepend_code(f"""#ifdef OS_WINDOWS
ResumeThread(({thread.code}).handle);
#else
{codegen.c_manager.symbol_not_supported('Thread.start()')}
#endif
""")
        
        return Object.NULL(call_position)
    
    @c_dec(param_types=('Thread',), is_method=True)
    def _Thread_join(self, codegen, call_position: Position, thread: Object) -> Object:
        codegen.prepend_code(f"""#ifdef OS_WINDOWS
WaitForSingleObject({thread.code}.handle, INFINITE);
#else
{codegen.c_manager.symbol_not_supported('Thread.join()')}
#endif
""")
        return Object.NULL(call_position)
