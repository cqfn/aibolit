from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast
from typing import List
from aibolit.ast_framework.ast_node import ASTNode


class MethodChainFind:
    '''
    In this pattern we check whether 
    more than one method chaining 
    invocation is used or not.
    '''
    def _check_chained_method(self, method_invocation: ASTNode) -> bool:
        childs = 0
        for node in method_invocation.children:
            if node.node_type == ASTNodeType.METHOD_INVOCATION:
                childs += 1
        return childs > 1

    def value(self, filename: str) -> List[int]:
        lines: List[int] = []
        ast = AST.build_from_javalang(build_ast(filename))
        for stetement_expression in ast.get_proxy_nodes(ASTNodeType.STATEMENT_EXPRESSION):
            expression_child = stetement_expression.expression
            if expression_child.node_type in [ASTNodeType.CLASS_CREATOR, ASTNodeType.METHOD_INVOCATION] and \
               self._check_chained_method(expression_child):
                lines.append(expression_child.line)

        return lines
