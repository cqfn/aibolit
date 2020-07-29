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


class NestedBlocks:
    '''
    Returns lines in the file where
    nested blocks statements are located
    '''

    def __init__(self, max_depth: int, *block_type: ASTNodeType):
        self._max_depth = max_depth
        self._block_type = block_type

    def value(self, filename: str) -> List[int]:
        lines: List[int] = []
        ast = AST.build_from_javalang(build_ast(filename))
        for node in ast.get_subtrees(*self._block_type):
            nested_node = self._is_overnested(node.get_root())
            if nested_node is not None:
                lines.append(nested_node.line)

        return lines

    def _is_overnested(self, node: ASTNode) -> Optional[ASTNode]:
        node_type = node.node_type
        nested_level = 1
        block = self._get_next_block(node)

        while len(block) == 1 and block[0].node_type == node_type:
            nested_level += 1
            nested_statement = block[0]
            if nested_level >= self._max_depth:
                return nested_statement

            block = self._get_next_block(nested_statement)

        return None

    def _get_next_block(self, node: ASTNode) -> List[ASTNode]:
        if node.node_type == ASTNodeType.IF_STATEMENT:
            return self._wrap_single_statement_block(node.then_statement)
        elif node.node_type in {ASTNodeType.DO_STATEMENT,
                                ASTNodeType.FOR_STATEMENT,
                                ASTNodeType.WHILE_STATEMENT}:
            return self._wrap_single_statement_block(node.body)

        raise RuntimeError(f"{node} was provided. Expected types are:\n"
                           " - ASTNodeType.DO_STATEMENT\n"
                           " - ASTNodeType.IF_STATEMENT\n"
                           " - ASTNodeType.FOR_STATEMENT\n"
                           " - ASTNodeType.WHILE_STATEMENT\n")

    def _wrap_single_statement_block(self, node: ASTNode) -> List[ASTNode]:
        if node.node_type == ASTNodeType.BLOCK_STATEMENT:
            return node.statements

        return [node]
