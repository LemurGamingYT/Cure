from llvmlite import ir as lir


class CRegistry:
    def __init__(self, module: lir.Module):
        self.__registry: dict[str, lir.Function | lir.FunctionType] = {}
        
        self.module = module
    
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
