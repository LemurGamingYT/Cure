from codegen.objects import Object, Position, EnvItem, Free, Type, TempVar, Param, Arg
from codegen.c_manager import c_dec, INCLUDES, func_modification
from codegen.function_manager import UserFunction
from codegen.target import Target


def get_result_field(params: list[Param]) -> str:
    result_struct_field = 'result'
    i = 0
    while result_struct_field in {p.name for p in params}:
        i += 1
        result_struct_field = f'result{i}'
    
    return result_struct_field

def get_function_info(name: str, codegen, pos: Position) -> UserFunction:
    if codegen.scope.env.get(name) is None:
        pos.error_here(f'Function \'{name}\' not found')
    
    return codegen.scope.env[name].func


class Thread:
    def create_thread(self, codegen, call_position: Position, name: str, *args: Object):
        fn = get_function_info(name, codegen, call_position)
            
        struct_t = Type(f'thread_{fn.name}_t')
        codegen.c_manager.reserve(str(struct_t))
        
        result_struct_field = get_result_field(fn.params)
        codegen.add_toplevel_code(f"""typedef struct {{
{'\n'.join(str(param) + ';' for param in fn.params)}
{fn.return_type.c_type} {result_struct_field};
}} {struct_t};
""")
        
        thread_fn = codegen.get_unique_name()
        codegen.scope.env[thread_fn] = EnvItem(thread_fn, Type('function'), call_position,
                                                reserved=True)
        
        arg: TempVar = codegen.create_temp_var(Type('any', 'void*'), call_position)
        
        codegen.add_toplevel_code(f"""
{fn.return_type.c_type} {fn.name}({', '.join(str(param) for param in fn.params)});
static int {thread_fn}(void* {arg}) {{
(({struct_t}*){arg})->{result_struct_field} = {name}({
    ', '.join(f'(({struct_t}*){arg})->{p.name}' for p in fn.params)
});
return 0;
}}
""")
        
        thread_close = Free(free_name='thrd_detach')
        thread: TempVar = codegen.create_temp_var(Type('Thread'), call_position, free=thread_close)
        thread_close.object_name = f'{thread}.t'
        
        params_initialization = ', '.join(f'.{p.name} = {args[i]}' for i, p in enumerate(fn.params))
        if params_initialization == '':
            params_initialization = '0'
        
        codegen.prepend_code(f"""Thread {thread};
{struct_t} {arg} = {{ {params_initialization} }};
{thread}.arg = &{arg};
if (!thrd_create(&{thread}.t, (thrd_start_t){thread_fn}, &{arg})) {{
{codegen.c_manager.err('Threading failed')}
}}
""")
        
        return thread.OBJECT(), struct_t, result_struct_field
    
    def __init__(self, codegen) -> None:
        codegen.c_manager.reserve((
            'thrd_t', 'thrd_create', 'thrd_success', 'thrd_busy', 'thrd_error', 'thrd_join',
            'thrd_detach', 'thrd_current', 'thrd_equal', 'thrd_sleep', 'thrd_yield', 'thrd_exit',
            'thrd_no_mem', 'thrd_start_t', 'thrd_timedout', '_TINYCTHREAD_H_',
            '_TTHREAD_PLATFORM_DEFINED_', '_TTHREAD_WIN32_', '_TTHREAD_POSIX_', '_GNU_SOURCE',
            '_POSIX_C_SOURCE', '_XOPEN_SOURCE', '_XPG6', 'TTHREAD_NORETURN', 'TIME_UTC',
            '_TTHREAD_EMULATE_TIMESPEC_GET_', '_tthread_timespec', 'timespec',
            '_tthread_timespec_get', 'timespec_get', 'TINYCTHREAD_VERSION_MAJOR',
            'TINYCTHREAD_VERSION_MINOR', 'TINYCTHREAD_VERSION', '_Thread_local', 'TSS_DTOR_ITERATIONS',
            'mtx_plain', 'mtx_timed', 'mtx_recursive', 'mtx_t', 'mtx_init', 'mtx_destroy',
            'mtx_lock', 'mtx_unlock', 'mtx_trylock', 'cnd_t', 'cnd_init', 'cnd_destroy', 'cnd_signal',
            'cnd_broadcast', 'cnd_wait', 'cnd_timedwait', 'tss_t', 'tss_dtor_t', 'tss_create',
            'tss_delete', 'tss_get', 'tss_set', 'once_flag', 'ONCE_FLAG_INIT', 'call_once'
        ))
        codegen.extra_compile_args.append(INCLUDES / 'tinycthread/tinycthread.c')
        codegen.c_manager.include(f'"{INCLUDES / "tinycthread/tinycthread.h"}"', codegen)
        
        codegen.add_toplevel_code("""typedef struct {
    void* arg;
    thrd_t t;
} Thread;
""")
        
        codegen.c_manager.init_class(self, 'Thread', Type('Thread'))
        
        @c_dec(param_types=(Param('thread', Type('Thread')),), is_property=True, add_to_class=self)
        def _Thread_id(codegen, call_position: Position, thread: Object) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.not_supported_err('Thread.id')
            
            return Object(f'((int)GetThreadId(({thread}).t))', Type('int'), call_position)
        
        @c_dec(param_types=(Param('thread', Type('Thread')),), is_method=True, add_to_class=self)
        def _Thread_join(codegen, call_position: Position, thread: Object) -> Object:
            codegen.prepend_code(f"""if (thrd_join(({thread}).t, NULL) != thrd_success) {{
    {codegen.c_manager.err('Thread.join() failed')}
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('thread', Type('Thread')),), is_method=True, add_to_class=self
        )
        def _Thread_close(codegen, call_position: Position, thread: Object) -> Object:
            codegen.prepend_code(f"""if (thrd_detach(({thread}).t) != thrd_success) {{
    {codegen.c_manager.err('Thread.close() failed')}
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('func', Type('function')), Param('*', Type('*'))),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Thread_new(codegen, call_position: Position, func: Object, *args: Object) -> Object:
            thread, _, _ = self.create_thread(codegen, call_position, str(func), *args)
            return thread
        
        @func_modification(
            params=(Param('join', Type('bool'), default=Object('true', Type('bool'))),),
            add_to_class=self
        )
        def _Thread(codegen, func_obj: UserFunction, call_position: Position, args: list[Arg],
                    join: Object) -> Object:
            thread, struct_t, res_field = self.create_thread(
                codegen, call_position, func_obj.name,
                *[arg.value for arg in args]
            )
            
            codegen.prepend_code(f"""if ({join}) {{
""")
            _Thread_join(codegen, call_position, thread)
            codegen.prepend_code('}')
            
            return Object(
                f'((({struct_t}*){thread}.arg)->{res_field})',
                func_obj.return_type, call_position
            )
