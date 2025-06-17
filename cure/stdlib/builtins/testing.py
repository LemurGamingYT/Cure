from cure.ir import Param, Position, TypeManager, FunctionFlags
from cure.lib import function, Lib, DefinitionContext


class testing(Lib):
    @function([
        Param(Position.zero(), 'condition', TypeManager.get('bool')),
        Param(Position.zero(), 'fail_message', TypeManager.get('string'))
    ], flags=FunctionFlags(public=True))
    @staticmethod
    def assert_(ctx: DefinitionContext):
        condition = ctx.param('condition').value
        with ctx.builder.if_then(ctx.builder.not_(condition)):
            fail_message = ctx.param('fail_message').value
            ctx.call('error', [fail_message])
    
    @function([
        Param(Position.zero(), 'condition', TypeManager.get('bool')),
        Param(Position.zero(), 'fail_message', TypeManager.get('string'))
    ], flags=FunctionFlags(public=True))
    @staticmethod
    def assert_not(ctx: DefinitionContext):
        condition = ctx.param('condition').value
        fail_message = ctx.param('fail_message').value
        ctx.call('assert', [ctx.builder.not_(condition), fail_message])
