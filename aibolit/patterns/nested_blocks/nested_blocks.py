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


class NestedBlocks:
    '''
    Returns lines in the file where
    nested blocks statements are located
    '''

    def __init__(self, max_depth: int, *block_types: ASTNodeType):
        self._max_depth = max_depth
        self._block_types = block_types

    def value(self, filename: str) -> List[int]:
        lines: List[int] = []
        ast = AST.build_from_javalang(build_ast(filename))
        for block_type in self._block_types:
            for block_ast in ast.get_subtrees(block_type):
                for overnested_block in self._find_overnested_blocks(block_ast.get_root()):
                    lines.append(overnested_block.line)

        return lines

    def _find_overnested_blocks(self, node: ASTNode, depth: int = 1) -> List[ASTNode]:
        if depth == self._max_depth:
            return [node]

        overnested_blocks: List[ASTNode] = []
        for nested_block in self._get_nested_statements(node):
            if nested_block.node_type == node.node_type:
                overnested_blocks.extend(self._find_overnested_blocks(nested_block, depth + 1))

        return overnested_blocks

    def _get_nested_statements(self, node: ASTNode) -> List[ASTNode]:
        nested_statements: List[ASTNode] = []

        if node.node_type == ASTNodeType.IF_STATEMENT:
            nested_statements.extend(self._get_block_statements_list(node.then_statement))

            while node.else_statement is not None and node.else_statement.node_type == ASTNodeType.IF_STATEMENT:
                node = node.else_statement
                nested_statements.extend(self._get_block_statements_list(node.then_statement))

            if node.else_statement is not None:
                nested_statements.extend(self._get_block_statements_list(node.else_statement))

        elif node.node_type in {ASTNodeType.DO_STATEMENT,
                                ASTNodeType.FOR_STATEMENT,
                                ASTNodeType.WHILE_STATEMENT}:
            nested_statements.extend(self._get_block_statements_list(node.body))

        return nested_statements

    def _get_block_statements_list(self, node: ASTNode) -> List[ASTNode]:
        if node.node_type == ASTNodeType.BLOCK_STATEMENT:
            return node.statements

        # A single statement is treated as a block with this statement
        # This happens in following situations
        # ```java
        # while(True)
        #     doSmth();
        # ```
        return [node]
