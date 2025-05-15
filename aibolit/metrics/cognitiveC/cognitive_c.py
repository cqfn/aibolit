# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import re
from itertools import groupby
from typing import List, Set

from aibolit.ast_framework import AST, ASTNodeType, ASTNode

only_increment_for: Set[ASTNodeType] = set([
    ASTNodeType.BREAK_STATEMENT,
    ASTNodeType.CONTINUE_STATEMENT,
    ASTNodeType.TERNARY_EXPRESSION,
    ASTNodeType.BINARY_OPERATION,
    ASTNodeType.METHOD_INVOCATION,
])

increment_and_nested_for: Set[ASTNodeType] = set([
    ASTNodeType.IF_STATEMENT,
    ASTNodeType.SWITCH_STATEMENT,
    ASTNodeType.FOR_STATEMENT,
    ASTNodeType.WHILE_STATEMENT,
    ASTNodeType.DO_STATEMENT,
    ASTNodeType.CATCH_CLAUSE,
])

logical_operators = ['&&', '||']


class CognitiveComplexity:

    def __init__(self):
        # store the name for the considered method declaration
        self.__method_name = None

    def _traverse_childs(self, ast: AST, node: int, nested_level: int) -> int:
        complexity = 0
        for each_child in ast.tree.succ[node]:
            complexity += self._get_complexity(ast, each_child, nested_level)
        return complexity

    def _check_if_statement(self, ast, expr, nested_level: int) -> int:
        '''function to work with IfStatement block'''
        complexity = 0
        all_childs = list([i for i in ast.tree.succ[expr]])
        complexity += self._get_complexity(ast, all_childs[0], 0)
        if len(all_childs) >= 2:
            complexity += nested_level + 1
            complexity += self._get_complexity(ast, all_childs[1], nested_level + 1)

        if len(all_childs) == 3:
            node_obj = ASTNode(ast.tree, all_childs[2])
            if node_obj.node_type == ASTNodeType.IF_STATEMENT:
                complexity -= nested_level
                complexity += self._check_if_statement(ast, all_childs[2], nested_level)
            else:
                complexity += 1
                complexity += self._get_complexity(ast, all_childs[2], nested_level + 1)
        return complexity

    def _increment_logical_operators(self, ast: AST, binary_operation_node: int) -> int:
        complexity = 0
        logical_operators_sequence = self._create_logical_operators_sequence(
            ast, binary_operation_node)
        complexity += len(list(groupby(logical_operators_sequence)))
        return complexity

    def _create_logical_operators_sequence(self, ast: AST, binary_operation_node: int) -> List[str]:
        node_obj = ASTNode(ast.tree, binary_operation_node)
        if node_obj.node_type != ASTNodeType.BINARY_OPERATION:
            return []

        # Get binary operation params using new API
        children = list(node_obj.children)
        if len(children) < 3:
            return []
        operation_node, left_side_node, right_side_node = children[0], children[1], children[2]
        operator = operation_node.string if operation_node.node_type == ASTNodeType.STRING else None

        if operator not in logical_operators:
            return []

        left_sequence = self._create_logical_operators_sequence(ast, left_side_node.node_index)
        right_sequence = self._create_logical_operators_sequence(ast, right_side_node.node_index)
        return left_sequence + [operator] + right_sequence

    def _is_recursion_call(self, ast, node) -> bool:
        node_obj = ASTNode(ast.tree, node)
        assert node_obj.node_type == ASTNodeType.METHOD_INVOCATION
        if self.__method_name == self._get_node_name(ast, node):
            return True
        return False

    def _nested_methods(self, ast, node, nested_level: int) -> int:
        complexity = 0
        original_name = self.__method_name
        self.__method_name = self._get_node_name(ast, node)
        complexity += self._get_complexity(ast, node, nested_level + 1)
        self.__method_name = original_name
        return complexity

    def _process_not_nested_structure(self, ast: AST, each_block: int, nested_level: int) -> int:
        complexity = 0
        each_block_obj = ASTNode(ast.tree, each_block)
        each_block_type = each_block_obj.node_type
        if each_block_type == ASTNodeType.BINARY_OPERATION:
            # Get binary operation name using new API
            string_nodes = [child for child in each_block_obj.children
                            if child.node_type == ASTNodeType.STRING]
            bin_operator = string_nodes[0].string if string_nodes else None
            if bin_operator in logical_operators:
                complexity += self._increment_logical_operators(ast, each_block)

        elif each_block_type == ASTNodeType.METHOD_INVOCATION:
            is_recursion = self._is_recursion_call(ast, each_block)
            complexity += is_recursion

        else:
            complexity += 1
            complexity += self._traverse_childs(ast, each_block, nested_level)

        return complexity

    def _get_complexity(self, ast: AST, each_block: int, nested_level: int) -> int:
        each_block_name = self._get_node_name(ast, each_block)
        each_block_obj = ASTNode(ast.tree, each_block)
        each_block_type = each_block_obj.node_type
        complexity = 0

        if (each_block_type == ASTNodeType.METHOD_DECLARATION and
                each_block_name != self.__method_name):
            complexity += self._nested_methods(ast, each_block, nested_level)

        elif each_block_type == ASTNodeType.IF_STATEMENT:
            complexity += self._check_if_statement(ast, each_block, nested_level)

        elif each_block_type in increment_and_nested_for:
            complexity += 1 + nested_level
            complexity += self._traverse_childs(ast, each_block, nested_level + 1)

        elif each_block_type in only_increment_for:
            complexity += self._process_not_nested_structure(ast, each_block, nested_level)

        else:
            complexity += self._traverse_childs(ast, each_block, nested_level)
        return complexity

    def _get_node_name(self, ast, node) -> str:
        extracted_name = None
        node_obj = ASTNode(ast.tree, node)
        names = [child for child in node_obj.children if child.node_type == ASTNodeType.STRING]
        for each_string in names:
            method_name = each_string.string
            # Checking not to start with '/' is aimed to get
            # rid of comments, which are all childs of node.
            # We check the occurance any letter in name in order
            # to get rid of '' string and None.
            if not method_name.startswith('/') and re.search(r'[^\W\d]', method_name) is not None:
                extracted_name = method_name
                return extracted_name
        return ''

    def value(self, ast: AST) -> int:
        complexity = 0
        for method_ast in ast.get_subtrees(ASTNodeType.METHOD_DECLARATION):
            method_declaration_index = method_ast.get_root().node_index
            self.__method_name = self._get_node_name(method_ast, method_declaration_index)
            complexity += self._get_complexity(method_ast, method_declaration_index, 0)
        return complexity
