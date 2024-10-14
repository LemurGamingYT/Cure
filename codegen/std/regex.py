from codegen.objects import Object, Position, Type, Arg, TempVar, Param
# from codegen.array_manager import DEFAULT_CAPACITY
from codegen.c_manager import c_dec, INCLUDES


class regex:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type('Regex')
        codegen.extra_compile_args.append(INCLUDES / 'tinyregexc/re.c')
        codegen.c_manager.include(f'"{INCLUDES / "tinyregexc/re.h"}"', codegen)
        codegen.c_manager.reserve((
            '_TINY_REGEX_C', 'RE_DOT_MATCHES_NEWLINE', 'regex_t', 're_t', 're_compile', 're_matchp',
            're_match'
        ))
        codegen.add_toplevel_code("""#ifndef CURE_REGEX_H
typedef struct {
    const char* pattern;
    re_t compiled;
} Regex;

typedef struct {
    int length;
    bool is_match;
} Match;

typedef struct {
    char* str;
    size_t length;
    size_t capacity;
    char* previously_added;
} RegexBuilder;
#define CURE_REGEX_H
#endif
""")
        
        codegen.c_manager.init_class(self, 'Regex', Type('Regex'))
        codegen.c_manager.init_class(self, 'Match', Type('Match'))
        codegen.c_manager.init_class(self, 'RegexBuilder', Type('RegexBuilder'))
        codegen.c_manager.wrap_struct_properties('match', Type('Match'), [
            Param('length', Type('int')), Param('is_match', Type('bool'))
        ])
        
        codegen.c_manager.wrap_struct_properties('regex', Type('regex'), [
            Param('pattern', Type('string'))
        ])
        
        codegen.c_manager.wrap_struct_properties('rbuilder', Type('RegexBuilder'), [
            Param('length', Type('int')), Param('capacity', Type('int'))
        ])
        
        
        @c_dec(param_types=(Param('regex', Type('Regex')),), is_method=True, add_to_class=self)
        def _Regex_to_string(codegen, call_position: Position, re: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position, '"Regex(pattern=%s)"', f'({re}).pattern'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(param_types=(Param('match', Type('Match')),), is_method=True, add_to_class=self)
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
        
        
        @c_dec(
            param_types=(Param('regex', Type('Regex')), Param('s', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _Regex_match(codegen, call_position: Position, re: Object, string: Object) -> Object:
            match_length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            is_match: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            obj: TempVar = codegen.create_temp_var(Type('Match'), call_position)
            codegen.prepend_code(f"""int {match_length};
bool {is_match} = re_matchp(({re}).compiled, {string}, &{match_length}) != -1;
Match {obj} = {{ .length = {match_length}, .is_match = {is_match} }};
""")
            
            return obj.OBJECT()
        
        @c_dec(
            param_types=(Param('regex', Type('Regex')), Param('s', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _Regex_fullmatch(codegen, call_position: Position, re: Object, string: Object) -> Object:
            obj = _Regex_match(codegen, call_position, re, string)
            codegen.prepend_code(f"""if (!(({obj}).is_match) && (*({string})) == '\\0') {{
    {obj}.is_match = false;
}}
""")
            
            return obj
        
#         @c_dec(
#             param_types=(Param('regex', Type('Regex')), Param('s', Type('string'))),
#             is_method=True, add_to_class=self
#         )
#         def _Regex_findall(codegen, call_position: Position, re: Object, string: Object) -> Object:
#             match_length: TempVar = codegen.create_temp_var(Type('int'), call_position)
#             match_start: TempVar = codegen.create_temp_var(Type('int'), call_position)
#             capacity: TempVar = codegen.create_temp_var(Type('int'), call_position)
#             start: TempVar = codegen.create_temp_var(Type('string'), call_position)
#             res: TempVar = codegen.create_temp_var(Type('string*'), call_position)
#             size: TempVar = codegen.create_temp_var(Type('int'), call_position)
#             codegen.prepend_code(f"""string {start} = {string};
# int {size} = 0, {capacity} = {DEFAULT_CAPACITY}, {match_length};
# string* {res} = (string*)malloc({capacity} * sizeof(string));
# {codegen.c_manager.buf_check(str(res))}
# while (*{start} != '\\0') {{
#     int {match_start} = re_matchp(({re}).compiled, {start}, &{match_length});
#     if ({match_start} == -1) break;
    
#     {res}[{size}] = (string)malloc(({match_length} + 1));
#     {codegen.c_manager.buf_check(str(res))}
#     strncpy({res}[{size}], {start} + {match_start}, {match_length});
#     {res}[{size}][{match_length}] = '\\0';
#     {size}++;
    
#     if ({size} == {capacity}) {{
#         {capacity} *= 2;
#         {res} = (string*)realloc({res}, {capacity} * sizeof(char*));
#         {codegen.c_manager.buf_check(str(res))}
#     }}
    
#     {start} += {match_start} + {match_length};
# }}
# """)
            
#             code, arr = codegen.c_manager.array_from_c_array(
#                 codegen, call_position, Type('string'), str(res), capacity
#             )
            
#             codegen.prepend_code(code)
#             return arr.OBJECT()
        
        @c_dec(
            param_types=(Param('pattern', Type('string')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Regex_new(codegen, call_position: Position, pattern: Object) -> Object:
            re: TempVar = codegen.create_temp_var(Type('Regex'), call_position)
            codegen.prepend_code(
                f'Regex {re} = {{ .pattern = {pattern}, .compiled = re_compile({pattern}) }};'
            )
            return re.OBJECT()
