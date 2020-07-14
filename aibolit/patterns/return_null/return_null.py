# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List

from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class ReturnNull:
    '''
    FInds all return statements that returns null directly or by ternary operator.
    NOTICE: nested ternary operators are not checked.
    '''

    def value(self, filename: str) -> List[int]:
        ast = AST.build_from_javalang(build_ast(filename))
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
