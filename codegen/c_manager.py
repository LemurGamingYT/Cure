from typing import Callable, Any, Iterable
from functools import wraps
from pathlib import Path

from colorama import Fore

from codegen.function_manager import (
    Overloads, BuiltinFunction, UserFunction, OverloadKey, OverloadValue
)
from codegen.objects import Object, Position, EnvItem, Free, Type, TempVar, POS_ZERO, Arg, Param


CURRENT_FILE = Path(__file__).absolute()
STD_PATH = CURRENT_FILE.parent / 'std'
INCLUDES = CURRENT_FILE.parent.parent / 'include'
LIBS = CURRENT_FILE.parent.parent / 'libs'
HEADER = (INCLUDES / 'header.h').as_posix()


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
    add_to_class: Any = None,
    generic_params: tuple[str, ...] | None = None
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
        generic_params (tuple[str, ...] | None, optional): The generic parameters. Defaults to
            an empty tuple.

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
        
        def get_kwargs(args: tuple[Object, ...]) -> dict:
            return {k.name: v for k, v in zip(param_types, args)}
        
        setattr(func, 'name', cname)
        setattr(func, 'is_method', is_method)
        setattr(func, 'is_static', is_static)
        setattr(func, 'is_property', is_property)
        setattr(func, 'return_type', return_type)
        setattr(func, 'can_user_call', can_user_call)
        setattr(func, 'get_kwargs', get_kwargs)
        setattr(func, 'object', BuiltinFunction(
            func, return_type, list(param_types), overloads,
            generic_params=list(generic_params) if generic_params is not None else []
        ))
        
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
    RESERVED_NAMES = {
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
        'Vector2', 'StringBuilder', '__cplusplus'
    }
    
    
    def reserve(self, name_or_names: str | Iterable[str]) -> None:
        if isinstance(name_or_names, str):
            self.RESERVED_NAMES.add(name_or_names)
        elif isinstance(name_or_names, Iterable):
            for name in name_or_names:
                self.reserve(name)
    
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
        
        def fix(s: str) -> str:
            return s.replace('"', '\\"').replace('\n', '\\n')
        
        vars_str = ', '.join(variables)
        vars_str = '' if vars_str == '' else ', ' + vars_str
        content = fix(fr'{self.codegen.pos.get_print_content(Fore.RED, f'{fmt}\\n')}')
        return f"""printf("{content}"{vars_str});
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
            size_expr: (str, optional): The size expression of the C array. If None, the size will be
            calculated as the size of the C array divided by the size of the type of the C array.

        Returns:
            tuple[str, TempVar]: The code to convert the C array to a Cure array and the variable of the
            created array.
        """
        
        array_type: Type = codegen.array_manager.define_array(type)
        
        arr: TempVar = codegen.create_temp_var(array_type, pos)
        i: TempVar = codegen.create_temp_var(Type('int'), pos)
        length: TempVar = codegen.create_temp_var(Type('int'), pos)
        expr = f'sizeof({value}) / sizeof({value}[0])' if size_expr is None else size_expr
        return f"""int {length} = {expr};
{array_type.c_type} {arr} = {{ .length = 0, .capacity = 0, .elements = NULL }};
if ({length} > 1) {{
    {arr} = ({array_type.c_type}){{
        .length = 0, .capacity = {length},
        .elements = ({type.c_type}*)malloc(sizeof({type.c_type}) * {length})
    }};
    {self.buf_check(f'{arr}.elements')}
    for (int {i} = 0; {i} < {length}; {i}++) {{
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
    
    def wrap_struct_properties(self, struct_name: str, struct: Type, names: list[Param],
                               sub_field: str | None = None) -> None:
        """Wrap properties from a struct into the programming language.

        Args:
            struct_name (str): The struct's name.
            struct (Type): The struct type.
            names (list[Param]): The struct's fields to wrap.
            sub_field (str, optional): The field to get the struct properties from. For example,
                struct.a.b (`a` would be this parameter here). You also need to add the `->` or
                `.` after the field name `->` if the field is a pointer and `.` if not.
        """
        
        sub_field = '' if sub_field is None else f'{sub_field}'
        
        for name in names:
            @c_dec(
                param_types=(Param(struct_name, struct),), is_property=True, add_to_class=self,
                func_name_override=f'{struct.c_type}_{name.name}'
            )
            def _(_, call_position: Position, obj: Object, n=name) -> Object:
                return Object(
                    f'(({n.type.c_type})(({obj}).{sub_field}{n.name}))',
                    n.type, call_position
                )
    
    def init_class(self, parent, name: str, type: Type) -> None:
        """Initialises the default type and to_string methods on a class type.

        Args:
            parent (type): The class to add the c declarations to.
            name (str): The name of the class.
            type (Type): The type of the class.
        """
        
        @c_dec(
            is_method=True, is_static=True, add_to_class=parent,
            func_name_override=f'{type.c_type}_type'
        )
        def _(_, call_position: Position) -> Object:
            return Object(f'"{type}"', Type('string'), call_position)
        
        @c_dec(
            param_types=(Param(name.lower(), type),), is_method=True, add_to_class=parent,
            func_name_override=f'{type.c_type}_to_string'
        )
        def _(_, call_position: Position, _instance: Object) -> Object:
            return Object(f'"class \'{type}\'"', Type('string'), call_position)
    
    
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
        from codegen.StringBuilder import StringBuilder
        from codegen.strings import strings
        from codegen.System import System
        from codegen.Logger import Logger
        from codegen.Math import Math
        from codegen.Cure import Cure
        self.add_objects(Math(self), self)
        self.add_objects(Cure(self), self)
        self.add_objects(Logger(self), self)
        self.add_objects(System(self), self)
        self.add_objects(strings(self), self)
        self.add_objects(StringBuilder(self), self)
        
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
        codegen.scope.env['Timer'] = EnvItem('Timer', Type('Timer'), POS_ZERO)
        
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
            
            return type_method(codegen, call_position)
        
        @c_dec(param_types=(Param('x', Type('any')),), can_user_call=True, add_to_class=self)
        def _to_string(codegen, call_position: Position, x: Object) -> Object:
            repr_method = self.get_object(f'{x.type.c_type}_to_string')
            if repr_method is None:
                call_position.error_here(f'String representation for \'{x.type}\' is not defined')

            return repr_method(codegen, call_position, x)
        
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

            return bool_method(codegen, call_position, x)
        
        @c_dec(param_types=(Param('object', Type('any')),), can_user_call=True, add_to_class=self)
        def _sizeof(_, call_position: Position, object: Object) -> Object:
            return Object(f'(sizeof({object}))', Type('int'), call_position)
        
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
            OverloadKey(Type('string'), (Param('value', Type('int')),)): OverloadValue(char_int)
        }, add_to_class=self)
        def _get_char(codegen, call_position: Position, value: Object) -> Object:
            slen = codegen.c_manager._string_length(codegen, call_position, value)
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
            OverloadKey(
                Type('nil'), (Param('condition', Type('bool')), Param('err', Type('string')))
            ): OverloadValue(assert_err)
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
                OverloadKey(Type('array[int]', 'int_array'), (
                    Param('start', Type('int')),
                    Param('end', Type('int')))
                ): OverloadValue(_range_no_step),
                OverloadKey(
                    Type('array[int]', 'int_array'), (Param('start', Type('int')),)
                ): OverloadValue(_range_no_start)
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
        
        @c_dec(
            param_types=(Param('value', Type('string')),), can_user_call=True, add_to_class=self
        )
        def _print_literal(_, call_position: Position, value: Object) -> Object:
            return Object(f'(printf({value}))', Type('int'), call_position)
        
        @c_dec(
            param_types=(Param('value', Type('any')),), can_user_call=True, add_to_class=self,
            generic_params=('T',), return_type=Type('optional_{T}')
        )
        def _optional(codegen, call_position: Position, value: Object, *, T: Type) -> Object:
            if value.type != T and value.type != Type('nil'):
                call_position.error_here('Invalid optional')
            
            if T == Type('nil'):
                call_position.warn_here('Optional type of nil will always be nil')
            
            opt_t: Type = codegen.optional_manager.define_optional(T)
            return codegen.call(f'{opt_t.c_type}_new', [Arg(value)], call_position)
        
        
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
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Timer_type(_, call_position: Position) -> Object:
            return Object('"Timer"', Type('string'), call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Logger_type(_, call_position: Position) -> Object:
            return Object('"Logger"', Type('string'), call_position)
        
        
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
        
        @c_dec(param_types=(Param('value', Type('Timer')),), is_method=True, add_to_class=self)
        def _Timer_to_string(codegen, call_position: Position, value: Object) -> Object:
            code, buf_free = self.fmt_length(
                codegen, call_position, '"Timer(is_running=%s)"',
                f'({value}).is_running'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        @c_dec(param_types=(Param('logger', Type('Logger')),), is_method=True, add_to_class=self)
        def _Logger_to_string(codegen, call_position: Position, value: Object) -> Object:
            path: TempVar = codegen.create_temp_var(Type('string'), call_position)
            codegen.prepend_code(f"""string {path} = NULL;
if (({value}).path == NULL) {{
    {path} = "stdout";
}} else {{
    {path} = ({value}).path;
}}
""")
            code, buf_free = self.fmt_length(
                codegen, call_position, '"Logger(path=%s)"',
                str(path)
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
    codegen.c_manager._string_length(codegen, call_position, b)
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
    codegen.c_manager._string_length(codegen, call_position, a)
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
            alen = codegen.c_manager._string_length(codegen, call_position, a)
            blen = codegen.c_manager._string_length(codegen, call_position, b)
            return Object(f'({alen} > {blen})', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_gte_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) >= ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_gte_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) >= ({b}))', Type('bool'), call_position)

        @c_dec(param_types=(Param('a', Type('string')), Param('b', Type('string'))), add_to_class=self)
        def _string_gte_string(codegen, call_position: Position, a: Object, b: Object) -> Object:
            alen = codegen.c_manager._string_length(codegen, call_position, a)
            blen = codegen.c_manager._string_length(codegen, call_position, b)
            return Object(f'({alen} >= {blen})', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_lt_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) < ({b}))', Type('bool'), call_position)

        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_lt_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) < ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('string')), Param('b', Type('string'))), add_to_class=self)
        def _string_lt_string(codegen, call_position: Position, a: Object, b: Object) -> Object:
            alen = codegen.c_manager._string_length(codegen, call_position, a)
            blen = codegen.c_manager._string_length(codegen, call_position, b)
            return Object(f'({alen} < {blen})', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('int')), Param('b', Type('int'))), add_to_class=self)
        def _int_lte_int(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) <= ({b}))', Type('bool'), call_position)

        @c_dec(param_types=(Param('a', Type('float')), Param('b', Type('float'))), add_to_class=self)
        def _float_lte_float(_, call_position: Position, a: Object, b: Object) -> Object:
            return Object(f'(({a}) <= ({b}))', Type('bool'), call_position)
        
        @c_dec(param_types=(Param('a', Type('string')), Param('b', Type('string'))), add_to_class=self)
        def _string_lte_string(codegen, call_position: Position, a: Object, b: Object) -> Object:
            alen = codegen.c_manager._string_length(codegen, call_position, a)
            blen = codegen.c_manager._string_length(codegen, call_position, b)
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
            abs_call: Object = codegen.c_manager._Math_abs(codegen, call_position, x.OBJECT())
            
            if 'sizeNames' not in self.RESERVED_NAMES:
                codegen.add_toplevel_code("""const string sizeNames[] = {
    "B", "KB", "MB", "GB", "TB", "PB"
};
""")
                self.reserve('sizeNames')

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
                Param('precision', Type('int'), default=Object('5', Type('int')))
            ),
            is_method=True, add_to_class=self
        )
        def _float_science(codegen, call_position: Position, f: Object, precision: Object) -> Object:
            return _int_science(codegen, call_position, f, precision)
        
        
        self.wrap_struct_properties('timer', Type('Timer'), [
            Param('is_running', Type('bool'))
        ])
        
        def elapsed_ns(codegen, call_position: Position, timer: Object):
            elapsed: TempVar = codegen.create_temp_var(Type('LARGE_INTEGER'), call_position)
            res: TempVar = codegen.create_temp_var(Type('float'), call_position)
            return f"""#if OS_WINDOWS
    LARGE_INTEGER {elapsed};
    {elapsed}.QuadPart = ({timer}).end.QuadPart - ({timer}).start.QuadPart;
    float {res} = {elapsed}.QuadPart * 1e9 / ({timer}).frequency.QuadPart;
#elif OS_LINUX
    float {res} = (float)((({timer}).end.tv_sec - ({timer}).start.tv_sec) * 1e9 +
        (({timer}).end.tv_sec - ({timer}).end.tv_nsec - ({timer}).start.tv_nsec));
#else
{self.symbol_not_supported('Timer.elapsed_ns')}
#endif
""", res
        
        @c_dec(param_types=(Param('timer', Type('Timer')),), is_property=True, add_to_class=self)
        def _Timer_elapsed_ns(codegen, call_position: Position, timer: Object) -> Object:
            code, res = elapsed_ns(codegen, call_position, timer)
            codegen.prepend_code(code)
            return res.OBJECT()
        
        @c_dec(param_types=(Param('timer', Type('Timer')),), is_property=True, add_to_class=self)
        def _Timer_elapsed_us(codegen, call_position: Position, timer: Object) -> Object:
            return _float_div_float(codegen, call_position,
                _Timer_elapsed_ns(codegen, call_position, timer),
                Object('1e3', Type('float'), call_position)
            )
        
        @c_dec(param_types=(Param('timer', Type('Timer')),), is_property=True, add_to_class=self)
        def _Timer_elapsed_ms(codegen, call_position: Position, timer: Object) -> Object:
            return _float_div_float(codegen, call_position,
                _Timer_elapsed_ns(codegen, call_position, timer),
                Object('1e6', Type('float'), call_position)
            )
        
        @c_dec(param_types=(Param('timer', Type('Timer')),), is_property=True, add_to_class=self)
        def _Timer_elapsed_s(codegen, call_position: Position, timer: Object) -> Object:
            return _float_div_float(codegen, call_position,
                _Timer_elapsed_ns(codegen, call_position, timer),
                Object('1e9', Type('float'), call_position)
            )
        
        @c_dec(param_types=(Param('timer', Type('Timer')),), is_method=True, add_to_class=self)
        def _Timer_start(codegen, call_position: Position, timer: Object) -> Object:
            codegen.prepend_code(f"""#if OS_WINDOWS
    QueryPerformanceFrequency(&({timer}).frequency);
    QueryPerformanceCounter(&({timer}).start);
#elif OS_LINUX
    clock_gettime(CLOCK_MONOTONIC, &({timer}).start);
#else
{self.symbol_not_supported('Timer.start')}
#endif

({timer}).is_running = true;
""")
            
            return Object.NULL(call_position)
        
        def timer_stop(timer: Object) -> str:
            return f"""#if OS_WINDOWS
    QueryPerformanceCounter(&({timer}).end);
#elif OS_LINUX
    clock_gettime(CLOCK_MONOTONIC, &({timer}).end);
#else
{self.symbol_not_supported('Timer.stop')}
#endif
({timer}).is_running = false;
"""
        
        @c_dec(param_types=(Param('timer', Type('Timer')),), is_method=True, add_to_class=self)
        def _Timer_stop(codegen, call_position: Position, timer: Object) -> Object:
            codegen.prepend_code(timer_stop(timer))
            return Object.NULL(call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _Timer_new(codegen, call_position: Position) -> Object:
            timer: TempVar = codegen.create_temp_var(Type('Timer'), call_position)
            codegen.prepend_code(f"""Timer {timer} = {{ .is_running = false }};
""")
            
            return timer.OBJECT()
    
        
        @func_modification(params=(Param('message', Type('string')),), add_to_class=self)
        def _Info(codegen, _func_obj: UserFunction, call_position: Position, _args: list[Arg],
                msg: Object) -> None:
            if not codegen.is_string_literal(msg):
                call_position.error_here('Info message must be a string literal')

            call_position.info_here(str(msg)[1:-1])
    
        @func_modification(params=(Param('message', Type('string')),), add_to_class=self)
        def _Warn(codegen, _func_obj: UserFunction, call_position: Position, _args: list[Arg],
                msg: Object) -> None:
            if not codegen.is_string_literal(msg):
                call_position.error_here('Warning message must be a string literal')
            
            call_position.warn_here(str(msg)[1:-1])

        @func_modification(params=(Param('message', Type('string')),), add_to_class=self)
        def _Error(codegen, _func_obj: UserFunction, call_position: Position, _args: list[Arg],
                msg: Object) -> None:
            if not codegen.is_string_literal(msg):
                call_position.error_here('Error message must be a string literal')
            
            call_position.error_here(str(msg)[1:-1])
        
        @func_modification(add_to_class=self)
        def _Benchmark(codegen, func_obj: UserFunction, call_position: Position,
                       _args: list[Arg]) -> None:
            timer = _Timer_new(codegen, call_position)
            _Timer_start(codegen, call_position, timer)
            code, res = elapsed_ns(codegen, call_position, timer)
            codegen.append_code(f"""{timer_stop(timer)};
{code};
printf("Time spent to execute '{func_obj.name}': %fms\\n", {res} / 1e6);
""")
        
        @func_modification(add_to_class=self)
        def _Cache(codegen, func_obj: UserFunction, call_position: Position, args: list[Arg]) -> Object:
            func_params = func_obj.params
            cache_struct_type = Type(f'cache_dict_{func_obj.name}')
            cache_key = f'cacheof_{func_obj.name}'
            global_scope = codegen.scope.toplevel
            previously_called = global_scope.env.get(cache_key) is not None
            if not previously_called:
                codegen.c_manager.reserve((cache_key, cache_struct_type.c_type))
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
        def _Transform(codegen, func_obj: UserFunction, call_position: Position, args: list[Arg],
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
