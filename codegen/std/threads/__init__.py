from codegen.std.threads.thread import Thread


class threads:
    def __init__(self, codegen) -> None:
        self.thread = Thread(codegen)
        
        codegen.add_toplevel_code("""#ifndef CURE_THREADS_H
#define CURE_THREADS_H
#endif
""")
        codegen.c_manager.add_objects(self.thread, self)
