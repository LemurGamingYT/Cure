from codegen.std.threads.thread import Thread
from codegen.objects import Object, Position
from codegen.c_manager import c_dec


class threads:
    def __init__(self, codegen) -> None:
        self.thread = Thread(codegen)
        
        codegen.add_toplevel_code("""#ifndef CURE_THREADS_H
#define CURE_THREADS_H
#endif
""")
        codegen.c_manager.add_objects(self.thread, self)
    
    
    @c_dec(param_types=('function', '*'), is_method=True, is_static=True)
    def _Thread_new(self, codegen, call_position: Position, func: Object, *args: Object) -> Object:
        return self.thread.create_thread(codegen, call_position, func, *args)
