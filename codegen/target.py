from platform import system
from enum import Enum


class Target(Enum):
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MAC = 'Darwin'


def get_target(name: str) -> Enum:
    return Target[name.upper()]

def get_current_target() -> Enum:
    if (current := get_target_from_string(system().upper())) is not None:
        return current
    
    # this should never happen, default to Windows
    return Target.WINDOWS

def get_target_from_string(target: str | None) -> Enum | None:
    if target is None:
        return get_current_target()
    
    try:
        return get_target(target)
    except KeyError:
        return None
