# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
from typing import Iterator

from aibolit.ast_framework import AST, ASTNode, ASTNodeType
from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast


class NonFinalArgument:
    def __init__(self):
        pass

    def value(self, filename: str | os.PathLike) -> list[LineNumber]:
        """
        Returns the line numbers of the file name which contains no final arguments

        :param filename: name of the file
        :return: number of the lines with non-final arguments
        """
        return sorted(
            node.line
            for node in _offending_nodes(AST.build_from_javalang(build_ast(filename)))
        )


def _offending_nodes(ast: AST) -> Iterator[ASTNode]:
    for node in ast.get_proxy_nodes(
        ASTNodeType.METHOD_DECLARATION,
        ASTNodeType.CONSTRUCTOR_DECLARATION,
    ):
        for parameter in node.parameters:
            if 'final' not in parameter.modifiers:
                yield node
