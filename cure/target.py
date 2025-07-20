from platform import system
from enum import Enum


class Target(Enum):
    Windows = 'Windows'
    Linux = 'Linux'

    @staticmethod
    def get(name: str):
        return Target[name]
    
    @staticmethod
    def get_current():
        return Target.get(system())
    
    @property
    def macro_name(self):
        return self.name.upper()
    
    @property
    def object_ext(self):
        return 'obj' if self == Target.Windows else 'o'
    
    @property
    def exe_ext(self):
        return 'exe' if self == Target.Windows else ''
