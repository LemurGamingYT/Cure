from codegen.objects import Object, Type, Param, Position, TempVar
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec


class Math:
    def __init__(self, c_manager) -> None:
        @c_dec(
            param_types=(Param('a', Type('Fraction')), Param('b', Type('Fraction'))),
            add_to_class=self
        )
        def _Fraction_add_Fraction(codegen, call_position: Position, a: Object, b: Object) -> Object:
            f: TempVar = codegen.create_temp_var(Type('Fraction'), call_position)
            codegen.prepend_code(f"""Fraction {f} = {{
    .top = ({a}).top * ({b}).bottom + ({b}).top * ({a}).bottom,
    .bottom = ({a}).bottom * ({b}).bottom
}};
""")
            
            return f.OBJECT()
        
        @c_dec(
            param_types=(Param('a', Type('Vector2')), Param('b', Type('Vector2'))),
            add_to_class=self
        )
        def _Vector2_add_Vector2(codegen, call_position: Position, a: Object, b: Object) -> Object:
            vec: TempVar = codegen.create_temp_var(Type('Vector2'), call_position)
            codegen.prepend_code(f"""Vector2 {vec} = {{
    .x = ({a}).x + ({b}).x, .y = ({a}).y + ({b}).y
}};
""")
            
            return vec.OBJECT()
        
        @c_dec(
            param_types=(Param('a', Type('Fraction')), Param('b', Type('Fraction'))),
            add_to_class=self
        )
        def _Fraction_sub_Fraction(codegen, call_position: Position, a: Object, b: Object) -> Object:
            f: TempVar = codegen.create_temp_var(Type('Fraction'), call_position)
            codegen.prepend_code(f"""Fraction {f} = {{
    .top = ({a}).top * ({b}).bottom - ({a}).bottom * ({b}).top,
    .bottom = ({b}).bottom * ({b}).bottom
}};
""")
            
            return f.OBJECT()
        
        @c_dec(
            param_types=(Param('a', Type('Vector2')), Param('b', Type('Vector2'))),
            add_to_class=self
        )
        def _Vector2_sub_Vector2(codegen, call_position: Position, a: Object, b: Object) -> Object:
            vec: TempVar = codegen.create_temp_var(Type('Vector2'), call_position)
            codegen.prepend_code(f"""Vector2 {vec} = {{
    .x = ({a}).x - ({b}).x, .y = ({a}).y - ({b}).y
}};
""")
            
            return vec.OBJECT()
        
        @c_dec(
            param_types=(Param('a', Type('Fraction')), Param('b', Type('Fraction'))),
            add_to_class=self
        )
        def _Fraction_mul_Fraction(codegen, call_position: Position, a: Object, b: Object) -> Object:
            f: TempVar = codegen.create_temp_var(Type('Fraction'), call_position)
            codegen.prepend_code(f"""Fraction {f} = {{
    .top = ({a}).top * ({b}).top, .bottom = ({b}).bottom * ({a}).bottom
}};
""")
            
            return f.OBJECT()
        
        @c_dec(
            param_types=(Param('a', Type('Vector2')), Param('b', Type('Vector2'))),
            add_to_class=self
        )
        def _Vector2_mul_Vector2(codegen, call_position: Position, a: Object, b: Object) -> Object:
            vec: TempVar = codegen.create_temp_var(Type('Vector2'), call_position)
            codegen.prepend_code(f"""Vector2 {vec} = {{
    .x = ({a}).x * ({b}).x, .y = ({b}).y * ({b}).y
}};
""")
            
            return vec.OBJECT()
        
        @c_dec(
            param_types=(Param('a', Type('Fraction')), Param('b', Type('Fraction'))),
            add_to_class=self
        )
        def _Fraction_div_Fraction(codegen, call_position: Position, a: Object, b: Object) -> Object:
            f: TempVar = codegen.create_temp_var(Type('Fraction'), call_position)
            codegen.prepend_code(f"""Fraction {f} = {{
    .top = ({a}).top * ({b}).bottom, .bottom = ({a}).bottom * ({b}).top
}};
""")
            
            return f.OBJECT()
        
        @c_dec(
            param_types=(Param('a', Type('Vector2')), Param('b', Type('Vector2'))),
            add_to_class=self
        )
        def _Vector2_div_Vector2(codegen, call_position: Position, a: Object, b: Object) -> Object:
            vec: TempVar = codegen.create_temp_var(Type('Vector2'), call_position)
            codegen.prepend_code(f"""Vector2 {vec} = {{
    .x = ({a}).x / ({b}).x, .y = ({a}).y / ({b}).y
}};
""")
            
            return vec.OBJECT()
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _Math_pi(_, call_position: Position) -> Object:
            return Object('3.14159265358979323846f', Type('float'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _Math_e(_, call_position: Position) -> Object:
            return Object('2.7182818284590452354f', Type('float'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _Math_tau(_, call_position: Position) -> Object:
            return Object('6.28318530717958647692f', Type('float'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _Math_phi(_, call_position: Position) -> Object:
            return Object('1.61803398874989484820f', Type('float'), call_position)
        
        def Math_absint(_, call_position: Position, x: Object) -> Object:
            return Object(f'(abs({x}))', Type('int'), call_position)
        
        @c_dec(param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
            OverloadKey(Type('int'), (Param('x', Type('int')),)): OverloadValue(Math_absint)
        }, add_to_class=self)
        def _Math_abs(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)fabsf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_sin(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'(sinf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_cos(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)cosf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_tan(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)tanf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_asin(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)asinf({x}))', Type('float'), call_position)

        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_acos(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)acosf({x}))', Type('float'), call_position)

        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_atan(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)atanf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('y', Type('float')), Param('x', Type('float'))),
            is_method=True, is_static=True, add_to_class=self, overloads={
                OverloadKey(
                    Type('float'), (Param('y', Type('int')), Param('x', Type('int')))
                ): OverloadValue(None),
                OverloadKey(
                    Type('float'), (Param('y', Type('int')), Param('x', Type('float')))
                ): OverloadValue(None),
                OverloadKey(
                    Type('float'), (Param('y', Type('float')), Param('x', Type('int')))
                ): OverloadValue(None)
            }
        )
        def _Math_atan2(codegen, call_position: Position, y: Object, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)atan2f({y}, {x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_sqrt(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)sqrtf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')), Param('n', Type('float'))),
            is_method=True, is_static=True, add_to_class=self, overloads={
                OverloadKey(
                    Type('float'), (Param('x', Type('int')), Param('n', Type('int')))
                ): OverloadValue(None),
                OverloadKey(
                    Type('float'), (Param('x', Type('int')), Param('n', Type('float')))
                ): OverloadValue(None),
                OverloadKey(
                    Type('float'), (Param('x', Type('float')), Param('n', Type('int')))
                ): OverloadValue(None)
            }
        )
        def _Math_nth_root(codegen, call_position: Position, x: Object, n: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)powf({x}, 1.0f / ({n})))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')), Param('y', Type('float'))),
            is_method=True, is_static=True, add_to_class=self, overloads={
                OverloadKey(
                    Type('float'), (Param('x', Type('int')), Param('y', Type('int')))
                ): OverloadValue(None),
                OverloadKey(
                    Type('float'), (Param('x', Type('int')), Param('y', Type('float')))
                ): OverloadValue(None),
                OverloadKey(
                    Type('float'), (Param('x', Type('float')), Param('y', Type('int')))
                ): OverloadValue(None)
            }
        )
        def _Math_pow(codegen, call_position: Position, x: Object, y: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)powf({x}, {y}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_log(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)logf({x}))', Type('float'), call_position)

        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_log10(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)log10f({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_log2(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)log2f({x}))', Type('float'), call_position)

        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_exp(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)expf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Math_ceil(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((int)ceilf({x}))', Type('int'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Math_floor(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((int)floorf({x}))', Type('int'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Math_round(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((int)roundf({x}))', Type('int'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')), Param('y', Type('float'))),
            is_method=True, is_static=True, add_to_class=self, overloads={
                OverloadKey(
                    Type('int'), (Param('x', Type('int')), Param('y', Type('int')))
                ): OverloadValue(None),
                OverloadKey(
                    Type('float'), (Param('x', Type('int')), Param('y', Type('float')))
                ): OverloadValue(None),
                OverloadKey(
                    Type('float'), (Param('x', Type('float')), Param('y', Type('int')))
                ): OverloadValue(None)
            }
        )
        def _Math_min(codegen, call_position: Position, x: Object, y: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(
                f'(({x}) < ({y}) ? ({x}) : ({y}))',
                Type('int') if x.type == Type('int') and y.type == Type('int') else Type('float'),
                call_position
            )
        
        @c_dec(
            param_types=(Param('x', Type('float')), Param('y', Type('float'))),
            is_method=True, is_static=True, add_to_class=self, overloads={
                OverloadKey(
                    Type('int'), (Param('x', Type('int')), Param('y', Type('int')))
                ): OverloadValue(None),
                OverloadKey(
                    Type('float'), (Param('x', Type('int')), Param('y', Type('float')))
                ): OverloadValue(None),
                OverloadKey(
                    Type('float'), (Param('x', Type('float')), Param('y', Type('int')))
                ): OverloadValue(None)
            }
        )
        def _Math_max(codegen, call_position: Position, x: Object, y: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(
                f'(({x}) < ({y}) ? ({y}) : ({x}))',
                Type('int') if x.type == Type('int') and y.type == Type('int') else Type('float'),
                call_position
            )
        
        def rand_start0(codegen, call_position: Position, max: Object) -> Object:
            return _Math_random(codegen, call_position, Object('0', Type('int'), call_position), max)
        
        @c_dec(
            param_types=(Param('min', Type('int')), Param('max', Type('int'))),
            is_method=True, is_static=True, add_to_class=self, overloads={
                OverloadKey(Type('int'), (Param('max', Type('int')),)): OverloadValue(rand_start0)
            }
        )
        def _Math_random(codegen, call_position: Position, min: Object, max: Object) -> Object:
            low_num: TempVar = codegen.create_temp_var(Type('int'), call_position)
            hi_num: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {low_num} = 0, {hi_num} = 0;
if (({min}) < ({max})) {{
{low_num} = {min};
{hi_num} = {max};
}} else {{
{low_num} = {max};
{hi_num} = {min};
}}
""")
            return Object(
                f'((rand() % ({hi_num} - {low_num} + 1)) + {low_num})',
                Type('int'), call_position
            )
        
        @c_dec(
            param_types=(Param('deg', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('deg', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_rad(codegen, call_position: Position, deg: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            pi = _Math_pi(codegen, call_position)
            return Object(f'((float)({deg}) * {pi} / 180.0f)', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('rad', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('rad', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_deg(codegen, call_position: Position, rad: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            pi = _Math_pi(codegen, call_position)
            return Object(f'((float)({rad}) * 180.0f / {pi})', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_sinh(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)sinh({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_cosh(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)cosh({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True, overloads={
                OverloadKey(Type('float'), (Param('x', Type('int')),)): OverloadValue(None)
            }, add_to_class=self
        )
        def _Math_tanh(codegen, call_position: Position, x: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)tanh({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')), Param('y', Type('float'))),
            is_method=True, is_static=True, add_to_class=self,
            overloads={
                OverloadKey(
                    Type('int'), (Param('x', Type('int')), Param('y', Type('int')))
                ): OverloadValue(None),
                OverloadKey(
                    Type('float'), (Param('x', Type('int')), Param('y', Type('float')))
                ): OverloadValue(None),
                OverloadKey(
                    Type('float'), (Param('x', Type('float')), Param('y', Type('int')))
                ): OverloadValue(None)
            }
        )
        def _Math_copysign(codegen, call_position: Position, x: Object, y: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(f'((float)copysignf({x}, {y}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('top', Type('int')), Param('bottom', Type('int'))),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Math_fraction(codegen, call_position: Position, top: Object, bottom: Object) -> Object:
            f: TempVar = codegen.create_temp_var(Type('Fraction'), call_position)
            codegen.prepend_code(f'Fraction {f} = {{ .top = {top}, .bottom = {bottom} }};')
            return f.OBJECT()
        
        @c_dec(
            param_types=(Param('a', Type('int')), Param('b', Type('int'))),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Math_gcd(codegen, call_position: Position, a: Object, b: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {res} = {_Math_min(codegen, call_position, a, b)};
while ({res} > 0) {{
    if (({a}) % {res} == 0 && ({b}) % {res} == 0)
        break;
    {res}--;
}}
""")
            
            return res.OBJECT()
        
        @c_dec(
            param_types=(Param('a', Type('int')), Param('b', Type('int'))),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Math_lcm(codegen, call_position: Position, a: Object, b: Object) -> Object:
            return Object(
                f'(({a}) * ({b}) / {_Math_gcd(codegen, call_position, a, b)})',
                Type('int'), call_position
            )
        
        @c_dec(
            param_types=(Param('x', Type('float')), Param('y', Type('float'))),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Math_vec2(codegen, call_position: Position, x: Object, y: Object) -> Object:
            vec: TempVar = codegen.create_temp_var(Type('Vector2'), call_position)
            codegen.prepend_code(f"""Vector2 {vec} = {{ .x = {x}, .y = {y} }};
""")
            
            return vec.OBJECT()

        
        c_manager.wrap_struct_properties('frac', Type('Fraction'), [
            Param('top', Type('int')), Param('bottom', Type('int'))
        ])
        
        @c_dec(param_types=(Param('frac', Type('Fraction')),), is_property=True, add_to_class=self)
        def _Fraction_simple(codegen, call_position: Position, frac: Object) -> Object:
            f: TempVar = codegen.create_temp_var(Type('Fraction'), call_position)
            g: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {g} = {_Math_gcd(
    codegen, call_position,
    Object(f'(({frac}).top)', Type('int'), call_position),
    Object(f'(({frac}).bottom)', Type('int'), call_position)
)};
Fraction {f} = {{ .top = ({frac}).top / {g}, .bottom = ({frac}).bottom / {g} }};
""")
            
            return f.OBJECT()
        
        @c_dec(param_types=(Param('frac', Type('Fraction')),), is_property=True, add_to_class=self)
        def _Fraction_recip(codegen, call_position: Position, frac: Object) -> Object:
            f: TempVar = codegen.create_temp_var(Type('Fraction'), call_position)
            codegen.prepend_code(f"""Fraction {f} = {{
    .top = ({frac}).bottom, .bottom = ({frac}).top
}};
""")
            return f.OBJECT()
        
        
        c_manager.wrap_struct_properties('vec', Type('Vector2'), [
            Param('x', Type('float')), Param('y', Type('float'))
        ])
        
        @c_dec(param_types=(Param('vec', Type('Vector2')),), is_property=True, add_to_class=self)
        def _Vector2_length(codegen, call_position: Position, vec: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(
                f'(sqrtf(({vec}).x * ({vec}).x + ({vec}).y * ({vec}).y))',
                Type('float'), call_position
            )
        
        @c_dec(param_types=(Param('vec', Type('Vector2')),), is_property=True, add_to_class=self)
        def _Vector2_norm(codegen, call_position: Position, vec: Object) -> Object:
            v: TempVar = codegen.create_temp_var(Type('Vector2'), call_position)
            codegen.prepend_code(f"""Vector2 {v} = {{
    .x = ({vec}).x / {_Vector2_length(codegen, call_position, vec)},
    .y = ({vec}).y / {_Vector2_length(codegen, call_position, vec)}
}};
""")
            return v.OBJECT()
        
        @c_dec(
            param_types=(Param('vec1', Type('Vector2')), Param('vec2', Type('Vector2'))),
            is_method=True, add_to_class=self
        )
        def _Vector2_dot(_, call_position: Position, vec1: Object, vec2: Object) -> Object:
            return Object(
                f'(({vec1}).x * ({vec2}).x + ({vec1}).y * ({vec2}).y)',
                Type('float'), call_position
            )
        
        @c_dec(
            param_types=(Param('vec1', Type('Vector2')), Param('vec2', Type('Vector2'))),
            is_method=True, add_to_class=self
        )
        def _Vector2_cross(_, call_position: Position, vec1: Object, vec2: Object) -> Object:
            return Object(
                f'(({vec1}).x * ({vec2}).y - ({vec1}).y * ({vec2}).x)',
                Type('float'), call_position
            )
        
        @c_dec(
            param_types=(Param('vec1', Type('Vector2')), Param('vec2', Type('Vector2'))),
            is_method=True, add_to_class=self
        )
        def _Vector2_dist(codegen, call_position: Position, vec1: Object, vec2: Object) -> Object:
            return _Vector2_length(
                codegen, call_position,
                _Vector2_sub_Vector2(codegen, call_position, vec1, vec2)
            )
        
        @c_dec(
            param_types=(Param('vec1', Type('Vector2')), Param('vec2', Type('Vector2'))),
            is_method=True, add_to_class=self
        )
        def _Vector2_angle(codegen, call_position: Position, vec1: Object, vec2: Object) -> Object:
            codegen.c_manager.include('<math.h>', codegen)
            return Object(
                f'atan2f(({vec1}).y, ({vec1}).x) - atan2f(({vec2}).y, ({vec2}).x)',
                Type('float'), call_position
            )
