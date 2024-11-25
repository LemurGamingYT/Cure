from codegen.c_manager import INCLUDES
from codegen.std.ai.ann import ANN


GENANN_PATH = (INCLUDES / 'genann').absolute()

class ai:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code("""#ifndef CURE_AI_H
#define CURE_AI_H
""")
        codegen.c_manager.include(f'"{(GENANN_PATH / "genann.h").as_posix()}"', codegen)
        codegen.extra_compile_args.append((GENANN_PATH / 'genann.c').as_posix())
        codegen.c_manager.add_objects(ANN(codegen), self)
        codegen.add_toplevel_code('#endif')
