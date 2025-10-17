# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
from collections import Counter
from dataclasses import dataclass

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class LocalMethodsCalls:
    """
    Measure the number of local methods called by the class.
    """

    def __init__(self) -> None:
        pass

    def value(self, filepath: str | os.PathLike) -> int:
        return LocalMethodsCallsCount(AST.build_from_javalang(build_ast(filepath))).total()


@dataclass(frozen=True)
class LocalMethodsCallsCount:
    ast: AST

    def total(self) -> int:
        methods_called_counter = self._methods_called()
        return sum(
            methods_called_counter[method_name]
            for method_name in self._local_methods_called()
        )

    def _local_methods_called(self) -> set[str]:
        methods_called = set(self._methods_called())
        return methods_called.intersection(self._local_methods_declared())

    def _methods_called(self) -> Counter:
        return Counter(
            node.member
            for node in self.ast.proxy_nodes(ASTNodeType.METHOD_INVOCATION)
        )

    def _local_methods_declared(self) -> set[str]:
        return set(
            node.name
            for node in self.ast.proxy_nodes(ASTNodeType.METHOD_DECLARATION)
        )
