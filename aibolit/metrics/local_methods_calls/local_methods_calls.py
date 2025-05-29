# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
from collections import Counter

from aibolit.ast_framework import AST, ASTNodeType
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
        return _local_methods_called(ast)


def _local_methods_called(ast: AST) -> int:
    methods_called_counter = Counter(
        node.member
        for node in ast.get_proxy_nodes(ASTNodeType.METHOD_INVOCATION)
    )
    methods_called = set(methods_called_counter)
    local_methods_called = methods_called.intersection(_local_methods_declared(ast))
    return sum(methods_called_counter[method_name] for method_name in local_methods_called)


def _local_methods_declared(ast: AST) -> set[str]:
    return set(
        node.name
        for node in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION)
    )
