# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework import ASTNodeType, AST


class MultipleTry:
    '''
    Check if a method contains more than one Try Statement
    '''
    def value(self, ast: AST) -> List[int]:
        total_code_lines: List[int] = []
        for method_declaration in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            try_nodes = list(ast.get_subtree(method_declaration).get_proxy_nodes(
                ASTNodeType.TRY_STATEMENT))
            if len(try_nodes) > 1:
                total_code_lines.append(method_declaration.line)
        return total_code_lines
