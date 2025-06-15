from logging import debug

from llvmlite import ir as lir

from cure.codegen_utils import set_struct_field, get_struct_field_ptr, NULL, get_type_size
from cure.lib import function, Lib, DefinitionContext
from cure import ir


class Ref(Lib):
    @function([
        ir.Param(ir.Position.zero(), 'data', ir.Type.pointer()),
        ir.Param(ir.Position.zero(), 'destroy_fn', ir.Type.any())
    ], ir.Type.Ref().as_pointer(), flags=ir.FunctionFlags(static=True, method=True))
    @staticmethod
    def Ref_new(ctx: DefinitionContext):
        malloc = ctx.c_registry.get('malloc')

        data = ctx.param('data').value
        destroy_fn = ctx.param('destroy_fn').value

        ref_type = ir.Type.Ref()
        struct_size = get_type_size(ctx.builder, ref_type.type)

        ptr = ctx.builder.bitcast(
            ctx.builder.call(malloc, [struct_size]), 
            ref_type.type.as_pointer()
        )

        debug('Allocating Ref pointer')
        
        set_struct_field(ctx.builder, ptr, 0, data)
        set_struct_field(ctx.builder, ptr, 1, destroy_fn)
        set_struct_field(ctx.builder, ptr, 2, lir.Constant(lir.IntType(64), 1))

        return ptr
    
    @function([ir.Param(ir.Position.zero(), 'self', ir.Type.Ref().as_pointer())],
              flags=ir.FunctionFlags(method=True))
    @staticmethod
    def Ref_inc(ctx: DefinitionContext):
        self = ctx.param('self').value
        ref_count_ptr = get_struct_field_ptr(ctx.builder, self, 2)
        debug(f'Incrementing Ref pointer {self}')

        ref_count = ctx.builder.load(ref_count_ptr)
        one = lir.Constant(lir.IntType(64), 1)
        new_count = ctx.builder.add(ref_count, one)
        ctx.builder.store(new_count, ref_count_ptr)
    
    @function([ir.Param(ir.Position.zero(), 'self', ir.Type.Ref().as_pointer())],
              flags=ir.FunctionFlags(method=True))
    @staticmethod
    def Ref_dec(ctx: DefinitionContext):
        self = ctx.param('self').value

        ref_count_ptr = get_struct_field_ptr(ctx.builder, self, 2)
        ref_count = ctx.builder.load(ref_count_ptr)
        one = lir.Constant(lir.IntType(64), 1)
        new_count = ctx.builder.sub(ref_count, one)
        ctx.builder.store(new_count, ref_count_ptr)
        debug('Decrementing Ref pointer')

        zero = lir.Constant(lir.IntType(64), 0)
        with ctx.builder.if_then(ctx.builder.icmp_signed('==', new_count, zero)):
            free = ctx.c_registry.get('free')

            data_ptr_ptr = get_struct_field_ptr(ctx.builder, self, 0)
            data_ptr = ctx.builder.load(data_ptr_ptr)
            
            destroy_fn_ptr = get_struct_field_ptr(ctx.builder, self, 1)
            destroy_fn = ctx.builder.load(destroy_fn_ptr)
            
            func_ptr_type = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(8).as_pointer()
            ]).as_pointer()
            null_func_ptr = lir.Constant(func_ptr_type, None)
            
            with ctx.builder.if_else(ctx.builder.icmp_signed('!=', destroy_fn, null_func_ptr))\
                as (then, else_):
                with then:
                    ctx.builder.call(destroy_fn, [data_ptr])
                
                with else_:
                    ctx.builder.call(free, [data_ptr])
            
            self_cast = ctx.builder.bitcast(self, lir.IntType(8).as_pointer())
            ctx.builder.call(free, [self_cast])
    

    @function([ir.Param(ir.Position.zero(), 'ptr', ir.Type.any())], ir.Type.any())
    @staticmethod
    def free_wrapper(ctx: DefinitionContext):
        ptr = ctx.param('ptr').value

        free = ctx.c_registry.get('free')

        ctx.builder.call(free, [ptr])
        ctx.builder.ret(NULL())
