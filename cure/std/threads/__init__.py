from cure.std.threads.thread import Thread
from cure.objects import Object, Position
from cure.c_manager import c_dec


class threads:
    def __init__(self, compiler) -> None:
        self.thread = Thread(compiler)
        
        compiler.valid_types.append('Thread')
        
        compiler.c_manager.add_objects(self.thread, self)
    
    
    @c_dec(param_types=('function', '*'), is_method=True, is_static=True)
    def _Thread_new(self, compiler, call_position: Position, func: Object, *args: Object) -> Object:
        return self.thread.create_thread(compiler, call_position, func, *args)
