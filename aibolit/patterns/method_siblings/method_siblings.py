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
    def __compare_next_nodes(self, node: ASTNode, new_node: ASTNode) -> List[int]:
        node_name = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node.name)
        if node.node_index < new_node.node_index and len(node_name) > 1 and \
           new_node.name.startswith(node_name[0]):
            return [node.line, new_node.line]
        return []

    def value(self, filename: str) -> List[int]:
        numbers: List[int] = []
        method_nodes = AST.build_from_javalang(
            build_ast(filename)).get_proxy_nodes(ASTNodeType.METHOD_DECLARATION)
        for node in method_nodes:
            for new_node in method_nodes:
                numbers.extend(self.__compare_next_nodes(node, new_node))
        return sorted(list(set(numbers)))
