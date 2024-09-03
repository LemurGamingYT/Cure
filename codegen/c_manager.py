from typing import Callable, Any
from functools import wraps
from pathlib import Path

from codegen.objects import Object, Position, EnvItem, Free, Type, ID_REGEX, Function, Arg


CURRENT_FILE = Path(__file__).absolute()
STD_PATH = CURRENT_FILE.parent / 'std'
INCLUDES = CURRENT_FILE.parent.parent / 'include'
LIBS = CURRENT_FILE.parent.parent / 'libs'
HEADER = (INCLUDES / 'header.h').as_posix()


def func_modification(param_types: tuple[str, ...] | None = None) -> Callable:
    """Modify a function to have special properties.
    
    Args:
        param_types (tuple[str, ...] | None, optional): The parameter types of the mod.
        Defaults to None (an empty tuple).

    Returns:
        Callable: The decorator callable.
    """
    
    if param_types is None:
        param_types = ()
    
    def decorator(func: Callable) -> Callable:
        setattr(func, 'param_types', param_types)
        
        @wraps(func)
        def wrapper(codegen, func_obj, call_position: Position, args: tuple[Arg],
                    mod_args: tuple[Arg]):
            return func(codegen, func_obj, call_position, args, mod_args)
        
        return wrapper
    
    return decorator

def c_dec(
    param_types: tuple[str, ...] | None = None,
    overloads: dict[tuple[tuple[str, ...], str], Callable | None] | None = None,
    is_method: bool = False,
    is_static: bool = False,
    is_property: bool = False,
    can_user_call: bool = False,
    return_type: Type | None = None,
    func_name_override: str | None = None,
    add_to_class: Any = None
) -> Callable:
    """Make a function able to be used as a C function.

    Args:
        param_types (tuple[str, ...] | None, optional): The function parameter types.
            Defaults to None.
        overloads ((tuple[tuple[str, ...], str], Callable), optional): The possible type overloads.
            The overloads are defined as: ((parameter types), return type): function. The function
            can None to reference the original function. Defaults to None.
        is_method (bool, optional): Defines if the function can only be called using the
            call syntax 'func(args)'. Defaults to False.
        is_static (bool, optional): Defines if the function can be called without needing an
            instance of the class (e.g. Math or System). Defaults to False.
        is_property (bool, optional): Defines if the function can only be got using the '.'
            operator. Defaults to False.
        can_user_call (bool, optional): Defines if the function can be called by the user
            directly. Defaults to False.
        return_type (Type | None, optional): Only used for the iter_type functions. Defaults to
            None.
        func_name_override (str | None, optional): Override the function name. Defaults to None.
        add_to_class (type | None, optional): The class to add the function to. Useful for adding
            the function to, for example, the `CManager` class. Defaults to None.

    Returns:
        Callable: The decorator callable.
    """
    
    if param_types is None:
        param_types = ()
    
    if overloads is None:
        overloads = {}
    
    def decorator(func: Callable) -> Callable:
        setattr(func, 'param_types', param_types)
        setattr(func, 'overloads', overloads)
        setattr(func, 'is_method', is_method)
        setattr(func, 'is_static', is_static)
        setattr(func, 'is_property', is_property)
        setattr(func, 'return_type', return_type)
        setattr(func, 'can_user_call', can_user_call)
        setattr(func, 'func_name_override', func_name_override)
        setattr(func, 'added_to_class', add_to_class)
        
        name = func_name_override if func_name_override is not None else func.__name__[1:]
        
        if add_to_class is not None:
            cname = name if name.startswith('_') else f'_{name}'
            if isinstance(add_to_class, CManager):
                add_to_class.add_func(cname, func)
            
            setattr(add_to_class, cname, func)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


class CManager:
    # reserved names mostly from standard library headers https://en.cppreference.com/w/c/header
    RESERVED_NAMES = [
        'string', 'int', 'float', 'bool', 'nil', 'static', 'typedef', 'const', 'char', 'struct',
        'enum', 'if', 'else', 'for', 'extern', 'return', 'while', 'break', 'continue', 'switch',
        'case', 'default', 'do', 'double', 'long', 'short', 'register', 'union', 'volatile',
        'goto', 'restrict', 'unsigned', 'inline', 'auto', 'asm', 'signed', 'printf', 'scanf',
        'abs', 'labs', 'llabs', 'div', 'ldiv', 'lldiv', 'imaxabs', 'imaxdiv', 'fabs', 'fabsf',
        'fabsl', 'fmod', 'fmodl', 'fmodf', 'remainder', 'remainderf', 'remainderl', 'remquo',
        'remquof', 'remquol', 'fma', 'fmaf', 'fmal', 'fmax', 'fmaxf', 'fmaxl', 'fmin', 'fminf',
        'fminl', 'fdim', 'fdimf', 'fdiml', 'nan', 'nanf', 'nanl', 'exp', 'expf', 'expl', 'exp2',
        'exp2f', 'exp2l', 'log', 'logf', 'logl', 'log10', 'log10f', 'log10l', 'log2', 'log2f',
        'log2l', 'loglp', 'loglpf', 'loglpl', 'pow', 'powf', 'powl', 'sqrt', 'sqrtf', 'sqrtl',
        'cbrt', 'cbrtf', 'cbrtl', 'hypot', 'hypotf', 'hypotl', 'sin', 'sinf', 'sinl', 'cos',
        'cosf', 'cosl', 'tan', 'tanf', 'tanl', 'asin', 'asinf', 'asinl', 'acos', 'acosf',
        'acosl', 'atan', 'atanf', 'atanl', 'atan2', 'atan2f', 'atan2l', 'sinh', 'sinhf',
        'sinhl', 'cosh', 'coshf', 'coshl', 'tanh', 'tanhf', 'tanhl', 'asinh', 'asinhf', 'asinhl',
        'acosh', 'acoshf', 'acoshl', 'atanh', 'atanhf', 'atanhl', 'erf', 'erff', 'erfl', 'erfc',
        'erfcl', 'erfcf', 'lgamma', 'lgammaf', 'lgammal', 'tgamma', 'tgammaf', 'tgammal', 'ceil',
        'ceilf', 'ceill', 'floor', 'floorf', 'floorl', 'trunc', 'truncf', 'truncl', 'round',
        'roundf', 'roundl', 'lround', 'lroundf', 'lroundl', 'llround', 'llroundf', 'llroundl',
        'rint', 'rintf', 'rintl', 'lrint', 'lrintf', 'lrintl', 'llrint', 'llrintf', 'llrintl',
        'nearbyint', 'nearbyintf', 'nearbyintl', 'frexp', 'frexpf', 'frexpl', 'modf', 'modff',
        'modfl', 'scalbn', 'scalbnf', 'scalbnl', 'scalbln', 'scalblnf', 'scalblnl', 'ldexp',
        'ldexpf', 'ldexpl', 'ilogb', 'ilogbf', 'ilogbl', 'logb', 'logbf', 'logbl', 'nextafter', 
        'nextafterf', 'nextafterl', 'copysign', 'copysignf', 'copysignl', 'nexttoward',
        'nexttowardf', 'nexttowardl', 'copysign', 'copysignf', 'copysignl', 'fpclassify',
        'isfinite', 'isinf', 'isnan', 'isnormal', 'signbit', 'isgreater', 'isgreaterequal',
        'isless', 'islessequal', 'islessgreater', 'isunordered', 'div_t', 'ldiv_t', 'lldiv_t',
        'imaxdiv_t', 'float_t', 'double_t', 'HUGE_VAL', 'HUGE_VALF', 'HUGE_VALL', 'INFINITY',
        'NAN', 'FP_FAST_FMAF', 'FP_FAST_FMA', 'FP_FAST_FMAF', 'FP_ILOGBNAN', 'FP_ILOGB0',
        'math_errhandling', 'MATH_ERRNO', 'MATH_ERREXCEPT', 'FP_NORMAL', 'FP_SUBNORMAL',
        'FP_ZERO', 'FP_INFINITE', 'FP_NAN', 'size_t', 'ptrdiff_t', 'nullptr_t', 'max_align_t',
        'offsetof', '__bool_true_false_are_defined', 'alignas', 'alignof', '__alignas_is_defined',
        '__alignof_is_defined', 'noreturn', 'FILE', 'fpos_t', 'stdin', 'stdout', 'stderr',
        'fopen', 'fopen_s', 'freopen', 'freopen_s', 'fclose', 'fflush', 'setbuf', 'setvbuf',
        'fwide', 'fread', 'fwrite', 'fgetc', 'getc', 'fgets', 'fputc', 'putc', 'fputs', 'getchar',
        'gets', 'gets_s', 'putchar', 'puts', 'ungetc', 'fgetwc', 'getwc', 'fgetws',
        'fputwc', 'putwc', 'fputws', 'getwchar', 'putwchar', 'ungetwc', 'fseek', 'fscanf',
        'sscanf', 'scanf_s', 'fscanf_s', 'sscanf_s', 'vscanf', 'vsscanf', 'vscanf_s', 'vfscanf_s',
        'vsscanf_s', 'fprintf', 'sprintf', 'snprintf', 'printf_s', 'fprintf_s', 'sprintf_s',
        'snprintf_s', 'vprintf', 'vfprintf', 'vsprintf', 'vsnprintf', 'vprintf_s', 'vfprintf_s',
        'vsprintf_s', 'vsnprintf_s', 'vprintf_s', 'vsnprintf_s', 'wscanf', 'fwscanf', 'fwscanf_s',
        'swscanf', 'swscanf_s', 'vwscanf', 'vswscanf', 'vwscanf_s', 'vswscanf_s', 'wprintf',
        'fwprintf', 'fwprintf_s', 'swprintf', 'swprintf_s', 'vfwprintf_s', 'vswprintf_s',
        'vfwprintf_s', 'vswprintf_s', 'vfwprintf_s', 'vswprintf_s', 'vfwprintf_s', 'ftell',
        'fgetpos', 'fseek', 'fsetpos', 'rewind', 'clearerr', 'feof', 'ferror', 'perror',
        'remove', 'rename', 'tmpfile', 'tmpfile_s', 'tmpnam', 'tmpnam_s', 'EOF', 'FOPEN_MAX',
        'FILENAME_MAX', 'BUFSIZ', '_IOFBF', '_IOLBF', '_IONBF', 'SEEK_SET', 'SEEK_CUR',
        'SEEK_END', 'TMP_MAX', 'TMP_MAX_S', 'L_tmpnam', 'L_tmpnam_s', 'abort', 'exit',
        'quick_exit', '_Exit', 'atexit', 'at_quick_exit', 'EXIT_SUCCESS', 'EXIT_FAILURE',
        'unreachable', 'system', 'getenv', 'getenv_s', 'signal', 'raise', 'sig_atomic_t',
        'SIG_DFL', 'SIG_IGN', 'SIG_ERR', 'SIGABRT', 'SIGFPE', 'SIGILL', 'SIGINT',
        'SIGSEGV', 'SIGTERM', 'setjmp', 'longjmp', 'jmp_buf', 'difftime', 'time', 'clock',
        'timespec_get', 'timespec_getres', 'asctime', 'asctime_s', 'ctime', 'ctime_s',
        'strftime', 'wcsftime', 'gmtime', 'gmtime_s', 'gmtime_r', 'localtime', 'localtime_s',
        'localtime_r', 'mktime', 'CLOCK_PER_SEC', 'tm', 'time_t', 'clock_t', 'timespec',
        'isalnum', 'isalpha', 'iscntrl', 'isdigit', 'isgraph', 'islower', 'isprint',
        'ispunct', 'isspace', 'isupper', 'isxdigit', 'tolower', 'toupper', 'isblank',
        'tolower', 'toupper', 'atof', 'atoi', 'atol', 'atoll', 'strtol', 'strtoll',
        'strtoul', 'strtoull', 'strtof', 'strtod', 'strtold', 'strtoimax', 'strtoumax',
        'strcpy', 'strcpy_s', 'strncpy', 'strncpy_s', 'strcat', 'strcat_s', 'strncat',
        'strncat_s', 'strdup', 'strdup_s', 'strndup', 'strndup_s', 'strchr', 'strrchr',
        'strspn', 'strcspn', 'strpbrk', 'strstr', 'strtok', 'strtok_s', 'strtok_r',
        'strlen', 'strnlen', 'strnlen_s', 'strnlen_s', 'strnlen_s', 'strnlen_s',
        'strspn_s', 'strcspn_s', 'strpbrk_s', 'strstr_s', 'strtok_s', 'strtok_r',
        'memchr', 'memcmp', 'memcpy', 'memset', 'memset_s', 'memset_explicit', 'memcpy_s',
        'memmove', 'memmove_s', 'memccpy', 'strerror', 'strerror_s', 'strerrorlen_s',
        'S_IFMT', 'S_IFBLK', 'S_IFCHR', 'S_IFIFO', 'S_IFREG', 'S_IFDIR', 'S_IFLNK',
        'S_IRWXU', 'S_IRUSR', 'S_IWUSR', 'S_IXUSR', 'S_IRWXG', 'S_IRGRP', 'S_IWGRP',
        'S_IXGRP', 'S_IRWXO', 'S_IROTH', 'S_IWOTH', 'S_IXOTH', 'S_IRWXG', 'S_IRGRP',
        'S_IWGRP', 'S_IXGRP', 'S_IRWXO', 'S_IROTH', 'S_IWOTH', 'S_IXOTH', 'S_ISUID',
        'S_ISGID', 'S_ISVTX', 'S_ISBLK', 'S_ISCHR', 'S_ISDIR', 'S_ISFIFO', 'S_ISREG', 'S_ISLNK',
        'S_TYPEISMQ', 'S_TYPEISSEM', 'S_TYPEISSHM', 'chmod', 'fchmod', 'fstat', 'lstat', 'mkdir',
        'mkfifo', 'mknod', 'stat', 'umask', 'IS_ADMIN', 'default', 'rand'
    ]
    
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        self.includes = set()
        
        if not getattr(codegen, '_initialised_CManager', False):
            self.include(f'"{HEADER}"', codegen)
            self.include('<stdbool.h>', codegen)
            self.include('<stdlib.h>', codegen)
            self.include('<stdio.h>', codegen)
            self.include('<time.h>', codegen)
            self.includes.add('<windows.h>')
            self.includes.add('<io.h>')
            self.includes.add('<shlobj.h>')
            self.includes.add('<unistd.h>')
            
            POS_ZERO = Position(0, 0, '')
            
            codegen.scope.env['Math'] = EnvItem('Math', Type('Math'), POS_ZERO)
            codegen.scope.env['System'] = EnvItem('System', Type('System'), POS_ZERO)
            codegen.scope.env['Time'] = EnvItem('Time', Type('Time'), POS_ZERO)
            codegen.scope.env['MIN_INT'] = EnvItem('MIN_INT', Type('int'), POS_ZERO)
            codegen.scope.env['MAX_INT'] = EnvItem('MAX_INT', Type('int'), POS_ZERO)
            codegen.scope.env['DIGITS'] = EnvItem('DIGITS', Type('string'), POS_ZERO)
            codegen.scope.env['PUNCTUATION'] = EnvItem('PUNCTUATION', Type('string'), POS_ZERO)
            codegen.scope.env['LETTERS'] = EnvItem('LETTERS', Type('string'), POS_ZERO)
            codegen.scope.env['VERSION'] = EnvItem('VERSION', Type('string'), POS_ZERO)
            codegen.scope.env['MIN_FLOAT'] = EnvItem('MIN_FLOAT', Type('float'), POS_ZERO)
            codegen.scope.env['MAX_FLOAT'] = EnvItem('MAX_FLOAT', Type('float'), POS_ZERO)
            codegen.scope.env['ONE_BILLION'] = EnvItem('ONE_BILLION', Type('int'), POS_ZERO)
            codegen.scope.env['ONE_MILLION'] = EnvItem('ONE_MILLION', Type('int'), POS_ZERO)
            codegen.scope.env['ONE_THOUSAND'] = EnvItem('ONE_THOUSAND', Type('int'), POS_ZERO)
            codegen.scope.env['Cure'] = EnvItem('Cure', Type('Cure'), POS_ZERO)
            
            setattr(codegen, '_initialised_CManager', True)
            
            def _Math_absint(_, call_position: Position, x: Object) -> Object:
                return Object(
                    f'(abs({x}))',
                    Type('int'), call_position
                )
            
            @c_dec(
                param_types=('float',),
                is_method=True,
                is_static=True,
                overloads={(('int',), 'int'): _Math_absint},
                add_to_class=self
            )
            def _Math_abs(codegen, call_position: Position, x: Object) -> Object:
                self.include('<math.h>', codegen)
                return Object(f'((float)fabsf({x}))', Type('float'), call_position)
            
            def _System_exit2(codegen, call_position: Position) -> Object:
                codegen.prepend_code(f'{codegen.get_end_code()}\nexit(0);')
                return Object.NULL(call_position)
            
            @c_dec(
                param_types=('int',),
                is_method=True,
                is_static=True,
                overloads={((), 'nil'): _System_exit2},
                add_to_class=self
            )
            def _System_exit(codegen, call_position: Position, code: Object) -> Object:
                codegen.prepend_code(f'{codegen.get_end_code()}\nexit({code});')
                return Object.NULL(call_position)
            
            def rand_start0(codegen, call_position: Position, max: Object) -> Object:
                return _Math_random(
                    codegen, call_position, Object('0', Type('int'), call_position), max
                )
            
            @c_dec(
                param_types=('int', 'int'),
                is_method=True,
                is_static=True,
                overloads={(('int',), 'int'): rand_start0},
                add_to_class=self
            )
            def _Math_random(codegen, call_position: Position, min: Object,
                             max: Object) -> Object:
                low_num = codegen.create_temp_var(Type('int'), call_position)
                hi_num = codegen.create_temp_var(Type('int'), call_position)
                codegen.prepend_code(f"""int {low_num} = 0, {hi_num} = 0;
if (({min}) < ({max})) {{
    {low_num} = {min};
    {hi_num} = {max};
}} else {{
    {low_num} = {max};
    {hi_num} = {min};
}}

srand(time(NULL));
""")
                return Object(
                    f'(rand() % ({hi_num} - {low_num})) + {low_num}',
                    Type('int'), call_position
                )
            
            def char_int(codegen, call_position: Position, value: Object) -> Object:
                char = codegen.create_temp_var(value.type, call_position)
                i = f'({value})'
                codegen.prepend_code(f"""if ({i} < 0 || {i} > 127) {{
    {self.err('Character is not a valid ASCII character')}
}}

static char {char}[2];
{char}[0] = (char)({value});
{char}[1] = '\\0';
""")
                
                return Object(char, Type('string'), call_position)
            
            @c_dec(param_types=('string',), can_user_call=True, overloads={
                (('int',), 'string'): char_int
            }, add_to_class=self)
            def _get_char(codegen, call_position: Position, value: Object) -> Object:
                slen = self._string_length(codegen, call_position, value)
                codegen.prepend_code(f"""if ({slen} > 1) {{
    {self.err('String is not a single character')}
}}
""")
                
                return Object(f'((int)(({value})[0]))', Type('int'), call_position)
            
            def assert_err(codegen, call_position: Position, value: Object, string: Object) -> Object:
                if not codegen.is_string_literal(string):
                    call_position.error_here('Assert error message must be a string literal')
                
                codegen.prepend_code(f'if (!{value}) {{ {self.err(string.code[1:-1])} }}')
                return Object.NULL(call_position)
            
            @c_dec(param_types=('bool',), can_user_call=True, overloads={
                (('bool', 'string'), 'nil'): assert_err
            }, add_to_class=self)
            def _assert(codegen, call_position: Position, value: Object) -> Object:
                codegen.prepend_code(f'if (!{value}) {{ {self.err("Assertion failed")} }}')
                return Object.NULL(call_position)
    
    def include(self, file: str, codegen) -> None:
        """Add a C include to the compiled C code.

        Args:
            file (str): The file name.
            codegen (type): The codegen instance.
        """
        
        self.includes.add(file)
        codegen.add_toplevel_code(f'#include {file}')
    
    @staticmethod
    def is_object(name: str) -> bool:
        """Checks if a name is a C object.

        Args:
            name (str): Name to check.

        Returns:
            bool: If the name is an object.
        """
        
        return name.startswith('_') and not name.endswith('__')
    
    @staticmethod
    def get_all_objects(class_) -> dict:
        """Get all the objects of a class

        Args:
            class_ (type): The class to get all the attributes of.

        Returns:
            dict: The objects of the class.
        """
        
        return {
            k: getattr(class_, k)
            for k in dir(class_)
            if CManager.is_object(k)
        } | {
            k: v for k, v in class_.__dict__.items() if CManager.is_object(k)
        }
    
    def get_object(self, name: str):
        """Gets an object from the `CManager` class.

        Args:
            name (str): The name of the object.

        Returns:
            type | None: The object, returns None if there is no object named that.
        """
        
        return self.get_all_objects(self).get('_' + name)
    
    def add_objects(self, from_class, to_class) -> None:
        """Add objects from a class to a class.

        Args:
            from_class (type): From the class.
            to_class (type): To the class.
        """
        
        to_class.__dict__.update(self.get_all_objects(from_class))
    
    def add_func(self, name: str, func: Callable) -> None:
        """Add a Python function to this `CManager`.

        Args:
            name (str): The name of the function.
            func (Callable): The Python function callable.
        """
        
        self.__dict__['_' + name] = func
    
    def err(self, fmt: str, *variables: str) -> str:
        """Print an error message.

        Args:
            fmt (str): The formatted error message using the '%' symbol.
            *variables (str): The variables to insert into the formatted error message. *Must* be
            python strings

        Returns:
            str: The error C code.
        """
        
        vars_str = ', '.join(variables)
        return f"""printf("error: {fmt}\\n"{", " + vars_str if vars_str != "" else ""});
{self.codegen.get_end_code()}
exit(1);
"""
    
    def buf_check(self, buf_var: str) -> str:
        """Check if a buffer (allocated using `malloc` is NULL).

        Args:
            buf_var (str): The buffer variable.

        Returns:
            str: The code to check the buffer.
        """

        return f'if ({buf_var} == NULL) {{ {self.err("out of memory")} }}'
    
    def symbol_not_supported(self, symbol_name: str) -> str:
        """Raise a compile time error if the symbol name is not supported.

        Args:
            symbol_name (str): The symbol name.

        Returns:
            str: The compile time error code.
        """
        
        return f'#error "{symbol_name} not supported"'
    
    def fmt_length(self, codegen, pos: Position, fmt: str, *format_vars: str,
                   buf_var: str | None = None) -> tuple[str, Free]:
        """Get the code required to check the length of a formatted string in C and output it
to a buffer.

        Args:
            codegen (Curecodegen): The codegen instance.
            pos (Position): The position.
            fmt (str): The format string.
            *format_vars (tuple[str]): The variables to be formatted into the format string.
            buf_var (str): Define an already created buffer variable instead of creating a new one
        
        Returns:
            tuple[str, Free]: The string is the C code and the `Free` object is the buffer.
        """
        
        length = codegen.create_temp_var(Type('int'), pos)
        buf_free = Free()
        buf = codegen.create_temp_var(Type('string'), pos, name=buf_var, free=buf_free)
        return f"""int {length} = snprintf(
    NULL, 0,
    {fmt}{''.join(', ' + s for s in format_vars)}
);
string {buf} = (string)malloc({length} + 1);
{codegen.c_manager.buf_check(buf)}
snprintf({buf}, {length} + 1, {fmt}{''.join(', ' + s for s in format_vars)});
""", buf_free

    def array_from_c_array(self, codegen, pos: Position, type: Type,
                           value: str) -> tuple[str, str]:
        """Generate a Cure array from a C array.

        Args:
            codegen (Curecodegen): The codegen instance.
            pos (Position): The position.
            type (str): The type of the C array.
            value (str): The variable or object of the C array.

        Returns:
            tuple[str, str]: The code to convert the C array to a Cure array and the name of the
            created array.
        """
        
        from codegen.array_manager import DEFAULT_CAPACITY
        
        array_type = codegen.array_manager.define_array(type)
        
        arr = codegen.create_temp_var(array_type, pos)
        i = codegen.create_temp_var(Type('int'), pos)
        length = codegen.create_temp_var(Type('int'), pos)
        
        return f"""{array_type.c_type} {arr} = {{
    .length = 0, .capacity = {DEFAULT_CAPACITY},
    .elements = ({type.c_type}*)malloc(sizeof({type.c_type}) * {DEFAULT_CAPACITY})
}};
int {length} = sizeof({value}) / sizeof({type.c_type});
if ({length} > 0) {{
    for (int {i} = 0; {i} <= {length}; {i}++) {{
        if ({arr}.length == {arr}.capacity) {{
            {arr}.capacity *= 2;
            {arr}.elements = ({type.c_type}*)realloc(
                {arr}.elements, sizeof({type.c_type}) * {arr}.capacity
            );
        }}
        
        {arr}.elements[{i}] = {value}[{i}];
        {arr}.length++;
    }}
}}
""", arr
    
    @c_dec(param_types=('*',), can_user_call=True)
    def _print(self, codegen, call_position: Position, *args: Object) -> Object:
        fmt_vars = []
        for arg in args:
            repr_method = self.get_object(f'{arg.type.c_type}_to_string')
            if repr_method is None:
                call_position.error_here(f'String representation for \'{arg.type}\' is not defined')
            
            fmt_vars.append(repr_method(codegen, call_position, arg).code)
        
        fmt = ' '.join('%s' for _ in range(len(fmt_vars)))
        return Object(
            f'(printf("{fmt}\\n", {", ".join(fmt_vars)}))',
            Type('int'), call_position
        )
    
    @c_dec(param_types=('any',), can_user_call=True)
    def _type(self, codegen, call_position: Position, value: Object) -> Object:
        type_method = self.get_object(f'{value.type.c_type}_type')
        if type_method is None:
            call_position.error_here(f'Type representation for \'{value.type}\' is not defined')
        
        return Object(
            type_method(codegen, call_position).code,
            Type('string'), call_position
        )
    
    @c_dec(param_types=('any',), can_user_call=True)
    def _to_string(self, codegen, call_position: Position, value: Object) -> Object:
        repr_method = self.get_object(f'{value.type.c_type}_to_string')
        if repr_method is None:
            call_position.error_here(f'String representation for \'{value.type}\' is not defined')

        return Object(
            repr_method(codegen, call_position, value).code,
            Type('string'), call_position
        )
    
    def _input_no_prompt(self, codegen, call_position: Position) -> Object:
        return self._input(codegen, call_position, None)
    
    @c_dec(
        param_types=('string',),
        overloads={
            ((), 'string'): _input_no_prompt
        },
        can_user_call=True,
    )
    def _input(self, codegen, call_position: Position, prompt: Object | None) -> Object:
        if prompt is not None:
            codegen.prepend_code(f'printf("%s", {prompt});')
        
        buf_size = codegen.create_temp_var(Type('int'), call_position)
        buf_free = Free()
        buf = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
        length = codegen.create_temp_var(Type('int'), call_position)
        c = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""size_t {buf_size} = 128;
string {buf} = (string)malloc({buf_size} * sizeof(char));
{codegen.c_manager.buf_check(buf)}
size_t {length} = 0;
int {c};
while (({c} = getchar()) != '\\n' && {c} != EOF) {{
    if ({length} + 1 >= {buf_size}) {{
        {buf_size} *= 2;
        {buf} = (string)realloc({buf}, {buf_size} * sizeof(char));
        {codegen.c_manager.buf_check(buf)}
    }}
    
    {buf}[{length}++] = (char){c};
}}
{buf}[{length}] = '\\0';
""")
        
        return Object(buf, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('any',), can_user_call=True)
    def _to_bool(self, _, call_position: Position, value: Object) -> Object:
        bool_method = self.get_object(f'{value.type.c_type}_to_bool')
        if bool_method is None:
            call_position.error_here(f'Boolean conversion for \'{value.type}\' is not defined')

        return Object(
            bool_method(call_position).code,
            Type('bool'), call_position
        )
    
    @c_dec(param_types=('any',), can_user_call=True)
    def _sizeof(self, _, call_position: Position, object: Object) -> Object:
        return Object(f'sizeof({object})', Type('int'), call_position)
    
    @c_dec(param_types=('string',), can_user_call=True)
    def _insert_c_code(self, codegen, call_position: Position, code: Object) -> Object:
        if not codegen.is_string_literal(code):
            call_position.error_here('Inserting C code can only be done as a string literal')
        
        codegen.prepend_code(f'{code.code[1:-1]};')
        return Object.NULL(call_position)
    
    @c_dec(param_types=('any',), can_user_call=True)
    def _addr_of(self, codegen, call_position: Position, obj: Object) -> Object:
        if (ident := ID_REGEX.fullmatch(obj.code)) is not None:
            code, buf_free = self.fmt_length(
                codegen, call_position,
                '"%p"', f'&{ident.group()}'
            )
            
            codegen.prepend_code(code)
            return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
        else:
            call_position.error_here(f'Cannot get address of non-variable \'{obj.code}\'')
    
    
    @c_dec(is_method=True, is_static=True)
    def _int_type(self, _, call_position: Position) -> Object:
        return Object('"int"', Type('string'), call_position)
    
    @c_dec(is_method=True, is_static=True)
    def _float_type(self, _, call_position: Position) -> Object:
        return Object('"float"', Type('string'), call_position)
    
    @c_dec(is_method=True, is_static=True)
    def _string_type(self, _, call_position: Position) -> Object:
        return Object('"string"', Type('string'), call_position)
    
    @c_dec(is_method=True, is_static=True)
    def _bool_type(self, _, call_position: Position) -> Object:
        return Object('"bool"', Type('string'), call_position)
    
    @c_dec(is_method=True, is_static=True)
    def _nil_type(self, _, call_position: Position) -> Object:
        return Object('"nil"', Type('string'), call_position)
    
    @c_dec(is_method=True, is_static=True)
    def _Math_type(self, _, call_position: Position) -> Object:
        return Object('"Math"', Type('string'), call_position)
    
    @c_dec(is_method=True, is_static=True)
    def _System_type(self, _, call_position: Position) -> Object:
        return Object('"System"', Type('string'), call_position)
    
    @c_dec(is_method=True, is_static=True)
    def _Time_type(self, _, call_position: Position) -> Object:
        return Object('"Time"', Type('string'), call_position)
    
    @c_dec(is_method=True, is_static=True)
    def _Cure_type(self, _, call_position: Position) -> Object:
        return Object('"Cure"', Type('string'), call_position)
    
    @c_dec(param_types=('int',), is_method=True)
    def _int_to_string(self, codegen, call_position: Position, value: Object) -> Object:
        # integer to string length formula is: (int)((ceil(log10(num))+1)*sizeof(char))
        temp_var = codegen.create_temp_var(Type('string'), call_position)
        codegen.prepend_code(f"""static char {temp_var}[13];
snprintf({temp_var}, 13, "%d", ({value}));
""")
        return Object(temp_var, Type('string'), call_position)
    
    @c_dec(param_types=('float',), is_method=True)
    def _float_to_string(self, codegen, call_position: Position, value: Object) -> Object:
        temp_var = codegen.create_temp_var(Type('string'), call_position)
        codegen.prepend_code(f"""static char {temp_var}[47];
snprintf({temp_var}, 47, "%f", ({value}));
""")
        return Object(temp_var, Type('string'), call_position)
    
    @c_dec(param_types=('string',))
    def _string_to_string(self, _, _call_position: Position, value: Object) -> Object:
        return value
    
    @c_dec(param_types=('bool',), is_method=True)
    def _bool_to_string(self, _, call_position: Position, value: Object) -> Object:
        return Object(f'(({value}) ? "true" : "false")', Type('string'), call_position)
    
    @c_dec(param_types=('nil',), is_method=True)
    def _nil_to_string(self, _, call_position: Position, _value: Object) -> Object:
        return Object('"nil"', Type('string'), call_position)
    
    @c_dec(param_types=('Math',), is_method=True, is_static=True)
    def _Math_to_string(self, _, call_position: Position, _value: Object) -> Object:
        return Object('"class \'Math\'"', Type('string'), call_position)
    
    @c_dec(param_types=('System',), is_method=True, is_static=True)
    def _System_to_string(self, _, call_position: Position, _value: Object) -> Object:
        return Object('"class \'System\'"', Type('string'), call_position)
    
    @c_dec(param_types=('Time',), is_method=True)
    def _Time_to_string(self, codegen, call_position: Position, value: Object) -> Object:
        t = f'({value.code})'
        code, buf_free = self.fmt_length(
            codegen, call_position,
            '"Time(%s)"',
            f'asctime({t}.ti)'
        )
        
        codegen.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('Cure',), is_method=True, is_static=True)
    def _Cure_to_string(self, _, call_position: Position, _value: Object) -> Object:
        return Object('"class \'Cure\'"', Type('string'), call_position)
    
    @c_dec(param_types=('int',), is_method=True)
    def _int_to_float(self, _, call_position: Position, value: Object) -> Object:
        return Object(f'((float)({value.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('float',), is_method=True)
    def _float_to_int(self, _, call_position: Position, value: Object) -> Object:
        return Object(f'((int)({value.code}))', Type('int'), call_position)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_to_int(self, _, call_position: Position, value: Object) -> Object:
        # TODO: Raise error if string is not a valid integer and fix undefined behaviour
        # overflow and underflow integers
        return Object(f'(atoi({value.code}))', Type('int'), call_position)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_to_float(self, _, call_position: Position, value: Object) -> Object:
        # TODO: Raise error if string is not a valid float and fix undefined behaviour
        # overflow and underflow floats
        return Object(f'(atof({value.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_to_bool(self, _, call_position: Position, value: Object) -> Object:
        return Object(f'(({value.code}) == "true" ? 1 : 0)', Type('bool'), call_position)

    @c_dec(param_types=('bool',), is_method=True)
    def _bool_to_int(self, _, call_position: Position, value: Object) -> Object:
        return Object(f'(({value.code}) ? 1 : 0)', Type('int'), call_position)
    
    @c_dec(param_types=('bool',))
    def _bool_to_bool(self, _, _call_position: Position, value: Object) -> Object:
        return value
    
    @c_dec(param_types=('int', 'int'))
    def _int_add_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) + ({b.code}))', Type('int'), call_position)
    
    @c_dec(param_types=('int', 'float'))
    def _int_add_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'((float)({a.code}) + ({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('float', 'int'))
    def _float_add_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) + (float)({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('float', 'float'))
    def _float_add_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) + ({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('string', 'string'))
    def _string_add_string(self, codegen, call_position: Position, a: Object, b: Object) -> Object:
        self.include('<string.h>', codegen)
        
        temp_var = codegen.create_temp_var(Type('string'), call_position, free=Free())
        codegen.prepend_code(
            f"""string {temp_var} = (string)malloc(strlen({a.code}) + strlen({b.code}) + 1);
{codegen.c_manager.buf_check(temp_var)}
strcpy({temp_var}, {a.code});
strcat({temp_var}, {b.code});
""")
        
        return Object(temp_var, Type('string'), call_position, free=Free(temp_var))
    
    @c_dec(param_types=('int', 'int'))
    def _int_sub_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) - ({b.code}))', Type('int'), call_position)
    
    @c_dec(param_types=('int', 'float'))
    def _int_sub_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'((float)({a.code}) - ({b.code}))', Type('float'), call_position)

    @c_dec(param_types=('float', 'int'))
    def _float_sub_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) - (float)({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('float', 'float'))
    def _float_sub_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) - ({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('int', 'int'))
    def _int_mul_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) * ({b.code}))', Type('int'), call_position)
    
    @c_dec(param_types=('int', 'float'))
    def _int_mul_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'((float)({a.code}) * ({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('float', 'int'))
    def _float_mul_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) * (float)({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('float', 'float'))
    def _float_mul_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) * ({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('int', 'int'))
    def _int_div_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'((int)(({a.code}) / ({b.code})))', Type('int'), call_position)
    
    @c_dec(param_types=('int', 'float'))
    def _int_div_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'((float)({a.code}) / ({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('float', 'int'))
    def _float_div_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) / (float)({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('float', 'float'))
    def _float_div_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) / ({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('int', 'int'))
    def _int_mod_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) % ({b.code}))', Type('int'), call_position)

    @c_dec(param_types=('int', 'float'))
    def _int_mod_float(self, codegen, call_position: Position, a: Object, b: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'(fmodf((float)({a.code}), ({b.code})))', Type('float'), call_position)
    
    @c_dec(param_types=('float', 'int'))
    def _float_mod_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(fmodf(({a.code}), (float)({b.code})))', Type('float'), call_position)
    
    @c_dec(param_types=('float', 'float'))
    def _float_mod_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(fmodf(({a.code}), ({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('int', 'string'))
    def _int_mod_string(self, codegen, call_position: Position, a: Object, b: Object) -> Object:
        length = f'({a.code})'
        res_free = Free()
        res = codegen.create_temp_var(Type('string'), call_position, free=res_free)
        current_length = codegen.create_temp_var(Type('int'), call_position)
        i = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""int {current_length} = {
    self._string_length(codegen, call_position, b).code
};
string {res} = (string)malloc({length} + 1);
{codegen.c_manager.buf_check(res)}
if ({length} > 0) {{
    if ({current_length} < {length}) {{
        free({res});
        {codegen.c_manager.err('Invalid string length')}
    }}
    
    for (size_t {i} = 0; {i} < {length}; {i}++) {{
        {res}[{i}] = {b.code}[{i}];
    }}

    {res}[{length}] = '\\0';
}} else {{
    free({res});
    {codegen.c_manager.err('Invalid string length')}
}}
""")
        
        return Object(res, Type('string'), call_position, free=res_free)
    
    @c_dec(param_types=('string', 'int'))
    def _string_mod_int(self, codegen, call_position: Position,
                        a: Object, b: Object) -> Object:
        length = f'({b.code})'
        res_free = Free()
        res = codegen.create_temp_var(Type('string'), call_position, free=res_free)
        current_length = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""int {current_length} = {
    self._string_length(codegen, call_position, a).code
};
string {res} = (string)malloc({length} + 1);
{codegen.c_manager.buf_check(res)}
if ({length} > 0) {{
    if ({current_length} < {length}) {{
        {codegen.c_manager.err('Invalid string length')}
    }}

    strncpy({res}, ({a.code}) + ({current_length} - {length}), {length});
    {codegen.c_manager.buf_check(res)}
    {res}[{length}] = '\\0';
}} else {{
    free({res});
    {codegen.c_manager.err('Invalid string length')}
}}""")
        
        return Object(res, Type('string'), call_position, free=res_free)
    
    @c_dec(param_types=('int', 'int'))
    def _int_eq_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) == ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('float', 'float'))
    def _float_eq_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) == ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('string', 'string'))
    def _string_eq_string(self, codegen, call_position: Position, a: Object, b: Object) -> Object:
        self.include('<string.h>', codegen)
        return Object(f'((strcmp({a.code}, {b.code}) == 0))', Type('bool'), call_position)
    
    @c_dec(param_types=('bool', 'bool'))
    def _bool_eq_bool(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) == ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('int', 'int'))
    def _int_neq_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) != ({b.code}))', Type('bool'), call_position)

    @c_dec(param_types=('float', 'float'))
    def _float_neq_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) != ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('string', 'string'))
    def _string_neq_string(self, codegen, call_position: Position, a: Object, b: Object) -> Object:
        self.include('<string.h>', codegen)
        return Object(f'((strcmp({a.code}, {b.code}) != 0))', Type('bool'), call_position)
    
    @c_dec(param_types=('bool', 'bool'))
    def _bool_neq_bool(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) != ({b.code}))', Type('bool'), call_position)

    @c_dec(param_types=('int', 'int'))
    def _int_gt_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) > ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('float', 'float'))
    def _float_gt_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) > ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('string', 'string'))
    def _string_gt_string(self, codegen, call_position: Position, a: Object, b: Object) -> Object:
        alen = self._string_length(codegen, call_position, a)
        blen = self._string_length(codegen, call_position, b)
        return Object(f'({alen.code} > {blen.code})', Type('bool'), call_position)
    
    @c_dec(param_types=('int', 'int'))
    def _int_gte_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) >= ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('float', 'float'))
    def _float_gte_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) >= ({b.code}))', Type('bool'), call_position)

    @c_dec(param_types=('string', 'string'))
    def _string_gte_string(self, codegen, call_position: Position, a: Object, b: Object) -> Object:
        alen = self._string_length(codegen, call_position, a)
        blen = self._string_length(codegen, call_position, b)
        return Object(f'({alen.code} >= {blen.code})', Type('bool'), call_position)
    
    @c_dec(param_types=('int', 'int'))
    def _int_lt_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) < ({b.code}))', Type('bool'), call_position)

    @c_dec(param_types=('float', 'float'))
    def _float_lt_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) < ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('string', 'string'))
    def _string_lt_string(self, codegen, call_position: Position, a: Object, b: Object) -> Object:
        alen = self._string_length(codegen, call_position, a)
        blen = self._string_length(codegen, call_position, b)
        return Object(f'({alen.code} < {blen.code})', Type('bool'), call_position)
    
    @c_dec(param_types=('int', 'int'))
    def _int_lte_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) <= ({b.code}))', Type('bool'), call_position)

    @c_dec(param_types=('float', 'float'))
    def _float_lte_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) <= ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('string', 'string'))
    def _string_lte_string(self, codegen, call_position: Position, a: Object, b: Object) -> Object:
        alen = self._string_length(codegen, call_position, a)
        blen = self._string_length(codegen, call_position, b)
        return Object(f'({alen.code} <= {blen.code})', Type('bool'), call_position)
    
    @c_dec(param_types=('bool', 'bool'))
    def _bool_and_bool(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) && ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('bool', 'bool'))
    def _bool_or_bool(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) || ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('bool',))
    def _not_bool(self, _, call_position: Position, a: Object) -> Object:
        return Object(f'(!({a}))', Type('bool'), call_position)
    
    @c_dec(param_types=('int',))
    def _sub_int(self, _, call_position: Position, a: Object) -> Object:
        return Object(f'(-({a.code}))', Type('int'), call_position)
    
    @c_dec(param_types=('int',))
    def _add_int(self, _, call_position: Position, a: Object) -> Object:
        return Object(f'(+({a.code}))', Type('int'), call_position)
    
    @c_dec(param_types=('float',))
    def _sub_float(self, _, call_position: Position, a: Object) -> Object:
        return Object(f'(-({a.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('float',))
    def _add_float(self, _, call_position: Position, a: Object) -> Object:
        return Object(f'(+({a.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('int',), is_property=True)
    def _int_humanize_size(self, codegen, call_position: Position, i: Object) -> Object:
        mag = codegen.create_temp_var(Type('int'), call_position)
        x = codegen.create_temp_var(Type('int'), call_position)
        abs_call = codegen.call('Math_abs', [
            Arg(Object(x, Type('int'), call_position))
        ], call_position)
        
        if 'sizeNames' not in self.RESERVED_NAMES:
            codegen.add_toplevel_code("""const string sizeNames[] = {{
    "B", "KB", "MB", "GB", "TB", "PB"
}};
""")
            self.RESERVED_NAMES.append('sizeNames')

        code, buf_free = self.fmt_length(codegen, call_position, '"%.4f%s"', x, f'sizeNames[{mag}]')
        codegen.prepend_code(f"""int {mag} = 0;
double {x} = (double){i.code};
while ({abs_call.code} >= 1024 && {mag} < (sizeof(sizeNames) / sizeof(sizeNames[0])) - 1) {{
    {x} /= 1024;
    {mag}++;
}}

{code}
""")
        
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('int',), is_method=True, overloads={
        (('int', 'int'), 'string'): None
    })
    def _int_science(self, codegen, call_position: Position,
                        i: Object, precision: Object | None = None) -> Object:
        self.include('<math.h>', codegen)
        
        if precision is None:
            precision = Object('5', Type('int'), call_position)
        
        exponent = codegen.create_temp_var(Type('int'), call_position)
        length = codegen.create_temp_var(Type('int'), call_position)
        num = codegen.create_temp_var(Type('float'), call_position)
        significand = codegen.create_temp_var(Type('float'), call_position)
        code, buf_free = self.fmt_length(
            codegen, call_position, '"%.*fe%+03d"',
            f'{precision.code}', significand, exponent
        )
        
        codegen.prepend_code(f"""int {exponent};
int {length};
double {num} = (double){i.code};
{exponent} = (int)floor(log10(fabs({num})));
double {significand} = {num} / pow(10.0, {exponent});
{code}
""")
        
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('float',), is_property=True)
    def _float_humanize_size(self, codegen, call_position: Position, f: Object) -> Object:
        return self._int_humanize_size(codegen, call_position, f)
    
    @c_dec(param_types=('float',), is_method=True, overloads={
        (('float', 'int'), 'string'): None
    })
    def _float_science(self, codegen, call_position: Position,
                          f: Object, precision: Object | None = None) -> Object:
        return self._int_science(codegen, call_position, f, precision)
    
    @c_dec(param_types=('string',), is_property=True)
    def _string_length(self, codegen, call_position: Position, string: Object) -> Object:
        self.include('<string.h>', codegen)
        return Object(f'((int)strlen({string.code}))', Type('int'), call_position)
    
    @c_dec(param_types=('string',), is_property=True)
    def _string_is_empty(self, codegen, call_position: Position, string: Object) -> Object:
        strlen = self._string_length(codegen, call_position, string)
        return Object(f'({strlen.code} == 0)', Type('bool'), call_position)
    
    @c_dec(param_types=('string',), is_property=True)
    def _string_is_char(self, codegen, call_position: Position, string: Object) -> Object:
        strlen = self._string_length(codegen, call_position, string)
        return Object(f'({strlen.code} == 1)', Type('bool'), call_position)
    
    @c_dec(param_types=('string',), is_property=True)
    def _string_is_digit(self, codegen, call_position: Position, string: Object) -> Object:
        self.include('<string.h>', codegen)
        self.include('<ctype.h>', codegen)
        
        i = codegen.create_temp_var(Type('int'), call_position)
        res = codegen.create_temp_var(Type('bool'), call_position)
        slen = self._string_length(codegen, call_position, string)
        codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {slen.code}; {i}++) {{
    if (!isdigit(({string.code})[{i}])) {res} = false;
}}
""")
        
        return Object(res, Type('bool'), call_position)
    
    @c_dec(param_types=('string',), is_property=True)
    def _string_is_lower(self, codegen, call_position: Position, string: Object) -> Object:
        self.include('<string.h>', codegen)
        self.include('<ctype.h>', codegen)
        
        i = codegen.create_temp_var(Type('int'), call_position)
        res = codegen.create_temp_var(Type('bool'), call_position)
        slen = self._string_length(codegen, call_position, string)
        codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {slen.code}; {i}++) {{
    if (!islower(({string.code})[{i}])) {res} = false;
}}
""")
        
        return Object(res, Type('bool'), call_position)
    
    @c_dec(param_types=('string',), is_property=True)
    def _string_is_upper(self, codegen, call_position: Position, string: Object) -> Object:
        self.include('<string.h>', codegen)
        self.include('<ctype.h>', codegen)

        i = codegen.create_temp_var(Type('int'), call_position)
        res = codegen.create_temp_var(Type('bool'), call_position)
        slen = self._string_length(codegen, call_position, string)
        codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {slen.code}; {i}++) {{
    if (!isupper(({string.code})[{i}])) {res} = false;
}}
""")
        
        return Object(res, Type('bool'), call_position)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_lower(self, codegen, call_position: Position, string: Object) -> Object:
        self.include('<string.h>', codegen)
        self.include('<ctype.h>', codegen)
        
        strlen = self._string_length(codegen, call_position, string)
        
        temp_free = Free()
        temp_var = codegen.create_temp_var(Type('string'), call_position, free=temp_free)
        i = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""string {temp_var} = (string)malloc({strlen.code} + 1);
{codegen.c_manager.buf_check(temp_var)}
for (size_t {i} = 0; {i} < {strlen.code}; {i}++)
    {temp_var}[{i}] = tolower({string.code}[{i}]);
{temp_var}[{strlen.code}] = '\\0';
""")
        
        return Object(temp_var, Type('string'), call_position, free=temp_free)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_upper(self, codegen, call_position: Position, string: Object) -> Object:
        self.include('<string.h>', codegen)
        self.include('<ctype.h>', codegen)

        strlen = self._string_length(codegen, call_position, string)

        temp_free = Free()
        temp_var = codegen.create_temp_var(Type('string'), call_position, free=temp_free)
        i = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""string {temp_var} = (string)malloc({strlen.code} + 1);
{codegen.c_manager.buf_check(temp_var)}
for (size_t {i} = 0; {i} < {strlen.code}; {i}++)
    {temp_var}[{i}] = toupper({string.code}[{i}]);
{temp_var}[{strlen.code}] = '\\0';
""")

        return Object(temp_var, Type('string'), call_position, free=temp_free)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_title(self, codegen, call_position: Position, string: Object) -> Object:
        self.include('<string.h>', codegen)
        self.include('<ctype.h>', codegen)
        
        temp_free = Free()
        temp_var = codegen.create_temp_var(Type('string'), call_position, free=temp_free)
        lv = codegen.create_temp_var(Type('string'), call_position)
        codegen.prepend_code(f"""string {temp_var} = strdup({string.code});
{codegen.c_manager.buf_check(temp_var)}
for (string {lv} = {temp_var}; *{lv} != '\\0'; ++{lv})
    *{lv} = ({lv} == {temp_var} || *({lv} - 1) == ' ') ? toupper(*{lv}) : tolower(*{lv});
""")
        
        return Object(temp_var, Type('string'), call_position, free=temp_free)
    
    @c_dec(param_types=('string', 'string'), is_method=True)
    def _string_startswith(self, codegen, call_position: Position,
                           string: Object, prefix: Object) -> Object:
        self.include('<string.h>', codegen)

        prefix_len = self._string_length(codegen, call_position, prefix)
        return Object(
            f'(strncmp({string.code}, {prefix.code}, {prefix_len.code}) == 0)',
            Type('bool'), call_position
        )
    
    @c_dec(param_types=('string', 'string'), is_method=True)
    def _string_endswith(self, codegen, call_position: Position,
                         string: Object, suffix: Object) -> Object:
        self.include('<string.h>', codegen)
        
        s = string.code
        su = suffix.code
        strlen = self._string_length(codegen, call_position, string)
        slen = codegen.create_temp_var(Type('int'), call_position)
        suffix_len = self._string_length(codegen, call_position, suffix)
        sulen = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""size_t {slen} = {strlen.code};
size_t {sulen} = {suffix_len.code};
""")
        return Object(
            f"""({slen} < {sulen} ? false : (strncmp(
                ({s}) + {slen} - {sulen}, {su}, {sulen}) == 0)
            )""",
            Type('bool'), call_position
        )
    
    @c_dec(param_types=('string', 'int'), is_method=True)
    def _string_at(self, codegen, call_position: Position,
                   string: Object, index: Object) -> Object:
        self.include('<string.h>', codegen)
        
        strlen = self._string_length(codegen, call_position, string)
        temp_var = codegen.create_temp_var(Type('string'), call_position)
        codegen.prepend_code(f"""if (({index.code}) > {strlen.code} - 1) {{
    {self.err('Index out of bounds on string')}
}}
static char {temp_var}[2];
{temp_var}[0] = ({string.code})[{index.code}];
{temp_var}[1] = '\\0';
""")
        
        return Object(temp_var, Type('string'), call_position)
    
    @c_dec(param_types=('string', 'string'), is_method=True)
    def _string_has(self, codegen, call_position: Position,
                   string: Object, substring: Object) -> Object:
        self.include('<string.h>', codegen)
        return Object(
            f'(strstr({string.code}, {substring.code}) != NULL)',
            Type('bool'), call_position
        )
    
    @c_dec(param_types=('string', 'string_array'), is_method=True)
    def _string_join(self, codegen, call_position: Position,
                     string: Object, arr: Object) -> Object:
        self.include('<string.h>', codegen)
        
        tlen = codegen.create_temp_var(Type('int'), call_position)
        sep_len = codegen.create_temp_var(Type('int'), call_position)
        res_free = Free()
        res = codegen.create_temp_var(Type('string'), call_position, free=res_free)
        count = codegen.create_temp_var(Type('int'), call_position)
        i = codegen.create_temp_var(Type('int'), call_position)
        a = f'({arr.code})'
        codegen.prepend_code(f"""size_t {tlen} = 0;
size_t {sep_len} = {self._string_length(codegen, call_position, string).code};
int {count} = 0;
for (int {i} = 0; {i} < {a}.length; {i}++) {{
    {tlen} += {self._string_length(
    codegen, call_position, Object(f'{a}.elements[{i}]', Type('string'), call_position)
).code};
    if ({i} > 0) {{
        {tlen} += {sep_len};
    }}
    {count}++;
}}

string {res} = (string)malloc({tlen} + 1);
{codegen.c_manager.buf_check(res)}
{res}[0] = '\\0';
for (int {i} = 0; {i} < {a}.length; {i}++) {{
    if ({i} > 0) {{
        strcat({res}, {string.code});
    }}
    strcat({res}, {a}.elements[{i}]);
}}
""")
        
        return Object(res, Type('string'), call_position, free=res_free)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_parse_int(self, codegen, call_position: Position, string: Object) -> Object:
        return self._string_to_int(codegen, call_position, string)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_parse_float(self, codegen, call_position: Position, string: Object) -> Object:
        return self._string_to_float(codegen, call_position, string)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_parse_bool(self, codegen, call_position: Position, string: Object) -> Object:
        return self._string_to_bool(codegen, call_position, string)
    
    @c_dec(param_types=('string', 'string'), is_method=True)
    def _string_find(self, codegen, call_position: Position,
                     string: Object, substring: Object) -> Object:
        self.include('<string.h>', codegen)
        idx = codegen.create_temp_var(Type('int'), call_position)
        i = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""int {idx} = -1;
for (size_t {i} = 0; {i} < {self._string_length(codegen, call_position, string).code}; {i}++) {{
    if (strncmp(
        {string.code} + {i},
        {substring.code},
        {self._string_length(codegen, call_position, substring).code}
    ) == 0) {{
        {idx} = {i};
        break;
    }}
}}
""")
        
        return Object(idx, Type('int'), call_position)
    
    @c_dec(param_types=('string', 'int', 'int'), is_method=True)
    def _string_slice(self, codegen, call_position: Position,
                      string: Object, start: Object, end: Object) -> Object:
        self.include('<string.h>', codegen)
        buf_free = Free()
        buf = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
        start_var = codegen.create_temp_var(Type('int'), call_position)
        end_var = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""string {buf} = NULL;
int {start_var} = {start.code};
int {end_var} = {end.code};
if ({start_var} < 0 || {end_var} < 0) {{
    {self.err('Index out of bounds on string slice')}
}} else if ({start_var} > {end_var}) {{
    {self.err('Start index must be less than end index')}
}}

{buf} = (string)malloc({end_var} - {start_var} + 1);
{self.buf_check(buf)}
strncpy({buf}, ({string.code}) + {start_var}, {end_var} - {start_var} + 1);
{buf}[{end_var} - {start_var} + 1] = '\\0';
""")
        
        return Object(buf, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('string', '*'), is_method=True)
    def _string_format(self, codegen, call_position: Position, string: Object,
                       *args: Object) -> Object:
        code, buf_free = self.fmt_length(
            codegen, call_position, string.code,
            *[arg.code for arg in args]
        )
        
        codegen.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('string', 'int'), return_type=Type('string'))
    def _iter_string(self, codegen, call_position: Position, string: Object, i: Object) -> Object:
        self.include('<string.h>', codegen)
        return self._string_at(codegen, call_position, string, i)
    
    @c_dec(param_types=('string', 'int'))
    def _index_string(self, codegen, call_position: Position, string: Object, i: Object) -> Object:
        self.include('<string.h>', codegen)
        return self._string_at(codegen, call_position, string, i)
    
    
    @c_dec(is_property=True, is_static=True)
    def _Math_pi(self, _, call_position: Position) -> Object:
        return Object('3.14159265358979323846f', Type('float'), call_position)
    
    @c_dec(is_property=True, is_static=True)
    def _Math_e(self, _, call_position: Position) -> Object:
        return Object('2.7182818284590452354f', Type('float'), call_position)
    
    @c_dec(is_property=True, is_static=True)
    def _Math_tau(self, _, call_position: Position) -> Object:
        return Object('6.28318530717958647692f', Type('float'), call_position)
    
    @c_dec(is_property=True, is_static=True)
    def _Math_phi(self, _, call_position: Position) -> Object:
        return Object('1.61803398874989484820f', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_sin(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)sinf({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_cos(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)cosf({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_tan(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)tanf({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_asin(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)asinf({x.code}))', Type('float'), call_position)

    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_acos(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)acosf({x.code}))', Type('float'), call_position)

    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_atan(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)atanf({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float', 'float'),
        is_method=True,
        is_static=True,
        overloads={
            (('int', 'int'), 'float'): None,
            (('int', 'float'), 'float'): None,
            (('float', 'int'), 'float'): None
        }
    )
    def _Math_atan2(self, codegen, call_position: Position, y: Object, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)atan2f({y.code}, {x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_sqrt(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)sqrtf({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float', 'float'),
        is_method=True,
        is_static=True,
        overloads={
            (('int', 'int'), 'float'): None,
            (('int', 'float'), 'float'): None,
            (('float', 'int'), 'float'): None
        }
    )
    def _Math_nth_root(self, codegen, call_position: Position, x: Object, n: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)powf({x.code}, 1.0f / ({n.code})))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float', 'float'),
        is_method=True,
        is_static=True,
        overloads={
            (('int', 'int'), 'float'): None,
            (('int', 'float'), 'float'): None,
            (('float', 'int'), 'float'): None
        }
    )
    def _Math_pow(self, codegen, call_position: Position, x: Object, y: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)powf({x.code}, {y.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_log(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)logf({x.code}))', Type('float'), call_position)

    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_log10(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)log10f({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_log2(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)log2f({x.code}))', Type('float'), call_position)

    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_exp(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)expf({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True
    )
    def _Math_ceil(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)ceilf({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True
    )
    def _Math_floor(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)floorf({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True
    )
    def _Math_round(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)roundf({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float', 'float'),
        is_method=True,
        is_static=True,
        overloads={
            (('int', 'int'), 'int'): None,
            (('int', 'float'), 'float'): None,
            (('float', 'int'), 'float'): None
        }
    )
    def _Math_min(self, codegen, call_position: Position, x: Object, y: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(
            f'(({x.code}) < ({y.code}) ? ({x.code}) : ({y.code}))',
            Type('int') if x.type == Type('int') and y.type == Type('int') else Type('float'),
            call_position
        )
    
    @c_dec(
        param_types=('float', 'float'),
        is_method=True, is_static=True,
        overloads={
            (('int', 'int'), 'int'): None,
            (('int', 'float'), 'float'): None,
            (('float', 'int'), 'float'): None
        }
    )
    def _Math_max(self, codegen, call_position: Position, x: Object, y: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(
            f'(({x.code}) < ({y.code}) ? ({y.code}) : ({x.code}))',
            Type('int') if x.type == Type('int') and y.type == Type('int') else Type('float'),
            call_position
        )
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_rad(self, codegen, call_position: Position, deg: Object) -> Object:
        self.include('<math.h>', codegen)
        pi = self._Math_pi(codegen, call_position)
        return Object(f'((float)({deg.code}) * {pi.code} / 180.0f)', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_deg(self, codegen, call_position: Position, rad: Object) -> Object:
        self.include('<math.h>', codegen)
        pi = self._Math_pi(codegen, call_position)
        return Object(f'((float)({rad.code}) * 180.0f / {pi.code})', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_sinh(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)sinh({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_cosh(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)cosh({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_tanh(self, codegen, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', codegen)
        return Object(f'((float)tanh({x.code}))', Type('float'), call_position)
    
    # TODO: add more https://en.cppreference.com/w/c/numeric/math
    
    
    @c_dec(is_property=True, is_static=True)
    def _System_pid(self, codegen, call_position: Position) -> Object:
        pid_var = codegen.create_temp_var(Type('int'), call_position)
        codegen.prepend_code(f"""#ifdef OS_WINDOWS
int {pid_var} = (int)GetCurrentProcessId();
#else
int {pid_var} = (int)getpid();
#endif
""")
        
        return Object(pid_var, Type('int'), call_position)
    
    @c_dec(is_property=True, is_static=True)
    def _System_os(self, _, call_position: Position) -> Object:
        return Object('OS', Type('string'), call_position)
    
    @c_dec(is_property=True, is_static=True)
    def _System_arch(self, _, call_position: Position) -> Object:
        return Object('ARCH', Type('string'), call_position)
    
    @c_dec(is_property=True, is_static=True)
    def _System_running_with_admin(self, _, call_position: Position) -> Object:
        return Object('((bool)IS_ADMIN)', Type('bool'), call_position)
    
    @c_dec(is_property=True, is_static=True)
    def _System_processor_count(self, codegen, call_position: Position) -> Object:
        sysinfo = codegen.create_temp_var(Type('SystemInfo'), call_position)
        codegen.prepend_code(f"""#ifdef OS_WINDOWS
SYSTEM_INFO {sysinfo};
GetSystemInfo(&{sysinfo});
#else
{self.symbol_not_supported('System.processor_count')}
#endif
""")
        
        return Object(f'((int){sysinfo}.dwNumberOfProcessors)', Type('int'), call_position)
    
    @c_dec(is_property=True, is_static=True)
    def _System_cwd(self, codegen, call_position: Position) -> Object:
        cwd_var = codegen.create_temp_var(Type('string'), call_position)
        codegen.prepend_code(f"""char {cwd_var}[1024];
if (getcwd({cwd_var}, sizeof({cwd_var})) == NULL) {{
    {self.err('Failed to get current working directory')}
}}
""")
        
        return Object(cwd_var, Type('string'), call_position)
    
    @c_dec(is_property=True, is_static=True)
    def _System_time(self, codegen, call_position: Position) -> Object:
        t = codegen.create_temp_var(Type('time_t'), call_position)
        codegen.prepend_code(f'time_t {t} = time(NULL);')
        return Object(f'(Time){{ .t = {t}, .ti = localtime(&{t}) }}', Type('Time'), call_position)
    
    @c_dec(param_types=('int',), is_method=True, is_static=True)
    def _System_sleep(self, codegen, call_position: Position, milliseconds: Object) -> Object:
        codegen.prepend_code(f"""#ifdef OS_WINDOWS
Sleep({milliseconds.code});
#elif defined(OS_LINUX) | defined(OS_MACOS)
usleep({milliseconds.code} * 1000);
#else
{self.symbol_not_supported('System.sleep')}
#endif
""")
        return Object.NULL(call_position)
    
    @c_dec(param_types=('function',), is_method=True, is_static=True)
    def _System_atexit(self, codegen, call_position: Position, func: Object) -> Object:
        void_func = codegen.get_unique_name()
        codegen.scope.env[void_func] = EnvItem(void_func, Type('nil'), call_position,
                                                reserved=True)
        
        func_obj = codegen.scope.env[func.code]
        if func_obj.func.returns != Type('nil'):
            call_position.error_here(
                f'\'{func.code}\' set as an atexit function but does not return nil'
            )
        elif func_obj.func.params != []:
            call_position.error_here(
                f'\'{func.code}\' set as an atexit function but has parameters'
            )
        
        codegen.add_toplevel_code(f"""nil {func.code}();
void {void_func}() {{ {func.code}(); }}
""")
        codegen.prepend_code(f'atexit({void_func});')
        return Object.NULL(call_position)
    
    @c_dec(param_types=('string',), is_method=True, is_static=True)
    def _System_shell(self, _, call_position: Position, command: Object) -> Object:
        return Object(f'((bool)system({command.code}))', Type('bool'), call_position)
    
    @c_dec(is_method=True, is_static=True)
    def _System_block_keyboard(self, codegen, call_position: Position) -> Object:
        codegen.prepend_code(f"""#ifdef OS_WINDOWS
if (!IS_ADMIN) {{
    {self.err('Blocking keyboard requires administrator permissions')}
}}
BlockInput(TRUE);
#else
{self.symbol_not_supported('System.block_keyboard')}
#endif
""")
        
        return Object.NULL(call_position)
    
    @c_dec(is_method=True, is_static=True)
    def _System_unblock_keyboard(self, codegen, call_position: Position) -> Object:
        codegen.prepend_code(f"""#ifdef OS_WINDOWS
if (!IS_ADMIN) {{
    {self.err('Unblocking keyboard requires administrator permissions')}
}}
BlockInput(FALSE);
#else
{self.symbol_not_supported('System.unblock_keyboard')}
#endif
""")
        
        return Object.NULL(call_position)
    
    @c_dec(param_types=('string',), is_method=True, is_static=True)
    def _System_is_key_pressed(self, codegen, call_position: Position, char: Object) -> Object:
        is_pressed = codegen.create_temp_var(Type('bool'), call_position)
        codegen.prepend_code(f"""if (!{self._string_is_char(codegen, call_position, char).code}) {{
    {self.err('Key must be a single character')}
}}

#ifdef OS_WINDOWS
bool {is_pressed} = (bool)(GetAsyncKeyState((int)({char.code})[0] & 0x8000));
#else
{self.symbol_not_supported('System.is_key_pressed')}
#endif
""")
        
        return Object(is_pressed, Type('bool'), call_position)


    @c_dec(param_types=('Time',), is_property=True)
    def _Time_second(self, _, call_position: Position, time: Object) -> Object:
        return Object(f'({time.code}.ti->tm_sec)', Type('int'), call_position)
    
    @c_dec(param_types=('Time',), is_property=True)
    def _Time_minute(self, _, call_position: Position, time: Object) -> Object:
        return Object(f'({time.code}.ti->tm_min)', Type('int'), call_position)
    
    @c_dec(param_types=('Time',), is_property=True)
    def _Time_hour(self, _, call_position: Position, time: Object) -> Object:
        return Object(f'({time.code}.ti->tm_hour)', Type('int'), call_position)
    
    @c_dec(param_types=('Time',), is_property=True)
    def _Time_day(self, _, call_position: Position, time: Object) -> Object:
        return Object(f'({time.code}.ti->tm_mday)', Type('int'), call_position)
    
    @c_dec(param_types=('Time',), is_property=True)
    def _Time_month(self, _, call_position: Position, time: Object) -> Object:
        return Object(f'({time.code}.ti->tm_mon)', Type('int'), call_position)
    
    @c_dec(param_types=('Time',), is_property=True)
    def _Time_year(self, _, call_position: Position, time: Object) -> Object:
        return Object(f'({time.code}.ti->tm_year + 1900)', Type('int'), call_position)
    
    @c_dec(param_types=('Time',), is_property=True)
    def _Time_weekday(self, _, call_position: Position, time: Object) -> Object:
        return Object(f'({time.code}.ti->tm_wday)', Type('int'), call_position)
    
    @c_dec(param_types=('Time',), is_property=True)
    def _Time_yearday(self, _, call_position: Position, time: Object) -> Object:
        return Object(f'({time.code}.ti->tm_yday)', Type('int'), call_position)
    
    @c_dec(param_types=('Time',), is_property=True)
    def _Time_isdst(self, _, call_position: Position, time: Object) -> Object:
        return Object(f'({time.code}.ti->tm_isdst)', Type('int'), call_position)
    
    
    @c_dec(is_property=True, is_static=True)
    def _Cure_version(self, _, call_position: Position) -> Object:
        return Object('(VERSION)', Type('string'), call_position)
    
    @c_dec(param_types=('string',), is_method=True, is_static=True)
    def _Cure_compile(self, codegen, call_position: Position, src: Object) -> Object:
        from codegen import str_to_c
        if not codegen.is_string_literal(src.code):
            call_position.error_here('Source code must be a string literal')
        
        _, code = str_to_c(src.code[1:-1], codegen.scope)
        codegen.prepend_code(code)
        return Object.NULL(call_position)
    
    
    @staticmethod
    @func_modification(param_types=('string',))
    def _Warn(codegen, _func_obj, call_position: Position, _args: list[Object],
              mod_args: list[Object]) -> None:
        msg = mod_args[0].code
        if not codegen.is_string_literal(msg):
            call_position.error_here('Warning message must be a string literal')
        
        call_position.warn_here(msg[1:-1])
    
    @staticmethod
    @func_modification(param_types=('string',))
    def _Info(codegen, _func_obj, call_position: Position, _args: list[Object],
              mod_args: list[Object]) -> None:
        msg = mod_args[0].code
        if not codegen.is_string_literal(msg):
            call_position.error_here('Info message must be a string literal')

        call_position.info_here(msg[1:-1])

    @staticmethod
    @func_modification(param_types=('string',))
    def _Error(codegen, _func_obj, call_position: Position, _args: list[Object],
               mod_args: list[Object]) -> None:
        msg = mod_args[0].code
        if not codegen.is_string_literal(msg):
            call_position.error_here('Error message must be a string literal')
        
        call_position.error_here(msg[1:-1])
    
    @staticmethod
    @func_modification()
    def _Benchmark(codegen, func_obj: Function, call_position: Position, _args: list[Object],
                   _mod_args: list[Object]) -> None:
        begin = codegen.create_temp_var(Type('int', 'clock_t'), call_position)
        end = codegen.create_temp_var(Type('int', 'clock_t'), call_position)
        codegen.prepend_code(f'clock_t {begin} = clock();\n')
        codegen.append_code(f"""clock_t {end} = clock();
printf("Time spent to execute '{func_obj.name}': %.3f", ({end} - {begin}) / CLOCKS_PER_SEC);
""")
