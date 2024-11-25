from codegen.std.threads.mutex_lock import MutexLock
from codegen.std.threads.thread import Thread
from codegen.c_manager import INCLUDES


class threads:
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
        
        codegen.type_checker.add_type(('Thread', 'MutexLock'))
        codegen.add_toplevel_code("""#ifndef CURE_THREADS_H
#define CURE_THREADS_H
""")
        codegen.extra_compile_args.append(INCLUDES / 'tinycthread/tinycthread.c')
        codegen.c_manager.include(f'"{INCLUDES / "tinycthread/tinycthread.h"}"', codegen)
        codegen.c_manager.add_objects(Thread(codegen), self)
        codegen.c_manager.add_objects(MutexLock(codegen), self)
        codegen.add_toplevel_code('#endif')
