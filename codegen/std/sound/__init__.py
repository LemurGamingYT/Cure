from codegen.objects import Object, Position
from codegen.std.sound.wav import Wav
from codegen.c_manager import c_dec


class sound:
    def __init__(self, codegen) -> None:
        self.wav = Wav(codegen)
        
        codegen.add_toplevel_code("""#ifndef CURE_SOUND_H
#define CURE_SOUND_H
#endif
""")
        codegen.c_manager.add_objects(self.wav, self)
    
    @c_dec(param_types=('string',), is_method=True, is_static=True)
    def _WavFile_new(self, codegen, call_position: Position, file: Object) -> Object:
        return self.wav.make_wav_file(codegen, call_position, file)
