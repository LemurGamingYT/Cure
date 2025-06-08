from cure.lib import function, Lib, DefinitionContext
from cure.codegen_utils import NULL
from cure import ir


class testing(Lib):
    @function([
        ir.Param(ir.Position.zero(), 'condition', ir.Type.bool()),
        ir.Param(ir.Position.zero(), 'fail_message', ir.Type.string())
    ])
    @staticmethod
    def assert_(ctx: DefinitionContext):
        condition = ctx.param('condition').value
        with ctx.builder.if_then(ctx.builder.not_(condition)):
            fail_message = ctx.param('fail_message').value
            ctx.call('error', [fail_message])
            ctx.builder.ret(NULL())
        
        ctx.builder.ret(NULL())
    
    @function([
        ir.Param(ir.Position.zero(), 'condition', ir.Type.bool()),
        ir.Param(ir.Position.zero(), 'fail_message', ir.Type.string())
    ])
    @staticmethod
    def assert_not(ctx: DefinitionContext):
        condition = ctx.param('condition').value
        fail_message = ctx.param('fail_message').value
        ctx.builder.ret(ctx.call('assert', [ctx.builder.not_(condition), fail_message]))
