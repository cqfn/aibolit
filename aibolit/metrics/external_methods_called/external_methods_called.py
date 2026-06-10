# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
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
        for node in self._parent_method_invocation_nodes():
            for first, second in itertools.pairwise(node.children):
                if self._member_reference_followed_by_method_invocation(first, second):
                    yield second.member

    def _parent_method_invocation_nodes(self) -> Iterator[ASTNode]:
        for node in self.ast.proxy_nodes(ASTNodeType.METHOD_INVOCATION):
            if (parent := node.parent) is not None:
                yield parent

    def _member_reference_followed_by_method_invocation(
        self,
        first: ASTNode,
        second: ASTNode,
    ) -> bool:
        return (
            first.node_type == ASTNodeType.MEMBER_REFERENCE and
            second.node_type == ASTNodeType.METHOD_INVOCATION
        )
