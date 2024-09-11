from codegen.objects import Object, Position, Type, TempVar
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
    
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _WavFile_type(_, call_position: Position) -> Object:
            return Object('"WavFile"', Type('string'), call_position)
        
        @c_dec(param_types=('WavFile',), is_method=True, add_to_class=self)
        def _WavFile_to_string(codegen, call_position: Position, wav: Object) -> Object:
            w = f'({wav})'
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position,
                '"WavFile(file=%s)"', f'{w}.filename',
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_chunk_id(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.chunkID)', Type('string'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_chunk_size(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.chunkSize)', Type('int'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_format(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.format)', Type('string'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_subchunk1_id(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.subchunk1ID)', Type('string'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_subchunk1_size(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.subchunk1Size)', Type('int'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_audio_format(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.audioFormat)', Type('int'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_num_channels(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.numChannels)', Type('int'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_sample_rate(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.sampleRate)', Type('int'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_byte_rate(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.byteRate)', Type('int'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_block_align(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.blockAlign)', Type('int'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_bits_per_sample(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.bitsPerSample)', Type('int'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_subchunk2_id(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.subchunk2ID)', Type('string'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_subchunk2_size(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).header.subchunk2Size)', Type('int'), call_position)
        
        @c_dec(param_types=('WavFile',), is_property=True, add_to_class=self)
        def _WavFile_filename(_, call_position: Position, wav: Object) -> Object:
            return Object(f'(({wav}).filename)', Type('string'), call_position)
        
        @c_dec(param_types=('WavFile',), is_method=True, add_to_class=self)
        def _WavFile_play(codegen, call_position: Position, wav: Object) -> Object:
            codegen.prepend_code(f"""#ifdef OS_WINDOWS
if (!PlaySound(({wav}).filename, NULL, SND_FILENAME | SND_SYNC)) {{
    {codegen.c_manager.err('WavFile.play() failed, error code %lu', 'GetLastError()')}
}}
#else
{codegen.c_manager.symbol_not_supported('WavFile.play()')}
#endif
""")
            return Object.NULL(call_position)

        
    def make_wav_file(self, codegen, call_position: Position, file: Object) -> Object:
        if file.type.type == 'string':
            fptr: TempVar = codegen.create_temp_var(Type('FilePointer', 'FILE*'), call_position)
            header: TempVar = codegen.create_temp_var(Type('WavHeader'), call_position)
            wav_file: TempVar = codegen.create_temp_var(Type('WavFile'), call_position)
            codegen.prepend_code(f"""FILE* {fptr} = fopen({file}, "rb");
if ({fptr} == NULL) {{
    {codegen.c_manager.err('Could not open file')}
}}

WavFile {wav_file} = {{ .filename = {file} }};
WavHeader {header};
fread(&{header}, sizeof({header}), 1, {fptr});
{wav_file}.header = {header};

fclose({fptr});
""")
            
            return wav_file.OBJECT()
        
        call_position.error_here(f'Expected string, got \'{file.type.type}\'')
