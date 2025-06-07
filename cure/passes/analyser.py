from typing import cast

from cure.passes import CompilerPass
from cure import ir


INT_MAX = 2_147_483_647
INT_MIN = -2_147_483_648


class Analyser(CompilerPass):
    def run_on_Program(self, node: ir.Program):
        nodes = []
        for n in node.nodes:
            nodes.append(self.run_on(n))
        
        return ir.Program(node.pos, nodes)
    
    def run_on_Param(self, node: ir.Param):
        return ir.Param(node.pos, node.name, self.run_on(node.type))
    
    def run_on_Body(self, node: ir.Body):
        self.scope = self.scope.clone()
        nodes = []
        for n in node.nodes:
            nodes.append(self.run_on(n))
        
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
        for param in params:
            self.scope.symbol_table.add(ir.Symbol(param.name, param.type, param))
        
        body = self.run_on(node.body) if isinstance(node.body, ir.Body) else node.body

        for param in params:
            self.scope.symbol_table.remove(param.name)

        func = ir.Function(node.pos, node.name, params, type, body, node.flags, node.overloads)
        self.scope.symbol_table.add(ir.Symbol(node.name, ir.Type.function(), func))
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
    
    def run_on_Int(self, node: ir.Int):
        if node.value > INT_MAX:
            node.pos.comptime_error('integer value is too large for a 32-bit integer', self.scope.src)
        
        if node.value < INT_MIN:
            node.pos.comptime_error('integer value is too small for a 32-bit integer', self.scope.src)
        
        return node
    
    def run_on_Float(self, node: ir.Float):
        return node
    
    def run_on_String(self, node: ir.String):
        return node
    
    def run_on_Bool(self, node: ir.Bool):
        return node
    
    def run_on_Nil(self, node: ir.Nil):
        return node
    
    def run_on_Id(self, node: ir.Id):
        symbol = self.scope.symbol_table.get(node.name)
        if symbol is None:
            node.pos.comptime_error(f'unknown identifier \'{node.name}\'', self.scope.src)
            return
        
        return ir.Id(node.pos, symbol.name, symbol.type)
    
    def run_on_Call(self, node: ir.Call):
        symbol = self.scope.symbol_table.get(node.callee)
        if symbol is None:
            node.pos.comptime_error(f'unknown callable \'{node.callee}\'', self.scope.src)
            return
        
        args = [self.run_on(arg) for arg in node.args]
        params = symbol.value.params
        if len(args) > len(params):
            node.pos.comptime_error('too many arguments', self.scope.src)
        elif len(args) < len(params):
            node.pos.comptime_error('not enough arguments', self.scope.src)

        ret_type = symbol.value.ret_type
        for i, (arg, param) in enumerate(zip(args, params), 1):
            arg_type = arg.get_type()
            param_type = param.type
            if param_type == arg_type or param_type == ir.Type.any():
                continue

            arg.pos.comptime_error(
                f'argument #{i} (type \'{arg_type}\') does not match expected type \'{param_type}\'',
                self.scope.src
            )
        
        return ir.Call(node.pos, node.callee, args, ret_type)
    
    def run_on_BinaryOp(self, node: ir.BinaryOp):
        lhs = self.run_on(node.left)
        rhs = self.run_on(node.right)
        op_name = ir.op_map[node.op]
        callee = f'{lhs.get_type()}_{op_name}_{rhs.get_type()}'
        return self.run_on(ir.Call(node.pos, callee, [lhs, rhs]))
