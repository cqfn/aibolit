# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
from typing import Iterator, List
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class ClassicSetter:
    """
    The method's name starts with set. There are attributes
    assigning in the method. Also, asserts are ignored.
    """
    def value(self, ast: AST) -> List[int]:
        return sorted(set(node.line for node in _setter_nodes(ast)))


def _setter_nodes(ast: AST) -> Iterator[ASTNode]:
    for node, parameters in _methods_with_parameters(ast):
        method_name = node.name
        parameter_name = node.parameters[0].name
        if node.return_type is None and method_name.startswith('set'):
            for child in node.children:
                if child.node_type == ASTNodeType.STATEMENT_EXPRESSION:
                    expression = child.expression
                    if expression.node_type == ASTNodeType.ASSIGNMENT:
                        value = expression.value
                        if (
                            value.node_type == ASTNodeType.MEMBER_REFERENCE and
                            value.member == parameter_name
                        ):
                            yield node


def _methods_with_parameters(ast: AST) -> Iterator[tuple[ASTNode, list[str]]]:
    for node in ast.proxy_nodes(ASTNodeType.METHOD_DECLARATION):
        if node.parameters:
            yield node, node.parameters
