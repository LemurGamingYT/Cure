from logging import debug, info, warning
from typing import cast

from llvmlite import ir as lir, binding as llvm

from cure.c_registry import CRegistry
from cure.passes import CompilerPass
from cure.lib import run_function
from cure.target import Target
from cure import ir
from cure.codegen_utils import (
    NULL, create_while_loop, store_in_pointer, create_string_constant, get_struct_field_ptr,
    get_struct_field_value, index_of_type
)


DONT_MANAGE_MEMORY = (
    ir.Type, ir.Param, ir.Function, ir.Variable, ir.Id, ir.Body, ir.Assignment, ir.Elif,
    ir.If, ir.Ref, ir.While, ir.Return
)


class CodeGeneration(CompilerPass):
    def __init__(self, scope):
        super().__init__(scope)

        info('Initialising LLVM')

        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        self.module = lir.Module('main')
        self.module.triple = llvm.get_default_triple()

        self.builder = lir.IRBuilder()

        info('Created module and builder')
        debug(f'Target = {self.module.triple}')

        self.c_registry = CRegistry(self.module)
        self.c_registry.register('snprintf', lir.FunctionType(lir.IntType(32), [
            lir.IntType(8).as_pointer(), # buf
            lir.IntType(64), # buflen
            lir.IntType(8).as_pointer() # fmt
        ], True))

        self.c_registry.register('puts', lir.FunctionType(lir.IntType(32), [
            lir.IntType(8).as_pointer() # str
        ]))

        self.c_registry.register('printf', lir.FunctionType(lir.IntType(32), [
            lir.IntType(8).as_pointer() # fmt
        ], var_arg=True))

        self.c_registry.register('exit', lir.FunctionType(lir.VoidType(), [
            lir.IntType(32) # exitcode
        ]))

        self.c_registry.register('malloc', lir.FunctionType(lir.IntType(8).as_pointer(), [
            lir.IntType(64) # size
        ]))

        self.c_registry.register('free', lir.FunctionType(lir.VoidType(), [
            lir.IntType(8).as_pointer() # ptr
        ]))

        self.c_registry.register('memcpy', lir.FunctionType(lir.IntType(8).as_pointer(), [
            lir.IntType(8).as_pointer(), # dest
            lir.IntType(8).as_pointer(), # src
            lir.IntType(64) # size
        ]))

        self.c_registry.register('sinf', lir.FunctionType(lir.FloatType(), [
            lir.FloatType() # arg
        ]))

        self.c_registry.register('cosf', lir.FunctionType(lir.FloatType(), [
            lir.FloatType() # arg
        ]))

        self.c_registry.register('tanf', lir.FunctionType(lir.FloatType(), [
            lir.FloatType() # arg
        ]))

        # self.c_registry.register('__acrt_iob_func', lir.FunctionType(
        #     lir.LiteralStructType([lir.IntType(8).as_pointer()]),
        #     [lir.IntType(32)])
        # )

        # self.c_registry.register('fgets', lir.FunctionType(lir.IntType(8).as_pointer(), [
        #     lir.IntType(8).as_pointer(), # buf
        #     lir.IntType(32), # size
        #     lir.LiteralStructType([lir.IntType(8).as_pointer()]) # file
        # ]))

        # self.c_registry.register('strlen', lir.FunctionType(lir.IntType(64), [
        #     lir.IntType(8).as_pointer() # str
        # ]))

        self.c_registry.register('memcmp', lir.FunctionType(lir.IntType(1), [
            lir.IntType(8).as_pointer(), # lhs
            lir.IntType(8).as_pointer(), # rhs
            lir.IntType(64) # count
        ]))

        if scope.target == Target.Windows:
            self.c_registry.register('GetCurrentProcessId', lir.FunctionType(lir.IntType(32), []))
        elif scope.target == Target.Linux:
            self.c_registry.register('getpid', lir.FunctionType(lir.IntType(32), []))

        debug(f'Registered: {', '.join(self.c_registry.get_registered_functions())}')

        setattr(self.module, 'c_registry', self.c_registry)
    
    def run_on(self, node: ir.Node):
        if isinstance(node, DONT_MANAGE_MEMORY):
            return super().run_on(node)

        node_type = node.get_type()
        if not node_type.needs_memory_management():
            return super().run_on(node)
        
        value = super().run_on(node)
        if isinstance(value.type, lir.PointerType):
            value = self.builder.load(value)
        
        if isinstance(value.type, lir.LiteralStructType):
            ref_index = index_of_type(value.type, ir.TypeManager.get('Ref').type.as_pointer())
            if ref_index == -1:
                warning(f'Type {node_type} needs memory management but has no Ref* field')
            else:
                ref = get_struct_field_value(self.builder, value, ref_index)
                run_function(node.pos, self.builder, self.module, self.scope, 'Ref_inc', [ref])

        ptr = store_in_pointer(self.builder, node_type.type, value, 'temp_var')
        self.scope.symbol_table.add(ir.Symbol(ptr.name, node_type, ptr))
        return self.builder.load(ptr, 'temp')
    
    def run_on_Type(self, node: ir.Type):
        return node.type
    
    def run_on_Program(self, node: ir.Program):
        info('Compiling program')
        for n in node.nodes:
            self.run_on(n)
        
        return str(self.module)
    
    def run_on_Body(self, node: ir.Body):
        self.scope = self.scope.clone()
        info('Compiling body')

        for stmt in node.nodes:
            info(f'Compiling body statement {stmt.__class__.__name__}')
            if isinstance(stmt, ir.Return):
                info('Inserting Ref_dec methods')
                for symbol in self.scope.symbol_table:
                    if not symbol.type.needs_memory_management():
                        continue

                    struct = symbol.value
                    llvm_type = cast(lir.LiteralStructType, symbol.type.type)
                    ref_index = index_of_type(llvm_type, ir.TypeManager.get('Ref').type.as_pointer())
                    if ref_index == -1:
                        warning(f'Type {symbol.type} needs memory management but has no Ref* field')
                        continue

                    ref = self.builder.load(get_struct_field_ptr(self.builder, struct, ref_index)) if\
                        isinstance(struct.type, lir.PointerType) else\
                        get_struct_field_value(self.builder, struct, ref_index)
                    
                    run_function(stmt.pos, self.builder, self.module, self.scope, 'Ref_dec', [ref])
                
                info('Finished inserting Ref_dec methods')
            
            self.run_on(stmt)
            info(f'Compiled body statement {stmt.__class__.__name__}')
        
        info('Compiled body')
        self.scope = cast(ir.Scope, self.scope.parent)
    
    def run_on_If(self, node: ir.If):
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
        info(f'Compiling function {node.name}')
        ret_type = self.run_on(node.type)
        param_types = [self.run_on(param) for param in node.params]
        func = lir.Function(self.module, lir.FunctionType(ret_type, param_types), node.name)
        self.scope.symbol_table.add(ir.Symbol(node.name, ir.TypeManager.get('function'), func))
        
        if isinstance(node.body, ir.Body):
            info('Compiling function body')

            old_builder = self.builder
            self.builder = lir.IRBuilder(func.append_basic_block('entry'))

            for i, param in enumerate(node.params):
                param_value = func.args[i]
                if param.type.needs_memory_management() and\
                    isinstance(param_value.type, lir.LiteralStructType):
                    ref_index = index_of_type(
                        param_value.type, ir.TypeManager.get('Ref').type.as_pointer()
                    )
                    if ref_index == -1:
                        warning(f'Type {param.type} needs memory management but has no Ref* field')
                    
                    ref = get_struct_field_value(self.builder, param_value, ref_index)
                    run_function(node.pos, self.builder, self.module, self.scope, 'Ref_inc', [ref])
                
                self.scope.symbol_table.add(ir.Symbol(param.name, param.type, store_in_pointer(
                    self.builder, param.type.type, param_value, f'param_{param.name}_ptr'
                )))
            
            self.run_on(node.body)

            if node.type == ir.TypeManager.get('nil'):
                info(f'{node.name} has no return type, inserting ret NULL')
                self.builder.ret(NULL())

            for param in node.params:
                self.scope.symbol_table.remove(param.name)

            self.builder = old_builder

        info(f'Finished compiling function {node.name}')
        return func
    
    def run_on_Variable(self, node: ir.Variable):
        value = self.run_on(node.value) if node.value is not None else node.value
        if value is None:
            node.pos.comptime_error('cannot generate code for uninitialised variables', self.scope.src)
            return
        
        ptr = store_in_pointer(self.builder, self.run_on(node.type), value, f'{node.name}_ptr')
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
        info(f'Returning {value}')
        return value
    
    def run_on_Int(self, node: ir.Int):
        return lir.Constant(self.run_on(ir.TypeManager.get('int')), node.value)
    
    def run_on_Float(self, node: ir.Float):
        return lir.Constant(self.run_on(ir.TypeManager.get('float')), node.value)
    
    def run_on_String(self, _):
        raise NotImplementedError
    
    def run_on_Bool(self, node: ir.Bool):
        return lir.Constant(self.run_on(ir.TypeManager.get('bool')), node.value)
    
    def run_on_Nil(self, _):
        return NULL()
    
    def run_on_StringLiteral(self, node: ir.StringLiteral):
        s = node.value.encode('utf-8').decode('unicode_escape')
        return create_string_constant(self.module, s)
    
    def run_on_Id(self, node: ir.Id):
        symbol = self.scope.symbol_table.get(node.name)
        if symbol is None:
            return
        
        if hasattr(symbol.value, 'type') and isinstance(symbol.value.type, lir.PointerType):
            info(f'Loading pointer {node.name}')
            return self.builder.load(symbol.value, node.name)
        
        info(f'Loading value {node.name}')
        return symbol.value
    
    def run_on_Ref(self, node: ir.Ref):
        symbol = self.scope.symbol_table.get(node.name)
        if symbol is None:
            return
        
        info(f'Returning pointer of {node.name}')
        return symbol.value
    
    def run_on_Call(self, node: ir.Call):
        symbol = self.scope.symbol_table.get(node.callee)
        if symbol is None:
            node.pos.comptime_error(f'unknown symbol {node.callee}', self.scope.src)
            return
        
        args = [self.run_on(arg) for arg in node.args]
        arg_types = [arg.get_type() for arg in node.args]
        func = ir.match_to_overloads(symbol.value, arg_types)
        if isinstance(func, lir.Function):
            info(f'Calling LLVM function {symbol.name}')
            return self.builder.call(func, args, 'func_call')
        elif callable(func):
            info(f'Calling stdlib function {symbol.name}')
            ir_func = func(self.module, self.scope, arg_types)
            return self.builder.call(ir_func, args, 'stdlib_call')
        
        node.pos.comptime_error(f'invalid callable {node.callee}', self.scope.src)
    
    def run_on_BinaryOp(self, _):
        raise NotImplementedError
    
    def run_on_UnaryOp(self, _):
        raise NotImplementedError
    
    def run_on_Attribute(self, _):
        raise NotImplementedError
