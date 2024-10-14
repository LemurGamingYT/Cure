from codegen.objects import Object, Position, Type, Param
from codegen.std.ui.widget import WidgetType
from codegen.c_manager import c_dec


class Button:
    def __init__(self, codegen, widget) -> None:
        codegen.add_toplevel_code(f"""typedef struct {{
    Widget* widget;
}} {WidgetType.BUTTON.value};
""")
        
        codegen.type_checker.add_type('Button')
        codegen.c_manager.init_class(self, 'Button', Type('Button'))
        
        @c_dec(
            param_types=(
                Param('parent', Type('Window')),
                Param('text', Type('string'), default=Object('"Button"', Type('string'))),
                Param('width', Type('int'), default=Object('100', Type('int'))),
                Param('height', Type('int'), default=Object('20', Type('int'))),
                Param('bg_color', Type('Color'), default=Object(
                    '(Color){255, 255, 255}', Type('Color')
                )),
                Param('text_color', Type('Color'), default=Object(
                    '(Color){0, 0, 0}', Type('Color'))
                ),
                Param('clicked', Type('function'), default=Object('NULL', Type('function'))),
                Param('font', Type('Font'), default=Object(
                    '(Font){ "Segoe UI", 12, FW_NORMAL }', Type('Font')
                ))
            ),
            is_method=True, is_static=True, add_to_class=self
        )
        def _Button_new(codegen, call_position: Position, *args) -> Object:
            kwargs = _Button_new.get_kwargs(args)
            return widget.create_widget(codegen, WidgetType.BUTTON, call_position, **kwargs)
