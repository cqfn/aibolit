# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class ClassicGetter:
    '''
    The method's name starts with get. Return statement is the only statement,
    excepting asserts.
    '''

    def _check_body_nodes(self, check_setter_body: List[ASTNode]) -> bool:
        '''
        Check whether nodes are agree with the following types
        (in self.suitable_nodes) or not.
        '''
        for node in check_setter_body:
            has_expression_value = hasattr(node, "expression")
            if not has_expression_value:
                return False

            is_return = node.node_type == ASTNodeType.RETURN_STATEMENT
            is_expression_memeber_ref = node.expression.node_type == ASTNodeType.MEMBER_REFERENCE
            if is_return and is_expression_memeber_ref:
                return True

        return False

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for node in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            method_name = node.name
            if method_name.startswith('get') and self._check_body_nodes(node.body):
                lines.append(node.line)
        return sorted(lines)
