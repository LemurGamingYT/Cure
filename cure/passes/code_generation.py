from typing import cast

from llvmlite import ir as lir, binding as llvm

from cure.codegen_utils import create_string_struct, NULL
from cure.passes import CompilerPass
from cure import ir


class CRegistry:
    def __init__(self, module: lir.Module):
        self.__registry: dict[str, lir.Function] = {}
        
        self.module = module
    
    def get(self, name: str):
        return self.__registry[name]
    
    def register(self, name: str, signature: lir.FunctionType):
        self.__registry[name] = lir.Function(self.module, signature, name)
    
    def is_registered(self, name: str):
        return name in self.__registry


class CodeGeneration(CompilerPass):
    def __init__(self, scope):
        super().__init__(scope)

        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        self.module = lir.Module('main')
        self.module.triple = llvm.get_default_triple()

        self.builder = lir.IRBuilder()

        self.c_registry = CRegistry(self.module)
        self.c_registry.register('snprintf', lir.FunctionType(lir.IntType(32), [
            lir.IntType(8).as_pointer(), # buf
            lir.IntType(64), # buf_len
            lir.IntType(8).as_pointer() # fmt
        ], True))

        self.c_registry.register('puts', lir.FunctionType(lir.IntType(32), [
            lir.IntType(8).as_pointer() # str
        ]))

        self.c_registry.register('exit', lir.FunctionType(lir.VoidType(), [
            lir.IntType(32) # exit_code
        ]))

        setattr(self.module, 'c_registry', self.c_registry)
    
    def run_on_Program(self, node: ir.Program):
        for n in node.nodes:
            self.run_on(n)
        
        return str(self.module)
    
    def run_on_Body(self, node: ir.Body):
        self.scope = self.scope.clone()
        for stmt in node.nodes:
            self.run_on(stmt)
        
        self.scope = cast(ir.Scope, self.scope.parent)
    
    def run_on_Param(self, node: ir.Param):
        return node.type.type
    
    def run_on_Function(self, node: ir.Function):
        ret_type = cast(ir.Type, self.run_on(node.type)).type
        param_types = [self.run_on(param) for param in node.params]
        func = lir.Function(self.module, lir.FunctionType(ret_type, param_types), node.name)
        if isinstance(node.body, ir.Body):
            old_builder = self.builder
            self.builder = lir.IRBuilder(func.append_basic_block())

            for i, param in enumerate(node.params):
                self.scope.symbol_table.add(ir.Symbol(param.name, param.type, func.args[i]))
            
            self.run_on(node.body)

            if node.type == ir.Type.nil():
                self.builder.ret(NULL())

            for param in node.params:
                self.scope.symbol_table.remove(param.name)

            self.builder = old_builder

        self.scope.symbol_table.add(ir.Symbol(node.name, ir.Type.function(), func))
        return func
    
    def run_on_Variable(self, node: ir.Variable):
        value = self.run_on(node.value) if node.value is not None else node.value
        if value is None:
            node.pos.comptime_error('cannot generate code for uninitialised variables', self.scope.src)
            return
        
        ptr = self.builder.alloca(node.type.type)
        self.builder.store(value, ptr)
        self.scope.symbol_table.add(ir.Symbol(node.name, node.type, ptr))
        return ptr
    
    def run_on_Assignment(self, node: ir.Assignment):
        value = self.run_on(node.value)
        symbol = cast(ir.Symbol, self.scope.symbol_table.get(node.name))

        ptr = symbol.value
        return self.builder.store(value, ptr)
    
    def run_on_Return(self, node: ir.Return):
        value = self.run_on(node.value)
        self.builder.ret(value)
        return value
    
    def run_on_Int(self, node: ir.Int):
        return lir.Constant(ir.Type.int().type, node.value)
    
    def run_on_Float(self, node: ir.Float):
        return lir.Constant(ir.Type.float().type, node.value)
    
    def run_on_String(self, node: ir.String):
        return create_string_struct(self.module, self.builder, node.value)
    
    def run_on_Bool(self, node: ir.Bool):
        return lir.Constant(ir.Type.bool().type, node.value)
    
    def run_on_Nil(self, _):
        return NULL()
    
    def run_on_Id(self, node: ir.Id):
        symbol = self.scope.symbol_table.get(node.name)
        if symbol is None:
            return
        
        return self.builder.load(symbol.value)
    
    def run_on_Call(self, node: ir.Call):
        symbol = self.scope.symbol_table.get(node.callee)
        if symbol is None:
            return
        
        args = [self.run_on(arg) for arg in node.args]
        arg_types = [arg.get_type() for arg in node.args]
        func = symbol.value
        if isinstance(func, lir.Function):
            return self.builder.call(func, args)
        elif callable(func):
            ir_func = func(self.module, self.scope, arg_types)
            return self.builder.call(ir_func, args)
