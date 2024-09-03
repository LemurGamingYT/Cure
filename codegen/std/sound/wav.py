from codegen.objects import Object, Position, Type
from codegen.c_manager import c_dec


class Wav:
    def __init__(self, codegen) -> None:
        codegen.extra_compile_args.append('-lwinmm')
        
        codegen.prepend_code(f"""#ifndef CURE_SOUND_H
#ifndef OS_WINDOWS
{codegen.c_manager.symbol_not_supported('sound')}
#else
typedef struct {{
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
}} WavHeader;

typedef struct {{
    WavHeader header;
    string filename;
}} WavFile;
#endif
#endif
""")
    
    @c_dec(is_method=True, is_static=True)
    def _WavFile_type(self, _, call_position: Position) -> Object:
        return Object('"WavFile"', Type('string'), call_position)
    
    @c_dec(param_types=('WavFile',), is_method=True)
    def _WavFile_to_string(self, codegen, call_position: Position, wav: Object) -> Object:
        w = f'({wav.code})'
        code, buf_free = codegen.c_manager.fmt_length(
            codegen, call_position,
            '"WavFile(file=%s)"', f'{w}.filename',
        )
        
        codegen.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    def make_wav_file(self, codegen, call_position: Position, file: Object) -> Object:
        if file.type.type == 'string':
            fptr = codegen.create_temp_var(Type('FilePointer', 'FILE*'), call_position)
            header = codegen.create_temp_var(Type('WavHeader'), call_position)
            wav_file = codegen.create_temp_var(Type('WavFile'), call_position)
            codegen.prepend_code(f"""FILE* {fptr} = fopen({file.code}, "rb");
if ({fptr} == NULL) {{
    {codegen.c_manager.err('Could not open file')}
}}

WavFile {wav_file} = {{ .filename = {file.code} }};
WavHeader {header};
fread(&{header}, sizeof({header}), 1, {fptr});
{wav_file}.header = {header};

fclose({fptr});
""")
            
            return Object(wav_file, Type('WavFile'), call_position)
        
        call_position.error_here(f'Expected string, got \'{file.type.type}\'')
    
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_chunk_id(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.chunkID)', Type('string'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_chunk_size(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.chunkSize)', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_format(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.format)', Type('string'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_subchunk1_id(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.subchunk1ID)', Type('string'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_subchunk1_size(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.subchunk1Size)', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_audio_format(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.audioFormat)', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_num_channels(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.numChannels)', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_sample_rate(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.sampleRate)', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_byte_rate(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.byteRate)', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_block_align(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.blockAlign)', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_bits_per_sample(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.bitsPerSample)', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_subchunk2_id(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.subchunk2ID)', Type('string'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_subchunk2_size(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).header.subchunk2Size)', Type('int'), call_position)
    
    @c_dec(param_types=('WavFile',), is_property=True)
    def _WavFile_filename(self, _, call_position: Position, wav: Object) -> Object:
        return Object(f'(({wav.code}).filename)', Type('string'), call_position)
    
    @c_dec(param_types=('WavFile',), is_method=True)
    def _WavFile_play(self, codegen, call_position: Position, wav: Object) -> Object:
        codegen.prepend_code(f"""#ifdef OS_WINDOWS
if (!PlaySound(({wav.code}).filename, NULL, SND_FILENAME | SND_SYNC)) {{
    {codegen.c_manager.err('WavFile.play() failed, error code %lu', 'GetLastError()')}
}}
#else
{codegen.c_manager.symbol_not_supported('WavFile.play()')}
#endif
""")
        return Object.NULL(call_position)
