from sys import exit as sys_exit
from platform import system
from enum import Enum


class Target(Enum):
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MACOS = 'Darwin'


def get_target(name: str) -> Enum:
    return Target[name.upper()]

def get_current_target() -> Enum:
    try:
        target = Target[system().upper()]
    except KeyError:
        print(f'Unknown target: {system()}')
        sys_exit(1)

    return target
