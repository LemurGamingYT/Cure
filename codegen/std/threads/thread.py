from codegen.objects import Object, Position, EnvItem, Free, Type, TempVar
from codegen.c_manager import c_dec, INCLUDES


class Thread:
    def __init__(self, codegen) -> None:
        codegen.valid_types.append('Thread')
        codegen.c_manager.RESERVED_NAMES.extend((
            'thrd_t', 'thrd_create', 'thrd_success', 'thrd_busy', 'thrd_error', 'thrd_join',
            'thrd_detach', 'thrd_current', 'thrd_equal', 'thrd_sleep', 'thrd_yield', 'thrd_exit',
            'thrd_no_mem', 'thrd_start_t', 'thrd_timedout'
        ))
        codegen.extra_compile_args.append(INCLUDES / 'tinycthread/tinycthread.c')
        codegen.c_manager.include(f'"{INCLUDES / "tinycthread/tinycthread.h"}"', codegen)
        
        codegen.add_toplevel_code("""#ifndef CURE_THREAD_H
typedef thrd_t Thread;
#endif
""")
    
    
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Thread_type(_, call_position: Position) -> Object:
            return Object('"Thread"', Type('string'), call_position)
        
        @c_dec(param_types=('Thread',), is_method=True, add_to_class=self)
        def _Thread_to_string(_, call_position: Position, _thread: Object) -> Object:
            return Object('"class \'Thread\'"', Type('string'), call_position)
        
        @c_dec(param_types=('Thread',), is_property=True, add_to_class=self)
        def _Thread_id(codegen, call_position: Position, thread: Object) -> Object:
            id: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""#ifdef OS_WINDOWS
int {id} = GetThreadId({thread});
#else
{codegen.c_manager.symbol_not_supported('Thread.id')}
#endif
""")
            
            return id.OBJECT()
        
        @c_dec(param_types=('Thread',), is_method=True, add_to_class=self)
        def _Thread_join(codegen, call_position: Position, thread: Object) -> Object:
            codegen.prepend_code(f'thrd_join({thread}, NULL);')
            return Object.NULL(call_position)
    
        
    def create_thread(self, codegen, call_position: Position, func: Object,
                    *args: Object) -> Object:
        if codegen.scope.env.get(str(func)) is None:
            call_position.error_here(f'Function \'{func}\' not found')
        
        fn = codegen.scope.env[str(func)].func
        
        thread_fn = codegen.get_unique_name()
        codegen.scope.env[thread_fn] = EnvItem(thread_fn, Type('function'), call_position,
                                                reserved=True)
        
        args_str = ', '.join(str(arg) for arg in args)
        codegen.add_toplevel_code(f"""
{fn.returns.c_type} {fn.name}({", ".join(str(param) for param in fn.params)});
static int {thread_fn}(void* _) {{
    {func}({args_str});
    return 0;
}}
""")
        
        thread_close = Free(free_name='thrd_detach')
        thread: TempVar = codegen.create_temp_var(Type('Thread'), call_position, free=thread_close)
        
        codegen.prepend_code(f"""Thread {thread};
if (!thrd_create(&{thread}, (thrd_start_t){thread_fn}, NULL)) {{
    {codegen.c_manager.err('Threading failed')}
}}
""")
        
        return thread.OBJECT()
