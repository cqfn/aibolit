# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class ForceTypeCastingFinder:
    """Find explicit type-cast expressions that should be reported as P5."""

    def value(self, ast: AST) -> List[int]:
        """Return source lines of reported cast expressions."""
        return [
            cast.expression.line
            for cast in ast.proxy_nodes(ASTNodeType.CAST)
            if cast.expression.node_type != ASTNodeType.LAMBDA_EXPRESSION
        ]
