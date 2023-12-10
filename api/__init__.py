from dataclasses import dataclass, field
from typing import Any


kwargs = {'unsafe_hash': True}


@dataclass(**kwargs)
class Arg:
    value: Any

@dataclass(**kwargs)
class Args:
    args: list[Arg]

@dataclass(**kwargs)
class Param:
    name: str
    type: str = field(default='auto')
    default: Any = field(default=None)

@dataclass(**kwargs)
class Params:
    params: list[Param]

@dataclass(**kwargs)
class Assignment:
    name: str
    value: Any = field(default=None)
    type: str = field(default='auto')

@dataclass(**kwargs)
class Call:
    name: str
    args: Args = field(default_factory=Args)

@dataclass(**kwargs)
class InputOp:
    function: str = field(default='std::cin')
    args: Args = field(default_factory=Args)

@dataclass(**kwargs)
class OutputOp:
    function: str = field(default='std::cout')
    args: Args = field(default_factory=Args)

@dataclass(**kwargs)
class BinaryOp:
    left: Any
    right: Any
    op: str

@dataclass(**kwargs)
class UnaryOp:
    value: Any
    op: str

@dataclass(**kwargs)
class Body:
    stmts: list[Any]
    spaces: int = 4

@dataclass(**kwargs)
class Return:
    value: Any

@dataclass(**kwargs)
class If:
    condition: Any
    body: Body
    else_body: Body = field(default=None)
    elseif: dict[Any: Body] = field(default_factory=dict)

@dataclass(**kwargs)
class While:
    condition: Any
    body: Body

@dataclass(**kwargs)
class For:
    init: Any
    condition: Any
    step: Any
    body: Body

@dataclass(**kwargs)
class FuncDef:
    name: str
    type: str
    params: Params
    body: Body

@dataclass(**kwargs)
class GetAttr:
    obj: Any
    attr: str
    is_pointer: bool = field(default=True)
    args: Args | None = field(default=None)

@dataclass(**kwargs)
class CompileTime:
    stmt: Any

@dataclass(**kwargs)
class Include:
    name: str
    use_crocodiles: bool = True

@dataclass(**kwargs)
class Empty:
    pass

@dataclass(**kwargs)
class LiteralCode:
    code: str

@dataclass(**kwargs)
class Program:
    stmts: list[Any]

@dataclass(**kwargs)
class Using:
    items: list[str]
    namespace: bool = field(default=False)


class ASTVisitor:
    def visit(self, node: Any) -> str:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, None)
        if method is None:
            if hasattr(node, 'as_c'):
                return node.as_c()
            
            print(f'No Method for {type(node).__name__}')
            return ''
        
        return method(node)

    def visit_Program(self, program: Program) -> str:
        return '\n'.join(self.visit(node) + '\n' for node in program.stmts)

    @staticmethod
    def visit_Using(node: Using) -> str:
        return f'using {"namespace" if node.namespace else ""} {", ".join(node.items)}'

    def visit_FuncDef(self, node: FuncDef) -> str:
        return f'{node.type} {node.name}({self.visit(node.params)})'\
            f'\n{{\n{self.visit(node.body)}\n}}'

    def visit_If(self, node: If) -> str:
        return f'if ({self.visit(node.condition)})\n{{\n{self.visit(node.body)}\n}}'\
            + (' else\n' + self.visit(node.else_body) + '\n' if node.else_body else '')\
            + ''.join(f' else if ({self.visit(condition)})\n{{\n{self.visit(body)}\n}}'
                      for condition, body in node.elseif.items())
    
    def visit_While(self, node: While) -> str:
        return f'while ({self.visit(node.condition)})\n{{\n{self.visit(node.body)}\n}}'

    # def visit_CompileTime(self, node: CompileTime) -> str:
    #     return f'constexpr {self.visit(node.stmt)}'

    @staticmethod
    def visit_Include(node: Include) -> str:
        return f'#include <{node.name}>' if node.use_crocodiles else\
            f'#include "{node.name}"'

    def visit_Body(self, node: Body) -> str:
        return '\n'.join((' ' * node.spaces) + self.visit(stmt) + ';' for stmt in node.stmts)
    
    def visit_Args(self, node: Args) -> str:
        return ', '.join(self.visit(arg) for arg in node.args)
    
    def visit_Arg(self, node: Arg) -> str:
        return self.visit(node.value)
    
    def visit_Params(self, node: Params) -> str:
        return ', '.join(self.visit(param) for param in node.params)
    
    def visit_Param(self, node: Param) -> str:
        default = f' = {self.visit(node.default)}' if node.default is not None else ''
        return f'{node.type} {node.name}{default}'
    
    def visit_Return(self, node: Return) -> str:
        return f'return {self.visit(node.value)}'
    
    def visit_Call(self, node: Call) -> str:
        return f'{node.name}({self.visit(node.args)})'
    
    def visit_GetAttr(self, node: GetAttr) -> str:
        op = '->' if node.is_pointer else '.'
        args = '' if node.args is None else f'({self.visit(node.args)})'
        return f'{self.visit(node.obj)}{op}{node.attr}{args}'
    
    def visit_Assignment(self, node: Assignment) -> str:
        return f'{node.type} {node.name} = {self.visit(node.value)}'
    
    def visit_OutputOp(self, node: OutputOp) -> str:
        return f'{node.function}{"".join(" << " + self.visit(arg) for arg in node.args.args)}'
    
    def visit_InputOp(self, node: InputOp) -> str:
        return f'{node.function}{"".join(" >> " + self.visit(arg) for arg in node.args.args)}'

    @staticmethod
    def visit_LiteralCode(node: LiteralCode) -> str:
        return node.code
    
    def visit_BinaryOp(self, node: BinaryOp) -> str:
        return f'{self.visit(node.left)} {node.op} {self.visit(node.right)}'

    def visit_UnaryOp(self, node: UnaryOp) -> str:
        return f'{node.op}{self.visit(node.value)}'
