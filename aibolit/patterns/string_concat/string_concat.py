# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import Set, List

from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class StringConcatFinder:
    '''
    Any usage string concatenation using '+' operator is considered as a pattern.
    '''
    def _check_left_right_operator(self, node: ASTNode) -> bool:
        assert node.node_type == ASTNodeType.BINARY_OPERATION
        for operator_side in [node.operandr, node.operandl]:
            if (operator_side.node_type == ASTNodeType.LITERAL and
                    isinstance(operator_side.value, str) and
                    not operator_side.value.isdigit()):
                return True
        return False

    def value(self, ast: AST) -> List[int]:
        lines: Set[int] = set()
        for node in ast.get_proxy_nodes(ASTNodeType.BINARY_OPERATION):
            if node.operator == '+' and self._check_left_right_operator(node):
                lines.add(node.line)

        return sorted(lines)
