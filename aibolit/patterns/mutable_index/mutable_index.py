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

        @todo #147:30min Implement MutableIndex pattern
        We need to implement the code on mutable index pattern. It must return the number
        of the lines where we have an index of a for loop being mutated. After implementing,
        the method, enable all tests in test_mutable_index.py
        """
        result = set()
        ast = AST.build_from_javalang(build_ast(filename))
        for node in ast.get_proxy_nodes(
            ASTNodeType.FOR_STATEMENT,
        ):
            index_names = set()
            for decl in ast.get_subtree(node.control).get_proxy_nodes(
                ASTNodeType.VARIABLE_DECLARATOR
            ):
                index_names.add(decl.name)
            for assignment in ast.get_subtree(node.control).get_proxy_nodes(
                ASTNodeType.ASSIGNMENT
            ):
                index_names.add(assignment.expressionl.member)
            # print(ast.get_subtree(node.body))
            # index_names = set(d.name for d in node.control.init.declarators)
            for op in ast.get_subtree(node.body).get_proxy_nodes(
                ASTNodeType.ASSIGNMENT
            ):
                if op.expressionl.node_type == ASTNodeType.MEMBER_REFERENCE:
                    if op.expressionl.member in index_names:
                        result.add(op.expressionl.line)

            for op in ast.get_subtree(node.body).get_proxy_nodes(
                ASTNodeType.STATEMENT_EXPRESSION
            ):
                if op.expression.node_type == ASTNodeType.ASSIGNMENT:
                    continue
                if op.expression.member not in index_names:
                    continue
                if any(
                    operator in ("++", "--")
                    for operator in op.expression.postfix_operators
                ):
                    result.add(op.expression.line)
                if any(
                    operator in ("++", "--")
                    for operator in op.expression.prefix_operators
                ):
                    result.add(op.expression.line)

        return sorted(result)
