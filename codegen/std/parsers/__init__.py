from codegen.std.parsers.json import json
from codegen.std.parsers.ini import ini


class parsers:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type(('JSONParser', 'INIParser'))
        codegen.add_toplevel_code("""#ifndef CURE_PARSERS_H
#define CURE_PARSERS_H
""")
        codegen.c_manager.add_objects(json(codegen), self)
        codegen.c_manager.add_objects(ini(codegen), self)
        codegen.add_toplevel_code('#endif')
