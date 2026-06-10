# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
from typing import List, Optional

from aibolit.ast_framework.ast import AST
from aibolit.ast_framework.ast_node import ASTNode
from aibolit.ast_framework.ast_node_type import ASTNodeType
from aibolit.types_decl import LineNumber


class VarDeclarationDistance:
    """
    Returns lines where variable first time used but declared more than
    specific number of lined before
    """

    def __init__(self, lines_th: int):
        self.__lines_th = lines_th

    def __node_name(self, node) -> Optional[str]:
        qualifier = node.qualifier if hasattr(node, 'qualifier') else None
        member = node.member if hasattr(node, 'member') else None
        name = node.name if hasattr(node, 'name') else None
        return qualifier or member or name

    def __line_diff(self, usage_line: int, declaration_line: int, empty_lines: set[int]) -> int:
        """
        Calculate line difference between variable declaration and first usage
        taking into account empty lines
        """
        lines_range = set(range(declaration_line + 1, usage_line))
        return len(lines_range.difference(empty_lines))

    def __find_empty_lines_in_ast(self, ast: AST) -> set[LineNumber]:
        """Figure out lines that are either empty or multiline statements"""
        lines_with_nodes = set()
        ast.traverse(lambda node: lines_with_nodes.add(node.line))
        if not lines_with_nodes:
            return set()
        max_line = max(lines_with_nodes)
        all_lines = set(range(1, max_line + 1))
        return all_lines.difference(lines_with_nodes)

    def __value_for_method_declaration(
        self, method_declaration: AST, empty_lines: set[LineNumber]
    ) -> set[LineNumber]:
        """Find variables declared far from their first usage in the method."""
        result = set()
        name_to_declaration_line = {}
        name_to_first_usage_line = {}

        def collect_declaration_or_usage(node: ASTNode):
            node_name = self.__node_name(node)
            if node_name:
                if node.node_type == ASTNodeType.VARIABLE_DECLARATOR:
                    name_to_declaration_line[node_name] = node.line
                elif (
                    node_name in name_to_declaration_line and
                    node_name not in name_to_first_usage_line
                ):
                    name_to_first_usage_line[node_name] = node.line

        method_declaration.traverse(collect_declaration_or_usage)
        for name, usage_line in name_to_first_usage_line.items():
            line_diff = self.__line_diff(
                usage_line,
                name_to_declaration_line[name],
                empty_lines,
            )
            if line_diff >= self.__lines_th:
                result.add(usage_line)
        return result

    def value(self, ast: AST) -> List[LineNumber]:
        """Find variables declared far from their first usage."""

        result = set()
        empty_lines = self.__find_empty_lines_in_ast(ast)
        for declaration in ast.subtrees(ASTNodeType.METHOD_DECLARATION):
            result.update(self.__value_for_method_declaration(declaration, empty_lines))

        return sorted(result)
