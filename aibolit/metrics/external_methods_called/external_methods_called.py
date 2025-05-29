# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import itertools
import os
from dataclasses import dataclass
from typing import Iterator

from aibolit.ast_framework import AST, ASTNode, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class ExternalMethodsCalled:
    """
    Measure the number of external methods called by the class.

    @todo #183:30min Implement external method called metric
    In the methods in the class an external method for this class can
    be called. So number of external methods called by all the methods
    in the class is suggested as a metric. Implement this metric and then
    enable tests in test_external_methods_called.py
    """

    def __init__(self):
        pass

    def value(self, filepath: str | os.PathLike):
        return ExternalMethodsCalledCount(AST.build_from_javalang(build_ast(filepath))).total()


@dataclass(frozen=True)
class ExternalMethodsCalledCount:
    ast: AST

    def total(self) -> int:
        return len(set(self._external_method_names_called()))

    def _external_method_names_called(self) -> Iterator[str]:
        for node in self.ast.get_proxy_nodes(ASTNodeType.METHOD_INVOCATION):
            parent = node.parent
            if parent is None:
                continue

            for first, second in itertools.pairwise(parent.children):
                if self._member_ref_followed_by_method_invocation(first, second):
                    yield second.member

    def _member_ref_followed_by_method_invocation(
        self,
        first: ASTNode | None,
        second: ASTNode | None,
    ) -> bool:
        return (
            first is not None and
            second is not None and
            first.node_type == ASTNodeType.MEMBER_REFERENCE and
            second.node_type == ASTNodeType.METHOD_INVOCATION
        )
