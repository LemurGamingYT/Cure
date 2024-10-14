from ir.nodes import (
    ClassMethod, Body, Identifier, ParamNode, UOp, TypeNode, Call, ArgNode, Cast, Position
)


class testing:
    CAN_USE = False
    
    def __init__(self, codegen) -> None:
        pos: Position = codegen.pos
        assertTrue = ClassMethod(
            pos, 'assertTrue', Body(pos, [
                Call(pos, 'assert', [
                    ArgNode(pos, Cast(pos, Identifier(pos, 'a'), TypeNode(pos, 'bool')))
                ])
            ]), [ParamNode(pos, 'a', TypeNode(pos, 'bool'))], TypeNode(pos, 'nil'), is_public=False
        )
        
        assertFalse = ClassMethod(
            pos, 'assertFalse', Body(pos, [
                Call(pos, 'assert', [
                    ArgNode(pos, UOp(pos, Cast(pos, Identifier(pos, 'a'), TypeNode(pos, 'bool')), '!'))
                ])
            ]), [ParamNode(pos, 'a', TypeNode(pos, 'bool'))], TypeNode(pos, 'nil'), is_public=False
        )
        
        # assertNotEqual = ClassMethod(
        #     pos, 'assertNotEqual', Body(pos, [
        #         Call(pos, 'assert', [
        #             ArgNode(pos, BinOp(pos, Identifier(pos, 'a'), '!=', Identifier(pos, 'b')))
        #         ])
        #     ]), [
        #         ParamNode(pos, 'a', TypeNode(pos, 'any')), ParamNode(pos, 'b', TypeNode(pos, 'any'))
        #     ], TypeNode(pos, 'nil'), is_public=False
        # )
        
        # assertEqual = ClassMethod(
        #     pos, 'assertEqual', Body(pos, [
        #         Call(pos, 'assert', [
        #             ArgNode(pos, BinOp(pos, Identifier(pos, 'a'), '==', Identifier(pos, 'b')))
        #         ])
        #     ]), [
        #         ParamNode(pos, 'a', TypeNode(pos, 'any')), ParamNode(pos, 'b', TypeNode(pos, 'any'))
        #     ], TypeNode(pos, 'nil'), is_public=False
        # )
        
        codegen.add_toplevel_code(codegen.class_manager.create_class(
            'UnitTest', [assertTrue, assertFalse], pos, []
        ))
