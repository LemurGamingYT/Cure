from cure.objects import Object, Position
from cure.std.sound.wav import Wav
from cure.c_manager import c_dec


class sound:
    def __init__(self, compiler) -> None:
        self.wav = Wav(compiler)
        
        compiler.c_manager.add_objects(self.wav, self)
    
    @c_dec(param_types=('string',), is_method=True, is_static=True)
    def _WavFile_new(self, compiler, call_position: Position, file: Object) -> Object:
        return self.wav.make_wav_file(compiler, call_position, file)
