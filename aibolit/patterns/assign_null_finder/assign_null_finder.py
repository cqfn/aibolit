# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework.ast import AST
from aibolit.ast_framework.ast_node import ASTNode
from aibolit.ast_framework.ast_node_type import ASTNodeType
from aibolit.types_decl import LineNumber


class NullAssignment:
    def value(self, ast: AST) -> List[LineNumber]:
        lines = set()
        for node in ast.get_proxy_nodes(ASTNodeType.ASSIGNMENT, ASTNodeType.VARIABLE_DECLARATOR):
            if self._is_null_assignment(node):
                lines.add(node.line)
        return sorted(lines)

    def _is_null_assignment(self, node: ASTNode) -> bool:
        return (
            node.node_type == ASTNodeType.ASSIGNMENT and
            self._is_null_literal(node.value) or
            node.node_type == ASTNodeType.VARIABLE_DECLARATOR and
            self._is_null_literal(node.initializer)
        )

    def _is_null_literal(self, node: ASTNode | None) -> bool:
        return node is not None and node.node_type == ASTNodeType.LITERAL and node.value == 'null'
