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
from aibolit.ast_framework.ast_node import ASTNode
from typing import List
import re


class MethodSiblings:
    '''
    Count those methods, which
    start with the same names
    '''
    def _is_method_names_close(self, node: ASTNode, new_node: ASTNode) -> bool:
        splited_name = re.split('([A-Z][^A-Z]*)', node.name)
        return len(splited_name) > 1 and new_node.name.startswith(splited_name[0])

    def value(self, filename: str) -> List[int]:
        numbers: List[int] = []
        ast = AST.build_from_javalang(build_ast(filename))
        method_nodes = ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION)

        for node in method_nodes:
            for new_node in method_nodes:
                if node.node_index < new_node.node_index and self._is_method_names_close(node, new_node):
                    numbers.extend([node.line, new_node.line])
        return sorted(list(set(numbers)))
