from codegen.std.threads.thread import Thread


class threads:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type('Thread')
        codegen.add_toplevel_code("""#ifndef CURE_THREADS_H
#define CURE_THREADS_H
""")
        codegen.c_manager.add_objects(Thread(codegen), self)
        codegen.add_toplevel_code('#endif')
