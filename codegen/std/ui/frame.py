from codegen.objects import Object, Position, Type, Param
from codegen.std.ui.widget import WidgetType
from codegen.c_manager import c_dec


class Frame:
    def __init__(self, codegen, widget) -> None:
        codegen.add_toplevel_code(f"""typedef struct {{
    Widget* widget;
}} {WidgetType.FRAME.value};
""")
        
        codegen.type_checker.add_type('Frame')
        codegen.c_manager.init_class(self, 'Frame', Type('Frame'))
        
        @c_dec(
            param_types=(
                Param('parent', Type('Window')),
                Param('width', Type('int'), default=Object('100', Type('int'))),
                Param('height', Type('int'), default=Object('20', Type('int'))),
                Param('bg_color', Type('Color'), default=Object(
                    '(Color){255, 255, 255}', Type('Color')))
            ),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Frame_new(codegen, call_position: Position, *args) -> Object:
            kwargs = _Frame_new.get_kwargs(args)
            return widget.create_widget(codegen, WidgetType.FRAME, call_position, **kwargs)
