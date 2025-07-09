# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import re
from itertools import groupby
from typing import List, Set

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
    def _traverse_children(self, node: ASTNode, nested_level: int, method_name: str) -> int:
        complexity = 0
        for child_node in node.children:
            complexity += self._get_complexity(child_node, nested_level, method_name)
        return complexity

    def _check_if_statement(self, node: ASTNode, nested_level: int, method_name: str) -> int:
        """function to work with IfStatement block"""
        complexity = 0
        children = list(node.children)
        complexity += self._get_complexity(children[0], 0, method_name)
        if len(children) >= 2:
            complexity += nested_level + 1
            complexity += self._get_complexity(children[1], nested_level + 1, method_name)

        if len(children) == 3:
            node_obj = children[2]
            if node_obj.node_type == ASTNodeType.IF_STATEMENT:
                complexity -= nested_level
                complexity += self._check_if_statement(
                    node_obj, nested_level, method_name)
            else:
                complexity += 1
                complexity += self._get_complexity(
                    node_obj, nested_level + 1, method_name)
        return complexity

    def _increment_logical_operators(self, node: ASTNode) -> int:
        complexity = 0
        logical_operators_sequence = self._create_logical_operators_sequence(node)
        complexity += len(list(groupby(logical_operators_sequence)))
        return complexity

    def _create_logical_operators_sequence(self, node: ASTNode) -> List[str]:
        if node.node_type != ASTNodeType.BINARY_OPERATION:
            return []

        # Get binary operation params using new API
        children = list(node.children)
        if len(children) < 3:
            return []
        operation_node, left_side_node, right_side_node = children[0], children[1], children[2]
        operator = operation_node.string if operation_node.node_type == ASTNodeType.STRING else None

        if operator not in logical_operators:
            return []

        left_sequence = self._create_logical_operators_sequence(left_side_node)
        right_sequence = self._create_logical_operators_sequence(right_side_node)
        return left_sequence + [operator] + right_sequence

    def _is_recursion_call(self, node: ASTNode, method_name: str) -> bool:
        assert node.node_type == ASTNodeType.METHOD_INVOCATION
        return method_name == self._get_node_name(node)

    def _nested_methods(self, node, nested_level: int, method_name: str) -> int:
        method_name = self._get_node_name(node)
        return self._get_complexity(node, nested_level + 1, method_name)

    def _process_not_nested_structure(
            self, node: ASTNode, nested_level: int, method_name: str) -> int:
        complexity = 0
        each_block_type = node.node_type
        if each_block_type == ASTNodeType.BINARY_OPERATION:
            # Get binary operation name using new API
            string_nodes = [child for child in node.children
                            if child.node_type == ASTNodeType.STRING]
            bin_operator = string_nodes[0].string if string_nodes else None
            if bin_operator in logical_operators:
                complexity += self._increment_logical_operators(node)

        elif each_block_type == ASTNodeType.METHOD_INVOCATION:
            is_recursion = self._is_recursion_call(node, method_name)
            complexity += is_recursion

        else:
            complexity += 1
            complexity += self._traverse_children(node, nested_level, method_name)

        return complexity

    def _get_complexity(
            self, node: ASTNode, nested_level: int, method_name: str) -> int:
        each_block_name = self._get_node_name(node)
        each_block_type = node.node_type
        complexity = 0

        if (each_block_type == ASTNodeType.METHOD_DECLARATION and
                each_block_name != method_name):
            complexity += self._nested_methods(node, nested_level, method_name)

        elif each_block_type == ASTNodeType.IF_STATEMENT:
            complexity += self._check_if_statement(node, nested_level, method_name)

        elif each_block_type in increment_and_nested_for:
            complexity += 1 + nested_level
            complexity += self._traverse_children(node, nested_level + 1, method_name)

        elif each_block_type in only_increment_for:
            complexity += self._process_not_nested_structure(
                node, nested_level, method_name)

        else:
            complexity += self._traverse_children(node, nested_level, method_name)
        return complexity

    def _get_node_name(self, node: ASTNode) -> str:
        extracted_name = None
        names = [child for child in node.children if child.node_type == ASTNodeType.STRING]
        for each_string in names:
            method_name = each_string.string
            # Checking not to start with '/' is aimed to get
            # rid of comments, which are all children of node.
            # We check the occurance any letter in name in order
            # to get rid of '' string and None.
            if not method_name.startswith('/') and re.search(r'[^\W\d]', method_name) is not None:
                extracted_name = method_name
                return extracted_name
        return ''

    def value(self, ast: AST) -> int:
        complexity = 0
        for method_ast in ast.get_subtrees(ASTNodeType.METHOD_DECLARATION):
            method_root = method_ast.get_root()
            method_name = self._get_node_name(method_root)
            complexity += self._get_complexity(method_root, 0, method_name)
        return complexity
