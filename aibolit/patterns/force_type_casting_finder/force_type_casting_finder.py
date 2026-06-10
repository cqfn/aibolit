# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class ForceTypeCastingFinder:
    def value(self, ast: AST) -> List[int]:
        return [cast.expression.line for cast in ast.proxy_nodes(ASTNodeType.CAST)]
