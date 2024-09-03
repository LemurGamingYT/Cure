from codegen.std.compression.rle import RLE


class compression:
    def __init__(self, codegen) -> None:
        self.rle = RLE()
        
        codegen.c_manager.add_objects(self.rle, self)
