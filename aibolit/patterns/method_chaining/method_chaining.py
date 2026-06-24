# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class MethodChainFind:
    """
    Finds chained methods, i.e. foo().bar()
    """

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for node in ast.proxy_nodes(ASTNodeType.CLASS_CREATOR,
                                    ASTNodeType.METHOD_INVOCATION,
                                    ASTNodeType.THIS):
            if self._is_jdk_class_chain(node):
                continue
            selectors_qty = self._get_selectors_qty(node)
            if selectors_qty > MethodChainFind._allowed_number_of_selectord[node.node_type]:
                lines.append(node.line)

        return lines

    def _get_selectors_qty(self, node: ASTNode) -> int:
        if not hasattr(node, 'selectors') or node.selectors is None:
            return 0

        return len(node.selectors)

    def _is_jdk_class_chain(self, node: ASTNode) -> bool:
        return node.node_type == ASTNodeType.METHOD_INVOCATION and node.member == 'getClass' and (
            self._get_selectors_qty(node) > 0
        )

    _allowed_number_of_selectord = {
        # found node already is a method invocation, so no further invocations are allowed
        ASTNodeType.METHOD_INVOCATION: 0,
        ASTNodeType.THIS: 1,
        # code example: new Object().foo().bar()
        ASTNodeType.CLASS_CREATOR: 1,
    }
