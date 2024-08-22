from cure.objects import Object, Position, EnvItem, Free, Type
from cure.c_manager import c_dec


class Thread:
    def __init__(self, compiler) -> None:
        self.compiler = compiler
        
        compiler.prepend_code("""#ifdef OS_WINDOWS
typedef struct {
    HANDLE handle;
} Thread;

void thread_close(Thread* t) {
#ifdef OS_WINDOWS
    if (t->handle != NULL) {
        CloseHandle(t->handle);
        t->handle = NULL;
    }
#endif
}
#else
    #error threading is not supported on this OS
#endif
""")
    
    
    @c_dec()
    def _Thread_type(self, _, call_position: Position) -> Object:
        return Object('"Thread"', Type('string'), call_position)
    
    @c_dec(param_types=('Thread',))
    def _Thread_to_string(self, _, call_position: Position, _thread: Object) -> Object:
        return Object('"class \'Thread\'"', Type('string'), call_position)
    
    
    def create_thread(self, compiler, call_position: Position, func: Object,
                       *args: Object) -> Object:
        if compiler.scope.env.get(func.code) is None:
            call_position.error_here(f'Function \'{func.code}\' not found')
        
        struct = compiler.get_unique_name()
        compiler.scope.env[struct] = EnvItem(struct, Type(struct), call_position, reserved=True)
        fn = compiler.scope.env[func.code].func
        
        if fn.params:
            compiler.add_toplevel_code(f"""typedef struct {{
    {'\n'.join(f'{param.type.c_type} {param.name};' for param in fn.params)}
}} {struct};
""")
        else:
            compiler.add_toplevel_code(f"""typedef struct {{
    unsigned char _;
}} {struct};
""")
        
        thread_fn = compiler.get_unique_name()
        compiler.scope.env[thread_fn] = EnvItem(thread_fn, Type('function'), call_position,
                                                reserved=True)
        
        args_str = ', '.join(arg.code for arg in args)
        body_str, _, _ = compiler.body_str(fn.body, fn.params)
        compiler.add_toplevel_code(f"""#ifdef OS_WINDOWS
    DWORD WINAPI {thread_fn}(void* __arg) {{
        void thread({', '.join(f'{param.type.c_type} {param.name}' for param in fn.params)}) {{
            {body_str}
        }}
        
        thread({args_str});
    }}
#else
    #error create_thread() is not implemented on this platform
#endif
""")
        
        func_args = compiler.create_temp_var(Type(struct + '*'), call_position)
        handle = compiler.create_temp_var(Type('HANDLE'), call_position)
        
        add_args = ''
        for arg, param in zip(args, fn.params):
            add_args += f'{func_args}.{param.name} = {arg.code};\n'
        
        thread_close = Free(free_name='thread_close')
        thread = compiler.create_temp_var(
            Type('Thread'), call_position,
            free=thread_close
        )
        thread_close.object_name = '&' + thread
        
        compiler.prepend_code(f"""#ifdef OS_WINDOWS
    Thread {thread};
    HANDLE {handle} = CreateThread(NULL, 0, {thread_fn}, NULL, 0, NULL);
    if ({handle} == NULL) {{
        {compiler.c_manager.err('Threading failed: %d', 'GetLastError()')}
    }}
    
    {thread}.handle = {handle};
#else
    #error create_thread() is not implemented on this platform
#endif
""")
        
        return Object(thread, Type('Thread'), call_position, free=thread_close)
    
    
    @c_dec(param_types=('Thread',), is_method=True)
    def _Thread_join(self, compiler, call_position: Position, thread: Object) -> Object:
        compiler.prepend_code(f'WaitForSingleObject({thread.code}.handle, INFINITE);')
        return Object('NULL', Type('nil'), call_position)
