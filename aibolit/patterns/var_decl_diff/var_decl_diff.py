# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
from typing import List, Optional

from aibolit.ast_framework.ast import AST
from aibolit.ast_framework.ast_node import ASTNode
from aibolit.ast_framework.ast_node_type import ASTNodeType
from aibolit.types_decl import LineNumber


class VarDeclarationDistance:
    """
    Returns lines where a variable is first used far from its declaration.
    """

    def __init__(self, lines_th: int):
        self.__statements_th = lines_th

    def __node_name(self, node) -> Optional[str]:
        qualifier = node.qualifier if hasattr(node, 'qualifier') else None
        member = node.member if hasattr(node, 'member') else None
        name = node.name if hasattr(node, 'name') else None
        return qualifier or member or name

    def __value_for_method_declaration(self, method_declaration: AST) -> set[LineNumber]:
        """Find variables declared far from their first usage in the method."""
        result = set()
        name_to_declaration_statement = {}
        name_to_first_usage_statement = {}
        name_to_first_usage_line = {}

        for statement_index, statement in enumerate(method_declaration.root().body or []):
            statement_ast = method_declaration.subtree(statement)
            for node in statement_ast.proxy_nodes(ASTNodeType.VARIABLE_DECLARATOR):
                name_to_declaration_statement[node.name] = statement_index

            def collect_usage(node: ASTNode, usage_statement: int = statement_index):
                node_name = self.__node_name(node)
                if (
                    node_name in name_to_declaration_statement and
                    node_name not in name_to_first_usage_statement and
                    node.node_type != ASTNodeType.VARIABLE_DECLARATOR
                ):
                    name_to_first_usage_statement[node_name] = usage_statement
                    name_to_first_usage_line[node_name] = node.line

            statement_ast.traverse(collect_usage)

        for name, usage_statement in name_to_first_usage_statement.items():
            statement_diff = usage_statement - name_to_declaration_statement[name] - 1
            if statement_diff >= self.__statements_th:
                usage_line = name_to_first_usage_line[name]
                result.add(usage_line)
        return result

    def value(self, ast: AST) -> List[LineNumber]:
        """Find variables declared far from their first usage."""

        result = set()
        for declaration in ast.subtrees(ASTNodeType.METHOD_DECLARATION):
            result.update(self.__value_for_method_declaration(declaration))

        return sorted(result)
