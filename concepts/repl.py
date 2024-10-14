"""REPL for Cure

How it works:
1. User types a piece of code
2. The code is converted to C code
3. The generated C code is written to a temporary C file
    - It is also concatenated with the C code of the previous run and the C code for creating a main
    function in C
4. The C file is used to generate a temporary .dll file
5. The dll file is ran and used by the Python `ctypes`'s `CDLL` class
"""

from tempfile import NamedTemporaryFile
from subprocess import run
from ctypes import CDLL

from codegen import str_to_c


def repl():
    code = ''
    while True:
        cmd = input('>>> ')
        if cmd == 'exit':
            break
        
        code += cmd + '\n'
        code = 'func main() -> int {\n' + code + '\n}'
        _, c_code = str_to_c(cmd)
        with NamedTemporaryFile('w', suffix='.c') as c_file:
            with NamedTemporaryFile('w', suffix='.dll') as dll_file:
                c_file.write(c_code)
                run(['gcc', c_file.name, '-o', dll_file.name, '-shared'])
                dll = CDLL(dll_file.name)
                dll.main()
