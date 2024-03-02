from dataclasses import dataclass, field
from sys import exit as sys_exit
from enum import Enum, auto
from typing import NoReturn


def error(name: str, msg: str) -> NoReturn:
    print(f'{name}Error: {msg}')
    sys_exit(1)


@dataclass(slots=True, unsafe_hash=True, eq=False)
class Statement:
    code: str
    type: 'Type'
    stmt_is_returning: bool = field(default=False)
    
    @property
    def str_type(self) -> str:
        return self.type.str_type


@dataclass(slots=True, unsafe_hash=True, eq=False)
class EnvItem:
    name: str
    type: 'Type'
    is_func: bool
    requires_free: bool = field(default=False)


@dataclass(slots=True, unsafe_hash=True, eq=False)
class Attribute:
    type: 'Type'
    static: bool = field(default=True)
    is_method: bool = field(default=False)


class Type(Enum):
    int = auto()
    float = auto()
    string = auto()
    bool = auto()
    nil = auto()
    
    math = auto()
    
    system = auto()
    timer = auto()
    file = auto()
    
    mem = auto()
    pointer = auto()
    
    logger = auto()
    log = auto()
    loglevel = auto()
    
    all_types = auto()
    
    @property
    def str_type(self):
        match self:
            case Type.int:
                return 'Int'
            case Type.float:
                return 'Float'
            case Type.string:
                return 'String'
            case Type.bool:
                return 'Bool'
            case Type.nil:
                return 'Nil'
            case Type.math:
                return 'Math'
            case Type.system:
                return 'System'
            case Type.timer:
                return 'Timer'
            case Type.file:
                return 'File'
            case Type.logger:
                return 'Logger'
            case Type.log:
                return 'Log'
            case Type.mem:
                return 'Mem'
            case Type.pointer:
                return 'Pointer'
            case Type.all_types:
                return 'AllTypes'
            case _:
                error('Type', f'Unknown type \'{self.value}\'')


OP_RETURN_TYPES = {
    '+': {
        (Type.int, Type.int): Type.int,
        (Type.float, Type.int): Type.float,
        (Type.int, Type.float): Type.float,
        (Type.float, Type.float): Type.float,
        (Type.string, Type.string): Type.string
    },
    '-': {
        (Type.int, Type.int): Type.int,
        (Type.float, Type.int): Type.float,
        (Type.int, Type.float): Type.float,
        (Type.float, Type.float): Type.float
    },
    '*': {
        (Type.int, Type.int): Type.int,
        (Type.float, Type.int): Type.float,
        (Type.int, Type.float): Type.float,
        (Type.float, Type.float): Type.float
    },
    '/': {
        (Type.int, Type.int): Type.float,
        (Type.float, Type.int): Type.float,
        (Type.int, Type.float): Type.float,
        (Type.float, Type.float): Type.float
    },
    '%': {
        (Type.int, Type.int): Type.int
    },
    '==': {
        (Type.int, Type.int): Type.bool,
        (Type.float, Type.int): Type.bool,
        (Type.string, Type.string): Type.bool,
        (Type.bool, Type.bool): Type.bool
    },
    '!=': {
        (Type.int, Type.int): Type.bool,
        (Type.float, Type.float): Type.bool,
        (Type.string, Type.string): Type.bool,
        (Type.bool, Type.bool): Type.bool
    },
    '<': {
        (Type.int, Type.int): Type.bool,
        (Type.float, Type.float): Type.bool,
        (Type.string, Type.string): Type.bool
    },
    '<=': {
        (Type.int, Type.int): Type.bool,
        (Type.float, Type.float): Type.bool,
        (Type.string, Type.string): Type.bool
    },
    '>': {
        (Type.int, Type.int): Type.bool,
        (Type.float, Type.float): Type.bool,
        (Type.string, Type.string): Type.bool
    },
    '>=': {
        (Type.int, Type.int): Type.bool,
        (Type.float, Type.float): Type.bool,
        (Type.string, Type.string): Type.bool
    },
    '&&': {
        (Type.bool, Type.bool): Type.bool
    },
    '||': {
        (Type.bool, Type.bool): Type.bool
    },
    '!': {
        Type.bool: Type.bool
    }
}

OP_FUNC_NAMES = {
    '+': 'add',
    '-': 'sub',
    '*': 'mul',
    '/': 'div',
    '%': 'mod',
    '==': 'eq',
    '!=': 'neq',
    '<': 'lt',
    '<=': 'lte',
    '>': 'gt',
    '>=': 'gte',
    '&&': 'and',
    '||': 'or'
}

ATTRIBUTES = {
    Type.string: {
        'length': Attribute(Type.int, False),
        'lower': Attribute(Type.string, False, True),
        'upper': Attribute(Type.string, False, True),
    },
    Type.math: {
        'PI': Attribute(Type.float),
        'E': Attribute(Type.float),
        'sin': Attribute(Type.float, is_method=True),
        'cos': Attribute(Type.float, is_method=True),
        'tan': Attribute(Type.float, is_method=True),
        'asin': Attribute(Type.float, is_method=True),
        'acos': Attribute(Type.float, is_method=True),
        'atan': Attribute(Type.float, is_method=True),
        'sqrt': Attribute(Type.float, is_method=True),
        'abs': Attribute(Type.float, is_method=True),
        'floor': Attribute(Type.float, is_method=True),
        'ceil': Attribute(Type.float, is_method=True),
        'log': Attribute(Type.float, is_method=True),
        'exp': Attribute(Type.float, is_method=True),
    },
    Type.system: {
        'exit': Attribute(Type.nil, is_method=True),
        'shell': Attribute(Type.int, is_method=True),
        'getenv': Attribute(Type.string, is_method=True),
        'current_time': Attribute(Type.timer),
        'total_memory_usage': Attribute(Type.float),
        'free_memory_usage': Attribute(Type.float),
        'console_color': Attribute(Type.nil, is_method=True),
        'fg_red': Attribute(Type.int),
        'fg_green': Attribute(Type.int),
        'fg_blue': Attribute(Type.int),
        'fg_yellow': Attribute(Type.int),
        'fg_magenta': Attribute(Type.int),
        'fg_cyan': Attribute(Type.int),
        'fg_white': Attribute(Type.int),
        'bg_red': Attribute(Type.int),
        'bg_green': Attribute(Type.int),
        'bg_blue': Attribute(Type.int),
        'bg_yellow': Attribute(Type.int),
        'bg_magenta': Attribute(Type.int),
        'bg_cyan': Attribute(Type.int),
        'bg_white': Attribute(Type.int),
        'clear_console': Attribute(Type.nil, is_method=True),
        'reset_console_color': Attribute(Type.nil, is_method=True),
        'open_file': Attribute(Type.file, is_method=True),
    },
    Type.file: {
        'path': Attribute(Type.string, False),
        'size': Attribute(Type.int, False),
        'read': Attribute(Type.string, False, True),
        'write': Attribute(Type.nil, False, True),
        'exists': Attribute(Type.bool, False),
        'create': Attribute(Type.nil, False, True),
        'copy': Attribute(Type.nil, False, True),
        'move': Attribute(Type.nil, False, True),
        'delete': Attribute(Type.nil, False, True),
    },
    Type.logger: {
        'debug': Attribute(Type.loglevel),
        'info': Attribute(Type.loglevel),
        'warning': Attribute(Type.loglevel),
        'error': Attribute(Type.loglevel),
        'open': Attribute(Type.log, is_method=True),
    },
    Type.log: {
        'set_level': Attribute(Type.nil, False, True),
        'log': Attribute(Type.nil, False, True),
    },
    Type.mem: {
        'free': Attribute(Type.nil, is_method=True),
        'alloc': Attribute(Type.pointer, is_method=True),
        'point': Attribute(Type.pointer, is_method=True),
        'copy': Attribute(Type.pointer, is_method=True),
        'clone': Attribute(Type.pointer, is_method=True),
        'sizeof': Attribute(Type.int, is_method=True),
    }
}
