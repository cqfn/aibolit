# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class ClassicSetter:
    '''
    The method's name starts with set. There are attributes
    assigning in the method. Also, asserts are ignored.
    '''
    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for node in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            method_name = node.name
            if not node.parameters:
                continue

            parameter_name = node.parameters[0].name
            if node.return_type is None and method_name.startswith('set'):
                for child in node.children:
                    if child.node_type == ASTNodeType.STATEMENT_EXPRESSION:
                        expression = child.expression
                        if expression.node_type == ASTNodeType.ASSIGNMENT and expression.value.member == parameter_name:
                            lines.append(node.line)

                lines.append(node.line)
        return sorted(set(lines))
