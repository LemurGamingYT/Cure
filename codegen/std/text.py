from codegen.objects import Object, Position, Free, Type
from codegen.c_manager import c_dec


class text:
    def __init__(self, codegen) -> None:
        codegen.RESERVED_NAMES.extend(('setlocale', 'localeconv', 'lconv'))
        codegen.valid_types.append('LocaleConv')
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
    
    @c_dec(is_method=True)
    def _LocaleConv_type(self, _, call_position: Position) -> Object:
        return Object('"LocaleConv"', Type('string'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_method=True)
    def _LocaleConv_to_string(self, _, call_position: Position, _localeconv: Object) -> Object:
        return Object('"class \'LocaleConv\'"', Type('string'), call_position)
    
    def _set_locale_category(self, codegen, call_position: Position, category: Object) -> Object:
        return self._set_locale(codegen, call_position, category, None)
    
    @c_dec(
        param_types=('int', 'string'),
        can_user_call=True,
        overloads={
            (('int',), 'nil'): _set_locale_category
        }
    )
    def _set_locale(self, codegen, call_position: Position,
                   category: Object, locale: Object | None) -> Object:
        codegen.prepend_code(
            f'setlocale({category.code}, {locale.code if locale is not None else "NULL"});'
        )
        return Object.NULL(call_position)
    
    @c_dec(can_user_call=True)
    def _localeconv(self, codegen, call_position: Position) -> Object:
        conv = codegen.create_temp_var(Type('LocaleConv'), call_position)
        codegen.prepend_code(f'LocaleConv {conv} = {{ .conv = localeconv() }};')
        return Object(conv, Type('LocaleConv'), call_position)
    
    @c_dec(param_types=(), is_method=True, is_static=True)
    def _LocaleConv_new(self, codegen, call_position: Position) -> Object:
        return self._localeconv(codegen, call_position)
    
    @c_dec(param_types=('string', 'int'), can_user_call=True)
    def _word_wrap(self, codegen, call_position: Position,
                   string: Object, width: Object) -> Object:
        codegen.c_manager.include('string.h')
        codegen.c_manager.include('ctype.h')
        
        slen = codegen.create_temp_var(Type('int'), call_position)
        start = codegen.create_temp_var(Type('int'), call_position)
        end = codegen.create_temp_var(Type('int'), call_position)
        buf_free = Free()
        buf = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
        temp = codegen.create_temp_var(Type('int'), call_position)
        i = codegen.create_temp_var(Type('int'), call_position)
        s = codegen.create_temp_var(Type('string'), call_position)
        codegen.prepend_code(f"""int {slen} = {codegen.c_manager._string_length(
    codegen, [string], call_position
)};
string {s} = {string.code};
size_t {start} = 0;
string {buf} = (string)malloc({slen} * 3);
{codegen.c_manager.buf_check(buf)}
while ({start} < {slen}) {{
    int {end} = {start} + ({width.code});
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
        
        return Object(buf, Type('string'), call_position, free=buf_free)
    
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_decimal_point(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).decimal_point)', Type('string'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_thousands_sep(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).thousands_sep)', Type('string'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_grouping(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).grouping)', Type('string'), call_position)

    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_int_curr_symbol(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).int_curr_symbol)', Type('string'), call_position)

    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_currency_symbol(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).currency_symbol)', Type('string'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_mon_decimal_point(self, _, call_position: Position,
                                      localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).mon_decimal_point)', Type('string'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_mon_thousands_sep(self, _, call_position: Position,
                                      localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).mon_thousands_sep)', Type('string'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_mon_grouping(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).mon_grouping)', Type('string'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_positive_sign(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).positive_sign)', Type('string'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_negative_sign(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).negative_sign)', Type('string'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_int_frac_digits(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).int_frac_digits)', Type('int'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_frac_digits(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).frac_digits)', Type('int'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_p_cs_precedes(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).p_cs_precedes)', Type('int'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_p_sep_by_space(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).p_sep_by_space)', Type('int'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_p_sign_posn(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).p_sign_posn)', Type('int'), call_position)
    
    @c_dec(param_types=('LocaleConv',), is_property=True)
    def _LocaleConv_n_sign_posn(self, _, call_position: Position, localeconv: Object) -> Object:
        return Object(f'(({localeconv.code}).n_sign_posn)', Type('int'), call_position)
