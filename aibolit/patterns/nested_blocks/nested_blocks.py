# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class NestedBlocks:
    '''
    Returns lines in the file where
    nested blocks statements are located
    '''

    def __init__(self, max_depth: int, *block_types: ASTNodeType):
        self._max_depth = max_depth
        self._block_types = block_types

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
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

            while (node.else_statement is not None and
                   node.else_statement.node_type == ASTNodeType.IF_STATEMENT):
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
