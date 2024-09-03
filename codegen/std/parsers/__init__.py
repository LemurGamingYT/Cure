from codegen.std.parsers.json import json


class parsers:
    def __init__(self, codegen) -> None:
        self.json = json(codegen)
        
        codegen.add_toplevel_code("""#ifndef CURE_JSON_H
#define CURE_JSON_H
#endif
""")
        
        codegen.c_manager.add_objects(self.json, self)
