from codegen.objects import Object, Position, Param, Free, Type, TempVar
from codegen.c_manager import c_dec


class MutexLock:
    def __init__(self, codegen) -> None:
        codegen.add_toplevel_code('typedef mtx_t MutexLock;')
        codegen.c_manager.init_class(self, 'MutexLock', Type('MutexLock'))
        
        
        @c_dec(params=(Param('mtx', Type('MutexLock')),), is_property=True, add_to_class=self)
        def _MutexLock_is_locked(_, call_position: Position, mtx: Object) -> Object:
            return Object(f'((bool)(({mtx}).mAlreadyLocked))', Type('bool'), call_position)
        
        @c_dec(params=(Param('mtx', Type('MutexLock')),), is_method=True, add_to_class=self)
        def _MutexLock_lock(codegen, call_position: Position, mtx: Object) -> Object:
            res: TempVar = codegen.create_temp_var(Type('int'), call_position)
            codegen.prepend_code(f"""int {res} = mtx_lock(&{mtx});
if ({res} != thrd_success) {{
    {codegen.c_manager.err('Failed to lock mutex')}
}}
""")
            return res.OBJECT()
        
        @c_dec(params=(Param('mtx', Type('MutexLock')),), is_method=True, add_to_class=self)
        def _MutexLock_unlock(codegen, call_position: Position, mtx: Object) -> Object:
            codegen.prepend_code(f"""if (mtx_unlock(&{mtx}) != thrd_success) {{
    {codegen.c_manager.err('Failed to unlock mutex')}
}}
""")
            return Object.NULL(call_position)
        
        @c_dec(is_method=True, is_static=True, add_to_class=self)
        def _MutexLock_new(codegen, call_position: Position) -> Object:
            mtx_free = Free(free_name='mtx_destroy')
            mtx: TempVar = codegen.create_temp_var(Type('MutexLock'), call_position, free=mtx_free)
            mtx_free.object_name = f'&{mtx}'
            
            codegen.prepend_code(f"""mtx_t {mtx};
if (mtx_init(&{mtx}, mtx_plain) != thrd_success) {{
    {codegen.c_manager.err('Failed to create mutex')}
}}
""")
            
            return mtx.OBJECT()
