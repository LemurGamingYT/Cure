TOKENS = {
    'float': r'-?\d*\.\d+',
    'int': r'-?\d+',
    'string': r'\"[^\"]*\"',
    'bool': r'true|false',
    'nil': r'nil',
    'FN': r'fn',
    'RETURN': r'return',
    'IF': r'if',
    'ELSE': r'else',
    'WHILE': r'while',
    'id': r'[a-zA-Z_][a-zA-Z_0-9]*',
    ',': r',',
    '->': r'->',
    '(': r'\(',
    ')': r'\)',
    '{': r'\{',
    '}': r'\}',
    '+': r'\+',
    '-': r'-',
    '*': r'\*',
    '/': r'/',
    '%': r'%',
    '==': r'==',
    '!=': r'!=',
    '>=': r'>=',
    '<=': r'<=',
    '>': r'>',
    '<': r'<',
    'and': r'&&',
    'or': r'\|\|',
    '!': r'!',
    '.': r'\.',
    '=': r'=',
}

IGNORES = [r'\s+', r'//.*', r'/\*[\s\S]*?\*/']
PRECEDENCE = [
    ('right', ['=']),           # Assignment should be lowest, but separate
    ('left', ['or']),           # Lowest precedence
    ('left', ['and']),
    ('left', ['==', '!=', '>', '<', '>=', '<=']),
    ('left', ['+', '-']),
    ('left', ['*', '/', '%']),
    ('right', ['!']),           # Highest precedence
    ('left', ['.'])
]
