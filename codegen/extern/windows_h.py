from codegen.target import Target



class windows_h:
    def __init__(self, codegen) -> None:
        if codegen.target != Target.WINDOWS:
            codegen.pos.error_here('Target is not Windows yet windows.h is tried to be used')
