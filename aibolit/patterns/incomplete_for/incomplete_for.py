# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
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
        for for_control in ast.proxy_nodes(ASTNodeType.FOR_CONTROL):
            if not all((for_control.init, for_control.update, for_control.condition)):
                parent = for_control.parent
                if parent is None:
                    raise RuntimeError('For control without For statement parent')
                lines.add(parent.line)
        return sorted(lines)
