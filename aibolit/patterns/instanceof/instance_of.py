# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class InstanceOf:
    """
    Finds instance_of operator and .isInstance() method call.
    """

    def value(self, ast: AST):
        lines: List[int] = []
        for binary_operator in ast.get_proxy_nodes(ASTNodeType.BINARY_OPERATION):
            if binary_operator.operator == 'instanceof':
                lines.append(binary_operator.line)

        for method_invocation in ast.get_proxy_nodes(ASTNodeType.METHOD_INVOCATION):
            if method_invocation.member == 'isInstance':
                lines.append(method_invocation.line)

        return lines
