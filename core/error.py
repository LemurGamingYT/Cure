from sys import exit as sys_exit
from typing import NoReturn


def report_error(t: str, msg: str) -> NoReturn:
    print(f'{t}Error: {msg}')
    sys_exit(1)
