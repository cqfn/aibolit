# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from aibolit.ast_framework import AST, ASTNodeType


class NumberMethods:
    def value(self, ast: AST) -> int:
        metric = 0
        for class_node in ast.get_proxy_nodes(ASTNodeType.CLASS_DECLARATION):
            for method_node in class_node.methods:
                metric += 1
        return metric
