# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class PublicStaticMethod:
    '''
    Check method with 'public static'
    '''
    def _check_public_static(self, node: ASTNode):
        if all(type in node.modifiers for type in ['public', 'static']):
            return True
        return False

    def value(self, ast: AST):
        lines: List[int] = []
        for method_declaration in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            if self._check_public_static(method_declaration):
                lines.append(method_declaration.line)
        return lines
