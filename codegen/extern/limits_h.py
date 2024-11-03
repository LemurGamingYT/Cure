from codegen.objects import Type


class limits_h:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_constant('CHAR_BIT', Type('int'), add_code=False)
        codegen.add_toplevel_constant('SCHAR_MIN', Type('int'), add_code=False)
        codegen.add_toplevel_constant('SCHAR_MAX', Type('int'), add_code=False)
        codegen.add_toplevel_constant('UCHAR_MAX', Type('int'), add_code=False)
        codegen.add_toplevel_constant('CHAR_MIN', Type('int'), add_code=False)
        codegen.add_toplevel_constant('CHAR_MAX', Type('int'), add_code=False)
        codegen.add_toplevel_constant('MB_CHAR_LEN', Type('int'), add_code=False)
        codegen.add_toplevel_constant('SHRT_MIN', Type('int'), add_code=False)
        codegen.add_toplevel_constant('SHRT_MAX', Type('int'), add_code=False)
        codegen.add_toplevel_constant('USHRT_MAX', Type('int'), add_code=False)
        codegen.add_toplevel_constant('INT_MIN', Type('int'), add_code=False)
        codegen.add_toplevel_constant('INT_MAX', Type('int'), add_code=False)
        
        # TODO: Implement unsigned integer, long and unsigned long min and max values
