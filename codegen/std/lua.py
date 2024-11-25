from codegen.objects import Object, Position, Type, Param, TempVar, Free
from codegen.function_manager import OverloadKey, OverloadValue
from codegen.c_manager import c_dec, INCLUDES


LUA_PATH = (INCLUDES / 'lua').absolute()

class lua:
    def __init__(self, codegen) -> None:
        codegen.type_checker.add_type('LuaInterpreter')
        codegen.add_toplevel_code("""#ifndef CURE_LUA_H
#define CURE_LUA_H
""")
        codegen.c_manager.include(f'"{(LUA_PATH / "lua.h").as_posix()}"', codegen)
        codegen.c_manager.include(f'"{(LUA_PATH / "lualib.h").as_posix()}"', codegen)
        codegen.c_manager.include(f'"{(LUA_PATH / "lauxlib.h").as_posix()}"', codegen)
        
        codegen.extra_compile_args.extend((f'{LUA_PATH}/*.c', f'-I{LUA_PATH}'))
        codegen.add_toplevel_code("""typedef lua_State* LuaInterpreter;
#endif
""")
        
        codegen.c_manager.init_class(self, 'LuaInterpreter', Type('LuaInterpreter'))
        
        
        @c_dec(
            params=(Param('interpreter', Type('LuaInterpreter')), Param('name', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _LuaInterpreter_get_global(codegen, call_position: Position,
                                       interpreter: Object, name: Object) -> Object:
            codegen.prepend_code(f'lua_getglobal({interpreter}, {name});')
            return Object.NULL(call_position)
        
        def push_float_overload(codegen, call_position: Position, interpreter: Object,
                                number: Object) -> Object:
            return _LuaInterpreter_push_number(codegen, call_position, interpreter, number)
        
        @c_dec(
            params=(Param('interpreter', Type('LuaInterpreter')), Param('number', Type('int'))),
            is_method=True, add_to_class=self, overloads={
                OverloadKey(Type('nil'), (Param('interpreter', Type('LuaInterpreter')),
                                          Param('number', Type('float')))): OverloadValue(
                                              push_float_overload)
            }
        )
        def _LuaInterpreter_push_number(codegen, call_position: Position,
                                        interpreter: Object, number: Object) -> Object:
            codegen.prepend_code(f'lua_pushnumber({interpreter}, {number});')
            return Object.NULL(call_position)
        
        @c_dec(
            params=(Param('interpreter', Type('LuaInterpreter')), Param('n', Type('int')),
                    Param('r', Type('int'))),
            is_method=True, add_to_class=self
        )
        def _LuaInterpreter_call(codegen, call_position: Position,
                                 interpreter: Object, n: Object, r: Object) -> Object:
            codegen.prepend_code(f'lua_call({interpreter}, {n}, {r});')
            return Object.NULL(call_position)
        
        @c_dec(
            params=(Param('interpreter', Type('LuaInterpreter')), Param('filename', Type('string'))),
            is_method=True, add_to_class=self
        )
        def _LuaInterpreter_execute_file(codegen, call_position: Position,
                                         interpreter: Object, filename: Object) -> Object:
            codegen.prepend_code(f"""if (luaL_dofile({interpreter}, {filename}) != LUA_OK) {{
    {codegen.c_manager.err('Could not execute file')}
}}
""")
            return Object.NULL(call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _LuaInterpreter_new(codegen, call_position: Position) -> Object:
            interp_free = Free(free_name='lua_close')
            interpreter: TempVar = codegen.create_temp_var(
                Type('LuaInterpreter'), call_position, free=interp_free,
                default_expr='luaL_newstate()'
            )
            
            codegen.prepend_code(f'luaL_openlibs({interpreter});')
            return interpreter.OBJECT()
