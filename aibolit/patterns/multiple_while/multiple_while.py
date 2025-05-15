# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class MultipleWhile:
    '''
    Finds methods, with more than one "while" cycle, exceluding nested ones.
    '''

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for method_declaration in ast.get_subtrees(ASTNodeType.METHOD_DECLARATION):
            top_level_while_loops = method_declaration.get_subtrees(ASTNodeType.WHILE_STATEMENT)
            if len(list(top_level_while_loops)) > 1:
                lines.append(method_declaration.get_root().line)

        return lines
