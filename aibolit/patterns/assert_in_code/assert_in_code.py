# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class AssertInCode:
    '''
    Finds use of all asserts.
    '''

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for assert_node in ast.get_proxy_nodes(ASTNodeType.ASSERT_STATEMENT):
            lines.append(assert_node.line)

        return lines
