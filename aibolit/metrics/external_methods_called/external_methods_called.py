# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from typing import Set

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class ExternalMethodsCalled:
    """
    Measure the number of external methods called by the class.
    """

    def value(self, ast: AST) -> int:
        if not isinstance(ast, AST):
            ast = AST.build_from_javalang(build_ast(ast))
        return ExternalMethodsCalledCount(ast).total()


@dataclass(frozen=True)
class ExternalMethodsCalledCount:
    ast: AST

    def total(self) -> int:
        return len(set(self._external_method_names_called()))

    def _external_method_names_called(self) -> Set[str]:
        local_methods = self._local_method_names()
        return set(
            node.member
            for node in self.ast.proxy_nodes(ASTNodeType.METHOD_INVOCATION)
            if node.member not in local_methods
        )

    def _local_method_names(self) -> Set[str]:
        return set(
            node.name
            for node in self.ast.proxy_nodes(ASTNodeType.METHOD_DECLARATION)
        )
