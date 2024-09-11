from codegen.objects import Object, Position, Type, Arg, TempVar
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
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Regex_type(_, call_position: Position) -> Object:
            return Object('"Regex"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Match_type(_, call_position: Position) -> Object:
            return Object('"Match"', Type('string'), call_position)
        
        @c_dec(param_types=('Regex',), is_method=True, add_to_class=self)
        def _Regex_to_string(codegen, call_position: Position, re: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, '"Regex(pattern=%s)"', f'({re}).pattern'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(param_types=('Match',), is_method=True, add_to_class=self)
        def _Match_to_string(codegen, call_position: Position, match: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, '"Match(length=%d, is_match=%s)"',
                f'(({match}).length)', codegen.call(
                    'bool_to_string',
                    [Arg(Object(f'(({match}).is_match)', Type('bool'), call_position))],
                    call_position
                ).code
            )

            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        

        @c_dec(param_types=('Match',), is_property=True, add_to_class=self)
        def _Match_length(_, call_position: Position, match: Object) -> Object:
            return Object(f'(({match}).length)', Type('int'), call_position)
        
        @c_dec(param_types=('Match',), is_property=True, add_to_class=self)
        def _Match_is_match(_, call_position: Position, match: Object) -> Object:
            return Object(f'(({match}).is_match)', Type('bool'), call_position)
        
        
        @c_dec(param_types=('Regex',), is_property=True, add_to_class=self)
        def _Regex_pattern(_, call_position: Position, re: Object) -> Object:
            return Object(f'(({re}).pattern)', Type('string'), call_position)
        
        @c_dec(param_types=('Regex', 'string'), is_method=True, add_to_class=self)
        def _Regex_match(codegen, call_position: Position, re: Object, string: Object) -> Object:
            match_length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            is_match: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            obj: TempVar = codegen.create_temp_var(Type('Match'), call_position)
            codegen.prepend_code(f"""int {match_length};
bool {is_match} = re_matchp(({re}).compiled, {string}, &{match_length}) != -1;
Match {obj} = {{ .length = {match_length}, .is_match = {is_match} }};
""")
            
            return obj.OBJECT()
        
        @c_dec(param_types=('Regex', 'string'), is_method=True, add_to_class=self)
        def _Regex_fullmatch(codegen, call_position: Position, re: Object, string: Object) -> Object:
            obj = _Regex_match(codegen, call_position, re, string)
            codegen.prepend_code(f"""if (!(({obj}).is_match) && (*({string})) == '\\0') {{
    {obj}.is_match = false;
}}
""")
            
            return obj
        
        @c_dec(param_types=('string',), is_method=True, is_static=True, add_to_class=self)
        def _Regex_new(codegen, call_position: Position, pattern: Object) -> Object:
            re: TempVar = codegen.create_temp_var(Type('Regex'), call_position)
            codegen.prepend_code(
                f'Regex {re} = {{ .pattern = {pattern}, .compiled = re_compile({pattern}) }};'
            )
            return re.OBJECT()
