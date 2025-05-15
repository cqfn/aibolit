# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework.ast import AST, ASTNodeType


class ImplementsMultiFinder:
    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for node in ast.get_proxy_nodes(ASTNodeType.CLASS_DECLARATION):
            if node.implements and len(node.implements) > 1:
                lines.append(node.line)
        return lines
