from codegen.objects import Object, Position, Free, Type, TempVar, Param
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec


class text:
    def __init__(self, codegen) -> None:
        codegen.c_manager.reserve(('setlocale', 'localeconv', 'lconv'))
        codegen.type_checker.add_type('LocaleConv')
        codegen.add_toplevel_code("""#ifndef CURE_TEXT_H
#include <locale.h>
typedef struct {
    struct lconv* conv;
} LocaleConv;
#define CURE_TEXT_H
#endif
""")
        
        codegen.add_toplevel_constant('LC_ALL', Type('int'), 'LC_ALL', False)
        codegen.add_toplevel_constant('LC_COLLATE', Type('int'), 'LC_COLLATE', False)
        codegen.add_toplevel_constant('LC_CTYPE', Type('int'), 'LC_CTYPE', False)
        codegen.add_toplevel_constant('LC_MONETARY', Type('int'), 'LC_MONETARY', False)
        codegen.add_toplevel_constant('LC_NUMERIC', Type('int'), 'LC_NUMERIC', False)
        codegen.add_toplevel_constant('LC_TIME', Type('int'), 'LC_TIME', False)
        codegen.add_toplevel_constant('LC_MAX', Type('int'), 'LC_MAX', False)
        codegen.add_toplevel_constant('LC_MIN', Type('int'), 'LC_MIN', False)
        
        codegen.c_manager.init_class(self, 'LocaleConv', Type('LocaleConv'))
        
        def _set_locale_category(codegen, call_position: Position, category: Object) -> Object:
            return _set_locale(codegen, call_position, category, None)
        
        @c_dec(
            param_types=(
                Param('category', Type('int')),
                Param('locale', Type('string'), default=Object('"NULL"', Type('string')))
            ), can_user_call=True, add_to_class=self, overloads={
                OverloadKey(
                    Type('nil'), (Param('category', Type('int')),)
                ): OverloadValue(_set_locale_category)
            }
        )
        def _set_locale(codegen, call_position: Position, category: Object, locale: Object) -> Object:
            codegen.prepend_code(f'setlocale({category}, {locale});')
            return Object.NULL(call_position)
        
        @c_dec(can_user_call=True, add_to_class=self)
        def _localeconv(codegen, call_position: Position) -> Object:
            conv: TempVar = codegen.create_temp_var(Type('LocaleConv'), call_position)
            codegen.prepend_code(f'LocaleConv {conv} = {{ .conv = localeconv() }};')
            return conv.OBJECT()
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _LocaleConv_new(codegen, call_position: Position) -> Object:
            return _localeconv(codegen, call_position)
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('width', Type('int'))),
            can_user_call=True, add_to_class=self
        )
        def _word_wrap(codegen, call_position: Position, string: Object, width: Object) -> Object:
            codegen.c_manager.include('<string.h>', codegen)
            codegen.c_manager.include('<ctype.h>', codegen)
            
            slen: TempVar = codegen.create_temp_var(Type('int'), call_position)
            start: TempVar = codegen.create_temp_var(Type('int'), call_position)
            end: TempVar = codegen.create_temp_var(Type('int'), call_position)
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            temp: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            s: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""size_t {slen} = {codegen.c_manager._string_length(
    codegen, call_position, string
)};
string {s} = {string};
size_t {start} = 0;
string {buf} = (string)malloc({slen} * 3);
{codegen.c_manager.buf_check(buf)}
while ({start} < {slen}) {{
    int {end} = {start} + ({width});
    if ({end} >= {slen}) {end} = {slen};
    if ({end} < {slen} && !isspace({s}[{end}])) {{
        int {temp} = {end};
        while ({temp} > {start} && !isspace({s}[{temp}])) {{
            {temp}--;
        }}
        
        if ({temp} > {start}) {end} = {temp};
    }}
    
    for (size_t {i} = {start}; {i} < {end}; {i}++) {{
        {buf}[{i}] = {s}[{i}];
    }}
    
    {buf}[{end}] = '\\n';
    
    {start} = {end};
    while ({start} < {slen} && isspace({s}[{start}])) {{
        {start}++;
    }}
}}
""")
            
            return buf.OBJECT()
        
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_decimal_point(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->decimal_point)', Type('string'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_thousands_sep(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->thousands_sep)', Type('string'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_grouping(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->grouping)', Type('string'), call_position)

        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_int_curr_symbol(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->int_curr_symbol)', Type('string'), call_position)

        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_currency_symbol(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->currency_symbol)', Type('string'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_mon_decimal_point(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->mon_decimal_point)', Type('string'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_mon_thousands_sep(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->mon_thousands_sep)', Type('string'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_mon_grouping(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->mon_grouping)', Type('string'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_positive_sign(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->positive_sign)', Type('string'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_negative_sign(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->negative_sign)', Type('string'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_int_frac_digits(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->int_frac_digits)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_frac_digits(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->frac_digits)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_p_cs_precedes(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->p_cs_precedes)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_p_sep_by_space(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->p_sep_by_space)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_p_sign_posn(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->p_sign_posn)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('conv', Type('LocaleConv')),), is_property=True, add_to_class=self)
        def _LocaleConv_n_sign_posn(_, call_position: Position, localeconv: Object) -> Object:
            return Object(f'(({localeconv}).conv->n_sign_posn)', Type('int'), call_position)
