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
from typing import List


class ErClass:
    '''
    Check if a class name include the forbidden word
    '''
    forbiden_words_in_class_names = (
        'manager',
        'controller',
        'router',
        'dispatcher',
        'printer',
        'writer',
        'reader',
        'parser',
        'generator',
        'renderer',
        'listener',
        'producer',
        'holder',
        'interceptor')

    def value(self, filename: str) -> List[int]:
        lines: List[int] = []
        ast = AST.build_from_javalang(build_ast(filename))
        for node in ast.get_proxy_nodes(ASTNodeType.CLASS_DECLARATION):
            class_name = node.name.lower()
            if any(forbiden_word in class_name for forbiden_word in self.forbiden_words_in_class_names):
                lines.append(node.line)
        return lines
