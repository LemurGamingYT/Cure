from typing import cast

from llvmlite import ir as lir, binding as llvm

from cure.codegen_utils import create_string_struct, NULL, create_while_loop
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
    
    def run_on_Type(self, node: ir.Type):
        return node.type
    
    def run_on_Program(self, node: ir.Program):
        for n in node.nodes:
            self.run_on(n)
        
        return str(self.module)
    
    def run_on_Body(self, node: ir.Body):
        self.scope = self.scope.clone()
        for stmt in node.nodes:
            self.run_on(stmt)
        
        self.scope = cast(ir.Scope, self.scope.parent)
    
    def run_on_Elif(self, node: ir.Elif):
        pass
    
    def run_on_If(self, node: ir.If):
        """Manual if-elif-else implementation"""
        
        function = self.builder.function
        merge_block = function.append_basic_block('if_merge')
        
        # Handle simple if-else case
        if not hasattr(node, 'elseifs') or not node.elseifs:
            return self._build_simple_if_else(node, merge_block)
        
        # Handle if-elif-else case
        return self._build_if_elif_else(node, merge_block)

    def _build_simple_if_else(self, node: ir.If, merge_block):
        """Build simple if-else"""
        function = self.builder.function
        
        then_block = function.append_basic_block('if_then')
        else_block = None
        
        if hasattr(node, 'else_body') and node.else_body:
            else_block = function.append_basic_block('if_else')
        
        # Test condition
        condition = self.run_on(node.condition)
        if not self.builder.block.is_terminated:
            self.builder.cbranch(condition, then_block, else_block or merge_block)
        
        # Build then block
        self.builder.position_at_end(then_block)
        self.run_on(node.body)  # or node.then_body depending on your IR structure
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)
        
        # Build else block
        if else_block:
            self.builder.position_at_end(else_block)
            self.run_on(cast(ir.Body, node.else_body))
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)
        
        # Position at merge
        self.builder.position_at_end(merge_block)
        return None

    def _build_if_elif_else(self, node: ir.If, merge_block):
        """Build if-elif-else chain manually"""
        function = self.builder.function
        
        # Create all blocks first
        then_block = function.append_basic_block('if_then')
        
        elif_test_blocks = []
        elif_then_blocks = []
        
        for i, elif_node in enumerate(node.elseifs):
            elif_test_blocks.append(function.append_basic_block(f'elif_test_{i}'))
            elif_then_blocks.append(function.append_basic_block(f'elif_then_{i}'))
        
        else_block = None
        if hasattr(node, 'else_body') and node.else_body:
            else_block = function.append_basic_block('if_else')
        
        # Build main if condition
        condition = self.run_on(node.condition)
        first_elif_target = elif_test_blocks[0] if elif_test_blocks else (else_block or merge_block)
        
        if not self.builder.block.is_terminated:
            self.builder.cbranch(condition, then_block, first_elif_target)
        
        # Build then block
        self.builder.position_at_end(then_block)
        self.run_on(node.body)
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)
        
        # Build elif chains
        for i, elif_node in enumerate(node.elseifs):
            # Build elif test block
            self.builder.position_at_end(elif_test_blocks[i])
            elif_condition = self.run_on(elif_node.condition)
            
            # Determine next target if condition fails
            if i + 1 < len(elif_test_blocks):
                next_target = elif_test_blocks[i + 1]
            else:
                next_target = else_block or merge_block
            
            if not self.builder.block.is_terminated:
                self.builder.cbranch(elif_condition, elif_then_blocks[i], next_target)
            
            # Build elif then block
            self.builder.position_at_end(elif_then_blocks[i])
            self.run_on(elif_node.body)
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)
        
        # Build else block
        if else_block:
            self.builder.position_at_end(else_block)
            self.run_on(cast(ir.Body, node.else_body))
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)
        
        # Position at merge
        self.builder.position_at_end(merge_block)
        return None
    
    def run_on_While(self, node: ir.While):
        def cond(builder):
            old_builder = self.builder
            self.builder = builder

            res = self.run_on(node.condition)

            self.builder = old_builder
            return res

        def body(builder):
            old_builder = self.builder
            self.builder = builder
            
            self.run_on(node.body)

            self.builder = old_builder

        create_while_loop(self.builder, cond, body)
    
    def run_on_Param(self, node: ir.Param):
        return self.run_on(node.type)
    
    def run_on_Function(self, node: ir.Function):
        ret_type = self.run_on(node.type)
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
        
        ptr = self.builder.alloca(self.run_on(node.type))
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
        return lir.Constant(self.run_on(ir.Type.int()), node.value)
    
    def run_on_Float(self, node: ir.Float):
        return lir.Constant(self.run_on(ir.Type.float()), node.value)
    
    def run_on_String(self, node: ir.String):
        return create_string_struct(self.module, self.builder, node.value)
    
    def run_on_Bool(self, node: ir.Bool):
        return lir.Constant(self.run_on(ir.Type.bool()), node.value)
    
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
