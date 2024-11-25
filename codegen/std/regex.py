from codegen.objects import Object, Position, Type, Free, TempVar, Param, Arg
from codegen.c_manager import c_dec, INCLUDES


class regex:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type('Regex')
        codegen.extra_compile_args.append(INCLUDES / 'slre/slre.c')
        codegen.c_manager.include(f'"{INCLUDES / "slre/slre.h"}"', codegen)
        codegen.c_manager.reserve((
            'slre_match', 'slre_cap', 'SLRE_NO_MATCH', 'SLRE_UNEXPECTED_QUANTIFIER',
            'SLRE_UNBALANCED_BRACKETS', 'SLRE_INTERNAL_ERROR', 'SLRE_INVALID_CHARACTER_SET',
            'SLRE_INVALID_METACHARACTER', 'SLRE_CAPS_ARRAY_TOO_SMALL', 'SLRE_TOO_MANY_BRANCHES',
            'SLRE_TOO_MANY_BRACKETS'
        ))
        codegen.add_toplevel_code("""#ifndef CURE_REGEX_H
#define CURE_REGEX_H
typedef struct {
    const string pattern;
} Regex;

typedef struct {
    string match;
    int length;
} Match;
#endif
""")
        
        codegen.c_manager.init_class(self, 'Regex', Type('Regex'))
        codegen.c_manager.init_class(self, 'Match', Type('Match'))
        codegen.c_manager.wrap_struct_properties('match', Type('Match'), [
            Param('match', Type('string')), Param('length', Type('int'))
        ])
        
        codegen.c_manager.wrap_struct_properties('regex', Type('Regex'), [
            Param('pattern', Type('string'))
        ])
        
        
        @c_dec(params=(Param('regex', Type('Regex')),), is_method=True, add_to_class=self)
        def _Regex_to_string(codegen, call_position: Position, re: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, '"Regex(pattern=%s)"', f'({re}).pattern'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(params=(Param('match', Type('Match')),), is_method=True, add_to_class=self)
        def _Match_to_string(codegen, call_position: Position, match: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, '"Match(length=%d, match=%s)"',
                f'({match}).length', f'({match}).match'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        
        @c_dec(
            params=(Param('regex', Type('Regex')), Param('s', Type('string')),
                    Param('num_matches', Type('int'))),
            is_method=True, add_to_class=self
        )
        def _Regex_match(codegen, call_position: Position, re: Object, string: Object,
                         num_matches: Object) -> Object:
            caps_free = Free()
            matches_type: Type = codegen.array_manager.define_array(Type('Match'))
            matches: Object = codegen.call(f'{matches_type.c_type}_make', [], call_position)
            ret: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            caps: TempVar = codegen.create_temp_var(
                Type('struct slre_cap*'), call_position, free=caps_free,
                default_expr=f'(struct slre_cap*)malloc(({num_matches}) * sizeof(struct slre_cap))'
            )
            codegen.prepend_code(f"""int {ret} = slre_match(
    {re.attr('pattern')}, {string}, {codegen.c_manager._string_length(codegen, call_position, string)},
    {caps}, {num_matches}, 0
);
if ({ret} < 0) {{
    if ({ret} == SLRE_UNEXPECTED_QUANTIFIER) {{
        {codegen.c_manager.err('unexpected quantifier')}
    }} else if ({ret} == SLRE_UNBALANCED_BRACKETS) {{
        {codegen.c_manager.err('unbalanced brackets')}
    }} else if ({ret} == SLRE_INTERNAL_ERROR) {{
        {codegen.c_manager.err('internal regex error')}
    }} else if ({ret} == SLRE_INVALID_CHARACTER_SET) {{
        {codegen.c_manager.err('invalid character set')}
    }} else if ({ret} == SLRE_INVALID_METACHARACTER) {{
        {codegen.c_manager.err('invalid metacharacter')}
    }} else if ({ret} == SLRE_CAPS_ARRAY_TOO_SMALL) {{
        {codegen.c_manager.err('too many matches')}
    }} else if ({ret} == SLRE_TOO_MANY_BRANCHES) {{
        {codegen.c_manager.err('too many branches')}
    }} else if ({ret} == SLRE_TOO_MANY_BRACKETS) {{
        {codegen.c_manager.err('too many brackets')}
    }}
}} else {{
    for (int {i} = 0; {i} < ({num_matches}); {i}++) {{
""")
            codegen.prepend_code(f"""{codegen.call(f'{matches_type.c_type}_add', [
    Arg(matches), Arg(Object(
        f'(Match){{.match = (string){caps}[{i}].ptr, .length = {caps}[{i}].len}}',
        Type('Match'), call_position
    ))
], call_position)};
    }}
}}
""")
            
            return matches
        
        @c_dec(
            params=(Param('pattern', Type('string')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Regex_new(codegen, call_position: Position, pattern: Object) -> Object:
            re: TempVar = codegen.create_temp_var(Type('Regex'), call_position)
            codegen.prepend_code(f'Regex {re} = {{ .pattern = {pattern} }};')
            return re.OBJECT()
