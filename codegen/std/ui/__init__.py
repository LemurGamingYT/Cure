from codegen.std.ui.window import Window
from codegen.std.ui.widget import Widget
from codegen.std.ui.button import Button
from codegen.std.ui.label import Label
from codegen.std.ui.frame import Frame
from codegen.std.ui.font import Font
from codegen.target import Target


class ui:
    def __init__(self, codegen) -> None:
        if codegen.target == Target.WINDOWS:
            codegen.extra_compile_args.append('-lgdi32')
        else:
            codegen.pos.warn_here('\'ui\' is only supported on windows')
        
        codegen.dependency_manager.use('color', codegen.pos)
        codegen.add_toplevel_code("""#ifndef CURE_UI_H
#define CURE_UI_H
#pragma comment(lib, "gdi32.lib")
""")
        
        codegen.c_manager.add_objects(Font(codegen), self)
        
        widget = Widget(codegen)
        codegen.c_manager.add_objects(widget, self)
        codegen.c_manager.add_objects(Window(codegen, widget), self)
        codegen.c_manager.add_objects(Frame(codegen, widget), self)
        codegen.c_manager.add_objects(Label(codegen, widget), self)
        codegen.c_manager.add_objects(Button(codegen, widget), self)
        codegen.add_toplevel_code('#endif')
