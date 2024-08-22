from cure.objects import Object, Position, Type
from cure.c_manager import c_dec


class Wav:
    def __init__(self, compiler) -> None:
        compiler.extra_compile_args.append('-lwinmm')
        
        compiler.prepend_code("""typedef struct {
    char chunkID[4]; // "RIFF"
    unsigned int chunkSize; // file size - 8 bytes
    char format[4]; // "WAVE"
    char subchunk1ID[4]; // "fmt "
    unsigned int subchunk1Size; // 16 for PCM
    unsigned short audioFormat; // PCM = 1
    unsigned short numChannels; // Mono = 1, Stereo = 2
    unsigned int sampleRate; // Sampling Frequency
    unsigned int byteRate; // == SampleRate * NumChannels * BitsPerSample/8
    unsigned short blockAlign; // == NumChannels * BitsPerSample/8
    unsigned short bitsPerSample; // 8 bits = 8, 16 bits = 16, etc.
    char subchunk2ID[4]; // "data"
    unsigned int subchunk2Size; // == NumSamples * NumChannels * BitsPerSample/8
} WavHeader;

typedef struct {
    WavHeader header;
    string filename;
} WavFile;

#ifndef OS_WINDOWS
#error sound only supports Windows
#endif
""")
    
    @c_dec()
    def _WavFile_type(self, _, call_position: Position) -> Object:
        return Object('"WavFile"', Type('string'), call_position)
    
    @c_dec(param_types=('WavFile',))
    def _WavFile_to_string(self, compiler, call_position: Position, wav: Object) -> Object:
        w = f'({wav.code})'
        code, buf_free = compiler.c_manager.fmt_length(
            compiler, call_position,
            'WavFile(file=%s)',
            f'{w}.filename',
        )
        
        compiler.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    def make_wav_file(self, compiler, call_position: Position, file: Object) -> Object:
        if file.type.type == 'string':
            fptr = compiler.create_temp_var(Type('FilePointer', 'FILE*'), call_position)
            header = compiler.create_temp_var(Type('WavHeader'), call_position)
            wav_file = compiler.create_temp_var(Type('WavFile'), call_position)
            compiler.prepend_code(f"""FILE* {fptr} = fopen({file.code}, "rb");
if ({fptr} == NULL) {{
    {compiler.c_manager.err('Could not open file')}
}}

WavFile {wav_file};
{wav_file}.filename = {file.code};

WavHeader {header};
fread(&{header}, sizeof({header}), 1, {fptr});
{wav_file}.header = {header};

fclose({fptr});
""")
            
            return Object(wav_file, Type('WavFile'), call_position)
    
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_chunk_id(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.chunkID', Type('string'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_chunk_size(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.chunkSize', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_format(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.format', Type('string'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_subchunk1_id(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.subchunk1ID', Type('string'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_subchunk1_size(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.subchunk1Size', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_audio_format(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.audioFormat', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_num_channels(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.numChannels', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_sample_rate(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.sampleRate', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_byte_rate(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.byteRate', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_block_align(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.blockAlign', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_bits_per_sample(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.bitsPerSample', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_subchunk2_id(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.subchunk2ID', Type('string'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_subchunk2_size(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).header.subchunk2Size', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_filename(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'({wav.code}).filename', Type('string'), call_position)
    
    @c_dec(param_types=('WavFile',), is_method=True)
    def _WavFile_play(self, compiler, call_position: Position, wav: Object) -> Object:
        compiler.prepend_code(f"""#ifdef OS_WINDOWS
    if (!PlaySound(({wav.code}).filename, NULL, SND_FILENAME | SND_SYNC)) {{
        {compiler.c_manager.err('WavFile.play() failed, error code %lu', 'GetLastError()')}
    }}
#else
    #error WavFile.play() is not supported on this platform
#endif
""")
        return Object('NULL', Type('nil'), call_position)
