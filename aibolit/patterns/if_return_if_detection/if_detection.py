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

from aibolit.ast_framework import AST, ASTNode, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class CountIfReturn:
    '''
    Finds "if" statements with else branches and return statement in then branch.
    '''

    def value(self, filename: str) -> List[int]:
        ast = AST.build_from_javalang(build_ast(filename))
        lines: List[int] = []
        for if_statement in ast.get_proxy_nodes(ASTNodeType.IF_STATEMENT):
            if if_statement.else_statement is not None and \
               self._is_then_branch_return(if_statement):
                lines.append(if_statement.line)

        return lines

    def _is_then_branch_return(self, if_statement: ASTNode) -> bool:
        if if_statement.then_statement.node_type == ASTNodeType.RETURN_STATEMENT:
            return True

        if if_statement.then_statement.node_type == ASTNodeType.BLOCK_STATEMENT:
            return any(statement.node_type == ASTNodeType.RETURN_STATEMENT
                       for statement in if_statement.then_statement.statements)

        return False
