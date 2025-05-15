# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework import ASTNodeType, AST


class NonFinalAttribute:
    '''
    return lines of non-final attributes
    '''
    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for field in ast.get_proxy_nodes(ASTNodeType.FIELD_DECLARATION):
            if 'final' not in field.modifiers:
                lines.append(field.line)
        return lines
