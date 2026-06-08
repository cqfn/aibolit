# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
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
        return sum(
            self._method_complexity(ast, node)
            for node in ast.proxy_nodes(
                ASTNodeType.METHOD_DECLARATION, ASTNodeType.CONSTRUCTOR_DECLARATION
            )
        )

    def _method_complexity(self, ast: AST, method: ASTNode) -> int:
        method_ast = ast.subtree(method)
        return 1 + sum(self._node_complexity(ast, node) for node in method_ast.proxy_nodes())

    def _node_complexity(self, ast: AST, node: ASTNode) -> int:
        if node.node_type in _SIMPLE_NODES:
            return 1
        elif node.node_type in _CONDITION_NODES:
            return self._condition_complexity(ast, node)
        elif node.node_type == ASTNodeType.FOR_STATEMENT:
            return self._for_statement_complexity(ast, node)
        return 0

    def _condition_complexity(self, ast: AST, node: ASTNode) -> int:
        return 1 + self._expression_complexity(ast, node.condition)

    def _for_statement_complexity(self, ast: AST, node: ASTNode) -> int:
        if hasattr(node.control, 'condition'):
            return self._condition_complexity(ast, node.control)
        return 1

    def _expression_complexity(self, ast: AST, expression: ASTNode | None) -> int:
        if expression is None:
            return 0
        expression_ast = ast.subtree(expression)
        return sum(
            1
            for node in expression_ast.proxy_nodes(ASTNodeType.BINARY_OPERATION)
            if node.operator in ('&&', '||')
        )


_SIMPLE_NODES = (
    ASTNodeType.BREAK_STATEMENT,
    ASTNodeType.CATCH_CLAUSE,
    ASTNodeType.CONTINUE_STATEMENT,
    ASTNodeType.SWITCH_STATEMENT_CASE,
    ASTNodeType.THROW_STATEMENT,
)

_CONDITION_NODES = (
    ASTNodeType.IF_STATEMENT,
    ASTNodeType.WHILE_STATEMENT,
    ASTNodeType.DO_STATEMENT,
    ASTNodeType.TERNARY_EXPRESSION,
)
