from codegen.objects import Object, Position, Type, Arg, Param
from codegen.c_manager import c_dec


class HexTriplet:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""#ifndef CURE_COLOR_H
typedef struct {
    string hex;
} HexTriplet;
#endif
""")
        
        codegen.c_manager.wrap_struct_properties('hex', Type('HexTriplet'), [
            Param('hex', Type('string'))
        ])
    
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _HexTriplet_type(_, call_position: Position) -> Object:
            return Object('"HexTriplet"', Type('string'), call_position)
        
        @c_dec(param_types=(Param('hex', Type('HexTriplet')),), is_method=True, add_to_class=self)
        def _HexTriplet_to_string(compiler, call_position: Position, hex_triplet: Object) -> Object:
            cls = f'({hex_triplet})'
            code, buf_free = compiler.c_manager.fmt_length(
                compiler, call_position,
                '"HexTriplet(#%s)"', f'{cls}.hex'
            )

            compiler.prepend_code(code)
            return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
        
        @c_dec(param_types=(Param('hex', Type('HexTriplet')),), is_property=True, add_to_class=self)
        def _HexTriplet_to_rgb(codegen, call_position: Position, hex_triplet: Object) -> Object:
            hex = codegen.create_temp_var(Type('uint', 'unsigned int'), call_position)
            codegen.prepend_code(f"""unsigned int {hex};
sscanf(({hex_triplet}).hex, "%x", &{hex});
""")
            
            return codegen.call(
                'RGB_new', [
                    Arg(Object(f'({hex} >> 16) & 0xFF', Type('int'), call_position)),
                    Arg(Object(f'({hex} >> 8) & 0xFF', Type('int'), call_position)),
                    Arg(Object(f'{hex} & 0xFF', Type('int'), call_position))
                ], call_position
            )
