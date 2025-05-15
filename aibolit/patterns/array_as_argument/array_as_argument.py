# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class ArrayAsArgument:
    '''
    Finds all methods declarations, which accept arrays as parameters.
    '''

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for method_declaration in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION,
                                                      ASTNodeType.CONSTRUCTOR_DECLARATION):
            if any(len(parameter.type.dimensions) > 0
                   for parameter in method_declaration.parameters):
                lines.append(method_declaration.line)
        return lines
