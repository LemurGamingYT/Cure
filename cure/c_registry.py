from llvmlite import ir as lir

from cure.target import Target
from cure import ir


class CRegistry:
    def __init__(self, module: lir.Module, scope: ir.Scope):
        self.__registry: dict[str, lir.Function | lir.FunctionType] = {}
        
        self.module = module
        self.scope = scope

        self.register('snprintf', lir.FunctionType(lir.IntType(32), [
            lir.IntType(8).as_pointer(), # buf
            lir.IntType(64), # buflen
            lir.IntType(8).as_pointer() # fmt
        ], True))

        self.register('puts', lir.FunctionType(lir.IntType(32), [
            lir.IntType(8).as_pointer() # str
        ]))

        self.register('printf', lir.FunctionType(lir.IntType(32), [
            lir.IntType(8).as_pointer() # fmt
        ], var_arg=True))

        self.register('exit', lir.FunctionType(lir.VoidType(), [
            lir.IntType(32) # exitcode
        ]))

        self.register('malloc', lir.FunctionType(lir.IntType(8).as_pointer(), [
            lir.IntType(64) # size
        ]))

        self.register('realloc', lir.FunctionType(lir.IntType(8).as_pointer(), [
            lir.IntType(8).as_pointer(), # ptr
            lir.IntType(64) # size
        ]))

        self.register('free', lir.FunctionType(lir.VoidType(), [
            lir.IntType(8).as_pointer() # ptr
        ]))

        self.register('memcpy', lir.FunctionType(lir.IntType(8).as_pointer(), [
            lir.IntType(8).as_pointer(), # dest
            lir.IntType(8).as_pointer(), # src
            lir.IntType(64) # size
        ]))

        self.register('sinf', lir.FunctionType(lir.FloatType(), [
            lir.FloatType() # arg
        ]))

        self.register('cosf', lir.FunctionType(lir.FloatType(), [
            lir.FloatType() # arg
        ]))

        self.register('tanf', lir.FunctionType(lir.FloatType(), [
            lir.FloatType() # arg
        ]))

        self.register('memcmp', lir.FunctionType(lir.IntType(1), [
            lir.IntType(8).as_pointer(), # lhs
            lir.IntType(8).as_pointer(), # rhs
            lir.IntType(64) # count
        ]))

        self.register('__acrt_iob_func', lir.FunctionType(
            lir.LiteralStructType([lir.IntType(8).as_pointer()]),
            [lir.IntType(32)])
        )

        self.register('fgets', lir.FunctionType(lir.IntType(8).as_pointer(), [
            lir.IntType(8).as_pointer(), # buf
            lir.IntType(32), # size
            lir.LiteralStructType([lir.IntType(8).as_pointer()]) # file
        ]))

        self.register('strlen', lir.FunctionType(lir.IntType(64), [
            lir.IntType(8).as_pointer() # str
        ]))

        self.register('floorf', lir.FunctionType(lir.FloatType(), [
            lir.FloatType() # arg
        ]))

        self.register('ceilf', lir.FunctionType(lir.FloatType(), [
            lir.FloatType() # arg
        ]))

        self.register('powf', lir.FunctionType(lir.FloatType(), [
            lir.FloatType(), # base
            lir.FloatType() # exponent
        ]))

        self.register('sqrtf', lir.FunctionType(lir.FloatType(), [
            lir.FloatType() # arg
        ]))

        self.register('strtol', lir.FunctionType(lir.IntType(64), [
            lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(),
            lir.IntType(32)
        ]))

        self.register('strtod', lir.FunctionType(lir.IntType(64), [
            lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer()
        ]))

        if scope.target == Target.Windows:
            self.register('GetCurrentProcessId', lir.FunctionType(lir.IntType(32), []))
        elif scope.target == Target.Linux:
            self.register('getpid', lir.FunctionType(lir.IntType(32), []))
    
    def get(self, name: str):
        if name not in self.__registry:
            return None
        
        value = self.__registry[name]
        if isinstance(value, lir.FunctionType):
            func = lir.Function(self.module, value, name)
            self.__registry[name] = func

            return func
        else:
            return value
    
    def register(self, name: str, signature: lir.FunctionType):
        self.__registry[name] = signature
    
    def is_registered(self, name: str):
        return name in self.__registry
    
    def get_registered_functions(self):
        return list(self.__registry.keys())
