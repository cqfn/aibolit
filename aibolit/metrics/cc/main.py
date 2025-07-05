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
                       ternary, break, continue
    - Boolean operators (&&, ||) add additional complexity paths
    """

    def value(self, ast: AST) -> int:
        total_complexity = 0

        for method in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            total_complexity += self._method_complexity(ast, method)

        for constructor in ast.get_proxy_nodes(ASTNodeType.CONSTRUCTOR_DECLARATION):
            total_complexity += self._method_complexity(ast, constructor)

        return total_complexity

    def _method_complexity(self, ast: AST, method: ASTNode) -> int:
        complexity = 1
        method_ast = ast.get_subtree(method)

        for node in method_ast.get_proxy_nodes():
            complexity += self._node_complexity(ast, node)

        return complexity

    def _node_complexity(self, ast: AST, node: ASTNode) -> int:
        simple_nodes = {
            ASTNodeType.BREAK_STATEMENT,
            ASTNodeType.CATCH_CLAUSE,
            ASTNodeType.CONTINUE_STATEMENT,
            ASTNodeType.SWITCH_STATEMENT_CASE,
            ASTNodeType.THROW_STATEMENT,
        }

        condition_nodes = {
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.WHILE_STATEMENT,
            ASTNodeType.DO_STATEMENT,
            ASTNodeType.TERNARY_EXPRESSION,
        }

        complexity = 0
        if node.node_type in simple_nodes:
            complexity = 1
        elif node.node_type in condition_nodes:
            complexity = self._condition_complexity(ast, node)
        elif node.node_type == ASTNodeType.FOR_STATEMENT:
            complexity = self._for_statement_complexity(ast, node)

        return complexity

    def _condition_complexity(self, ast: AST, node: ASTNode) -> int:
        return 1 + self._expression_complexity(ast, node.condition)

    def _for_statement_complexity(self, ast: AST, node: ASTNode) -> int:
        complexity = 1
        if hasattr(node.control, 'condition'):
            complexity = self._condition_complexity(ast, node.control)
        return complexity

    def _expression_complexity(self, ast: AST, expression: ASTNode | None) -> int:
        if expression is None:
            return 0

        expression_ast = ast.get_subtree(expression)
        count = 0

        for node in expression_ast.get_proxy_nodes(ASTNodeType.BINARY_OPERATION):
            if node.operator in ('&&', '||'):
                count += 1

        return count
