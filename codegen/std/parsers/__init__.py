from codegen.std.parsers.json import json


class parsers:
    def __init__(self, compiler) -> None:
        self.json = json(compiler)
        
        compiler.c_manager.add_objects(self.json, self)
