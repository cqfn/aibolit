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

from typing import List, Optional

from aibolit.ast_framework import AST, ASTNode, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class InstanceOf:
    """
    Finds instance_of operator and .isInstance() method call.
    """

    def value(self, filename: str):
        ast = AST.build_from_javalang(build_ast(filename))
        lines: List[int] = []
        for binary_operator in ast.get_proxy_nodes(ASTNodeType.BINARY_OPERATION):
            if binary_operator.operator == 'instanceof':
                operator_line = self._get_binary_operator_line(binary_operator)
                if operator_line:
                    lines.append(operator_line)

        for method_invocation in ast.get_proxy_nodes(ASTNodeType.METHOD_INVOCATION):
            if method_invocation.member == 'isInstance':
                lines.append(method_invocation.line)

        return lines

    def _get_binary_operator_line(self, binary_operator_node: ASTNode) -> Optional[int]:
        assert binary_operator_node.node_type == ASTNodeType.BINARY_OPERATION
        if binary_operator_node.line is not None:
            return binary_operator_node.lines

        if binary_operator_node.operandl.line is not None:
            return binary_operator_node.operandl.line

        # TODO: log that operator line was not found
        return None
