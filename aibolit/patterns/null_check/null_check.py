# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class NullCheck():
    '''
    If we check that something equals
    (or not equals) null (except in constructor)
    it is considered a pattern.
    '''
    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for method_declaration in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            for bin_op in ast.get_subtree(method_declaration).get_proxy_nodes(
                    ASTNodeType.BINARY_OPERATION):
                if self._check_null(bin_op):
                    lines.append(bin_op.operandr.line)
        return lines

    def _check_null(self, bin_operation: ASTNode) -> bool:
        return (bin_operation.operator in ["==", "!="] and
                bin_operation.operandr.node_type == ASTNodeType.LITERAL and
                bin_operation.operandr.value == "null")
