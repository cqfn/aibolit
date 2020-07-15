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


class JoinedValidation:
    '''
    Finds all if statements, which "then" branch consist of a single throw statement
    and logical or "||" used in condition.
    '''

    def value(self, filename: str) -> List[int]:
        ast = AST.build_from_javalang(build_ast(filename))
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
