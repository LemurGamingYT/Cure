from codegen.std.encoding.base64 import base64


class encoding:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""#ifndef CURE_ENCODING_H
#define CURE_ENCODING_H
""")
        codegen.c_manager.add_objects(base64(codegen), self)
        codegen.add_toplevel_code('#endif')
