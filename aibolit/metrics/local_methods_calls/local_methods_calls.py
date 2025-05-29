# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
from typing import Iterator

from aibolit.ast_framework import AST, ASTNode, ASTNodeType
from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast


class LocalMethodsCalls:
    """
    Measure the number of local methods called by the class.

    @todo #183:30min Implement local method called metric
    In the methods in the class an local method (method that is defined in this class)
    can be called. So number of local methods calls by all the methods in the
    class is suggested as a metric. Implement this metric and then
    enable tests in test_local_methods_calls.py
    """

    def __init__(self):
        pass

    def value(self, filepath: str | os.PathLike):
        ast = AST.build_from_javalang(build_ast(filepath))
        return sum(1 for _ in _offending_lines(ast))


def _offending_lines(ast: AST) -> Iterator[LineNumber]:
    methods_called = set(
        node.member
        for node in ast.get_proxy_nodes(ASTNodeType.METHOD_INVOCATION)
    )
    local_methods_declared = set(
        node.name
        for node in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION)
    )
    yield from methods_called.difference(local_methods_declared)
