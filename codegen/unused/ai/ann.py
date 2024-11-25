from codegen.objects import Object, Position, Free, TempVar, Type, Param, Arg
from codegen.c_manager import c_dec


class ANN:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type(Type('ANN'))
        codegen.c_manager.init_class(self, 'ANN', Type('ANN'))
        codegen.add_toplevel_code('typedef genann* ANN;')
        
        codegen.c_manager.wrap_struct_properties('ann', Type('ANN'), [
            Param('inputs', Type('int')), Param('outputs', Type('int')),
            Param('hidden_layers', Type('int')), Param('hidden_neurons', Type('int'))
        ], True)
        
        @c_dec(params=(Param('ann', Type('ANN')),), is_method=True, add_to_class=self)
        def _ANN_to_string(codegen, call_position: Position, ann: Object) -> Object:
            code, buf_free = codegen.c_manager.fmt_length(
                codegen, call_position,
                '"ANN(inputs=%d, outputs=%d, hidden_layers=%d, hidden_neurons=%d)"',
                f'({ann})->inputs', f'({ann})->outputs', f'({ann})->hidden_layers',
                f'({ann})->hidden'
            )
            
            codegen.prepend_code(code)
            return Object.STRINGBUF(buf_free, call_position)
        
        array_type: Type = codegen.array_manager.define_array(Type('int'))
        inputs_array_type: Type = codegen.array_manager.define_array(array_type)
        
        @c_dec(params=(
            Param('ann', Type('ANN')), Param('inputs', inputs_array_type),
            Param('outputs', array_type), Param('epochs', Type('int'),),
            Param('learning_rate', Type('float')),
        ), is_method=True, add_to_class=self)
        def _ANN_train(codegen, call_position: Position, ann: Object, inputs: Object,
                       outputs: Object, epochs: Object, learning_rate: Object) -> Object:
            epoch: TempVar = codegen.create_temp_var(Type('int'), call_position)
            i: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""for (int {epoch} = 0; {epoch} < ({epochs}); {epoch}++) {{
for (int {i} = 0; {i} < ({inputs}).length; {i}++) {{
""")
            codegen.prepend_code(f"""genann_train({ann}, (const double*){codegen.call(
    f'index_{inputs_array_type.c_type}', [Arg(inputs), Arg(i.OBJECT())], call_position
)}, {codegen.call(f'index_{array_type.c_type}', [
    Arg(outputs), Arg(i.OBJECT())], call_position)}, {learning_rate});
}}
}}
""")
            
            return Object.NULL(call_position)
        
        @c_dec(
            params=(Param('ann', Type('ANN')), Param('inputs', array_type)),
            is_method=True, add_to_class=self
        )
        def _ANN_predict(_, call_position: Position, ann: Object, inputs: Object) -> Object:
            return Object(f'(float)*genann_run({ann}, {inputs})', Type('float'), call_position)
        
        @c_dec(params=(
            Param('inputs', Type('int')), Param('outputs', Type('int')),
            Param('hidden_layers', Type('int')), Param('hidden_neurons', Type('int'))
        ), is_method=True, is_static=True, add_to_class=self)
        def _ANN_new(codegen, call_position: Position, inputs: Object, outputs: Object,
                     hidden_layers: Object, hidden_neurons: Object) -> Object:
            ann: TempVar = codegen.create_temp_var(
                Type('ANN'), call_position, free=Free(free_name='genann_free'),
                default_expr=f'genann_init({inputs}, {hidden_layers}, {hidden_neurons}, {outputs})'
            )
            
            return ann.OBJECT()
