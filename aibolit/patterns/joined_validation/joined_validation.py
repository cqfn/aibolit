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

from typing import List, Tuple

from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNodeType


class JoinedValidation:
    """
    Pattern which matches joined validations: validations (if with a single throw inside) which condition
    contains more than condition joined with OR
    """

    def __init__(self):
        pass

    def check_throw(self, node: int, tree: 'AST', lines: List[int]) -> Tuple[List[int], bool]:
        children_throw = list(tree.children_with_type(node, ASTNodeType.THROW_STATEMENT))
        if len(children_throw) > 0:
            lines.append(tree.get_attr(node, 'line'))
            return lines, True
        return lines, False

    def value(self, filename: str) -> List[int]:
        """
        Returns the line number of joined validations found in file.
        """
        tree = AST.build_from_javalang(build_ast(filename))
        lines: List[int] = []
        for node in tree.get_nodes(ASTNodeType.IF_STATEMENT):
            flag_or = False
            for child in tree.all_children_with_type(node, ASTNodeType.BINARY_OPERATION):
                operation_name = tree.get_binary_operation_name(child)
                if operation_name == '||':
                    flag_or = True
            if not flag_or:
                continue
            lines, flag = self.check_throw(node, tree, lines)
            if flag:
                continue
            child_block = list(tree.children_with_type(node, ASTNodeType.BLOCK_STATEMENT))
            if len(child_block) == 0:
                continue
            lines, _ = self.check_throw(child_block[0], tree, lines)
        return lines
