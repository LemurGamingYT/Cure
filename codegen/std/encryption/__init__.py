from codegen.std.encryption.base64 import base64


class encryption:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""#ifndef CURE_ENCRYPTION_H
#define CURE_ENCRYPTION_H
""")
        codegen.c_manager.add_objects(base64(codegen), self)
        codegen.add_toplevel_code('#endif')
