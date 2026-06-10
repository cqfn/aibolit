# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework.ast import AST
from aibolit.ast_framework.ast_node import ASTNode
from aibolit.ast_framework.ast_node_type import ASTNodeType
from aibolit.types_decl import LineNumber


class NullAssignment:
    def value(self, ast: AST) -> List[LineNumber]:
        lines = set()
        for assignment in ast.proxy_nodes(ASTNodeType.ASSIGNMENT):
            if self._is_null_literal(assignment.value):
                lines.add(assignment.line)
        for declarator in ast.proxy_nodes(ASTNodeType.VARIABLE_DECLARATOR):
            if self._is_null_literal(declarator.initializer):
                lines.add(declarator.line)
        return sorted(lines)

    def _is_null_literal(self, node: ASTNode | None) -> bool:
        return node is not None and node.node_type == ASTNodeType.LITERAL and node.value == 'null'
