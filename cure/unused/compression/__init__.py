from cure.objects import Object, Position
from cure.std.compression.rle import RLE
from cure.c_manager import c_dec


class compression:
    def __init__(self, compiler) -> None:
        self.compiler = compiler
        
        self.rle = RLE()
    
    @c_dec(param_types=('string',), can_user_call=True)
    def _rle_compress(self, compiler, call_position: Position, string: Object) -> Object:
        return self.rle.rle_compress(compiler, call_position, string)

    @c_dec(param_types=('string',), can_user_call=True)
    def _rle_decompress(self, compiler, call_position: Position, string: Object) -> Object:
        return self.rle.rle_decompress(compiler, call_position, string)
