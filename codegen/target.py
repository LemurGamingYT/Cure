from platform import system
from enum import Enum


class Target(Enum):
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MACOS = 'Darwin'


def get_target() -> Enum:
    target = Target[system().upper()]
    if target is None:
        raise NotImplementedError('Os not supported')

    return target
