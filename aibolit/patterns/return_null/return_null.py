# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class ReturnNull:
    '''
    FInds all return statements that returns null directly or by ternary operator.
    NOTICE: nested ternary operators are not checked.
    '''

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for return_statement in ast.get_proxy_nodes(ASTNodeType.RETURN_STATEMENT):
            if self._check_null_return_statement(return_statement):
                lines.append(return_statement.line)

        return lines

    def _check_null_return_statement(self, return_statement: ASTNode) -> bool:
        # return statement with no expression `return;` does not return null
        if return_statement.expression is None:
            return False

        if return_statement.expression.node_type == ASTNodeType.TERNARY_EXPRESSION:
            return self._check_null_expression(return_statement.expression.if_true) or \
                self._check_null_expression(return_statement.expression.if_false)

        return self._check_null_expression(return_statement.expression)

    def _check_null_expression(self, expression: ASTNode) -> bool:
        return expression.node_type == ASTNodeType.LITERAL and expression.value == 'null'
