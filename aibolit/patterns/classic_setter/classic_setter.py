# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class ClassicSetter:
    '''
    The method's name starts with set. There are attributes
    assigning in the method. Also, asserts are ignored.
    '''
    suitable_nodes: List[ASTNodeType] = [
        ASTNodeType.ASSERT_STATEMENT,
        ASTNodeType.STATEMENT_EXPRESSION,
    ]

    def _check_body_nodes(self, check_setter_body: List[ASTNode]) -> bool:
        '''
        Check whether nodes are agree with the following types
        (in self.suitable_nodes) or not.
        '''
        for node in check_setter_body:
            if node.node_type not in self.suitable_nodes:
                return False
        return True

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for node in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            method_name = node.name
            if node.return_type is None and method_name.startswith('set') and \
                    self._check_body_nodes(node.body):
                lines.append(node.line)
        return sorted(lines)
