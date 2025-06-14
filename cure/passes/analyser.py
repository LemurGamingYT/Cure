from pprint import pformat
from logging import info
from typing import cast

from cure.codegen_utils import max_value, min_value
from cure.ir import match_to_overloads
from cure.passes import CompilerPass
from cure import ir


INT_MAX = max_value(32)
INT_MIN = min_value(32)


class Analyser(CompilerPass):
    def run_on_Program(self, node: ir.Program):
        info(f'Analysing program {pformat(node, indent=4)}')

        nodes = []
        for n in node.nodes:
            info(f'Analysing {n.__class__.__name__}')
            nodes.append(self.run_on(n))
        
        info(f'Finished analysing program {pformat(node, indent=4)}')
        return ir.Program(node.pos, nodes)
    
    def run_on_Type(self, node: ir.Type):
        return node
    
    def run_on_Param(self, node: ir.Param):
        return ir.Param(node.pos, node.name, self.run_on(node.type))
    
    def run_on_Body(self, node: ir.Body):
        self.scope = self.scope.clone()

        info('Entered child scope for body')
        nodes = []
        for n in node.nodes:
            info(f'Analysing body node {n.__class__.__name__}')
            nodes.append(self.run_on(n))

        info('Exiting body')
        self.scope = cast(ir.Scope, self.scope.parent)
        return ir.Body(node.pos, nodes)
    
    def run_on_Elif(self, node: ir.Elif):
        return ir.Elif(node.pos, self.run_on(node.condition), self.run_on(node.body))
    
    def run_on_If(self, node: ir.If):
        return ir.If(
            node.pos, self.run_on(node.condition), self.run_on(node.body),
            self.run_on(node.else_body) if node.else_body is not None else node.else_body,
            [self.run_on(elseif) for elseif in node.elseifs]
        )
    
    def run_on_While(self, node: ir.While):
        return ir.While(node.pos, self.run_on(node.condition), self.run_on(node.body))
    
    def run_on_Function(self, node: ir.Function):
        params = [self.run_on(param) for param in node.params]
        type = self.run_on(node.type)
        func = ir.Function(node.pos, node.name, params, type, node.body, node.flags, node.overloads)
        self.scope.symbol_table.add(ir.Symbol(node.name, ir.TypeManager.get('function'), func))

        info('Adding parameters to environment')
        for param in params:
            self.scope.symbol_table.add(ir.Symbol(param.name, param.type, param))
        
        body = self.run_on(node.body) if isinstance(node.body, ir.Body) else node.body

        info('Removing parameters from environment')
        for param in params:
            self.scope.symbol_table.remove(param.name)

        func.body = body
        return func
    
    def run_on_Variable(self, node: ir.Variable):
        value = self.run_on(node.value) if node.value is not None else node.value
        if self.scope.symbol_table.has(node.name) and value is not None:
            return self.run_on(ir.Assignment(node.pos, node.name, value))
        
        var_type = value.get_type() if value is not None else node.type
        self.scope.symbol_table.add(ir.Symbol(node.name, var_type, value))
        return ir.Variable(node.pos, node.name, value, var_type)
    
    def run_on_Assignment(self, node: ir.Assignment):
        symbol = self.scope.symbol_table.get(node.name)
        if symbol is None:
            raise RuntimeError()

        symbol.value = node.value
        return node
    
    def run_on_Return(self, node: ir.Return):
        value = self.run_on(node.value)
        return ir.Return(node.pos, value)
    
    def run_on_Int(self, node: ir.Int):
        if node.value > INT_MAX:
            node.pos.comptime_error('integer value is too large for a 32-bit integer', self.scope.src)
        
        if node.value < INT_MIN:
            node.pos.comptime_error('integer value is too small for a 32-bit integer', self.scope.src)
        
        return node
    
    def run_on_Float(self, node: ir.Float):
        return node
    
    def run_on_String(self, node: ir.String):
        return self.run_on(ir.Call(node.pos, 'string_new', [
            ir.StringLiteral(node.pos, node.value),
            ir.Int(node.pos, len(node.value))
        ]))
    
    def run_on_Bool(self, node: ir.Bool):
        return node
    
    def run_on_Nil(self, node: ir.Nil):
        return node
    
    def run_on_StringLiteral(self, node: ir.StringLiteral):
        return node
    
    def run_on_Id(self, node: ir.Id):
        symbol = self.scope.symbol_table.get(node.name)
        type = ir.TypeManager.get(node.name)
        if symbol is None and type is None:
            node.pos.comptime_error(f'unknown identifier \'{node.name}\'', self.scope.src)
            return
        
        if symbol is not None:
            return ir.Id(node.pos, symbol.name, symbol.type)
        
        return ir.Id(node.pos, node.name, type)
    
    def run_on_Call(self, node: ir.Call):
        symbol = self.scope.symbol_table.get(node.callee)
        if symbol is None:
            node.pos.comptime_error(f'unknown callable \'{node.callee}\'', self.scope.src)
            return
        
        args = [self.run_on(arg) for arg in node.args]
        func = symbol.value

        # attributes
        if func.flags.static:
            args = args[1:]
        
        func = match_to_overloads(func, [arg.get_type() for arg in args])

        ret_type = func.ret_type
        return ir.Call(node.pos, node.callee, args, ret_type)
    
    def run_on_BinaryOp(self, node: ir.BinaryOp):
        lhs = self.run_on(node.left)
        rhs = self.run_on(node.right)
        ltype = lhs.get_type()
        rtype = rhs.get_type()
        op_name = ir.op_map[node.op]
        callee = f'{ltype}_{op_name}_{rtype}'
        if not self.scope.symbol_table.has(callee):
            node.pos.comptime_error(
                f'unsupported operation \'{node.op}\' between types \'{ltype}\' and \'{rtype}\'',
                self.scope.src
            )
        
        return self.run_on(ir.Call(node.pos, callee, [lhs, rhs]))
    
    def run_on_UnaryOp(self, node: ir.UnaryOp):
        expr = self.run_on(node.expr)
        op_name = ir.op_map[node.op]
        callee = f'{op_name}_{expr.get_type()}'
        if not self.scope.symbol_table.has(callee):
            node.pos.comptime_error(
                f'unsupported operation \'{node.op}\' on type \'{expr.get_type()}\'',
                self.scope.src
            )
        
        return self.run_on(ir.Call(node.pos, callee, [expr]))
    
    def run_on_Attribute(self, node: ir.Attribute):
        obj = self.run_on(node.obj)
        args = [obj] + ([self.run_on(arg) for arg in node.args] if node.args is not None else [])
        callee = f'{obj.get_type()}_{node.attr}'
        if not self.scope.symbol_table.has(callee):
            node.pos.comptime_error(
                f'unknown attribute \'{node.attr}\' on type \'{obj.get_type()}\'',
                self.scope.src
            )
        
        return self.run_on(ir.Call(node.pos, callee, args))
