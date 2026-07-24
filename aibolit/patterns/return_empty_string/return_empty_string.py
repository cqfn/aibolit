# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class ReturnEmptyString:
    """
    Finds all return statements that return an empty string literal "" directly
    or by ternary operator.
    NOTICE: nested ternary operators are not checked (consistent with ReturnNull).
    """

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for return_statement in ast.proxy_nodes(ASTNodeType.RETURN_STATEMENT):
            if self._check_empty_string_return_statement(return_statement):
                lines.append(return_statement.line)

        return lines

    def _check_empty_string_return_statement(self, return_statement: ASTNode) -> bool:
        """
        Check if a return statement returns an empty string, 
        including via a single-level ternary operator.
        """
        # return statement with no expression `return;` does not return an empty string
        if return_statement.expression is None:
            return False
        # Check if the expression is a ternary operator (a ? b : c)
        if return_statement.expression.node_type == ASTNodeType.TERNARY_EXPRESSION:
            return self._check_empty_string_expression(return_statement.expression.if_true) or \
                self._check_empty_string_expression(return_statement.expression.if_false)
        return self._check_empty_string_expression(return_statement.expression)

    def _check_empty_string_expression(self, expression: ASTNode) -> bool:
        """
        Check that the expression is a string literal strictly equal to '""'.
        (javalang preserves the quotes as part of the string value).
        """
        return expression.node_type == ASTNodeType.LITERAL and expression.value == '""'
