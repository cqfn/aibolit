# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class CCMetric:
    """
    Calculates cyclomatic complexity by counting
    decision points in all methods and constructors:

    - Base complexity: 1 per method/constructor
    - Decision points: if, while, for, do-while,
                       switch cases, catch, throw,
                       ternary, break, continue, assert
    - Boolean operators (&&, ||) add additional complexity paths
    """

    def value(self, ast: AST) -> int:
        total_complexity = 0

        for method in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            total_complexity += self._method_complexity(method)

        for constructor in ast.get_proxy_nodes(ASTNodeType.CONSTRUCTOR_DECLARATION):
            total_complexity += self._method_complexity(constructor)

        return total_complexity

    def _method_complexity(self, method: ASTNode) -> int:
        complexity = 1

        for node in self._get_all_nodes(method):
            complexity += self._get_node_complexity(node)

        return complexity

    def _get_all_nodes(self, root: ASTNode) -> list[ASTNode]:
        nodes = []
        stack = [root]

        while stack:
            node = stack.pop()
            nodes.append(node)
            stack.extend(node.children)

        return nodes

    def _get_node_complexity(self, node: ASTNode) -> int:
        simple_nodes = {
            ASTNodeType.BREAK_STATEMENT,
            ASTNodeType.CATCH_CLAUSE,
            ASTNodeType.CONTINUE_STATEMENT,
            ASTNodeType.SWITCH_STATEMENT_CASE,
            ASTNodeType.THROW_STATEMENT,
        }

        complexity = 0
        if node.node_type in simple_nodes:
            complexity = 1
        elif node.node_type == ASTNodeType.IF_STATEMENT:
            complexity = self._handle_if_statement(node)
        elif node.node_type == ASTNodeType.FOR_STATEMENT:
            complexity = self._handle_for_statement(node)
        elif node.node_type == ASTNodeType.WHILE_STATEMENT:
            complexity = self._handle_while_statement(node)
        elif node.node_type == ASTNodeType.DO_STATEMENT:
            complexity = self._handle_do_statement(node)
        elif node.node_type == ASTNodeType.TERNARY_EXPRESSION:
            complexity = self._handle_ternary_expression(node)

        return complexity

    def _handle_if_statement(self, node: ASTNode) -> int:
        return 1 + self._count_boolean_operators(node.condition)

    def _handle_for_statement(self, node: ASTNode) -> int:
        complexity = 1
        if (hasattr(node.control, 'condition') and
                node.control.condition):
            complexity += self._count_boolean_operators(node.control.condition)
        return complexity

    def _handle_while_statement(self, node: ASTNode) -> int:
        return 1 + self._count_boolean_operators(node.condition)

    def _handle_do_statement(self, node: ASTNode) -> int:
        return 1 + self._count_boolean_operators(node.condition)

    def _handle_ternary_expression(self, node: ASTNode) -> int:
        return 1 + self._count_boolean_operators(node.condition)

    def _count_boolean_operators(self, expression: ASTNode) -> int:
        if expression is None:
            return 0

        count = 0
        nodes_to_check = [expression]

        while nodes_to_check:
            node = nodes_to_check.pop()

            if (node.node_type == ASTNodeType.BINARY_OPERATION and
                    node.operator in ('&&', '||')):
                count += 1

            nodes_to_check.extend(node.children)

        return count
