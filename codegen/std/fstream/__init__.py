from codegen.std.fstream.file import File


class fstream:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type('File')
        codegen.add_toplevel_code("""#ifndef CURE_FSTREAM_H
#define CURE_FSTREAM_H
""")
        codegen.c_manager.add_objects(File(codegen), self)
        codegen.add_toplevel_code('#endif')
