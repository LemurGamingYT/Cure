from typing import Callable, Any
from functools import wraps
from pathlib import Path

from codegen.objects import (
    Object, Position, EnvItem, Free, Type, Function, Arg, TempVar, Param, Overloads, BuiltinFunction,
    POS_ZERO
)


CURRENT_FILE = Path(__file__).absolute()
STD_PATH = CURRENT_FILE.parent / 'std'
INCLUDES = CURRENT_FILE.parent.parent / 'include'
LIBS = CURRENT_FILE.parent.parent / 'libs'
HEADER = (INCLUDES / 'header.h').as_posix()


STRINGBUILDER_CAPACITY = 50


def func_modification(
    params: tuple[Param, ...] | None = None,
    add_to_class: Any = None
) -> Callable:
    """Modify a function to have special properties.
    
    Args:
        params (tuple[Param, ...] | None, optional): The parameter types of the modification.
        Defaults to None (an empty tuple).
        add_to_class (type | None, optional): The class to add the function to. Useful for adding
            the function to, for example, the `CManager` class. Defaults to None.

    Returns:
        Callable: The decorator callable.
    """
    
    if params is None:
        params = ()
    
    def decorator(func: Callable) -> Callable:
        setattr(func, 'params', params)
        
        if add_to_class is not None:
            if isinstance(add_to_class, CManager):
                add_to_class.add_func(func.__name__, func)
            
            setattr(add_to_class, func.__name__, func)
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

def c_dec(
    param_types: tuple[Param, ...] | None = None,
    overloads: Overloads | None = None,
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
        param_types (tuple[Param, ...] | None, optional): The function parameters.
            Defaults to None.
        overloads (Overloads | None, optional): The possible type
            overloads. The overloads are defined as: ((parameter types), return type): function. The
            function can be None to reference the original function. Defaults to None.
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
        name = func_name_override if func_name_override is not None else func.__name__[1:]
        cname = name if name.startswith('_') else f'_{name}'
        
        setattr(func, 'name', cname)
        setattr(func, 'param_types', param_types)
        setattr(func, 'overloads', overloads)
        setattr(func, 'is_method', is_method)
        setattr(func, 'is_static', is_static)
        setattr(func, 'is_property', is_property)
        setattr(func, 'return_type', return_type)
        setattr(func, 'can_user_call', can_user_call)
        setattr(func, 'func_name_override', func_name_override)
        setattr(func, 'added_to_class', add_to_class)
        setattr(func, 'object', BuiltinFunction(func, list(param_types), overloads))
        
        if add_to_class is not None:
            if isinstance(add_to_class, CManager):
                add_to_class.add_func(cname, func)
            
            setattr(add_to_class, cname, func)
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
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
        'mkfifo', 'mknod', 'stat', 'umask', 'IS_ADMIN', 'default', 'rand', 'OS', 'ARCH', 'Fraction',
        'Vector2', 'StringBuilder'
    ]
    
    
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
        
        length: TempVar = codegen.create_temp_var(Type('int'), pos)
        buf_free = Free()
        buf: TempVar = codegen.create_temp_var(Type('string'), pos, name=buf_var, free=buf_free)
        return f"""int {length} = snprintf(
    NULL, 0,
    {fmt}{''.join(', ' + s for s in format_vars)}
);
string {buf} = (string)malloc({length} + 1);
{codegen.c_manager.buf_check(buf)}
snprintf({buf}, {length} + 1, {fmt}{''.join(', ' + s for s in format_vars)});
""", buf_free

    def array_from_c_array(self, codegen, pos: Position, type: Type,
                           value: str, size_expr: str | None = None) -> tuple[str, TempVar]:
        """Generate a Cure array from a C array.

        Args:
            codegen (Curecodegen): The codegen instance.
            pos (Position): The position.
            type (str): The type of the C array.
            value (str): The variable or object of the C array.
            size_expr: str | None: The size expression of the C array. If None, the size will be
            calculated as the size of the C array divided by the size of the type of the C array.

        Returns:
            tuple[str, TempVar]: The code to convert the C array to a Cure array and the variable of the
            created array.
        """
        
        from codegen.array_manager import DEFAULT_CAPACITY
        
        array_type: Type = codegen.array_manager.define_array(type)
        
        arr: TempVar = codegen.create_temp_var(array_type, pos)
        i: TempVar = codegen.create_temp_var(Type('int'), pos)
        length: TempVar = codegen.create_temp_var(Type('int'), pos)
        return f"""{array_type.c_type} {arr} = {{
    .length = 0, .capacity = {DEFAULT_CAPACITY},
    .elements = ({type.c_type}*)malloc(sizeof({type.c_type}) * {DEFAULT_CAPACITY})
}};
int {length} = {f"sizeof({value}) / sizeof({value}[0])" if size_expr is None else size_expr};
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

    def c_array_from_list(self, codegen, pos: Position, type: Type, value: list[Object]) -> Object:
        """Convert a Python list and generate code to convert it to a C array. Note that this function
        also prepends the code instead of returning it.

        Args:
            codegen (Codegen): The code generator.
            pos (Position): The current position.
            type (Type): The type of the C array.
            value list[Object]: The python list objects.

        Returns:
            Object: The C array.
        """
        
        array_type: Type = codegen.array_manager.define_array(type)
        array: Object = codegen.call(f'{array_type.c_type}_make', [], pos)
        for elem in value:
            codegen.call(f'{array_type.c_type}_add', [Arg(array), Arg(elem)], pos)
        
        return array
    
    def wrap_struct_properties(self, struct_name: str, struct: Type, names: list[Param]) -> None:
        """Wrap properties from a struct into the programming language.

        Args:
            struct_name (str): The struct's name.
            struct (Type): The struct type.
            names (list[Param]): The struct's fields to wrap.
        """
        
        for name in names:
            @c_dec(
                param_types=(Param(struct_name, struct),), is_property=True, add_to_class=self,
                func_name_override=f'{struct.c_type}_{name.name}'
            )
            def _(_, call_position: Position, obj: Object, n=name) -> Object:
                return Object(f'(({n.type})(({obj}).{n.name}))', n.type, call_position)
    
    
    def __init__(self, codegen) -> None:
        self.codegen = codegen
        self.includes = set()
        
        self.include(f'"{HEADER}"', codegen)
        self.include('<stdbool.h>', codegen)
        self.include('<stdlib.h>', codegen)
        self.include('<stdio.h>', codegen)
        self.include('<time.h>', codegen)
        self.includes.add('<windows.h>')
        self.includes.add('<io.h>')
        self.includes.add('<shlobj.h>')
        self.includes.add('<unistd.h>')
        
        self.init(codegen)
    
    def init(self, codegen) -> None:
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
        
        @c_dec(param_types=(Param('*', Type('*')),), can_user_call=True, add_to_class=self)
        def _print(codegen, call_position: Position, *args: Object) -> Object:
            fmt_vars = []
            for arg in args:
                repr_method = self.get_object(f'{arg.type.c_type}_to_string')
                if repr_method is None:
                    call_position.error_here(f'String representation for \'{arg.type}\' is not defined')
                
                fmt_vars.append(str(repr_method(codegen, call_position, arg)))
            
            fmt = ' '.join('%s' for _ in range(len(fmt_vars)))
            return Object(
                f'(printf("{fmt}\\n", {", ".join(fmt_vars)}))',
                Type('int'), call_position
            )
        
        @c_dec(param_types=(Param('x', Type('any')),), can_user_call=True, add_to_class=self)
        def _type(codegen, call_position: Position, x: Object) -> Object:
            type_method = self.get_object(f'{x.type.c_type}_type')
            if type_method is None:
                call_position.error_here(f'Type representation for \'{x.type}\' is not defined')
            
            return Object(
                str(type_method(codegen, call_position)),
                Type('string'), call_position
            )
        
        @c_dec(param_types=(Param('x', Type('any')),), can_user_call=True, add_to_class=self)
        def _to_string(codegen, call_position: Position, x: Object) -> Object:
            repr_method = self.get_object(f'{x.type.c_type}_to_string')
            if repr_method is None:
                call_position.error_here(f'String representation for \'{x.type}\' is not defined')

            return Object(
                str(repr_method(codegen, call_position, x)),
                Type('string'), call_position
            )
        
        def _input_no_prompt(codegen, call_position: Position) -> Object:
            return _input(codegen, call_position, None)
        
        @c_dec(
            param_types=(
                Param('prompt', Type('string'), default=Object('""', Type('string'), POS_ZERO)),
            ), can_user_call=True, add_to_class=self
        )
        def _input(codegen, call_position: Position, prompt: Object) -> Object:
            if prompt.code != '""':
                codegen.prepend_code(f'printf("%s", {prompt});')
            
            buf_size: TempVar = codegen.create_temp_var(Type('int'), call_position)
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            c: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""size_t {buf_size} = 128;
string {buf} = (string)malloc({buf_size});
{codegen.c_manager.buf_check(buf)}
size_t {length} = 0;
int {c};
while (({c} = getchar()) != '\\n' && {c} != EOF) {{
    if ({length} + 1 >= {buf_size}) {{
        {buf_size} *= 2;
        {buf} = (string)realloc({buf}, {buf_size});
        {codegen.c_manager.buf_check(buf)}
    }}
    
    {buf}[{length}++] = (char){c};
}}
{buf}[{length}] = '\\0';
""")
            
            return buf.OBJECT()
        
        @c_dec(param_types=(Param('x', Type('any')),), can_user_call=True, add_to_class=self)
        def _to_bool(_, call_position: Position, x: Object) -> Object:
            bool_method = self.get_object(f'{x.type.c_type}_to_bool')
            if bool_method is None:
                call_position.error_here(f'Boolean conversion for \'{x.type}\' is not defined')

            return Object(
                str(bool_method(codegen, call_position, x)),
                Type('bool'), call_position
            )
        
        @c_dec(param_types=(Param('object', Type('any')),), can_user_call=True, add_to_class=self)
        def _sizeof(_, call_position: Position, object: Object) -> Object:
            return Object(f'sizeof({object})', Type('int'), call_position)
        
        @c_dec(param_types=(Param('code', Type('string')),), can_user_call=True, add_to_class=self)
        def _insert_c_code(codegen, call_position: Position, code: Object) -> Object:
            if not codegen.is_string_literal(code):
                call_position.error_here('Inserting C code can only be done as a string literal')
            
            codegen.prepend_code(f'{str(code)[1:-1]};')
            return Object.NULL(call_position)
        
        @c_dec(param_types=(Param('var', Type('any')),), can_user_call=True, add_to_class=self)
        def _addr_of(codegen, call_position: Position, var: Object) -> Object:
            if codegen.is_identifier(var):
                return Object(f'&({var})', Type('hex'), call_position)
            else:
                call_position.error_here(f'Cannot get address of non-variable \'{var}\'')
        
        def char_int(codegen, call_position: Position, value: Object) -> Object:
            char: TempVar = codegen.create_temp_var(value.type, call_position)
            i = f'({value})'
            codegen.prepend_code(f"""if ({i} < 0 || {i} > 127) {{
{self.err('Character is not a valid ASCII character')}
}}

static char {char}[2];
{char}[0] = (char)({value});
{char}[1] = '\\0';
""")
            
            return char.OBJECT()
        
        @c_dec(param_types=(Param('value', Type('string')),), can_user_call=True, overloads={
            ((Param('value', Type('int')),), Type('string')): char_int
        }, add_to_class=self)
        def _get_char(codegen, call_position: Position, value: Object) -> Object:
            slen = _string_length(codegen, call_position, value)
            codegen.prepend_code(f"""if ({slen} > 1) {{
{self.err('String is not a single character')}
}}
""")
            
            return Object(f'((int)(({value})[0]))', Type('int'), call_position)
        
        def assert_err(codegen, call_position: Position, value: Object, string: Object) -> Object:
            if not codegen.is_string_literal(string):
                call_position.error_here('Assert error message must be a string literal')
            
            codegen.prepend_code(f'if (!{value}) {{ {self.err(str(string)[1:-1])} }}')
            return Object.NULL(call_position)
        
        @c_dec(param_types=(Param('condition', Type('bool')),), can_user_call=True, overloads={
            ((Param('condition', Type('bool')), Param('err', Type('string'))), Type('nil')): assert_err
        }, add_to_class=self)
        def _assert(codegen, call_position: Position, value: Object) -> Object:
            codegen.prepend_code(f'if (!{value}) {{ {self.err("Assertion failed")} }}')
            return Object.NULL(call_position)
        
        
        def _range_no_step(codegen, call_position: Position, start: Object,
                            end: Object) -> Object:
            return _range(
                codegen, call_position, start, end,
                Object('1', Type('int'), call_position)
            )
        
        def _range_no_start(codegen, call_position: Position, end: Object) -> Object:
            return _range_no_step(
                codegen, call_position, Object('0', Type('int'), call_position), end
            )
        
        @c_dec(
            param_types=(
                Param('start', Type('int'), default=Object('0', Type('int'), POS_ZERO)),
                Param('end', Type('int')),
                Param('step', Type('int'), default=Object('1', Type('int'), POS_ZERO))
            ), can_user_call=True, add_to_class=self, overloads={
                ((
                    Param('start', Type('int')),
                    Param('end', Type('int'))), Type('array[int]', 'int_array')
                ): _range_no_step,
                ((Param('start', Type('int')),), Type('array[int]', 'int_array')): _range_no_start
            }
        )
        def _range(codegen, call_position: Position, start: Object, end: Object,
                step: Object) -> Object:
            int_array: Type = codegen.array_manager.define_array(Type('int'))
            make_call: Object = codegen.call(f'{int_array.c_type}_make', [], call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""for (int {i} = ({start}); {i} < ({end}); {i} += ({step})) {{
""")
            codegen.prepend_code(f"""{codegen.call(
    f'{int_array.c_type}_add', [Arg(make_call), Arg(i.OBJECT())], call_position
)};
}}
""")
            
            return make_call
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _int_type(_, call_position: Position) -> Object:
            return Object('"int"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _float_type(_, call_position: Position) -> Object:
            return Object('"float"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _string_type(_, call_position: Position) -> Object:
            return Object('"string"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _bool_type(_, call_position: Position) -> Object:
            return Object('"bool"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _nil_type(_, call_position: Position) -> Object:
            return Object('"nil"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Math_type(_, call_position: Position) -> Object:
            return Object('"Math"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _System_type(_, call_position: Position) -> Object:
            return Object('"System"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Time_type(_, call_position: Position) -> Object:
            return Object('"Time"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Cure_type(_, call_position: Position) -> Object:
            return Object('"Cure"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Fraction_type(_, call_position: Position) -> Object:
            return Object('"Fraction"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Vector2_type(_, call_position: Position) -> Object:
            return Object('"Vector2"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _StringBuilder_type(_, call_position: Position) -> Object:
            return Object('"StringBuilder"', Type('string'), call_position)
        
        
        @c_dec(param_types=(Param('value', Type('int')),), is_method=True, add_to_class=self)
        def _int_to_string(codegen, call_position: Position, value: Object) -> Object:
            # integer to string length formula is: (int)((ceil(log10(num))+1)*sizeof(char))
            temp_var: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""static char {temp_var}[13];
snprintf({temp_var}, 13, "%d", ({value}));
""")
            
            return temp_var.OBJECT()
        
        @c_dec(param_types=(Param('value', Type('float')),), is_method=True, add_to_class=self)
        def _float_to_string(codegen, call_position: Position, value: Object) -> Object:
            temp_var: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""static char {temp_var}[47];
snprintf({temp_var}, 47, "%f", ({value}));
""")
            
            return temp_var.OBJECT()
        
        @c_dec(param_types=(Param('value', Type('string')),), add_to_class=self)
        def _string_to_string(_, _call_position: Position, value: Object) -> Object:
            return value
        
        @c_dec(param_types=(Param('value', Type('bool')),), is_method=True, add_to_class=self)
        def _bool_to_string(_, call_position: Position, value: Object) -> Object:
            return Object(f'(({value}) ? "true" : "false")', Type('string'), call_position)
        
        @c_dec(param_types=(Param('value', Type('nil')),), is_method=True, add_to_class=self)
        def _nil_to_string(codegen, call_position: Position, value: Object) -> Object:
            # prepend the code because it could be a function that returns nil
            # even if it is just a NULL value, the C compiler will optimize it out
            codegen.prepend_code(f'{value};')
            return Object('"nil"', Type('string'), call_position)
        
        @c_dec(
            param_types=(Param('value', Type('Math')),), is_method=True, is_static=True,
            add_to_class=self
        )
        def _Math_to_string(_, call_position: Position, _value: Object) -> Object:
            return Object('"class \'Math\'"', Type('string'), call_position)
        
        @c_dec(
            param_types=(Param('value', Type('System')),), is_method=True, is_static=True,
            add_to_class=self
        )
        def _System_to_string(_, call_position: Position, _value: Object) -> Object:
            return Object('"class \'System\'"', Type('string'), call_position)
        
        @c_dec(param_types=(Param('value', Type('Time')),), is_method=True, add_to_class=self)
        def _Time_to_string(codegen, call_position: Position, value: Object) -> Object:
            self.include('<string.h>', codegen)
            t = f'({value})'
            code, buf_free = self.fmt_length(
                codegen, call_position,
                '"Time(%s)"',
                f'asctime({t}.ti)'
            )
            
            codegen.prepend_code(f"""{code}
({buf_free.object_name})[strlen({buf_free.object_name}) - 1] = '\\0';
""")
            
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(
            param_types=(Param('value', Type('Cure')),), is_method=True, is_static=True,
            add_to_class=self
        )
        def _Cure_to_string(_, call_position: Position, _value: Object) -> Object:
            return Object('"class \'Cure\'"', Type('string'), call_position)
        
        @c_dec(param_types=(Param('value', Type('Fraction')),), is_method=True, add_to_class=self)
        def _Fraction_to_string(codegen, call_position: Position, value: Object) -> Object:
            code, buf_free = self.fmt_length(
                codegen, call_position, '"%d/%d"',
                f'({value}).top', f'({value}).bottom'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(param_types=(Param('value', Type('Vector2')),), is_method=True, add_to_class=self)
        def _Vector2_to_string(codegen, call_position: Position, value: Object) -> Object:
            code, buf_free = self.fmt_length(
                codegen, call_position, '"Vector2(x=%f, y=%f)"',
                f'({value}).x', f'({value}).y'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(param_types=(Param('value', Type('hex')),), is_method=True, add_to_class=self)
        def _hex_to_string(codegen, call_position: Position, value: Object) -> Object:
            code, buf_free = self.fmt_length(
                codegen, call_position,
                '"%p"', str(value)
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(param_types=(Param('value', Type('StringBuilder')),), is_method=True, add_to_class=self)
        def _StringBuilder_to_string(codegen, call_position: Position, value: Object) -> Object:
            code, buf_free = self.fmt_length(
                codegen, call_position,
                '"StringBuilder(length=%zu)"',
                f'({value}).length'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        
        @c_dec(param_types=(Param('value', Type('int')),), is_method=True, add_to_class=self)
        def _int_to_float(_, call_position: Position, value: Object) -> Object:
            return Object(f'((float)({value}))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('value', Type('float')),), is_method=True, add_to_class=self)
        def _float_to_int(_, call_position: Position, value: Object) -> Object:
            return Object(f'((int)({value}))', Type('int'), call_position)
        
        @c_dec(param_types=(Param('value', Type('string')),), is_method=True, add_to_class=self)
        def _string_to_int(_, call_position: Position, value: Object) -> Object:
            # TODO: Raise error if string is not a valid integer and fix undefined behaviour
            # overflow and underflow integers
            return Object(f'(atoi({value}))', Type('int'), call_position)
        
        @c_dec(param_types=(Param('value', Type('string')),), is_method=True, add_to_class=self)
        def _string_to_float(_, call_position: Position, value: Object) -> Object:
            # TODO: Raise error if string is not a valid float and fix undefined behaviour
            # overflow and underflow floats
            return Object(f'(atof({value}))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('value', Type('string')),), is_method=True, add_to_class=self)
        def _string_to_bool(_, call_position: Position, value: Object) -> Object:
            return Object(f'(({value}) == "true" ? true : false)', Type('bool'), call_position)

        @c_dec(param_types=(Param('value', Type('bool')),), is_method=True, add_to_class=self)
        def _bool_to_int(_, call_position: Position, value: Object) -> Object:
            return Object(f'(({value}) ? 1 : 0)', Type('int'), call_position)
        
        @c_dec(param_types=(Param('value', Type('bool')),), add_to_class=self)
        def _bool_to_bool(_, _call_position: Position, value: Object) -> Object:
            return value
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_add_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) + ({b}))', Type('int'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('float'))), add_to_class=self)
        def _int_add_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'((float)({a}) + ({b}))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('int'))), add_to_class=self)
        def _float_add_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) + (float)({b}))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_add_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) + ({b}))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('string')), Param('b', Type('string'))), add_to_class=self)
        def _string_add_string(codegen, call_position: Position, a: Object, b: Object) -> Object:
            self.include('<string.h>', codegen)
            
            buf_free = Free()
            buf_var: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            codegen.prepend_code(f"""string {buf_var} = (string)malloc(strlen({a}) + strlen({b}) + 1);
{codegen.c_manager.buf_check(buf_var)}
strcpy({buf_var}, {a});
strcat({buf_var}, {b});
""")
            
            return Object.STRINGBUF(buf_free, call_position)
        
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
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_sub_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) - ({b}))', Type('int'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('float'))), add_to_class=self)
        def _int_sub_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'((float)({a}) - ({b}))', Type('float'), call_position)

        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('int'))), add_to_class=self)
        def _float_sub_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) - (float)({b}))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_sub_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) - ({b}))', Type('float'), call_position)
        
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
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_mul_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) * ({b}))', Type('int'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('float'))), add_to_class=self)
        def _int_mul_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'((float)({a}) * ({b}))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('int'))), add_to_class=self)
        def _float_mul_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) * (float)({b}))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_mul_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) * ({b}))', Type('float'), call_position)
        
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
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_div_int( _, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'((float)(({a}) / ({b})))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('float'))), add_to_class=self)
        def _int_div_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'((float)({a}) / ({b}))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('int'))), add_to_class=self)
        def _float_div_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) / (float)({b}))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_div_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) / ({b}))', Type('float'), call_position)
        
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
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_mod_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) % ({b}))', Type('int'), call_position)

        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('float'))), add_to_class=self)
        def _int_mod_float(codegen, call_position: Position, a: Object, b: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'(fmodf((float)({a}), ({b})))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('int'))), add_to_class=self)
        def _float_mod_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(fmodf(({a}), (float)({b})))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_mod_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(fmodf(({a}), ({b}))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('string'))), add_to_class=self)
        def _int_mod_string(codegen, call_position: Position, a: Object, b: Object) -> Object:
            length = f'({a})'
            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free)
            current_length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {current_length} = {
    _string_length(codegen, call_position, b)
};
string {res} = (string)malloc({length} + 1);
{codegen.c_manager.buf_check(res)}
if ({length} > 0) {{
    if ({current_length} < {length}) {{
        free({res});
        {codegen.c_manager.err('Invalid string length')}
    }}
    
    for (size_t {i} = 0; {i} < {length}; {i}++) {{
        {res}[{i}] = {b}[{i}];
    }}

    {res}[{length}] = '\\0';
}} else {{
    free({res});
    {codegen.c_manager.err('Invalid string length')}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(param_types=(Param('a', Type('string')), Param('b', Type('int'))), add_to_class=self)
        def _string_mod_int(codegen, call_position: Position, a: Object, b: Object) -> Object:
            length = f'({b})'
            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free)
            current_length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {current_length} = {
    _string_length(codegen, call_position, a)
};
string {res} = (string)malloc({length} + 1);
{codegen.c_manager.buf_check(res)}
if ({length} > 0) {{
    if ({current_length} < {length}) {{
        {codegen.c_manager.err('Invalid string length')}
    }}

    strncpy({res}, ({a}) + ({current_length} - {length}), {length});
    {codegen.c_manager.buf_check(res)}
    {res}[{length}] = '\\0';
}} else {{
    free({res});
    {codegen.c_manager.err('Invalid string length')}
}}""")
            
            return res.OBJECT()
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_eq_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) == ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_eq_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) == ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('string')), Param('b', Type('string'))), add_to_class=self)
        def _string_eq_string(codegen, call_position: Position, a: Object, b: Object) -> Object:
            self.include('<string.h>', codegen)
            return Object(f'((strcmp({a}, {b}) == 0))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('bool')), Param('b', Type('bool'))), add_to_class=self)
        def _bool_eq_bool(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) == ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_neq_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) != ({b}))', Type('bool'), call_position)

        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_neq_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) != ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('string')), Param('b', Type('string'))), add_to_class=self)
        def _string_neq_string(codegen, call_position: Position, a: Object, b: Object) -> Object:
            self.include('<string.h>', codegen)
            return Object(f'((strcmp({a}, {b}) != 0))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('bool')), Param('b', Type('bool'))), add_to_class=self)
        def _bool_neq_bool(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) != ({b}))', Type('bool'), call_position)

        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_gt_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) > ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_gt_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) > ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('string')), Param('b', Type('string'))), add_to_class=self)
        def _string_gt_string(codegen, call_position: Position, a: Object, b: Object) -> Object:
            alen = _string_length(codegen, call_position, a)
            blen = _string_length(codegen, call_position, b)
            return Object(f'({alen} > {blen})', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_gte_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) >= ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_gte_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) >= ({b}))', Type('bool'), call_position)

        @c_dec(param_types=(Param('a', Type('string')), Param('b', Type('string'))), add_to_class=self)
        def _string_gte_string(codegen, call_position: Position, a: Object, b: Object) -> Object:
            alen = _string_length(codegen, call_position, a)
            blen = _string_length(codegen, call_position, b)
            return Object(f'({alen} >= {blen})', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_lt_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) < ({b}))', Type('bool'), call_position)

        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_lt_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) < ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('string')), Param('b', Type('string'))), add_to_class=self)
        def _string_lt_string(codegen, call_position: Position, a: Object, b: Object) -> Object:
            alen = _string_length(codegen, call_position, a)
            blen = _string_length(codegen, call_position, b)
            return Object(f'({alen} < {blen})', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_lte_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) <= ({b}))', Type('bool'), call_position)

        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_lte_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) <= ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('string')), Param('b', Type('string'))), add_to_class=self)
        def _string_lte_string(codegen, call_position: Position, a: Object, b: Object) -> Object:
            alen = _string_length(codegen, call_position, a)
            blen = _string_length(codegen, call_position, b)
            return Object(f'({alen} <= {blen})', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('bool')), Param('b', Type('bool'))), add_to_class=self)
        def _bool_and_bool(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) && ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('bool')), Param('b', Type('bool'))), add_to_class=self)
        def _bool_or_bool(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) || ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('bool')),), add_to_class=self)
        def _not_bool(_, call_position: Position, a: Object) -> Object:
            return Object(f'(!({a}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')),), add_to_class=self)
        def _sub_int(_, call_position: Position, a: Object) -> Object:
            return Object(f'(-({a}))', Type('int'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')),), add_to_class=self)
        def _add_int(_, call_position: Position, a: Object) -> Object:
            return Object(f'(+({a}))', Type('int'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')),), add_to_class=self)
        def _sub_float(_, call_position: Position, a: Object) -> Object:
            return Object(f'(-({a}))', Type('float'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')),), add_to_class=self)
        def _add_float(_, call_position: Position, a: Object) -> Object:
            return Object(f'(+({a}))', Type('float'), call_position)
        
        
        @c_dec(param_types=(Param('i', Type('int')),), is_property=True, add_to_class=self)
        def _int_humanize_size(codegen, call_position: Position, i: Object) -> Object:
            mag: TempVar = codegen.create_temp_var(Type('int'), call_position)
            x: TempVar = codegen.create_temp_var(Type('int'), call_position)
            abs_call: Object = _Math_abs(codegen, call_position, x.OBJECT())
            
            if 'sizeNames' not in self.RESERVED_NAMES:
                codegen.add_toplevel_code("""const string sizeNames[] = {
    "B", "KB", "MB", "GB", "TB", "PB"
};
""")
                self.RESERVED_NAMES.append('sizeNames')

            code, buf_free = self.fmt_length(codegen, call_position, '"%.4f%s"', str(x),
                                            f'sizeNames[{mag}]')
            codegen.prepend_code(f"""int {mag} = 0;
double {x} = (double){i};
while ({abs_call} >= 1024 && {mag} < (sizeof(sizeNames) / sizeof(sizeNames[0])) - 1) {{
    {x} /= 1024;
    {mag}++;
}}

{code}
""")
            
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(
            param_types=(
                Param('i', Type('int')),
                Param('precision', Type('int'), default=Object('5', Type('int'), POS_ZERO))
            ),
            is_method=True, add_to_class=self
        )
        def _int_science(codegen, call_position: Position, i: Object, precision: Object) -> Object:
            self.include('<math.h>', codegen)
            
            exponent: TempVar = codegen.create_temp_var(Type('int'), call_position)
            length: TempVar = codegen.create_temp_var(Type('int'), call_position)
            num: TempVar = codegen.create_temp_var(Type('float'), call_position)
            significand: TempVar = codegen.create_temp_var(Type('float'), call_position)
            code, buf_free = self.fmt_length(
                codegen, call_position, '"%.*fe%+03d"',
                str(precision), str(significand), str(exponent)
            )
            
            codegen.prepend_code(f"""int {exponent};
int {length};
double {num} = (double){i};
{exponent} = (int)floor(log10(fabs({num})));
double {significand} = {num} / pow(10.0, {exponent});
{code}
""")
            
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(param_types=(Param('f', Type('float')),), is_property=True, add_to_class=self)
        def _float_humanize_size(codegen, call_position: Position, f: Object) -> Object:
            return _int_humanize_size(codegen, call_position, f)
        
        @c_dec(
            param_types=(
                Param('f', Type('float')),
                Param('precision', Type('int'), default=Object('5', Type('int'), POS_ZERO))
            ),
            is_method=True, add_to_class=self
        )
        def _float_science(codegen, call_position: Position, f: Object, precision: Object) -> Object:
            return _int_science(codegen, call_position, f, precision)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_length(codegen, call_position: Position, s: Object) -> Object:
            self.include('<string.h>', codegen)
            return Object(f'((int)strlen({s}))', Type('int'), call_position)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_empty(codegen, call_position: Position, s: Object) -> Object:
            return Object(
                f'({_string_length(codegen, call_position, s)} == 0)',
                Type('bool'), call_position
            )
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_char(codegen, call_position: Position, s: Object) -> Object:
            return Object(
                f'({_string_length(codegen, call_position, s)} == 1)',
                Type('bool'), call_position
            )
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_digit(codegen, call_position: Position, s: Object) -> Object:
            self.include('<string.h>', codegen)
            self.include('<ctype.h>', codegen)
            
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!isdigit(({s})[{i}])) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_lower(codegen, call_position: Position, s: Object) -> Object:
            self.include('<string.h>', codegen)
            self.include('<ctype.h>', codegen)
            
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!islower(({s})[{i}])) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(param_types=(Param('s', Type('string')),), is_property=True, add_to_class=self)
        def _string_is_upper(codegen, call_position: Position, s: Object) -> Object:
            self.include('<string.h>', codegen)
            self.include('<ctype.h>', codegen)

            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""bool {res} = true;
for (int {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (!isupper(({s})[{i}])) {{
        {res} = false;
        break;
    }}
}}
""")
            
            return res.OBJECT()
        
        @c_dec(param_types=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_lower(codegen, call_position: Position, s: Object) -> Object:
            self.include('<string.h>', codegen)
            self.include('<ctype.h>', codegen)
            
            strlen = _string_length(codegen, call_position, s)
            
            temp_free = Free()
            temp_var: TempVar = codegen.create_temp_var(Type('string'), call_position, free=temp_free)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""string {temp_var} = (string)malloc({strlen} + 1);
{codegen.c_manager.buf_check(temp_var)}
for (size_t {i} = 0; {i} < {strlen}; {i}++)
    {temp_var}[{i}] = tolower({s}[{i}]);
{temp_var}[{strlen}] = '\\0';
""")
            
            return Object.STRINGBUF(temp_free, call_position)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_upper(codegen, call_position: Position, s: Object) -> Object:
            self.include('<string.h>', codegen)
            self.include('<ctype.h>', codegen)

            strlen = _string_length(codegen, call_position, s)

            temp_free = Free()
            temp_var: TempVar = codegen.create_temp_var(Type('string'), call_position, free=temp_free)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""string {temp_var} = (string)malloc({strlen} + 1);
{codegen.c_manager.buf_check(temp_var)}
for (size_t {i} = 0; {i} < {strlen}; {i}++)
    {temp_var}[{i}] = toupper({s}[{i}]);
{temp_var}[{strlen}] = '\\0';
""")

            return Object.STRINGBUF(temp_free, call_position)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_title(codegen, call_position: Position, s: Object) -> Object:
            self.include('<string.h>', codegen)
            self.include('<ctype.h>', codegen)
            
            temp_free = Free()
            temp_var: TempVar = codegen.create_temp_var(Type('string'), call_position, free=temp_free)
            lv: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""string {temp_var} = strdup({s});
{codegen.c_manager.buf_check(temp_var)}
for (string {lv} = {temp_var}; *{lv} != '\\0'; ++{lv})
    *{lv} = ({lv} == {temp_var} || *({lv} - 1) == ' ') ? toupper(*{lv}) : tolower(*{lv});
""")
            
            return Object.STRINGBUF(temp_free, call_position)
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('prefix', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _string_startswith(codegen, call_position: Position, s: Object, prefix: Object) -> Object:
            self.include('<string.h>', codegen)

            return Object(
                f'(strncmp({s}, {prefix}, {_string_length(codegen, call_position, prefix)}) == 0)',
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('suffix', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _string_endswith(codegen, call_position: Position, s: Object, suffix: Object) -> Object:
            self.include('<string.h>', codegen)
            
            su = str(suffix)
            slen: TempVar = codegen.create_temp_var(Type('int'), call_position)
            suffix_len: TempVar = _string_length(codegen, call_position, suffix)
            sulen: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""size_t {slen} = {_string_length(codegen, call_position, s)};
size_t {sulen} = {suffix_len};
""")
            return Object(
                f"""({slen} < {sulen} ? false : (strncmp(
                    ({s}) + {slen} - {sulen}, {su}, {sulen}) == 0)
                )""",
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('index', Type('int'))),
            is_method=True, add_to_class=self
        )
        def _string_at(codegen, call_position: Position, s: Object, index: Object) -> Object:
            self.include('<string.h>', codegen)
            
            strlen = _string_length(codegen, call_position, s)
            temp_var: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""if (({index}) > {strlen} - 1) {{
    {self.err('Index out of bounds on string')}
}}
static char {temp_var}[2];
{temp_var}[0] = ({s})[{index}];
{temp_var}[1] = '\\0';
""")
            
            return temp_var.OBJECT()
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('substr', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _string_has(codegen, call_position: Position, s: Object, substr: Object) -> Object:
            self.include('<string.h>', codegen)
            return Object(
                f'(strstr({s}, {substr}) != NULL)',
                Type('bool'), call_position
            )
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('arr', Type('array[string]', 'string_array'))),
            is_method=True, add_to_class=self
        )
        def _string_join(codegen, call_position: Position, s: Object, arr: Object) -> Object:
            self.include('<string.h>', codegen)
            
            tlen: TempVar = codegen.create_temp_var(Type('int'), call_position)
            sep_len: TempVar = codegen.create_temp_var(Type('int'), call_position)
            res_free = Free()
            res: TempVar = codegen.create_temp_var(Type('string'), call_position, free=res_free)
            count: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            a = f'({arr})'
            codegen.prepend_code(f"""size_t {tlen} = 0;
size_t {sep_len} = {_string_length(codegen, call_position, s)};
int {count} = 0;
for (int {i} = 0; {i} < {a}.length; {i}++) {{
    {tlen} += {_string_length(
    codegen, call_position, Object(f'{a}.elements[{i}]', Type('string'), call_position)
)};
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
        strcat({res}, {s});
    }}
    strcat({res}, {a}.elements[{i}]);
}}
""")
            
            return Object.STRINGBUF(res_free, call_position)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_parse_int(codegen, call_position: Position, s: Object) -> Object:
            return _string_to_int(codegen, call_position, s)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_parse_float(codegen, call_position: Position, s: Object) -> Object:
            return _string_to_float(codegen, call_position, s)
        
        @c_dec(param_types=(Param('s', Type('string')),), is_method=True, add_to_class=self)
        def _string_parse_bool(codegen, call_position: Position, string: Object) -> Object:
            return _string_to_bool(codegen, call_position, string)
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('substr', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _string_find(codegen, call_position: Position, s: Object, substring: Object) -> Object:
            self.include('<string.h>', codegen)
            idx: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {idx} = -1;
for (size_t {i} = 0; {i} < {_string_length(codegen, call_position, s)}; {i}++) {{
    if (strncmp(
        {s} + {i},
        {substring},
        {_string_length(codegen, call_position, substring)}
    ) == 0) {{
        {idx} = {i};
        break;
    }}
}}
""")
            
            return idx.OBJECT()
        
        @c_dec(
            param_types=(
                Param('s', Type('string')), Param('start', Type('int')), Param('end', Type('int'))
            ), is_method=True, add_to_class=self
        )
        def _string_slice(codegen, call_position: Position, s: Object, start: Object,
                          end: Object) -> Object:
            self.include('<string.h>', codegen)
            buf_free = Free()
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position, free=buf_free)
            start_var: TempVar = codegen.create_temp_var(Type('int'), call_position)
            end_var: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""string {buf} = NULL;
int {start_var} = {start};
int {end_var} = {end};
if ({start_var} < 0 || {end_var} < 0) {{
    {self.err('Index out of bounds on string slice')}
}} else if ({start_var} > {end_var}) {{
    {self.err('Start index must be less than end index')}
}}

{buf} = (string)malloc({end_var} - {start_var} + 1);
{self.buf_check(str(buf))}
strncpy({buf}, ({s}) + {start_var}, {end_var} - {start_var} + 1);
{buf}[{end_var} - {start_var} + 1] = '\\0';
""")
            
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('*', Type('*'))),
            is_method=True, add_to_class=self
        )
        def _string_format(codegen, call_position: Position, s: Object, *args: Object) -> Object:
            code, buf_free = self.fmt_length(
                codegen, call_position, str(s),
                *[str(arg) for arg in args]
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(
            param_types=(Param('s', Type('string')), Param('i', Type('int'))),
            return_type=Type('string'), add_to_class=self
        )
        def _iter_string(codegen, call_position: Position, string: Object, i: Object) -> Object:
            self.include('<string.h>', codegen)
            return _string_at(codegen, call_position, string, i)
        
        @c_dec(param_types=(Param('s', Type('string')), Param('i', Type('int'))), add_to_class=self)
        def _index_string(codegen, call_position: Position, string: Object, i: Object) -> Object:
            self.include('<string.h>', codegen)
            return _string_at(codegen, call_position, string, i)
        
        
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
            ((Param('x', Type('int')),), Type('int')): Math_absint
        }, add_to_class=self)
        def _Math_abs(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)fabsf({x}))', Type('float'), call_position)
        
        def rand_start0(codegen, call_position: Position, max: Object) -> Object:
            return _Math_random(codegen, call_position, Object('0', Type('int'), call_position), max)
        
        @c_dec(
            param_types=(Param('min', Type('int')), Param('max', Type('int'))),
            is_method=True, is_static=True, add_to_class=self, overloads={
                ((Param('max', Type('int')),), Type('int')): rand_start0
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
                f'((rand() % ({hi_num} - {low_num})) + {low_num})',
                Type('int'), call_position
            )
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_sin(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'(sinf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_cos(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)cosf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_tan(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)tanf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_asin(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)asinf({x}))', Type('float'), call_position)

        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_acos(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)acosf({x}))', Type('float'), call_position)

        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_atan(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)atanf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('y', Type('float')), Param('x', Type('float'))),
            is_method=True, is_static=True, add_to_class=self,
            overloads={
                ((Param('y', Type('int')), Param('x', Type('int'))), Type('float')): None,
                ((Param('y', Type('int')), Param('x', Type('float'))), Type('float')): None,
                ((Param('y', Type('float')), Param('x', Type('int'))), Type('float')): None
            }
        )
        def _Math_atan2(codegen, call_position: Position, y: Object, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)atan2f({y}, {x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_sqrt(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)sqrtf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')), Param('n', Type('float'))),
            is_method=True, is_static=True, add_to_class=self,
            overloads={
                ((Param('x', Type('int')), Param('n', Type('int'))), Type('float')): None,
                ((Param('x', Type('int')), Param('n', Type('float'))), Type('float')): None,
                ((Param('x', Type('float')), Param('n', Type('int'))), Type('float')): None
            }
        )
        def _Math_nth_root(codegen, call_position: Position, x: Object, n: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)powf({x}, 1.0f / ({n})))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')), Param('y', Type('float'))),
            is_method=True, is_static=True, add_to_class=self,
            overloads={
                ((Param('x', Type('int')), Param('y', Type('int'))), Type('float')): None,
                ((Param('x', Type('int')), Param('y', Type('float'))), Type('float')): None,
                ((Param('x', Type('float')), Param('y', Type('int'))), Type('float')): None
            }
        )
        def _Math_pow(codegen, call_position: Position, x: Object, y: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)powf({x}, {y}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_log(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)logf({x}))', Type('float'), call_position)

        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_log10(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)log10f({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_log2(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)log2f({x}))', Type('float'), call_position)

        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_exp(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)expf({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Math_ceil(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((int)ceilf({x}))', Type('int'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Math_floor(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((int)floorf({x}))', Type('int'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Math_round(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((int)roundf({x}))', Type('int'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')), Param('y', Type('float'))),
            is_method=True, is_static=True, add_to_class=self,
            overloads={
                ((Param('x', Type('int')), Param('y', Type('int'))), Type('int')): None,
                ((Param('x', Type('int')), Param('y', Type('float'))), Type('float')): None,
                ((Param('x', Type('float')), Param('y', Type('int'))), Type('float')): None
            }
        )
        def _Math_min(codegen, call_position: Position, x: Object, y: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(
                f'(({x}) < ({y}) ? ({x}) : ({y}))',
                Type('int') if x.type == Type('int') and y.type == Type('int') else Type('float'),
                call_position
            )
        
        @c_dec(
            param_types=(Param('x', Type('float')), Param('y', Type('float'))),
            is_method=True, is_static=True, add_to_class=self,
            overloads={
                ((Param('x', Type('int')), Param('y', Type('int'))), Type('int')): None,
                ((Param('x', Type('int')), Param('y', Type('float'))), Type('float')): None,
                ((Param('x', Type('float')), Param('y', Type('int'))), Type('float')): None
            }
        )
        def _Math_max(codegen, call_position: Position, x: Object, y: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(
                f'(({x}) < ({y}) ? ({y}) : ({x}))',
                Type('int') if x.type == Type('int') and y.type == Type('int') else Type('float'),
                call_position
            )
        
        @c_dec(
            param_types=(Param('deg', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('deg', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_rad(codegen, call_position: Position, deg: Object) -> Object:
            self.include('<math.h>', codegen)
            pi = _Math_pi(codegen, call_position)
            return Object(f'((float)({deg}) * {pi} / 180.0f)', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('rad', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('rad', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_deg(codegen, call_position: Position, rad: Object) -> Object:
            self.include('<math.h>', codegen)
            pi = _Math_pi(codegen, call_position)
            return Object(f'((float)({rad}) * 180.0f / {pi})', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_sinh(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)sinh({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_cosh(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)cosh({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')),), is_method=True, is_static=True,
            overloads={((Param('x', Type('int')),), Type('float')): None}, add_to_class=self
        )
        def _Math_tanh(codegen, call_position: Position, x: Object) -> Object:
            self.include('<math.h>', codegen)
            return Object(f'((float)tanh({x}))', Type('float'), call_position)
        
        @c_dec(
            param_types=(Param('x', Type('float')), Param('y', Type('float'))),
            is_method=True, is_static=True, add_to_class=self,
            overloads={
                ((Param('x', Type('int')), Param('y', Type('int'))), Type('float')): None,
                ((Param('x', Type('int')), Param('y', Type('float'))), Type('float')): None,
                ((Param('x', Type('float')), Param('y', Type('int'))), Type('float')): None
            }
        )
        def _Math_copysign(codegen, call_position: Position, x: Object, y: Object) -> Object:
            self.include('<math.h>', codegen)
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

        
        self.wrap_struct_properties('frac', Type('Fraction'), [
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
        
        
        self.wrap_struct_properties('vec', Type('Vector2'), [
            Param('x', Type('float')), Param('y', Type('float'))
        ])
        
        @c_dec(param_types=(Param('vec', Type('Vector2')),), is_property=True, add_to_class=self)
        def _Vector2_length(_, call_position: Position, vec: Object) -> Object:
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


        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_pid(codegen, call_position: Position) -> Object:
            pid_var: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""#ifdef OS_WINDOWS
int {pid_var} = (int)GetCurrentProcessId();
#else
int {pid_var} = (int)getpid();
#endif
""")
            
            return pid_var.OBJECT()
        
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
            sysinfo: TempVar = codegen.create_temp_var(Type('SystemInfo'), call_position)
            codegen.prepend_code(f"""#ifdef OS_WINDOWS
SYSTEM_INFO {sysinfo};
GetSystemInfo(&{sysinfo});
#else
{self.symbol_not_supported('System.processor_count')}
#endif
""")
            
            return Object(f'((int){sysinfo}.dwNumberOfProcessors)', Type('int'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_cwd(codegen, call_position: Position) -> Object:
            cwd_var: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""char {cwd_var}[1024];
#ifdef OS_WINDOWS
if (GetCurrentDirectory(sizeof({cwd_var}), {cwd_var}) == 0) {{
    {self.err('Failed to get current working directory')}
}}
#else
if (getcwd({cwd_var}, sizeof({cwd_var})) == NULL) {{
    {self.err('Failed to get current working directory')}
}}
#endif
""")
            
            return cwd_var.OBJECT()
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_time(codegen, call_position: Position) -> Object:
            t: TempVar = codegen.create_temp_var(Type('TimeInt', 'time_t'), call_position)
            codegen.prepend_code(f'time_t {t} = time(NULL);')
            return Object(f'(Time){{ .t = {t}, .ti = localtime(&{t}) }}', Type('Time'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _System_cursor_pos(codegen, call_position: Position) -> Object:
            point: TempVar = codegen.create_temp_var(Type('POINT'), call_position)
            codegen.prepend_code(f"""#ifdef OS_WINDOWS
POINT {point};
GetCursorPos(&{point});
#else
{self.symbol_not_supported('System.cursor_pos')}
#endif
""")
            
            return _Math_vec2(
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
            param_types=(Param('code', Type('int'), default=Object('0', Type('int'), POS_ZERO)),),
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
            codegen.prepend_code(f"""#ifdef OS_WINDOWS
Sleep({milliseconds});
#elif defined(OS_LINUX) | defined(OS_MACOS)
usleep({milliseconds} * 1000);
#else
{self.symbol_not_supported('System.sleep')}
#endif
""")
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
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _System_unblock_keyboard(codegen, call_position: Position) -> Object:
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
        
        @c_dec(
            param_types=(Param('char', Type('string')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _System_is_key_pressed(codegen, call_position: Position, char: Object) -> Object:
            is_pressed: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            codegen.prepend_code(f"""if (!{_string_is_char(codegen, call_position, char)}) {{
    {self.err('Key must be a single character')}
}}

#ifdef OS_WINDOWS
bool {is_pressed} = (bool)(GetAsyncKeyState((int)({char})[0] & 0x8000));
#else
{self.symbol_not_supported('System.is_key_pressed')}
#endif
""")
            
            return is_pressed.OBJECT()
        
        def Sscp_intint(codegen, call_position: Position,
                                        x: Object, y: Object) -> Object:
            codegen.prepend_code(f"""#ifdef OS_WINDOWS
SetCursorPos({x}, {y});
#else
{self.symbol_not_supported('System.set_cursor_pos')}
#endif
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            param_types=(Param('vec', Type('Vector2')),),
            is_method=True, is_static=True, add_to_class=self, overloads={
                ((Param('x', Type('int')), Param('y', Type('int'))), Type('nil')): Sscp_intint
            }
        )
        def _System_set_cursor_pos(codegen, call_position: Position, vec: Object) -> Object:
            codegen.prepend_code(f"""#ifdef OS_WINDOWS
SetCursorPos(({vec}).x, ({vec}).y);
#else
{self.symbol_not_supported('System.set_cursor_pos')}
#endif
""")
            
            return Object.NULL(call_position)


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
        
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _Cure_version(_, call_position: Position) -> Object:
            return Object('(VERSION)', Type('string'), call_position)
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _Cure_flags(codegen, call_position: Position) -> Object:
            return self.c_array_from_list(codegen, call_position, Type('string'), [
                Object(f'"{flag}"', Type('string'), call_position)
                for flag in codegen.extra_compile_args
            ])
        
        @c_dec(is_property=True, is_static=True, add_to_class=self)
        def _Cure_dependencies(codegen, call_position: Position) -> Object:
            return self.c_array_from_list(codegen, call_position, Type('string'), [
                Object(dep if dep.startswith('"') else f'"{dep}"', Type('string'), call_position)
                for dep in self.includes
            ])
        
        @c_dec(
            param_types=(Param('src', Type('string')),),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Cure_compile(codegen, call_position: Position, src: Object) -> Object:
            from codegen import str_to_c
            if not codegen.is_string_literal(str(src)):
                call_position.error_here('Source code must be a string literal')
            
            _, code = str_to_c(str(src)[1:-1], codegen.scope)
            codegen.prepend_code(code)
            return Object.NULL(call_position)
        
        
        self.wrap_struct_properties('builder', Type('StringBuilder'), [
            Param('length', Type('int')), Param('capacity', Type('int'))
        ])
        
        @c_dec(
            param_types=(Param('builder', Type('StringBuilder')),),
            is_property=True, add_to_class=self
        )
        def _StringBuilder_str(codegen, call_position: Position, obj: Object) -> Object:
            buf: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""string {buf} = ({obj}).buf;
{buf}[({obj}).length] = '\\0';
""")
            
            return buf.OBJECT()
        
        @c_dec(
            param_types=(Param('builder', Type('StringBuilder')), Param('s', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _StringBuilder_add(codegen, call_position: Position, builder: Object, s: Object) -> Object:
            slen = _string_length(codegen, call_position, s)
            lvar: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""size_t {lvar} = {slen};
if (({builder}).capacity - ({builder}).length < {lvar}) {{
    ({builder}).capacity *= 2;
    ({builder}).buf = (string)realloc(({builder}).buf, ({builder}).capacity);
}}

memcpy(({builder}).buf + ({builder}).length, {s}, {lvar});
({builder}).length += {lvar};
""")
            
            return Object.NULL(call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _StringBuilder_new(codegen, call_position: Position) -> Object:
            obj_free = Free()
            obj: TempVar = codegen.create_temp_var(Type('StringBuilder'), call_position, free=obj_free)
            obj_free.object_name = f'{obj}.buf'
            
            codegen.prepend_code(f"""StringBuilder {obj} = {{
    .buf = (string)malloc({STRINGBUILDER_CAPACITY}), .capacity = {STRINGBUILDER_CAPACITY},
    .length = 0
}};
{self.buf_check(f'{obj}.buf')}
""")
            
            return obj.OBJECT()
    
        
        @func_modification(params=(Param('message', Type('string')),), add_to_class=self)
        def _Info(codegen, _func_obj: Function, call_position: Position, _args: list[Arg],
                msg: Object) -> None:
            if not codegen.is_string_literal(msg):
                call_position.error_here('Info message must be a string literal')

            call_position.info_here(str(msg)[1:-1])
    
        @func_modification(params=(Param('message', Type('string')),), add_to_class=self)
        def _Warn(codegen, _func_obj: Function, call_position: Position, _args: list[Arg],
                msg: Object) -> None:
            if not codegen.is_string_literal(msg):
                call_position.error_here('Warning message must be a string literal')
            
            call_position.warn_here(str(msg)[1:-1])

        @func_modification(params=(Param('message', Type('string')),), add_to_class=self)
        def _Error(codegen, _func_obj: Function, call_position: Position, _args: list[Arg],
                msg: Object) -> None:
            if not codegen.is_string_literal(msg):
                call_position.error_here('Error message must be a string literal')
            
            call_position.error_here(str(msg)[1:-1])
        
        @func_modification(add_to_class=self)
        def _Benchmark(codegen, func_obj: Function, call_position: Position, _args: list[Arg]) -> None:
            begin: TempVar = codegen.create_temp_var(Type('int', 'clock_t'), call_position)
            end: TempVar = codegen.create_temp_var(Type('int', 'clock_t'), call_position)
            codegen.prepend_code(f'clock_t {begin} = clock();\n')
            codegen.append_code(f"""clock_t {end} = clock();
printf(
    "Time spent to execute '{func_obj.name}': %f seconds\\n",
    ((double)({end} - {begin})) / CLOCKS_PER_SEC
);
""")
        
        @func_modification(add_to_class=self)
        def _Cache(codegen, func_obj: Function, call_position: Position, args: list[Arg]) -> Object:
            func_params = func_obj.params
            cache_struct_type = Type(f'cache_dict_{func_obj.name}')
            cache_key = f'cacheof_{func_obj.name}'
            global_scope = codegen.scope.toplevel
            previously_called = global_scope.env.get(cache_key) is not None
            if not previously_called:
                codegen.c_manager.RESERVED_NAMES.extend((cache_key, cache_struct_type.c_type))
                global_scope.env[cache_key] = EnvItem(
                    cache_key, cache_struct_type, call_position, reserved=True
                )
                
                codegen.add_toplevel_code(f"""typedef struct {{
    {func_obj.return_type.c_type} res;
    {'\n'.join(str(param) + ';' for param in func_params)}
}} {cache_struct_type.c_type};
""")
                
                @c_dec(
                    param_types=(Param('a', cache_struct_type), Param('b', cache_struct_type)),
                    add_to_class=codegen.c_manager,
                    func_name_override=f'{cache_struct_type.c_type}_eq_{cache_struct_type.c_type}'
                )
                def cache_compare(codegen, call_position: Position, a: Object, b: Object) -> Object:
                    res: TempVar = codegen.create_temp_var(Type('bool'), call_position)
                    codegen.prepend_code(f'bool {res} = true;')
                    for param in func_params:
                        codegen.prepend_code(f"""if ({a}.{param.name} != {b}.{param.name}) {{
    {res} = false;
}}
""")
                    
                    return res.OBJECT()
                
            array_type: Type = codegen.array_manager.define_array(cache_struct_type)
            
            if not previously_called:
                codegen.add_toplevel_code(f'{array_type.c_type}* {cache_key} = NULL;')
                codegen.main_end_code += f'free({cache_key}->elements);\n'
            
            res: TempVar = codegen.create_temp_var(func_obj.return_type, call_position)
            cache_signature: TempVar = codegen.create_temp_var(cache_struct_type, call_position)
            has_cached: TempVar = codegen.create_temp_var(Type('bool'), call_position)
            idx: TempVar = codegen.create_temp_var(Type('int'), call_position)
            
            codegen.prepend_code(f"""{func_obj.return_type.c_type} {res};
bool {has_cached} = false;
{cache_struct_type.c_type} {cache_signature} = {{
    {''.join(f'.{param.name} = {arg.value}, ' for param, arg in zip(func_params, args))}
}};
if ({cache_key} == NULL) {{
""")
            codegen.prepend_code(f"""
    {cache_key} = &{(make_call := codegen.call(f'{array_type.c_type}_make', [], call_position))};
}} else {{
""")
            codegen.scope.remove_free(make_call.free)
            codegen.scope.env[str(make_call)].free = None
            codegen.prepend_code(f"""int {idx} = {codegen.call(f'{array_type.c_type}_find', [
    Arg(Object(f'(*{cache_key})', array_type, call_position)),
    Arg(cache_signature.OBJECT())
], call_position)};
    if ({idx} != -1) {{
        {res} = {cache_key}->elements[{idx}].res;
        {has_cached} = true;
    }}
}}

if (!{has_cached}) {{
    {res} = {func_obj.name}({", ".join(str(arg.value) for arg in args)});
    {cache_signature}.res = {res};
""")
            codegen.prepend_code(f"""{codegen.call(
        f'{array_type.c_type}_add',
        [
            Arg(Object(f'(*{cache_key})', array_type, call_position)),
            Arg(cache_signature.OBJECT())
        ], call_position
    )};
}}
""")
            
            return res.OBJECT()
        
        @func_modification(params=(Param('transformer', Type('function')),), add_to_class=self)
        def _Transform(codegen, func_obj: Function, call_position: Position, args: list[Arg],
                       transformer: Object) -> Object:
            func = codegen.scope.env[func_obj.name]
            if func.func is not None:
                func = func.func
            
            tname = transformer.code
            transformer_func = codegen.scope.env.get(tname)
            if transformer_func is None:
                call_position.error_here(f'Unknown transformer function \'{tname}\'')
            
            transformer_func = transformer_func.func
            if transformer_func is None:
                call_position.error_here(f'Invalid transformer \'{tname}\': not a function')
            elif len(transformer_func.params) != 1:
                call_position.error_here(
                    f'Invalid transformer \'{tname}\': expected exactly 1 parameter'
                )
            elif transformer_func.params[0].type != func_obj.return_type:
                call_position.error_here(
                    f'Invalid transformer \'{tname}\': function return type does not match'\
                        'transformer parameter'
                )
            elif transformer_func.return_type != func_obj.return_type:
                call_position.error_here(
                    f'Invalid transformer \'{tname}\': function return type does not match'\
                        'transformer return type'
                )
            
            res: TempVar = codegen.create_temp_var(func_obj.return_type, call_position)
            codegen.prepend_code(f"""{func_obj.return_type.c_type} {res} = {func_obj.name}({
    ', '.join(str(arg.value) for arg in args)
});
""")
            
            return codegen.call(transformer.code, [Arg(res.OBJECT())], call_position)
        
#         @func_modification(
#             params=(Param('limit', Type('int')), Param('time', Type('int'))), add_to_class=self
#         )
#         def _RateLimit(codegen, func_obj: Function, call_position: Position, args: list[Arg],
#                        limit: Object, time: Object) -> None:
#             global_scope = codegen.scope.toplevel
#             time_since_call = f'{func_obj.name}_time_since_last_call'
#             call_count = f'{func_obj.name}_call_count'
#             previously_called = global_scope.env.get(time_since_call) is not None
#             if not previously_called:
#                 codegen.c_manager.RESERVED_NAMES.extend((call_count, time_since_call))
#                 global_scope.env[time_since_call] = EnvItem(
#                     time_since_call, Type('int', 'time_t'), call_position
#                 )
                
#                 global_scope.env[call_count] = EnvItem(call_count, Type('int'), call_position)
                
#                 codegen.add_toplevel_code(f"""time_t {time_since_call} = 0;
# int {call_count} = 0;
# """)
            
#             difftime: TempVar = codegen.create_temp_var(Type('int', 'time_t'), call_position)
#             codegen.prepend_code(f"""double {difftime} = difftime(time(NULL), {time_since_call});
# if ({difftime} < {time_since_call}) {{
#     {time_since_call} = 0;
#     {call_count} = 0;
# }}

# if ({call_count} > {limit}) {{
#     {codegen.c_manager.err(f'\'{func_obj.name}\' exceeded rate call limit')}
# }}
# """)
#             codegen.append_code(f"""{call_count}++;
# """)
