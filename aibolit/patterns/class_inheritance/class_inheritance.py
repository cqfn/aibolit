# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class ClassInheritance:
    """
    Find classes that use implementation inheritance via the `extends` keyword.
    """

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for class_declaration in ast.proxy_nodes(ASTNodeType.CLASS_DECLARATION):
            if class_declaration.extends is not None:
                lines.append(class_declaration.line)
        return lines
