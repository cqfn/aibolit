# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os

from aibolit.ast_framework.ast import AST
from aibolit.ast_framework.ast_node import ASTNode
from aibolit.ast_framework.ast_node_type import ASTNodeType
from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast


class MutableIndex:
    def __init__(self) -> None:
        pass

    def value(self, filename: str | os.PathLike) -> list[LineNumber]:
        """
        Traverse over AST tree and finds loops with mutable index

        :return: List of line number of loops with mutable index
        """
        result = set()
        ast = AST.build_from_javalang(build_ast(filename))
        for node in ast.proxy_nodes(ASTNodeType.FOR_STATEMENT):
            index_names = self._collect_index_names(ast, node)
            for_body = ast.subtree(node.body)
            result.update(self._handle_assignment(index_names, for_body))
            result.update(self._handle_unary_operations(index_names, for_body))
        return sorted(result)

    def _collect_index_names(self, ast: AST, node: ASTNode) -> set[str]:
        result = set()
        node_control = ast.subtree(node.control)
        for decl in node_control.proxy_nodes(ASTNodeType.VARIABLE_DECLARATOR):
            result.add(decl.name)
        for assignment in node_control.proxy_nodes(ASTNodeType.ASSIGNMENT):
            result.add(assignment.expressionl.member)
        return result

    def _handle_assignment(self, index_names: set[str], for_body: AST) -> set[LineNumber]:
        result = set()
        for op in for_body.proxy_nodes(ASTNodeType.ASSIGNMENT):
            expr = op.expressionl
            if expr.node_type == ASTNodeType.MEMBER_REFERENCE and expr.member in index_names:
                result.add(expr.line)
        return result

    def _handle_unary_operations(self, index_names: set[str], for_body: AST) -> set[LineNumber]:
        result = set()
        for op in for_body.proxy_nodes(ASTNodeType.STATEMENT_EXPRESSION):
            expr = op.expression
            if expr.node_type != ASTNodeType.ASSIGNMENT and expr.member in index_names:
                unary_operators = ('++', '--')
                for operator in expr.prefix_operators:
                    if operator in unary_operators:
                        result.add(expr.line)
                for operator in expr.postfix_operators:
                    if operator in unary_operators:
                        result.add(expr.line)
        return result
