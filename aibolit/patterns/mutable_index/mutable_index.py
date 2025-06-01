# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os

from aibolit.ast_framework.ast import AST
from aibolit.ast_framework.ast_node import ASTNode
from aibolit.ast_framework.ast_node_type import ASTNodeType
from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast


class MutableIndex:
    def __init__(self):
        pass

    def value(self, filename: str | os.PathLike) -> list[LineNumber]:
        """
        Traverse over AST tree and finds loops with mutable index

        :return: List of line number of loops with mutable index
        """
        result = set()
        ast = AST.build_from_javalang(build_ast(filename))
        for node in ast.get_proxy_nodes(
            ASTNodeType.FOR_STATEMENT,
        ):
            index_names = self._collect_index_names(ast, node)
            for_body = node.body
            result.update(self._handle_assignment(ast, index_names, for_body))
            result.update(self._handle_unary_operations(ast, index_names, for_body))

        return sorted(result)

    def _collect_index_names(self, ast: AST, node: ASTNode) -> set[str]:
        result = set()
        node_control = ast.get_subtree(node.control)
        for decl in node_control.get_proxy_nodes(ASTNodeType.VARIABLE_DECLARATOR):
            result.add(decl.name)
        for assignment in node_control.get_proxy_nodes(ASTNodeType.ASSIGNMENT):
            result.add(assignment.expressionl.member)
        return result

    def _handle_assignment(self, ast: AST, index_names: set[str], for_body: ASTNode) -> set[LineNumber]:
        result = set()
        for op in ast.get_subtree(for_body).get_proxy_nodes(ASTNodeType.ASSIGNMENT):
            if op.expressionl.node_type != ASTNodeType.MEMBER_REFERENCE:
                continue
            if op.expressionl.member not in index_names:
                continue
            result.add(op.expressionl.line)
        return result

    def _handle_unary_operations(self, ast: AST, index_names: set[str], for_body: ASTNode) -> set[LineNumber]:
        result = set()
        for op in ast.get_subtree(for_body).get_proxy_nodes(ASTNodeType.STATEMENT_EXPRESSION):
            if op.expression.node_type == ASTNodeType.ASSIGNMENT:
                continue
            if op.expression.member not in index_names:
                continue
            unary_operators = ("++", "--")
            for operator in op.expression.prefix_operators:
                if operator in unary_operators:
                    result.add(op.expression.line)
            for operator in op.expression.postfix_operators:
                if operator in unary_operators:
                    result.add(op.expression.line)
        return result
