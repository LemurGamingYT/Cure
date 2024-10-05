from codegen.std.compression.rle import RLE


class compression:
    def __init__(self, codegen) -> None:
        codegen.c_manager.reserve(('rle_compress', 'rle_decompress'))
        codegen.c_manager.add_objects(RLE(), self)
