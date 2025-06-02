# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.types_decl import LineNumber


class IncompleteFor:
    """
    Finds all for statements, which don't have at least one control part
    """

    def value(self, ast: AST) -> List[LineNumber]:
        lines: set[int] = set()
        for for_statement in ast.get_proxy_nodes(ASTNodeType.FOR_STATEMENT):
            for_control = for_statement.control
            if not all((for_control.init, for_control.update, for_control.condition)):
                lines.add(for_statement.line)
        return sorted(lines)
