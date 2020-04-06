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

from collections import defaultdict
from aibolit.utils.ast import AST

import javalang


class ReturnNull:

    def __init__(self):
        pass

    def value(self, filename: str):
        """
        Travers over AST tree and finds pattern
        :param filename:
        """
        tree = AST(filename).value()
        chain_lst = defaultdict(int)
        for _, method_node in tree.filter(javalang.tree.MethodDeclaration):
            for _, return_node in method_node.filter(javalang.tree.ReturnStatement):
                return_literal = return_node.children[1]
                if isinstance(return_literal, javalang.tree.Literal) and return_literal.value == 'null':
                    chain_lst[method_node.name] = return_literal.position.line or return_node.position.line
                elif isinstance(return_literal, javalang.tree.TernaryExpression):
                    chain_lst[method_node.name] = return_node.position.line

        filtered_dict = list(filter(lambda elem: elem > 0, chain_lst.values()))
        return filtered_dict
