from llvmlite import ir as lir

from cure.lib import function, Class, ClassField, DefinitionContext
from cure.ir import Scope, TypeManager, Type, Position, Param


class Array(Class):
    def fields(self):
        return [
            ClassField('elements', self.T.as_pointer()),
            ClassField('length', TypeManager.get('int')),
            ClassField('capacity', TypeManager.get('int')),
            ClassField('ref', TypeManager.get('Ref').as_pointer())
        ]
    
    def __init__(self, scope: Scope, T: Type):
        self.T = T

        super().__init__(scope)
