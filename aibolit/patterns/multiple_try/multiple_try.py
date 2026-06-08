# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework import ASTNodeType, AST


class MultipleTry:
    """
    Check if a method contains more than one Try Statement
    """
    def value(self, ast: AST) -> List[int]:
        total_code_lines: List[int] = []
        for method_declaration in ast.proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            try_nodes = list(ast.subtree(method_declaration).proxy_nodes(
                ASTNodeType.TRY_STATEMENT))
            if len(try_nodes) > 1:
                total_code_lines.append(method_declaration.line)
        return total_code_lines
