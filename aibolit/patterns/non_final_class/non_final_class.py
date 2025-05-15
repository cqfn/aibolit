# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class NonFinalClass:
    '''
    Find all classes that are neither "final" nor "abstract".
    '''

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for class_declaration in ast.get_proxy_nodes(ASTNodeType.CLASS_DECLARATION):
            if len(class_declaration.modifiers & NonFinalClass._allowed_class_modifiers) == 0:
                lines.append(class_declaration.line)

        return lines

    _allowed_class_modifiers = {'final', 'abstract'}
