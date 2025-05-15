# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List, Union

from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class ManyPrimaryCtors:
    '''
    If there is more than one primary
    constructors in a class, it is
    considered a pattern
    '''
    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for class_declaration in ast.get_proxy_nodes(ASTNodeType.CLASS_DECLARATION):
            primary_lines = self.__find_primary(ast, class_declaration.body)
            if len(primary_lines) > 1:
                lines.extend(primary_lines)
        return lines

    def __find_primary(self, ast: AST, class_body: List[ASTNode]) -> List[int]:
        lines: List[int] = []
        for node in class_body:
            if self.__check_primary(ast, node):
                lines.append(node.line)
        return lines

    def __check_primary(self, ast: AST, node: Union[ASTNode, List[ASTNode]]) -> bool:
        if isinstance(node, ASTNode) and node.node_type == ASTNodeType.CONSTRUCTOR_DECLARATION:
            for assignment in ast.get_subtree(node).get_proxy_nodes(ASTNodeType.ASSIGNMENT):
                if assignment.expressionl.node_type == ASTNodeType.THIS:
                    return True
        return False
