from codegen.std.parsers.json import json


class parsers:
    def __init__(self, codegen) -> None:
        codegen.add_type('JSONParser')
        codegen.c_manager.add_objects(json(codegen), self)
        codegen.add_toplevel_code("""#ifndef CURE_PARSERS_H
#define CURE_PARSERS_H
#endif
""")
