# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List, Tuple

from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class MaxDiameter:
    """
    Max diameter of class methods.
    """

    def value(self, ast: AST) -> int:
        method_diameters: List[int] = [
            self._calcalute_diameter(method_ast)
            for method_ast in ast.get_subtrees(ASTNodeType.METHOD_DECLARATION)
        ]

        return max(method_diameters, default=0)

    def _calcalute_diameter(self, ast: AST) -> int:
        distant_node_from_root, _ = self._find_distant_node(ast, ast.get_root(), False)

        # traverse undirected graph, because we need to be able to traverse from child to parent in
        # general. It's not needed at previous call, as the most distant node of a tree is anyway
        # a child of root
        # and there is no need to traverse from child to parent, which simply safe time
        _, diameter = self._find_distant_node(ast, distant_node_from_root, True)
        return diameter

    def _find_distant_node(self, ast: AST, source_node: ASTNode,
                           undirected: bool) -> Tuple[ASTNode, int]:
        distance = 0

        max_distance = 0
        distant_node = source_node

        def on_node_entering(node: ASTNode) -> None:
            nonlocal distance
            distance += 1

        def on_node_leaving(node: ASTNode) -> None:
            nonlocal distance, max_distance, distant_node
            if distance > max_distance:
                max_distance = distance
                distant_node = node

            distance -= 1

        ast.traverse(on_node_entering, on_node_leaving, source_node, undirected)

        return (distant_node, max_distance)
