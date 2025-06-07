from llvmlite import ir as lir

from cure.lib import function, Lib, DefinitionContext
from cure import ir
from cure.codegen_utils import (
    get_or_add_global, create_string_constant, create_struct_value, get_struct_field_value
)


class operations(Lib):
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.int())
    @staticmethod
    def int_add_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        intrinsic_name = f'llvm.sadd.with.overflow.{ir.Type.int().type}'
        res_type = lir.LiteralStructType([ir.Type.int().type, lir.IntType(1)])
        intrinsic = get_or_add_global(ctx.module, intrinsic_name, lir.Function(
            ctx.module, lir.FunctionType(res_type, [lir.IntType(32), lir.IntType(32)]),
            intrinsic_name
        ))
        struct = ctx.builder.call(intrinsic, [a, b])
        res = get_struct_field_value(ctx.builder, struct, 0)
        overflow = get_struct_field_value(ctx.builder, struct, 1)

        overflow_block = ctx.builder.function.append_basic_block('overflow')
        success_block = ctx.builder.function.append_basic_block()
        ctx.builder.cbranch(overflow, overflow_block, success_block)

        ctx.builder.position_at_end(overflow_block)
        err_str = 'integer overflow'
        err_msg = create_string_constant(ctx.module, err_str)
        err_string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [
            err_msg, lir.Constant(lir.IntType(64), len(err_str))
        ])
        ctx.call('error', [err_string_struct])
        ctx.builder.ret(lir.Constant(lir.IntType(32), 0))

        ctx.builder.position_at_end(success_block)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.int())
    @staticmethod
    def int_sub_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        intrinsic_name = f'llvm.ssub.with.overflow.{ir.Type.int().type}'
        res_type = lir.LiteralStructType([ir.Type.int().type, lir.IntType(1)])
        intrinsic = get_or_add_global(ctx.module, intrinsic_name, lir.Function(
            ctx.module, lir.FunctionType(res_type, [lir.IntType(32), lir.IntType(32)]),
            intrinsic_name
        ))
        struct = ctx.builder.call(intrinsic, [a, b])
        res = get_struct_field_value(ctx.builder, struct, 0)
        underflow = get_struct_field_value(ctx.builder, struct, 1)

        underflow_block = ctx.builder.function.append_basic_block('underflow')
        success_block = ctx.builder.function.append_basic_block()
        ctx.builder.cbranch(underflow, underflow_block, success_block)

        ctx.builder.position_at_end(underflow_block)
        err_str = 'integer underflow'
        err_msg = create_string_constant(ctx.module, err_str)
        err_string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [
            err_msg, lir.Constant(lir.IntType(64), len(err_str))
        ])
        ctx.call('error', [err_string_struct])
        ctx.builder.ret(lir.Constant(lir.IntType(32), 0))

        ctx.builder.position_at_end(success_block)
        ctx.builder.ret(res)

    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.int())
    @staticmethod
    def int_mul_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value
        intrinsic_name = f'llvm.smul.with.overflow.{ir.Type.int().type}'
        res_type = lir.LiteralStructType([ir.Type.int().type, lir.IntType(1)])
        intrinsic = get_or_add_global(ctx.module, intrinsic_name, lir.Function(
            ctx.module, lir.FunctionType(res_type, [lir.IntType(32), lir.IntType(32)]),
            intrinsic_name
        ))
        struct = ctx.builder.call(intrinsic, [a, b])
        res = get_struct_field_value(ctx.builder, struct, 0)
        underflow = get_struct_field_value(ctx.builder, struct, 1)

        overflow_block = ctx.builder.function.append_basic_block('overflow')
        success_block = ctx.builder.function.append_basic_block()
        ctx.builder.cbranch(underflow, overflow_block, success_block)

        ctx.builder.position_at_end(overflow_block)
        err_str = 'integer overflow'
        err_msg = create_string_constant(ctx.module, err_str)
        err_string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [
            err_msg, lir.Constant(lir.IntType(64), len(err_str))
        ])
        ctx.call('error', [err_string_struct])
        ctx.builder.ret(lir.Constant(lir.IntType(32), 0))

        ctx.builder.position_at_end(success_block)
        ctx.builder.ret(res)
    
    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.int())
    @staticmethod
    def int_div_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        zero = lir.Constant(ir.Type.int().type, 0)
        div_by_zero = ctx.builder.icmp_signed('==', b, zero)
        
        res = ctx.builder.sdiv(a, b)
        div_by_zero_block = ctx.builder.function.append_basic_block('div_by_zero')
        success_block = ctx.builder.function.append_basic_block()
        ctx.builder.cbranch(div_by_zero, div_by_zero_block, success_block)

        ctx.builder.position_at_end(div_by_zero_block)
        err_str = 'division by zero'
        err_msg = create_string_constant(ctx.module, err_str)
        err_string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [
            err_msg, lir.Constant(lir.IntType(64), len(err_str))
        ])
        ctx.call('error', [err_string_struct])
        ctx.builder.ret(lir.Constant(lir.IntType(32), 0))

        ctx.builder.position_at_end(success_block)
        ctx.builder.ret(res)

    @function([
        ir.Param(ir.Position.zero(), 'a', ir.Type.int()),
        ir.Param(ir.Position.zero(), 'b', ir.Type.int())
    ], ir.Type.int())
    @staticmethod
    def int_mod_int(ctx: DefinitionContext):
        a = ctx.param('a').value
        b = ctx.param('b').value

        zero = lir.Constant(ir.Type.int().type, 0)
        div_by_zero = ctx.builder.icmp_signed('==', b, zero)
        
        res = ctx.builder.srem(a, b)
        div_by_zero_block = ctx.builder.function.append_basic_block('div_by_zero')
        success_block = ctx.builder.function.append_basic_block()
        ctx.builder.cbranch(div_by_zero, div_by_zero_block, success_block)

        ctx.builder.position_at_end(div_by_zero_block)
        err_str = 'modulo by zero'
        err_msg = create_string_constant(ctx.module, err_str)
        err_string_struct = create_struct_value(ctx.builder, ir.Type.string().type, [
            err_msg, lir.Constant(lir.IntType(64), len(err_str))
        ])
        ctx.call('error', [err_string_struct])
        ctx.builder.ret(lir.Constant(lir.IntType(32), 0))

        ctx.builder.position_at_end(success_block)
        ctx.builder.ret(res)
