from cure.lib import function, Lib, DefinitionContext
from cure import ir


class testing(Lib):
    @function([
        ir.Param(ir.Position.zero(), 'condition', ir.TypeManager.get('bool')),
        ir.Param(ir.Position.zero(), 'fail_message', ir.TypeManager.get('string'))
    ], flags=ir.FunctionFlags(public=True))
    @staticmethod
    def assert_(ctx: DefinitionContext):
        condition = ctx.param('condition').value
        with ctx.builder.if_then(ctx.builder.not_(condition)):
            fail_message = ctx.param('fail_message').value
            ctx.call('error', [fail_message])
    
    @function([
        ir.Param(ir.Position.zero(), 'condition', ir.TypeManager.get('bool')),
        ir.Param(ir.Position.zero(), 'fail_message', ir.TypeManager.get('string'))
    ], flags=ir.FunctionFlags(public=True))
    @staticmethod
    def assert_not(ctx: DefinitionContext):
        condition = ctx.param('condition').value
        fail_message = ctx.param('fail_message').value
        ctx.call('assert', [ctx.builder.not_(condition), fail_message])
