# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class JoinedValidation:
    '''
    Finds all if statements, which "then" branch consist of a single throw statement
    and logical or "||" used in condition.
    '''

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for if_statement in ast.get_proxy_nodes(ASTNodeType.IF_STATEMENT):
            if self._is_logical_or_used_in_expression(if_statement.condition) and \
               self._is_block_consist_of_single_throw(if_statement.then_statement):
                lines.append(if_statement.line)
        return lines

    def _is_logical_or_used_in_expression(self, expression: ASTNode) -> bool:
        if expression.node_type == ASTNodeType.BINARY_OPERATION and expression.operator == '||':
            return True

        return any(self._is_logical_or_used_in_expression(child) for child in expression.children)

    def _is_block_consist_of_single_throw(self, block: ASTNode) -> bool:
        if block.node_type == ASTNodeType.THROW_STATEMENT:
            return True

        children = list(block.children)
        return len(children) == 1 and children[0].node_type == ASTNodeType.THROW_STATEMENT
