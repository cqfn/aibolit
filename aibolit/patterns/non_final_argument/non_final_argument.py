# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.types_decl import LineNumber


class NonFinalArgument:
    def value(self, ast: AST) -> list[LineNumber]:
        """
        Returns line numbers of methods and constructors with non-final arguments.

        :param ast: AST to inspect
        :return: number of the lines with non-final arguments
        """
        lines: List[LineNumber] = []
        for node in ast.proxy_nodes(
            ASTNodeType.METHOD_DECLARATION,
            ASTNodeType.CONSTRUCTOR_DECLARATION,
        ):
            if any('final' not in parameter.modifiers for parameter in node.parameters):
                lines.append(node.line)
        return lines
