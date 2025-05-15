# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework.ast import AST, ASTNodeType


class SuperMethod:
    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for statement in ast.get_proxy_nodes(ASTNodeType.STATEMENT_EXPRESSION):
            if any(child.node_type == ASTNodeType.SUPER_METHOD_INVOCATION
                    for child in statement.children):
                lines.append(statement.line)
        return lines
