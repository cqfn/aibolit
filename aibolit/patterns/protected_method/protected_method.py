# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework import ASTNodeType, AST


class ProtectedMethod:
    '''
    Once we find a protected method in a class, it's a pattern.
    '''
    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for method_declaration in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            if 'protected' in method_declaration.modifiers:
                lines.append(method_declaration.line)
        return lines
