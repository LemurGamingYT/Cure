from codegen.objects import Object, Position, Free, Type, TempVar, Param
from codegen.c_manager import c_dec, INCLUDES


class lz4:
    def __init__(self, codegen) -> None:
        codegen.extra_compile_args.append(f'{INCLUDES}/lz4/*.c')
        
        @c_dec(param_types=(Param('s', Type('string')),), can_user_call=True, add_to_class=self)
        def _lz4_compress(codegen, call_position: Position, string: Object) -> Object:
            codegen.c_manager.include(f'"{INCLUDES}/lz4/lz4.h"', codegen)
            
            size: TempVar = codegen.create_temp_var(Type('int'), call_position)
            max_dst_size: TempVar = codegen.create_temp_var(Type('int'), call_position)
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            compressed_size: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""const int {size} = {
    codegen.c_manager._string_length(codegen, call_position, string)
};
const int {max_dst_size} = LZ4_compressBound({size});
string {buf} = (string)malloc({max_dst_size});
{codegen.c_manager.buf_check(str(buf))}

const int {compressed_size} = LZ4_compress_default({string}, {buf}, {size}, {max_dst_size});
if ({compressed_size} <= 0) {{
    {codegen.c_manager.err('Failed to compress string')}
}}
""")
            
            return buf.OBJECT()
        
        @c_dec(param_types=(Param('s', Type('string')),), can_user_call=True, add_to_class=self)
        def _lz4_decompress(codegen, call_position: Position, string: Object) -> Object:
            codegen.c_manager.include(f'"{INCLUDES}/lz4/lz4.h"', codegen)

            size: TempVar = codegen.create_temp_var(Type('int'), call_position)
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            decompressed_size: TempVar = codegen.create_temp_var(Type('int'), call_position)
            max_dst_size: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""const int {size} = {
    codegen.c_manager._string_length(codegen, call_position, string)
};
const int {max_dst_size} = LZ4_compressBound({size});
string {buf} = (string)malloc({max_dst_size});
{codegen.c_manager.buf_check(str(buf))}

const int {decompressed_size} = LZ4_decompress_safe({string}, {buf}, {size}, {max_dst_size});
if ({decompressed_size} <= 0) {{
    {codegen.c_manager.err('Failed to decompress string')}
}}
""")

            return buf.OBJECT()
