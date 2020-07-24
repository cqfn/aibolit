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
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast
from typing import Set, List
from aibolit.ast_framework.ast_node import ASTNode


class StringConcatFinder:
    '''
    Any usage string concatenation using '+' operator is considered as a pattern.
    '''
    def _check_left_right_operator(self, node: ASTNode) -> bool:
        assert node.node_type == ASTNodeType.BINARY_OPERATION
        for operator_side in [node.operandr, node.operandl]:
            if operator_side.node_type == ASTNodeType.LITERAL and isinstance(operator_side.value, str) and \
               not operator_side.value.isdigit():
                return True
        return False

    def value(self, filename: str) -> List[int]:
        lines: Set[int] = set()
        ast = AST.build_from_javalang(build_ast(filename))
        for node in ast.get_proxy_nodes(ASTNodeType.BINARY_OPERATION):
            if node.operator == '+' and self._check_left_right_operator(node):
                lines.add(node.line)

        return sorted(lines)
