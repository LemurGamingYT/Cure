from codegen.std.big.constants import MAX_DIGITS
from codegen.std.big.BigFloat import BigFloat
from codegen.std.big.BigInt import BigInt


class big:
    def __init__(self, codegen) -> None:
        codegen.add_type(('BigInt', 'BigFloat'))
        codegen.c_manager.reserve(('BigInt', 'BigFloat'))
        codegen.c_manager.add_objects(BigInt(), self)
        codegen.c_manager.add_objects(BigFloat(), self)
        codegen.add_toplevel_code(f"""#ifndef CURE_BIG_H
typedef struct {{
    char digits[{MAX_DIGITS}];
    size_t length;
}} BigInt;

typedef struct {{
    BigInt integer_part;
    BigInt fractional_part;
    int exponent;
}} BigFloat;
#define CURE_BIG_H
#endif
""")
