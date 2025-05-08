# SPDX-FileCopyrightText: Copyright (c) 2020 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class ForceTypeCastingFinder:
    def value(self, ast: AST) -> List[int]:
        return [cast.expression.line for cast in ast.get_proxy_nodes(ASTNodeType.CAST)]
