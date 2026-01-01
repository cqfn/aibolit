# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
from itertools import groupby
from typing import Iterable, Set

from aibolit.ast_framework import AST, ASTNodeType, ASTNode

only_increment_for: Set[ASTNodeType] = {
    ASTNodeType.BREAK_STATEMENT,
    ASTNodeType.CONTINUE_STATEMENT,
    ASTNodeType.TERNARY_EXPRESSION,
    ASTNodeType.BINARY_OPERATION,
    ASTNodeType.METHOD_INVOCATION,
}

increment_and_nested_for: Set[ASTNodeType] = {
    ASTNodeType.IF_STATEMENT,
    ASTNodeType.SWITCH_STATEMENT,
    ASTNodeType.FOR_STATEMENT,
    ASTNodeType.WHILE_STATEMENT,
    ASTNodeType.DO_STATEMENT,
    ASTNodeType.CATCH_CLAUSE,
}

logical_operators = ('&&', '||')


class CognitiveComplexity:
    def value(self, ast: AST) -> int:
        complexity = 0
        for method_ast in ast.subtrees(ASTNodeType.METHOD_DECLARATION):
            method_root = method_ast.root()
            method_name = self._method_name(method_root)
            complexity += self._complexity(method_root, 0, method_name)
        return complexity

    def _complexity(self, node: ASTNode, nested_level: int, method_name: str) -> int:
        complexity = 0
        if node.node_type == ASTNodeType.METHOD_DECLARATION and not self._is_recursion_call(
            node, method_name
        ):
            complexity += self._nested_methods(node, nested_level, method_name)

        elif node.node_type == ASTNodeType.IF_STATEMENT:
            complexity += self._if_complexity(node, nested_level, method_name)

        elif node.node_type in increment_and_nested_for:
            complexity += 1 + nested_level
            complexity += self._children_complexity(node, nested_level + 1, method_name)

        elif node.node_type in only_increment_for:
            complexity += self._not_nested_complexity(node, nested_level, method_name)

        else:
            complexity += self._children_complexity(node, nested_level, method_name)
        return complexity

    def _is_recursion_call(self, node: ASTNode, method_name: str) -> bool:
        return method_name == self._method_name(node)

    def _nested_methods(self, node: ASTNode, nested_level: int, method_name: str) -> int:
        method_name = self._method_name(node)
        return self._complexity(node, nested_level + 1, method_name)

    def _if_complexity(self, node: ASTNode, nested_level: int, method_name: str) -> int:
        complexity = self._complexity(node.condition, 0, method_name)
        if then_ := node.then_statement:
            complexity += nested_level + 1 + self._complexity(then_, nested_level + 1, method_name)
        if else_ := node.else_statement:
            if else_.node_type == ASTNodeType.IF_STATEMENT:
                complexity += (-nested_level) + self._if_complexity(
                    else_, nested_level, method_name
                )
            else:
                complexity += 1 + self._complexity(else_, nested_level + 1, method_name)
        return complexity

    def _children_complexity(self, node: ASTNode, nested_level: int, method_name: str) -> int:
        return sum(
            self._complexity(child_node, nested_level, method_name) for child_node in node.children
        )

    def _condition_complexity(self, node: ASTNode) -> int:
        return sum(1 for _ in groupby(self._logical_operators_sequence(node)))

    def _logical_operators_sequence(self, node: ASTNode) -> Iterable[str]:
        if node.node_type != ASTNodeType.BINARY_OPERATION:
            return

        if node.operator not in logical_operators:
            return

        yield from self._logical_operators_sequence(node.operandl)
        yield node.operator
        yield from self._logical_operators_sequence(node.operandr)

    def _not_nested_complexity(self, node: ASTNode, nested_level: int, method_name: str) -> int:
        complexity = 0
        if node.node_type == ASTNodeType.BINARY_OPERATION:
            complexity += self._condition_complexity(node)
        elif node.node_type == ASTNodeType.METHOD_INVOCATION:
            complexity += self._is_recursion_call(node, method_name)
        else:
            complexity += 1
            complexity += self._children_complexity(node, nested_level, method_name)

        return complexity

    def _method_name(self, node: ASTNode) -> str:
        if node.node_type == ASTNodeType.METHOD_DECLARATION:
            return node.name
        if node.node_type == ASTNodeType.METHOD_INVOCATION:
            if node.qualifier:
                return node.qualifier + '.' + node.member
            return node.member
        return ''
