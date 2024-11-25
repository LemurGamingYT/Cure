from codegen.std.crypto.base64 import base64


class crypto:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""#ifndef CURE_CRYPTOGRAPHY_H
#define CURE_CRYPTOGRAPHY_H
""")
        codegen.c_manager.add_objects(base64(codegen), self)
        codegen.add_toplevel_code('#endif')
