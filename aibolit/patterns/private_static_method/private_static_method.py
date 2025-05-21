# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework import ASTNodeType, AST


class PrivateStaticMethod:
    '''
    Once you see a 'private static' method, it's a pattern.
    '''
    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for method_declaration in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            if {'private', 'static'}.issubset(method_declaration.modifiers):
                lines.append(method_declaration.line)
        return lines
