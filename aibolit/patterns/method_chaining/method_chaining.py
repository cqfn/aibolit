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
    def _is_invocation_inside(self, node: ASTNode) -> bool:
        # to process structures such as:
        # obj.methodInv1(list).methodInv2("blabla")
        for i in node.children:
            if i.node_type == ASTNodeType.METHOD_INVOCATION:
                return True

        return False

    def _check_chained_method(self, ast: AST, method_invocation: ASTNode) -> bool:
        childs = 0
        for node in method_invocation.children:
            if node.node_type == ASTNodeType.METHOD_INVOCATION:
                # we check structures such as:
                # new MyObject().Start()
                #   .SpecifySomeParameter(list)
                #   .SpecifySomeOtherParameter("list")
                if self._is_invocation_inside(node) or node.qualifier is None:
                    childs += 1
        return childs > 0

    def value(self, filename: str) -> List[int]:
        lines: List[int] = []
        ast = AST.build_from_javalang(build_ast(filename))
        for stetement_expression in ast.get_proxy_nodes(ASTNodeType.STATEMENT_EXPRESSION):
            expression_child = stetement_expression.expression
            if expression_child.node_type == ASTNodeType.METHOD_INVOCATION and \
                    self._check_chained_method(ast, expression_child):
                lines.append(stetement_expression.line)

            elif expression_child.node_type == ASTNodeType.CLASS_CREATOR and \
                    len(expression_child.selectors) > 1:
                lines.append(stetement_expression.line)

        return lines
