from codegen.objects import Object, Position, Type, Arg
from codegen.c_manager import c_dec


class HexTriplet:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""#ifndef CURE_COLOR_H
typedef struct {
    string hex;
} HexTriplet;
#endif
""")
    
    @c_dec(is_method=True, is_static=True)
    def _HexTriplet_type(self, _, call_position: Position) -> Object:
        return Object('"HexTriplet"', Type('string'), call_position)
    
    @c_dec(param_types=('HexTriplet',), is_method=True)
    def _HexTriplet_to_string(self, compiler, call_position: Position, hex_triplet: Object) -> Object:
        cls = f'({hex_triplet})'
        code, buf_free = compiler.c_manager.fmt_length(
            compiler, call_position,
            '"HexTriplet(#%s)"', f'{cls}.hex'
        )

        compiler.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    
    @c_dec(param_types=('HexTriplet',), is_property=True)
    def _HexTriplet_hex(self, _, call_position: Position, hex_triplet: Object) -> Object:
        return Object(f'(({hex_triplet}).hex)', Type('string'), call_position)
    
    @c_dec(param_types=('HexTriplet',), is_property=True)
    def _HexTriplet_to_rgb(self, codegen, call_position: Position, hex_triplet: Object) -> Object:
        cls = f'({hex_triplet.code})'
        hex = codegen.create_temp_var(Type('uint', 'unsigned int'), call_position)
        codegen.prepend_code(f"""unsigned int {hex};
sscanf({cls}.hex, "%x", &{hex});
""")
        
        return codegen.call(
            'RGB_new', [
                Arg(Object(f'({hex} >> 16) & 0xFF', Type('int'), call_position)),
                Arg(Object(f'({hex} >> 8) & 0xFF', Type('int'), call_position)),
                Arg(Object(f'{hex} & 0xFF', Type('int'), call_position))
            ], call_position
        )
