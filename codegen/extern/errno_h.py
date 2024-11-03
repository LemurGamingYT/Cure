from codegen.objects import Type


class errno_h:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_constant('errno', Type('int'), add_code=False)
