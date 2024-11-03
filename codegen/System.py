from codegen.objects import Object, Type, Param, Position, TempVar, EnvItem
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec
from codegen.target import Target


class System:
    def __init__(self, c_manager) -> None:
        c_manager.codegen.add_toplevel_code("""typedef struct {
    byte _;
} System;

typedef struct {
    time_t t;
    struct tm *ti;
} Time;
""")
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_pid(codegen, call_position: Position) -> Object:
            return Object('((int)GetCurrentProcessId())' if codegen.target == Target.WINDOWS else\
                '((int)getpid())', Type('int'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_os(_, call_position: Position) -> Object:
            return Object('OS', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_arch(_, call_position: Position) -> Object:
            return Object('ARCH', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_admin(_, call_position: Position) -> Object:
            return Object('((bool)IS_ADMIN)', Type('bool'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_processor_count(codegen, call_position: Position) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.not_supported_err('System.processor_count')
            
            sysinfo: TempVar = codegen.create_temp_var(Type('SystemInfo'), call_position)
            codegen.prepend_code(f"""SYSTEM_INFO {sysinfo};
GetSystemInfo(&{sysinfo});
""")
            
            return Object(f'((int){sysinfo}.dwNumberOfProcessors)', Type('int'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_cwd(codegen, call_position: Position) -> Object:
            cwd_var: TempVar = codegen.create_temp_var(Type('string'), call_position)
            error_condition: str
            if codegen.target == Target.WINDOWS:
                error_condition = f'GetCurrentDirectory(sizeof({cwd_var}), {cwd_var}) == 0'
            else:
                error_condition = f'getcwd({cwd_var}, sizeof({cwd_var})) == NULL'
            
            codegen.prepend_code(f"""char {cwd_var}[1024];
if ({error_condition}) {{
    {codegen.c_manager.err('Failed to get current working directory')}
}}
""")
            
            return cwd_var.OBJECT()
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_time(codegen, call_position: Position) -> Object:
            t: TempVar = codegen.create_temp_var(Type('TimeInt', 'time_t'), call_position)
            codegen.prepend_code(f'time_t {t} = time(NULL);')
            return Object(f'(Time){{ .t = {t}, .ti = localtime(&{t}) }}', Type('Time'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_cursor_pos(codegen, call_position: Position) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.not_supported_err('System.cursor_pos')
            
            point: TempVar = codegen.create_temp_var(Type('POINT'), call_position)
            codegen.prepend_code(f"""POINT {point};
GetCursorPos(&{point});
""")
            
            return codegen.c_manager._Math_vec2(
                codegen, call_position, Object(f'(int){point}.x', Type('int'), call_position),
                Object(f'(int){point}.y', Type('int'), call_position)
            )
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_BLACK(_, call_position: Position) -> Object:
            return Object('"\\033[30m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_RED(_, call_position: Position) -> Object:
            return Object('"\\033[31m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_GREEN(_, call_position: Position) -> Object:
            return Object('"\\033[32m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_YELLOW(_, call_position: Position) -> Object:
            return Object('"\\033[33m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_BLUE(_, call_position: Position) -> Object:
            return Object('"\\033[34m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_MAGENTA(_, call_position: Position) -> Object:
            return Object('"\\033[35m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_CYAN(_, call_position: Position) -> Object:
            return Object('"\\033[36m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_WHITE(_, call_position: Position) -> Object:
            return Object('"\\033[37m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_BBLACK(_, call_position: Position) -> Object:
            return Object('"\\033[90m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_BRED(_, call_position: Position) -> Object:
            return Object('"\\033[91m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_BGREEN(_, call_position: Position) -> Object:
            return Object('"\\033[92m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_BYELLOW(_, call_position: Position) -> Object:
            return Object('"\\033[93m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_BBLUE(_, call_position: Position) -> Object:
            return Object('"\\033[94m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_BMAGENTA(_, call_position: Position) -> Object:
            return Object('"\\033[95m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_BCYAN(_, call_position: Position) -> Object:
            return Object('"\\033[96m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_COLOR_BWHITE(_, call_position: Position) -> Object:
            return Object('"\\033[97m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_TERMINAL_RESET(_, call_position: Position) -> Object:
            return Object('"\\033[0m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_TERMINAL_BOLD(_, call_position: Position) -> Object:
            return Object('"\\033[1m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_TERMINAL_CROSS(_, call_position: Position) -> Object:
            return Object('"\\033[9m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_TERMINAL_ITALIC(_, call_position: Position) -> Object:
            return Object('"\\033[3m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_TERMINAL_UNDERLINE(_, call_position: Position) -> Object:
            return Object('"\\033[4m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_TERMINAL_SLOW_BLINK(_, call_position: Position) -> Object:
            return Object('"\\033[5m"', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_TERMINAL_FAST_BLINK(_, call_position: Position) -> Object:
            return Object('"\\033[6m"', Type('string'), call_position)
        
        # https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
        
        @c_dec(
            param_types=(Param('code', Type('int'), default=Object('0', Type('int'))),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _System_exit(codegen, call_position: Position, code: Object) -> Object:
            codegen.prepend_code(f'{codegen.get_end_code()}\nexit({code});')
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('milliseconds', Type('int')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _System_sleep(codegen, call_position: Position, milliseconds: Object) -> Object:
            code: str
            if codegen.target == Target.WINDOWS:
                code = f'Sleep({milliseconds});'
            elif codegen.target == Target.LINUX or codegen.target == Target.MAC:
                code = f'usleep({milliseconds} * 1000);'
            else:
                call_position.not_supported_err('System.sleep()')
            
            codegen.prepend_code(code)
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('func', Type('function')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _System_atexit(codegen, call_position: Position, func: Object) -> Object:
            void_func: str = codegen.get_unique_name()
            codegen.scope.env[void_func] = EnvItem(
                void_func, Type('nil'), call_position, reserved=True
            )
            
            func_obj: EnvItem = codegen.scope.env[str(func)]
            if func_obj.func is None:
                call_position.error_here(f'\'{func}\' is not a function')
            
            if func_obj.func.return_type != Type('nil'):
                call_position.error_here(
                    f'\'{func}\' set as an atexit function but does not return nil'
                )
            elif func_obj.func.params != []:
                call_position.error_here(
                    f'\'{func}\' set as an atexit function but has parameters'
                )
            
            codegen.add_toplevel_code(f"""nil {func}();
void {void_func}() {{ {func}(); }}
""")
            codegen.prepend_code(f'atexit({void_func});')
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('command', Type('string')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _System_shell(_, call_position: Position, command: Object) -> Object:
            return Object(f'((bool)system({command}))', Type('bool'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _System_block_keyboard(codegen, call_position: Position) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.not_supported_err('System.block_keyboard()')
            
            codegen.prepend_code(f"""if (!IS_ADMIN) {{
    {codegen.c_manager.err('Blocking keyboard requires administrator permissions')}
}}

BlockInput(TRUE);
""")
            
            return Object.NULL(call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _System_unblock_keyboard(codegen, call_position: Position) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.not_supported_err('System.unblock_keyboard()')
            
            codegen.prepend_code(f"""if (!IS_ADMIN) {{
    {codegen.c_manager.err('Unblocking keyboard requires administrator permissions')}
}}

BlockInput(FALSE);
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('char', Type('string')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _System_is_key_pressed(codegen, call_position: Position, char: Object) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.not_supported_err('System.is_key_pressed()')
            
            codegen.prepend_code(f"""if (!{
    codegen.c_manager._string_is_char(codegen, call_position, char)
}) {{
    {codegen.c_manager.err('Key must be a single character')}
}}
""")
            
            return Object(
                f'(bool)(GetAsyncKeyState((int)({char})[0] & 0x8000))',
                Type('bool'), call_position
            )
        
        # System set cursor position with int, int
        def Sscp_intint(codegen, call_position: Position,
                                        x: Object, y: Object) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.not_supported_err('System.set_cursor_pos()')
            
            codegen.prepend_code(f'SetCursorPos({x}, {y});')
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('vec', Type('Vector2')),), is_method=True, is_static=True,
            add_to_class=self, overloads={
                OverloadKey(
                    Type('nil'), (Param('x', Type('int')), Param('y', Type('int')))
                ): OverloadValue(Sscp_intint)
            }
        )
        def _System_set_cursor_pos(codegen, call_position: Position, vec: Object) -> Object:
            if codegen.target != Target.WINDOWS:
                call_position.not_supported_err('System.set_cursor_pos()')
            
            codegen.prepend_code(f'SetCursorPos(({vec}).x, ({vec}).y);')
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('time', Type('string')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _System_time_from_string(codegen, call_position: Position, time: Object) -> Object:
            year: TempVar = codegen.create_temp_var(Type('int'), call_position)
            month: TempVar = codegen.create_temp_var(Type('int'), call_position)
            day: TempVar = codegen.create_temp_var(Type('int'), call_position)
            hour: TempVar = codegen.create_temp_var(Type('int'), call_position)
            minute: TempVar = codegen.create_temp_var(Type('int'), call_position)
            second: TempVar = codegen.create_temp_var(Type('int'), call_position)
            result: TempVar = codegen.create_temp_var(Type('time_t'), call_position)
            breakdown: TempVar = codegen.create_temp_var(Type('struct tm'), call_position)
            obj: TempVar = codegen.create_temp_var(Type('Time'), call_position)
            
            codegen.prepend_code(f"""time_t {result} = 0;
int {year} = 0, {month} = 0, {day} = 0, {hour} = 0, {minute} = 0, {second} = 0;
if (sscanf({time}, "%4d.%2d.%2d %2d:%2d:%2d", &{year}, &{month}, &{day}, &{hour}, &{minute},
    &{second}) != 6) {{
    {codegen.c_manager.err('Invalid date format, expected: YYYY.MM.DD HH:MM:SS')}
}}

struct tm {breakdown} = {{0}};
{breakdown}.tm_year = {year};
{breakdown}.tm_mon = {month};
{breakdown}.tm_mday = {day};
{breakdown}.tm_hour = {hour};
{breakdown}.tm_min = {minute};
{breakdown}.tm_sec = {second};

if (({result} = mktime(&{breakdown})) == (time_t)-1) {{
    {codegen.c_manager.err('Could not convert time input to time_t')}
}}

Time {obj} = {{ .t = {result}, .ti = &{breakdown} }};
""")
            
            return obj.OBJECT()


        @c_dec(param_types=(Param('a', Type('Time')), Param('b', Type('Time'))), add_to_class=self)
        def _Time_eq_Time(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'({a.attr("t")} == {b.attr("t")})', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('Time')), Param('b', Type('Time'))), add_to_class=self)
        def _Time_neq_Time(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'({a.attr("t")} != {b.attr("t")})', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('Time')), Param('b', Type('Time'))), add_to_class=self)
        def _Time_gt_Time(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'({a.attr("t")} > {b.attr("t")})', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('Time')), Param('b', Type('Time'))), add_to_class=self)
        def _Time_lt_Time(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'({a.attr("t")} < {b.attr("t")})', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('Time')), Param('b', Type('Time'))), add_to_class=self)
        def _Time_gte_Time(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'({a.attr("t")} >= {b.attr("t")})', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('Time')), Param('b', Type('Time'))), add_to_class=self)
        def _Time_lte_Time(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'({a.attr("t")} <= {b.attr("t")})', Type('bool'), call_position)

        @c_dec(param_types=(Param('time', Type('Time')),), is_property=True, add_to_class=self)
        def _Time_second(_, call_position: Position, time: Object) -> Object:
            return Object(f'(({time}).ti->tm_sec)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('time', Type('Time')),), is_property=True, add_to_class=self)
        def _Time_minute(_, call_position: Position, time: Object) -> Object:
            return Object(f'(({time}).ti->tm_min)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('time', Type('Time')),), is_property=True, add_to_class=self)
        def _Time_hour(_, call_position: Position, time: Object) -> Object:
            return Object(f'(({time}).ti->tm_hour)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('time', Type('Time')),), is_property=True, add_to_class=self)
        def _Time_day(_, call_position: Position, time: Object) -> Object:
            return Object(f'(({time}).ti->tm_mday)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('time', Type('Time')),), is_property=True, add_to_class=self)
        def _Time_month(_, call_position: Position, time: Object) -> Object:
            return Object(f'(({time}).ti->tm_mon + 1)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('time', Type('Time')),), is_property=True, add_to_class=self)
        def _Time_year(_, call_position: Position, time: Object) -> Object:
            return Object(f'(({time}).ti->tm_year + 1900)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('time', Type('Time')),), is_property=True, add_to_class=self)
        def _Time_weekday(_, call_position: Position, time: Object) -> Object:
            return Object(f'(({time}).ti->tm_wday)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('time', Type('Time')),), is_property=True, add_to_class=self)
        def _Time_yearday(_, call_position: Position, time: Object) -> Object:
            return Object(f'(({time}).ti->tm_yday)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('time', Type('Time')),), is_property=True, add_to_class=self)
        def _Time_isdst(_, call_position: Position, time: Object) -> Object:
            return Object(f'(({time}).ti->tm_isdst)', Type('int'), call_position)
