from codegen.objects import Object, Position, Type, Arg
from codegen.c_manager import c_dec, INCLUDES


class regex:
    def __init__(self, codegen) -> None:
        codegen.valid_types.append('Regex')
        codegen.extra_compile_args.append(INCLUDES / 'tinyregexc/re.c')
        codegen.c_manager.include(f'"{INCLUDES / "tinyregexc/re.h"}"', codegen)
        
        codegen.add_toplevel_code("""#ifndef CURE_REGEX_H
typedef struct {
    const char* pattern;
    re_t compiled;
} Regex;

typedef struct {
    int length;
    bool is_match;
} Match;
#define CURE_REGEX_H
#endif
""")
        
    @c_dec(is_method=True, is_static=True)
    def _Regex_type(self, _, call_position: Position) -> Object:
        return Object('"Regex"', Type('string'), call_position)
    
    @c_dec(is_method=True, is_static=True)
    def _Match_type(self, _, call_position: Position) -> Object:
        return Object('"Match"', Type('string'), call_position)
    
    @c_dec(param_types=('Regex',), is_method=True)
    def _Regex_to_string(self, codegen, call_position: Position, re: Object) -> Object:
        code, buf_free = codegen.c_manager.fmt_length(
            codegen, call_position, '"Regex(pattern=%s)"', f'({re}).pattern'
        )
        
        codegen.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('Match',), is_method=True)
    def _Match_to_string(self, codegen, call_position: Position, match: Object) -> Object:
        code, buf_free = codegen.c_manager.fmt_length(
            codegen, call_position, '"Match(length=%d, is_match=%s)"',
            f'(({match}).length)', codegen.call(
                'bool_to_string',
                [Arg(Object(f'(({match}).is_match)', Type('bool'), call_position))],
                call_position
            ).code
        )

        codegen.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    

    @c_dec(param_types=('Match',), is_property=True)
    def _Match_length(self, _, call_position: Position, match: Object) -> Object:
        return Object(f'(({match}).length)', Type('int'), call_position)
    
    @c_dec(param_types=('Match',), is_property=True)
    def _Match_is_match(self, _, call_position: Position, match: Object) -> Object:
        return Object(f'(({match}).is_match)', Type('bool'), call_position)
    
    
    @c_dec(param_types=('Regex',), is_property=True)
    def _Regex_pattern(self, _, call_position: Position, re: Object) -> Object:
        return Object(f'(({re}).pattern)', Type('string'), call_position)
    
    @c_dec(param_types=('Regex', 'string'), is_method=True)
    def _Regex_match(self, codegen, call_position: Position, re: Object, string: Object) -> Object:
        match_length = codegen.create_temp_var(Type('int'), call_position)
        is_match = codegen.create_temp_var(Type('bool'), call_position)
        obj = codegen.create_temp_var(Type('Match'), call_position)
        codegen.prepend_code(f"""int {match_length};
bool {is_match} = re_matchp(({re}).compiled, {string}, &{match_length}) != -1;
Match {obj} = {{ .length = {match_length}, .is_match = {is_match} }};
""")
        return Object(obj, Type('Match'), call_position)
    
    @c_dec(param_types=('string',), is_method=True, is_static=True)
    def _Regex_new(self, codegen, call_position: Position, pattern: Object) -> Object:
        re = codegen.create_temp_var(Type('Regex'), call_position)
        codegen.prepend_code(
            f'Regex {re} = {{ .pattern = {pattern}, .compiled = re_compile({pattern}) }};'
        )
        return Object(re, Type('Regex'), call_position)
