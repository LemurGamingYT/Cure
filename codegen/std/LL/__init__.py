from codegen.std.LL.pointer import Pointer


class LL:
    def __init__(self, compiler) -> None:
        self.ptr = Pointer(compiler)
        
        compiler.c_manager.add_objects(self.ptr, self)
