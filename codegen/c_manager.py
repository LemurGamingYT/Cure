from typing import Callable, Any
from functools import wraps
from pathlib import Path

from codegen.objects import Object, Position, EnvItem, Free, Type, ID_REGEX, Function


HEADER = (Path(__file__).parent / 'include/header.h').absolute().as_posix()


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
        def wrapper(compiler, func_obj, call_position: Position, args: tuple[Object],
                    mod_args: tuple[Object]):
            return func(compiler, func_obj, call_position, args, mod_args)
        
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
    # reserved names all from standard library headers https://en.cppreference.com/w/c/header
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
        'memmove', 'memmove_s', 'memccpy', 'strerror', 'strerror_s', 'strerrorlen_s'
    ]
    
    def __init__(self, compiler) -> None:
        self.compiler = compiler
        self.includes = set()
        
        if not getattr(compiler, '_initialised_CManager', False):
            self.include(f'"{HEADER}"', compiler)
            self.include('<stdbool.h>', compiler)
            self.include('<stdlib.h>', compiler)
            self.include('<stdio.h>', compiler)
            self.include('<time.h>', compiler)
            self.includes.add('<windows.h>')
            self.includes.add('<io.h>')
            self.includes.add('<unistd.h>')
            
            POS_ZERO = Position(0, 0, '')
            
            compiler.scope.env['Math'] = EnvItem('Math', Type('Math'), POS_ZERO)
            compiler.scope.env['System'] = EnvItem('System', Type('System'), POS_ZERO)
            compiler.scope.env['Time'] = EnvItem('Time', Type('Time'), POS_ZERO)
            compiler.scope.env['MIN_INT'] = EnvItem('MIN_INT', Type('int'), POS_ZERO)
            compiler.scope.env['MAX_INT'] = EnvItem('MAX_INT', Type('int'), POS_ZERO)
            compiler.scope.env['DIGITS'] = EnvItem('DIGITS', Type('string'), POS_ZERO)
            compiler.scope.env['PUNCTUATION'] = EnvItem('PUNCTUATION', Type('string'), POS_ZERO)
            compiler.scope.env['LETTERS'] = EnvItem('LETTERS', Type('string'), POS_ZERO)
            compiler.scope.env['VERSION'] = EnvItem('VERSION', Type('string'), POS_ZERO)
            compiler.scope.env['MIN_FLOAT'] = EnvItem('MIN_FLOAT', Type('float'), POS_ZERO)
            compiler.scope.env['MAX_FLOAT'] = EnvItem('MAX_FLOAT', Type('float'), POS_ZERO)
            compiler.scope.env['ONE_BILLION'] = EnvItem('ONE_BILLION', Type('int'), POS_ZERO)
            compiler.scope.env['ONE_MILLION'] = EnvItem('ONE_MILLION', Type('int'), POS_ZERO)
            compiler.scope.env['ONE_THOUSAND'] = EnvItem('ONE_THOUSAND', Type('int'), POS_ZERO)
            
            setattr(compiler, '_initialised_CManager', True)
            
            def _Math_absint(_, call_position: Position, x: Object) -> Object:
                return Object(
                    f'(abs({x.code}))',
                    Type('int'), call_position
                )
            
            @c_dec(
                param_types=('float',),
                is_method=True,
                is_static=True,
                overloads={(('int',), 'int'): _Math_absint},
                add_to_class=self
            )
            def _Math_abs(compiler, call_position: Position, x: Object) -> Object:
                self.include('<math.h>', compiler)
                return Object(f'((float)fabsf({x.code}))', Type('float'), call_position)
            
            def _System_exit2(compiler, call_position: Position) -> Object:
                compiler.prepend_code(f'{compiler.get_end_code()}\nexit(0);')
                return Object('NULL', Type('nil'), call_position)
            
            @c_dec(
                param_types=('int',),
                is_method=True,
                is_static=True,
                overloads={((), 'nil'): _System_exit2},
                add_to_class=self
            )
            def _System_exit(compiler, call_position: Position, code: Object) -> Object:
                compiler.prepend_code(f'{compiler.get_end_code()}\nexit({code.code});')
                return Object('NULL', Type('nil'), call_position)
            
            def rand_start0(compiler, call_position: Position, max: Object) -> Object:
                return _Math_random(
                    compiler, call_position, Object('0', Type('int'), call_position), max
                )
            
            @c_dec(
                param_types=('int', 'int'),
                is_method=True,
                is_static=True,
                overloads={(('int',), 'int'): rand_start0},
                add_to_class=self
            )
            def _Math_random(compiler, call_position: Position, min: Object,
                             max: Object) -> Object:
                res = compiler.create_temp_var(Type('int'), call_position)
                low_num = compiler.create_temp_var(Type('int'), call_position)
                hi_num = compiler.create_temp_var(Type('int'), call_position)
                compiler.prepend_code(f"""int {res} = 0, {low_num} = 0, {hi_num} = 0;
if (({min.code}) < ({max.code})) {{
    {low_num} = {min.code};
    {hi_num} = {max.code};
}} else {{
    {low_num} = {max.code};
    {hi_num} = {min.code};
}}

srand(time(NULL));
{res} = (rand() % ({hi_num} - {low_num})) + {low_num};
""")
                return Object(res, Type('int'), call_position)
    
    def include(self, file: str, compiler) -> None:
        """Add a C include to the compiled C code.

        Args:
            file (str): The file name.
            compiler (type): The compiler instance.
        """
        
        self.includes.add(file)
        compiler.add_toplevel_code(f'#include {file}')
    
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
        } | class_.__dict__
    
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
{self.compiler.get_end_code()}
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
    
    def fmt_length(self, compiler, pos: Position, fmt: str, *format_vars: str,
                   buf_var: str | None = None) -> tuple[str, Free]:
        """Get the code required to check the length of a formatted string in C and output it
to a buffer.

        Args:
            compiler (CureCompiler): The compiler instance.
            pos (Position): The position.
            fmt (str): The format string.
            *format_vars (tuple[str]): The variables to be formatted into the format string.
            buf_var (str): Define an already created buffer variable instead of creating a new one
        
        Returns:
            tuple[str, Free]: The string is the C code and the `Free` object is the buffer.
        """
        
        length = compiler.create_temp_var(Type('int'), pos)
        buf_free = Free()
        buf = compiler.create_temp_var(Type('string'), pos, name=buf_var, free=buf_free)
        return f"""int {length} = snprintf(
    NULL, 0,
    "{fmt}"{''.join(', ' + s for s in format_vars)}
);
string {buf} = (string)malloc({length} + 1);
{compiler.c_manager.buf_check(buf)}
snprintf({buf}, {length} + 1, "{fmt}"{''.join(', ' + s for s in format_vars)});
""", buf_free

    def array_from_c_array(self, compiler, pos: Position, type: Type,
                           value: str) -> tuple[str, str]:
        """Generate a Cure array from a C array.

        Args:
            compiler (CureCompiler): The compiler instance.
            pos (Position): The position.
            type (str): The type of the C array.
            value (str): The variable or object of the C array.

        Returns:
            tuple[str, str]: The code to convert the C array to a Cure array and the name of the
            created array.
        """
        
        from codegen.array_manager import DEFAULT_CAPACITY
        
        compiler.array_manager.define_array(type)
        array_type = Type(f'array[{type}]', f'{type}_array')
        
        arr = compiler.create_temp_var(array_type, pos)
        i = compiler.create_temp_var(Type('int'), pos)
        length = compiler.create_temp_var(Type('int'), pos)
        
        return f"""{array_type.c_type} {arr};
{arr}.length = 0;
{arr}.capacity = {DEFAULT_CAPACITY};
{arr}.elements = ({type.c_type}*)malloc(sizeof({type.c_type}) * {DEFAULT_CAPACITY});
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
    
    @c_dec(
        param_types=('*',),
        can_user_call=True
    )
    def _print(self, compiler, call_position: Position, *args: Object) -> Object:
        fmt_vars = []
        for arg in args:
            repr_method = self.get_object(f'{arg.type.c_type}_to_string')
            if repr_method is None:
                call_position.error_here(f'String representation for \'{arg.type}\' is not defined')
            
            fmt_vars.append(repr_method(compiler, call_position, arg).code)
        
        fmt = ' '.join('%s' for _ in range(len(fmt_vars)))
        return Object(
            f'(printf("{fmt}\\n", {", ".join(fmt_vars)}))',
            Type('int'), call_position
        )
    
    @c_dec(
        param_types=('any',),
        can_user_call=True
    )
    def _type(self, compiler, call_position: Position, value: Object) -> Object:
        type_method = self.get_object(f'{value.type.c_type}_type')
        if type_method is None:
            call_position.error_here(f'Type representation for \'{value.type}\' is not defined')
        
        return Object(
            type_method(compiler, call_position).code,
            Type('string'), call_position
        )
    
    @c_dec(
        param_types=('any',),
        can_user_call=True
    )
    def _to_string(self, compiler, call_position: Position, value: Object) -> Object:
        repr_method = self.get_object(f'{value.type.c_type}_to_string')
        if repr_method is None:
            call_position.error_here(f'String representation for \'{value.type}\' is not defined')

        return Object(
            repr_method(compiler, call_position, value).code,
            Type('string'), call_position
        )
    
    def _input_no_prompt(self, compiler, call_position: Position) -> Object:
        return self._input(compiler, call_position, None)
    
    @c_dec(
        param_types=('string',),
        overloads={
            ((), 'string'): _input_no_prompt
        },
        can_user_call=True,
    )
    def _input(self, compiler, call_position: Position, prompt: Object | None) -> Object:
        if prompt is not None:
            compiler.prepend_code(f'printf("%s", {prompt.code});')
        
        buf_size = compiler.create_temp_var(Type('int'), call_position)
        buf = compiler.create_temp_var(Type('string'), call_position, free=Free())
        length = compiler.create_temp_var(Type('int'), call_position)
        c = compiler.create_temp_var(Type('int'), call_position)
        compiler.prepend_code(f"""size_t {buf_size} = 128;
string {buf} = (string)malloc({buf_size} * sizeof(char));
{compiler.c_manager.buf_check(buf)}
size_t {length} = 0;
int {c};
while (({c} = getchar()) != '\\n' && {c} != EOF) {{
    if ({length} + 1 >= {buf_size}) {{
        {buf_size} *= 2;
        {buf} = (string)realloc({buf}, {buf_size} * sizeof(char));
        {compiler.c_manager.buf_check(buf)}
    }}
    
    {buf}[{length}++] = (char){c};
}}
{buf}[{length}] = '\\0';
""")
        
        return Object(buf, Type('string'), call_position, free=Free(buf))
    
    @c_dec(
        param_types=('any',),
        can_user_call=True
    )
    def _to_bool(self, _, call_position: Position, value: Object) -> Object:
        bool_method = self.get_object(f'{value.type.c_type}_to_bool')
        if bool_method is None:
            call_position.error_here(f'Boolean conversion for \'{value.type}\' is not defined')

        return Object(
            bool_method(call_position).code,
            Type('bool'), call_position
        )
    
    @c_dec(
        param_types=('string',),
        can_user_call=True
    )
    def _get_char(self, compiler, call_position: Position, value: Object) -> Object:
        slen = self._string_length(compiler, call_position, value)
        compiler.prepend_code(f"""if ({slen.code} > 1) {{
    {self.err('String is not a single character')}
}}
""")
        
        return Object(f'((int)(({value.code})[0]))', Type('int'), call_position)
    
    @c_dec(
        param_types=('int',),
        can_user_call=True
    )
    def _char_int(self, compiler, call_position: Position, value: Object) -> Object:
        char = compiler.create_temp_var(value.type, call_position)
        i = f'({value.code})'
        compiler.prepend_code(f"""if ({i} < 0 || {i} > 127) {{
    {self.err('Character is not a valid ASCII character')}
}}

char {char}[2];
{char}[0] = (char)({value.code});
{char}[1] = '\\0';
""")
        
        return Object(char, Type('string'), call_position)
    
    @c_dec(param_types=('any',), can_user_call=True)
    def _sizeof(self, _, call_position: Position, object: Object) -> Object:
        return Object(f'sizeof({object.code})', Type('int'), call_position)
    
    @c_dec(param_types=('string',), can_user_call=True)
    def _insert_c_code(self, compiler, call_position: Position, code: Object) -> Object:
        compiler.prepend_code(f'{code.code};')
        return Object('NULL', Type('nil'), call_position)
    
    @c_dec(param_types=('any',), can_user_call=True)
    def _addr_of(self, compiler, call_position: Position, obj: Object) -> Object:
        if (ident := ID_REGEX.fullmatch(obj.code)) is not None:
            code, buf_free = self.fmt_length(
                compiler, call_position,
                '%p', f'&{ident.group()}'
            )
            
            compiler.prepend_code(code)
            return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
        else:
            call_position.error_here(f'Cannot get address of non-variable \'{obj.code}\'')
    
    
    @c_dec()
    def _int_type(self, _, call_position: Position) -> Object:
        return Object('"int"', Type('string'), call_position)
    
    @c_dec()
    def _float_type(self, _, call_position: Position) -> Object:
        return Object('"float"', Type('string'), call_position)
    
    @c_dec()
    def _string_type(self, _, call_position: Position) -> Object:
        return Object('"string"', Type('string'), call_position)
    
    @c_dec()
    def _bool_type(self, _, call_position: Position) -> Object:
        return Object('"bool"', Type('string'), call_position)
    
    @c_dec()
    def _nil_type(self, _, call_position: Position) -> Object:
        return Object('"nil"', Type('string'), call_position)
    
    @c_dec()
    def _Math_type(self, _, call_position: Position) -> Object:
        return Object('"Math"', Type('string'), call_position)
    
    @c_dec()
    def _System_type(self, _, call_position: Position) -> Object:
        return Object('"System"', Type('string'), call_position)
    
    @c_dec()
    def _Time_type(self, _, call_position: Position) -> Object:
        return Object('"Time"', Type('string'), call_position)
    
    @c_dec(param_types=('int',))
    def _int_to_string(self, compiler, call_position: Position, value: Object) -> Object:
        # integer to string length formula is: (int)((ceil(log10(num))+1)*sizeof(char))
        temp_var = compiler.create_temp_var(Type('string'), call_position)
        compiler.prepend_code(f"""char {temp_var}[13];
snprintf({temp_var}, 13, "%d", ({value.code}));""")
        return Object(temp_var, Type('string'), call_position)
    
    @c_dec(param_types=('float',))
    def _float_to_string(self, compiler, call_position: Position, value: Object) -> Object:
        temp_var = compiler.create_temp_var(Type('string'), call_position)
        compiler.prepend_code(f"""char {temp_var}[47];
snprintf({temp_var}, 47, "%f", ({value.code}));""")
        return Object(temp_var, Type('string'), call_position)
    
    @c_dec(param_types=('string',))
    def _string_to_string(self, _, _call_position: Position, value: Object) -> Object:
        return value
    
    @c_dec(param_types=('bool',))
    def _bool_to_string(self, _, call_position: Position, value: Object) -> Object:
        return Object(f'(({value.code}) ? "true" : "false")', Type('string'), call_position)
    
    @c_dec(param_types=('nil',))
    def _nil_to_string(self, _, call_position: Position, _value: Object) -> Object:
        return Object('"nil"', Type('string'), call_position)
    
    @c_dec(param_types=('Math',))
    def _Math_to_string(self, _, call_position: Position, _value: Object) -> Object:
        return Object('"class \'Math\'"', Type('string'), call_position)
    
    @c_dec(param_types=('System',))
    def _System_to_string(self, _, call_position: Position, _value: Object) -> Object:
        return Object('"class \'System\'"', Type('string'), call_position)
    
    @c_dec(param_types=('bin',))
    def _bin_to_string(self, compiler, call_position: Position, value: Object) -> Object:
        size = compiler.create_temp_var(Type('int'), call_position)
        temp = compiler.create_temp_var(Type('int'), call_position)
        buf_free = Free()
        buf = compiler.create_temp_var(Type('string'), call_position, free=buf_free)
        i = compiler.create_temp_var(Type('int'), call_position)
        b = compiler.create_temp_var(Type('int'), call_position)
        compiler.prepend_code(f"""string {buf};
int {b} = {value.code};
if ({b} == 0) {{
    {buf} = malloc(2);
    {compiler.c_manager.buf_check(buf)}
    {buf}[0] = '0';
    {buf}[1] = '\\0';
}} else {{
    int {size} = 0;
    int {temp} = {b};
    while ({temp} > 0) {{
        {size}++;
        {temp} >>= 1;
    }}
    
    {buf} = malloc({size} + 1);
    {compiler.c_manager.buf_check(buf)}
    {buf}[{size}] = '\\0';
    for (int {i} = {size} - 1; {i} >= 0; {i}--) {{
        {buf}[{i}] = ({b} & 1) ? '1' : '0';
        {b} >>= 1;
    }}
}}
""")
        
        return Object(buf, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('Time',))
    def _Time_to_string(self, compiler, call_position: Position, value: Object) -> Object:
        t = f'({value.code})'
        code, buf_free = self.fmt_length(
            compiler, call_position,
            'Time(%s)',
            f'asctime({t}.ti)'
        )
        
        compiler.prepend_code(code)
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
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
    def _string_add_string(self, compiler, call_position: Position, a: Object, b: Object) -> Object:
        self.include('<string.h>', compiler)
        
        temp_var = compiler.create_temp_var(Type('string'), call_position, free=Free())
        compiler.prepend_code(
            f"""string {temp_var} = (string)malloc(strlen({a.code}) + strlen({b.code}) + 1);
{compiler.c_manager.buf_check(temp_var)}
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
    def _int_mod_float(self, compiler, call_position: Position, a: Object, b: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'(fmodf((float)({a.code}), ({b.code})))', Type('float'), call_position)
    
    @c_dec(param_types=('float', 'int'))
    def _float_mod_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(fmodf(({a.code}), (float)({b.code})))', Type('float'), call_position)
    
    @c_dec(param_types=('float', 'float'))
    def _float_mod_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(fmodf(({a.code}), ({b.code}))', Type('float'), call_position)
    
    @c_dec(param_types=('int', 'string'))
    def _int_mod_string(self, compiler, call_position: Position, a: Object, b: Object) -> Object:
        length = f'({a.code})'
        res = compiler.create_temp_var(Type('string'), call_position)
        current_length = compiler.create_temp_var(Type('int'), call_position)
        i = compiler.create_temp_var(Type('int'), call_position)
        compiler.prepend_code(f"""int {current_length} = {
    self._string_length(compiler, call_position, b).code
};
string {res} = (string)malloc({length} + 1);
{compiler.c_manager.buf_check(res)}
if ({length} > 0) {{
    if ({current_length} < {length}) {{
        free(res);
        {compiler.c_manager.err('Invalid string length')}
    }}
    
    for (size_t {i} = 0; {i} < {length}; {i}++) {{
        {res}[{i}] = {b.code}[{i}];
    }}

    {res}[{length}] = '\\0';
}} else {{
    free({res});
    {compiler.c_manager.err('Invalid string length')}
}}
""")
        
        return Object(res, Type('string'), call_position)
    
    @c_dec(param_types=('string', 'int'))
    def _string_mod_int(self, compiler, call_position: Position,
                        a: Object, b: Object) -> Object:
        length = f'({b.code})'
        res = compiler.create_temp_var(Type('string'), call_position)
        current_length = compiler.create_temp_var(Type('int'), call_position)
        compiler.prepend_code(f"""int {current_length} = {
    self._string_length(compiler, call_position, a).code
};
string {res} = (string)malloc({length} + 1);
{compiler.c_manager.buf_check(res)}
if ({length} > 0) {{
    if ({current_length} < {length}) {{
        {compiler.c_manager.err('Invalid string length')}
    }}

    strncpy({res}, ({a.code}) + ({current_length} - {length}), {length});
    {compiler.c_manager.buf_check(res)}
    {res}[{length}] = '\\0';
}} else {{
    free({res});
    {compiler.c_manager.err('Invalid string length')}
}}""")
        
        return Object(res, Type('string'), call_position)
    
    @c_dec(param_types=('int', 'int'))
    def _int_eq_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) == ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('float', 'float'))
    def _float_eq_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) == ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('string', 'string'))
    def _string_eq_string(self, compiler, call_position: Position, a: Object, b: Object) -> Object:
        self.include('<string.h>', compiler)
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
    def _string_neq_string(self, compiler, call_position: Position, a: Object, b: Object) -> Object:
        self.include('<string.h>', compiler)
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
    def _string_gt_string(self, compiler, call_position: Position, a: Object, b: Object) -> Object:
        alen = self._string_length(compiler, call_position, a)
        blen = self._string_length(compiler, call_position, b)
        return Object(f'({alen.code} > {blen.code})', Type('bool'), call_position)
    
    @c_dec(param_types=('int', 'int'))
    def _int_gte_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) >= ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('float', 'float'))
    def _float_gte_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) >= ({b.code}))', Type('bool'), call_position)

    @c_dec(param_types=('string', 'string'))
    def _string_gte_string(self, compiler, call_position: Position, a: Object, b: Object) -> Object:
        alen = self._string_length(compiler, call_position, a)
        blen = self._string_length(compiler, call_position, b)
        return Object(f'({alen.code} >= {blen.code})', Type('bool'), call_position)
    
    @c_dec(param_types=('int', 'int'))
    def _int_lt_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) < ({b.code}))', Type('bool'), call_position)

    @c_dec(param_types=('float', 'float'))
    def _float_lt_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) < ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('string', 'string'))
    def _string_lt_string(self, compiler, call_position: Position, a: Object, b: Object) -> Object:
        alen = self._string_length(compiler, call_position, a)
        blen = self._string_length(compiler, call_position, b)
        return Object(f'({alen.code} < {blen.code})', Type('bool'), call_position)
    
    @c_dec(param_types=('int', 'int'))
    def _int_lte_int(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) <= ({b.code}))', Type('bool'), call_position)

    @c_dec(param_types=('float', 'float'))
    def _float_lte_float(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) <= ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('string', 'string'))
    def _string_lte_string(self, compiler, call_position: Position, a: Object, b: Object) -> Object:
        alen = self._string_length(compiler, call_position, a)
        blen = self._string_length(compiler, call_position, b)
        return Object(f'({alen.code} <= {blen.code})', Type('bool'), call_position)
    
    @c_dec(param_types=('bool', 'bool'))
    def _bool_and_bool(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) && ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('bin', 'bin'))
    def _bin_and_bin(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) & ({b.code}))', Type('bin'), call_position)
    
    @c_dec(param_types=('bool', 'bool'))
    def _bool_or_bool(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) || ({b.code}))', Type('bool'), call_position)
    
    @c_dec(param_types=('bin', 'bin'))
    def _bin_or_bin(self, _, call_position: Position, a: Object, b: Object) -> Object:
        return Object(f'(({a.code}) | ({b.code}))', Type('bin'), call_position)
    
    @c_dec(param_types=('bool',))
    def _not_bool(self, _, call_position: Position, a: Object) -> Object:
        return Object(f'(!({a.code}))', Type('bool'), call_position)
    
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
    def _int_humanize_size(self, compiler, call_position: Position, i: Object) -> Object:
        mag = compiler.create_temp_var(Type('int'), call_position)
        x = compiler.create_temp_var(Type('int'), call_position)
        abs_call = compiler.call('Math_abs', [Object(x, Type('int'), call_position)], call_position)
        if 'sizeNames' not in self.RESERVED_NAMES:
            compiler.add_toplevel_code("""const string sizeNames[] = {{
    "B", "KB", "MB", "GB", "TB", "PB"
}};
""")
            self.RESERVED_NAMES.append('sizeNames')

        code, buf_free = self.fmt_length(compiler, call_position, '%.4f%s', x, f'sizeNames[{mag}]')
        compiler.prepend_code(f"""int {mag} = 0;
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
    def _int_science(self, compiler, call_position: Position,
                        i: Object, precision: Object | None = None) -> Object:
        self.include('<math.h>', compiler)
        
        if precision is None:
            precision = Object('5', Type('int'), call_position)
        
        exponent = compiler.create_temp_var(Type('int'), call_position)
        length = compiler.create_temp_var(Type('int'), call_position)
        num = compiler.create_temp_var(Type('float'), call_position)
        significand = compiler.create_temp_var(Type('float'), call_position)
        code, buf_free = self.fmt_length(
            compiler, call_position,
            '%.*fe%+03d',
            f'{precision.code}', significand, exponent
        )
        
        compiler.prepend_code(f"""int {exponent};
int {length};
double {num} = (double){i.code};
{exponent} = (int)floor(log10(fabs({num})));
double {significand} = {num} / pow(10.0, {exponent});
{code}
""")
        
        return Object(buf_free.object_name, Type('string'), call_position, free=buf_free)
    
    @c_dec(param_types=('float',), is_property=True)
    def _float_humanize_size(self, compiler, call_position: Position, f: Object) -> Object:
        return self._int_humanize_size(compiler, call_position, f)
    
    @c_dec(param_types=('float',), is_method=True, overloads={
        (('float', 'int'), 'string'): None
    })
    def _float_science(self, compiler, call_position: Position,
                          f: Object, precision: Object | None = None) -> Object:
        return self._int_science(compiler, call_position, f, precision)
    
    @c_dec(param_types=('string',), is_property=True)
    def _string_length(self, compiler, call_position: Position, string: Object) -> Object:
        self.include('<string.h>', compiler)
        return Object(f'(strlen({string.code}))', Type('int'), call_position)
    
    @c_dec(param_types=('string',), is_property=True)
    def _string_is_empty(self, compiler, call_position: Position, string: Object) -> Object:
        strlen = self._string_length(compiler, call_position, string)
        return Object(f'({strlen.code} == 0)', Type('bool'), call_position)
    
    @c_dec(param_types=('string',), is_property=True)
    def _string_is_char(self, compiler, call_position: Position, string: Object) -> Object:
        strlen = self._string_length(compiler, call_position, string)
        return Object(f'({strlen.code} == 1)', Type('bool'), call_position)
    
    @c_dec(param_types=('string',), is_property=True)
    def _string_is_digit(self, compiler, call_position: Position, string: Object) -> Object:
        self.include('<ctype.h>', compiler)
        
        i = compiler.create_temp_var(Type('int'), call_position)
        res = compiler.create_temp_var(Type('bool'), call_position)
        slen = self._string_length(compiler, call_position, string)
        compiler.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {slen.code}; {i}++) {{
    if (!isdigit(({string.code})[{i}])) {res} = false;
}}
""")
        
        return Object(res, Type('bool'), call_position)
    
    @c_dec(param_types=('string',), is_property=True)
    def _string_is_lower(self, compiler, call_position: Position, string: Object) -> Object:
        self.include('<ctype.h>', compiler)
        
        i = compiler.create_temp_var(Type('int'), call_position)
        res = compiler.create_temp_var(Type('bool'), call_position)
        slen = self._string_length(compiler, call_position, string)
        compiler.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {slen.code}; {i}++) {{
    if (!islower(({string.code})[{i}])) {res} = false;
}}
""")
        
        return Object(res, Type('bool'), call_position)
    
    @c_dec(param_types=('string',), is_property=True)
    def _string_is_upper(self, compiler, call_position: Position, string: Object) -> Object:
        self.include('<ctype.h>', compiler)

        i = compiler.create_temp_var(Type('int'), call_position)
        res = compiler.create_temp_var(Type('bool'), call_position)
        slen = self._string_length(compiler, call_position, string)
        compiler.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {slen.code}; {i}++) {{
    if (!isupper(({string.code})[{i}])) {res} = false;
}}
""")
        
        return Object(res, Type('bool'), call_position)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_lower(self, compiler, call_position: Position, string: Object) -> Object:
        self.include('<ctype.h>', compiler)
        
        strlen = self._string_length(compiler, call_position, string)
        
        temp_free = Free()
        temp_var = compiler.create_temp_var(Type('string'), call_position, free=temp_free)
        i = compiler.create_temp_var(Type('int'), call_position)
        compiler.prepend_code(f"""string {temp_var} = (string)malloc({strlen.code} + 1);
{compiler.c_manager.buf_check(temp_var)}
for (size_t {i} = 0; {i} < {strlen.code}; {i}++)
    {temp_var}[{i}] = tolower({string.code}[{i}]);
{temp_var}[{strlen.code}] = '\\0';""")
        
        return Object(temp_var, Type('string'), call_position, free=temp_free)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_upper(self, compiler, call_position: Position, string: Object) -> Object:
        self.include('<ctype.h>', compiler)

        strlen = self._string_length(compiler, call_position, string)

        temp_free = Free()
        temp_var = compiler.create_temp_var(Type('string'), call_position, free=temp_free)
        i = compiler.create_temp_var(Type('int'), call_position)
        compiler.prepend_code(f"""string {temp_var} = (string)malloc({strlen.code} + 1);
{compiler.c_manager.buf_check(temp_var)}
for (size_t {i} = 0; {i} < {strlen.code}; {i}++)
    {temp_var}[{i}] = toupper({string.code}[{i}]);
{temp_var}[{strlen.code}] = '\\0';""")

        return Object(temp_var, Type('string'), call_position, free=temp_free)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_title(self, compiler, call_position: Position, string: Object) -> Object:
        self.include('<string.h>', compiler)
        self.include('<ctype.h>', compiler)
        
        temp_free = Free()
        temp_var = compiler.create_temp_var(Type('string'), call_position, free=temp_free)
        lv = compiler.create_temp_var(Type('string'), call_position)
        compiler.prepend_code(f"""string {temp_var} = strdup({string.code});
{compiler.c_manager.buf_check(temp_var)}
for (string {lv} = {temp_var}; *{lv} != '\\0'; ++{lv})
    *{lv} = ({lv} == {temp_var} || *({lv} - 1) == ' ') ? toupper(*{lv}) : tolower(*{lv});""")
        
        return Object(temp_var, Type('string'), call_position, free=temp_free)
    
    @c_dec(param_types=('string', 'string'), is_method=True)
    def _string_startswith(self, compiler, call_position: Position,
                           string: Object, prefix: Object) -> Object:
        self.include('<string.h>', compiler)

        prefix_len = self._string_length(compiler, call_position, prefix)
        return Object(
            f'(strncmp({string.code}, {prefix.code}, {prefix_len.code}) == 0)',
            Type('bool'), call_position
        )
    
    @c_dec(param_types=('string', 'string'), is_method=True)
    def _string_endswith(self, compiler, call_position: Position,
                         string: Object, suffix: Object) -> Object:
        self.include('<string.h>', compiler)
        
        s = string.code
        su = suffix.code
        strlen = self._string_length(compiler, call_position, string)
        slen = compiler.create_temp_var(Type('int'), call_position)
        suffix_len = self._string_length(compiler, call_position, suffix)
        sulen = compiler.create_temp_var(Type('int'), call_position)
        compiler.prepend_code(f"""size_t {slen} = {strlen.code};
size_t {sulen} = {suffix_len.code}
;""")
        return Object(
            f"""({slen} < {sulen} ? false : (strncmp(
                ({s}) + {slen} - {sulen}, {su}, {sulen}) == 0)
            )""",
            Type('bool'), call_position
        )
    
    @c_dec(param_types=('string', 'int'), is_method=True)
    def _string_at(self, compiler, call_position: Position,
                   string: Object, index: Object) -> Object:
        self.include('<string.h>', compiler)
        
        strlen = self._string_length(compiler, call_position, string)
        temp_var = compiler.create_temp_var(Type('string'), call_position)
        compiler.prepend_code(f"""if (({index.code}) > {strlen.code} - 1) {{
    {self.err('Index out of bounds on string')}
}}
char {temp_var}[2];
{temp_var}[0] = ({string.code})[{index.code}];
{temp_var}[1] = '\\0';
""")
        
        return Object(temp_var, Type('string'), call_position)
    
    @c_dec(param_types=('string', 'string'), is_method=True)
    def _string_has(self, compiler, call_position: Position,
                   string: Object, substring: Object) -> Object:
        self.include('<string.h>', compiler)
        return Object(
            f'(strstr({string.code}, {substring.code}) != NULL)',
            Type('bool'), call_position
        )
    
    @c_dec(param_types=('string', 'string_array'), is_method=True)
    def _string_join(self, compiler, call_position: Position,
                     string: Object, arr: Object) -> Object:
        self.include('<string.h>', compiler)
        
        tlen = compiler.create_temp_var(Type('int'), call_position)
        sep_len = compiler.create_temp_var(Type('int'), call_position)
        res_free = Free()
        res = compiler.create_temp_var(Type('string'), call_position, free=res_free)
        count = compiler.create_temp_var(Type('int'), call_position)
        i = compiler.create_temp_var(Type('int'), call_position)
        a = f'({arr.code})'
        compiler.prepend_code(f"""size_t {tlen} = 0;
size_t {sep_len} = {self._string_length(compiler, call_position, string).code};
int {count} = 0;
for (int {i} = 0; {i} < {a}.length; {i}++) {{
    {tlen} += {self._string_length(
    compiler, call_position, Object(f'{a}.elements[{i}]', Type('string'), call_position)
).code};
    if ({i} > 0) {{
        {tlen} += {sep_len};
    }}
    {count}++;
}}

string {res} = (string)malloc({tlen} + 1);
{compiler.c_manager.buf_check(res)}
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
    def _string_parse_int(self, _, call_position: Position, string: Object) -> Object:
        # TODO: Raise error if string is not a valid integer and fix undefined behaviour
        # overflow and underflow integers
        return Object(f'atoi({string.code})', Type('int'), call_position)
    
    @c_dec(param_types=('string',), is_method=True)
    def _string_parse_float(self, _, call_position: Position, string: Object) -> Object:
        # TODO: Raise error if string is not a valid float and fix undefined behaviour
        # overflow and underflow floats
        return Object(f'atof({string.code})', Type('float'), call_position)
    
    @c_dec(param_types=('string', 'string'), is_method=True)
    def _string_find(self, compiler, call_position: Position,
                     string: Object, substring: Object) -> Object:
        self.include('<string.h>', compiler)
        idx = compiler.create_temp_var(Type('int'), call_position)
        i = compiler.create_temp_var(Type('int'), call_position)
        compiler.prepend_code(f"""int {idx} = -1;
for (size_t {i} = 0; {i} < {self._string_length(compiler, call_position, string).code}; {i}++) {{
    if (strncmp(
        {string.code} + {i},
        {substring.code},
        {self._string_length(compiler, call_position, substring).code}
    ) == 0) {{
        {idx} = {i};
        break;
    }}
}}
""")
        
        return Object(idx, Type('int'), call_position)
    
    @c_dec(param_types=('string', 'int', 'int'), is_method=True)
    def _string_slice(self, compiler, call_position: Position,
                      string: Object, start: Object, end: Object) -> Object:
        self.include('<string.h>', compiler)
        buf_free = Free()
        buf = compiler.create_temp_var(Type('string'), call_position, free=buf_free)
        start_var = compiler.create_temp_var(Type('int'), call_position)
        end_var = compiler.create_temp_var(Type('int'), call_position)
        compiler.prepend_code(f"""string {buf} = NULL;
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
    
    @c_dec(param_types=('string', 'int'), return_type=Type('string'))
    def _iter_string(self, compiler, call_position: Position, string: Object, i: Object) -> Object:
        self.include('<string.h>', compiler)
        return self._string_at(compiler, call_position, string, i)
    
    @c_dec(param_types=('string', 'int'))
    def _index_string(self, compiler, call_position: Position, string: Object, i: Object) -> Object:
        self.include('<string.h>', compiler)
        return self._string_at(compiler, call_position, string, i)
    
    
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
    def _Math_sin(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)sin({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_cos(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)cos({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_tan(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)tan({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_asin(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)asin({x.code}))', Type('float'), call_position)

    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_acos(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)acos({x.code}))', Type('float'), call_position)

    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_atan(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)atan({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={
            (('int', 'int'), 'float'): None,
            (('int', 'float'), 'float'): None,
            (('float', 'int'), 'float'): None
        }
    )
    def _Math_atan2(self, compiler, call_position: Position, y: Object, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)atan2({y.code}, {x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_sqrt(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)sqrt({x.code}))', Type('float'), call_position)
    
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
    def _Math_nth_root(self, compiler, call_position: Position, x: Object, n: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)pow({x.code}, 1.0f / ({n.code})))', Type('float'), call_position)
    
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
    def _Math_pow(self, compiler, call_position: Position, x: Object, y: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)pow({x.code}, {y.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_log(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)log({x.code}))', Type('float'), call_position)

    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_log10(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)log10({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_log2(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)log2({x.code}))', Type('float'), call_position)

    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_exp(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)exp({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True
    )
    def _Math_ceil(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)ceilf({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True
    )
    def _Math_floor(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)floorf({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True
    )
    def _Math_round(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
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
    def _Math_min(self, compiler, call_position: Position, x: Object, y: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(
            f'(({x.code}) > ({y.code}) ? ({x.code}) : ({y.code}))',
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
    def _Math_max(self, compiler, call_position: Position, x: Object, y: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(
            f'(({x.code}) > ({y.code}) ? ({y.code}) : ({x.code}))',
            Type('int') if x.type == Type('int') and y.type == Type('int') else Type('float'),
            call_position
        )
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_rad(self, compiler, call_position: Position, deg: Object) -> Object:
        self.include('<math.h>', compiler)
        pi = self._Math_pi(compiler, call_position)
        return Object(f'((float)({deg.code}) * {pi.code} / 180.0f)', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_deg(self, compiler, call_position: Position, rad: Object) -> Object:
        self.include('<math.h>', compiler)
        pi = self._Math_pi(compiler, call_position)
        return Object(f'((float)({rad.code}) * 180.0f / {pi.code})', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_sinh(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)sinh({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_cosh(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)cosh({x.code}))', Type('float'), call_position)
    
    @c_dec(
        param_types=('float',),
        is_method=True,
        is_static=True,
        overloads={(('int',), 'float'): None}
    )
    def _Math_tanh(self, compiler, call_position: Position, x: Object) -> Object:
        self.include('<math.h>', compiler)
        return Object(f'((float)tanh({x.code}))', Type('float'), call_position)
    
    # TODO: add more https://en.cppreference.com/w/c/numeric/math
    
    
    @c_dec(is_property=True, is_static=True)
    def _System_pid(self, compiler, call_position: Position) -> Object:
        pid_var = compiler.create_temp_var(Type('int'), call_position)
        compiler.prepend_code(f"""#ifdef OS_WINDOWS
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
    def _System_cwd(self, compiler, call_position: Position) -> Object:
        cwd_var = compiler.create_temp_var(Type('string'), call_position)
        compiler.prepend_code(f"""char {cwd_var}[1024];
if (getcwd({cwd_var}, sizeof({cwd_var})) == NULL) {{
    {self.err('Failed to get current working directory')}
}}
""")
        
        return Object(cwd_var, Type('string'), call_position)
    
    @c_dec(is_property=True, is_static=True)
    def _System_time(self, compiler, call_position: Position) -> Object:
        time_var = compiler.create_temp_var(Type('Time'), call_position)
        compiler.prepend_code(f"""Time {time_var};
{time_var}.t = time(NULL);
{time_var}.ti = localtime(&{time_var}.t);
""")
        
        return Object(time_var, Type('Time'), call_position)
    
    @c_dec(param_types=('int',), is_method=True, is_static=True)
    def _System_sleep(self, compiler, call_position: Position, milliseconds: Object) -> Object:
        compiler.prepend_code(f"""#ifdef OS_WINDOWS
    Sleep({milliseconds.code});
#endif
""")
        return Object('NULL', Type('nil'), call_position)
    
    @c_dec(param_types=('function',), is_method=True, is_static=True)
    def _System_atexit(self, compiler, call_position: Position, func: Object) -> Object:
        void_func = compiler.get_unique_name()
        compiler.scope.env[void_func] = EnvItem(void_func, Type('nil'), call_position,
                                                reserved=True)
        
        func_obj = compiler.scope.env[func.code]
        if func_obj.func.returns != Type('nil'):
            call_position.error_here(
                f'\'{func.code}\' set as an atexit function but does not return nil'
            )
        elif func_obj.func.params != []:
            call_position.error_here(
                f'\'{func.code}\' set as an atexit function but has parameters'
            )
        
        compiler.add_toplevel_code(f"""nil {func.code}();
void {void_func}() {{ {func.code}(); }}
""")
        compiler.prepend_code(f'atexit({void_func});')
        return Object('NULL', Type('nil'), call_position)
    
    @c_dec(param_types=('string',), is_method=True, is_static=True)
    def _System_shell(self, _, call_position: Position, command: Object) -> Object:
        return Object(f'((bool)system({command.code}))', Type('bool'), call_position)


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

    
    @staticmethod
    @func_modification(param_types=('string',))
    def _Warn(_, _func_obj, call_position: Position, _args: list[Object],
              mod_args: list[Object]) -> None:
        msg = mod_args[0].code
        if not msg.startswith('"') and not msg.endswith('"'):
            call_position.error_here('Warning message must be a string literal')
        
        call_position.warn_here(msg[1:-1])
    
    @staticmethod
    @func_modification(param_types=('string',))
    def _Info(_, _func_obj, call_position: Position, _args: list[Object],
              mod_args: list[Object]) -> None:
        msg = mod_args[0].code
        if not msg.startswith('"') and not msg.endswith('"'):
            call_position.error_here('Info message must be a string literal')

        call_position.info_here(msg[1:-1])

    @staticmethod
    @func_modification(param_types=('string',))
    def _Error(_, _func_obj, call_position: Position, _args: list[Object],
               mod_args: list[Object]) -> None:
        msg = mod_args[0].code
        if not msg.startswith('"') and not msg.endswith('"'):
            call_position.error_here('Error message must be a string literal')
        
        call_position.error_here(msg[1:-1])
    
    @staticmethod
    @func_modification()
    def _Benchmark(compiler, func_obj: Function, call_position: Position, _args: list[Object],
                   _mod_args: list[Object]) -> None:
        begin = compiler.create_temp_var(Type('int', 'clock_t'), call_position)
        end = compiler.create_temp_var(Type('int', 'clock_t'), call_position)
        compiler.prepend_code(f'clock_t {begin} = clock();\n')
        compiler.append_code(f"""clock_t {end} = clock();
printf("Time spent to execute '{func_obj.name}': %f", (float)(({end} - {begin}) / CLOCKS_PER_SEC));
""")
