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
from aibolit.ast_framework import AST, ASTNodeType


class ReturnNull:

    def __init__(self):
        pass

    def __check_null_in_return_args(self, node: int, tree: AST) -> bool:
        for child1 in tree.children_with_type(node, ASTNodeType.LITERAL):
            for child2 in tree.children_with_type(child1, ASTNodeType.STRING):
                if tree.get_attr(child2, 'string') == 'null':
                    return True
        return False

    def __check_null_in_return_statement(self, node: int, tree: AST) -> bool:
        child_ternary = list(tree.children_with_type(node, ASTNodeType.TERNARY_EXPRESSION))
        if len(child_ternary) > 0:
            return self.__check_null_in_return_args(child_ternary[0], tree)
        return self.__check_null_in_return_args(node, tree)

    def value(self, filename: str) -> List[int]:
        """
        Travers over AST tree and finds pattern
        :param filename:
        """
        tree = AST.build_from_javalang(build_ast(filename))
        lines: List[int] = []
        for node in tree.get_nodes(ASTNodeType.METHOD_DECLARATION):
            for child in tree.children_with_type(node, ASTNodeType.RETURN_STATEMENT):
                if self.__check_null_in_return_statement(child, tree):
                    lines.append(tree.get_attr(child, 'line'))

        return lines
