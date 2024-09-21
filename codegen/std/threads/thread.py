from codegen.objects import Object, Position, EnvItem, Free, Type, TempVar, Param, Function, Arg
from codegen.c_manager import c_dec, INCLUDES, func_modification
from codegen.target import Target


def get_result_field(params: list[Param]) -> str:
    result_struct_field = 'result'
    i = 0
    while result_struct_field in {p.name for p in params}:
        i += 1
        result_struct_field = f'result{i}'
    
    return result_struct_field

def get_function_info(name: str, codegen, pos: Position) -> Function:
    if codegen.scope.env.get(name) is None:
        pos.error_here(f'Function \'{name}\' not found')
    
    return codegen.scope.env[name].func


class Thread:
    def create_thread(self, codegen, call_position: Position, name: str, *args: Object):
        fn = get_function_info(name, codegen, call_position)
            
        struct_t = Type(f'thread_{fn.name}_t')
        codegen.c_manager.RESERVED_NAMES.append(str(struct_t))
        
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
{fn.return_type.c_type} {fn.name}({", ".join(str(param) for param in fn.params)});
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
        
        codegen.prepend_code(f"""Thread {thread};
{struct_t} {arg} = {{ {', '.join(f'.{p.name} = {args[i]}' for i, p in enumerate(fn.params))} }};
{thread}.arg = &{arg};
if (!thrd_create(&{thread}.t, (thrd_start_t){thread_fn}, &{arg})) {{
{codegen.c_manager.err('Threading failed')}
}}
""")
        
        return thread.OBJECT(), struct_t, result_struct_field
    
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
typedef struct {
    void* arg;
    thrd_t t;
} Thread;
#endif
""")
    
    
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Thread_type(_, call_position: Position) -> Object:
            return Object('"Thread"', Type('string'), call_position)
        
        @c_dec(param_types=(Param('thread', Type('Thread')),), is_method=True, add_to_class=self)
        def _Thread_to_string(_, call_position: Position, _thread: Object) -> Object:
            return Object('"class \'Thread\'"', Type('string'), call_position)
        
        @c_dec(param_types=(Param('thread', Type('Thread')),), is_property=True, add_to_class=self)
        def _Thread_id(codegen, call_position: Position, thread: Object) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.warn_here('Thread.id is only supported on Windows')
            
            id: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""#ifdef OS_WINDOWS
int {id} = GetThreadId(({thread}).t);
#else
{codegen.c_manager.symbol_not_supported('Thread.id')}
#endif
""")
            
            return id.OBJECT()
        
        @c_dec(param_types=(Param('thread', Type('Thread')),), is_method=True, add_to_class=self)
        def _Thread_join(codegen, call_position: Position, thread: Object) -> Object:
            codegen.prepend_code(f'thrd_join(({thread}).t, NULL);')
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
        def _Thread(codegen, func_obj: Function, call_position: Position, args: list[Arg],
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
