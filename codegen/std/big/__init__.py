
from codegen.std.big.BigFloat import BigFloat
from codegen.std.big.BigInt import BigInt


class big:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type(('BigInt', 'BigFloat'))
        codegen.c_manager.reserve(('BigInt', 'BigFloat'))
        codegen.add_toplevel_code("""#ifndef CURE_BIG_H
#define CURE_BIG_H
""")
        codegen.c_manager.add_objects(BigInt(codegen), self)
        codegen.c_manager.add_objects(BigFloat(codegen), self)
        codegen.add_toplevel_code('#endif')
