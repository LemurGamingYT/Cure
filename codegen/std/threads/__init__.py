from codegen.std.threads.thread import Thread


class threads:
    def __init__(self, codegen) -> None:
        codegen.add_type('Thread')
        codegen.c_manager.add_objects(Thread(codegen), self)
        codegen.add_toplevel_code("""#ifndef CURE_THREADS_H
#define CURE_THREADS_H
#endif
""")
