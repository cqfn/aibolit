# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class PartiallySynchronizedMethods:
    """
    Methods and constructors must have no 'synchronized' statements at all,
    including statements in lambda functions and anonymous class methods,
    or consist of single 'synchronized' statement (fully synchronized)
    """

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for method_ast in ast.get_subtrees(
            ASTNodeType.METHOD_DECLARATION, ASTNodeType.CONSTRUCTOR_DECLARATION
        ):
            method_declaration = method_ast.get_root()
            is_fully_sync_method = len(method_declaration.body) == 1 and \
                method_declaration.body[0].node_type == ASTNodeType.SYNCHRONIZED_STATEMENT

            synchronized_statements = list(
                method_ast.get_proxy_nodes(ASTNodeType.SYNCHRONIZED_STATEMENT)
            )

            if len(synchronized_statements) > 0 and not is_fully_sync_method:
                lines.extend(statement.line for statement in synchronized_statements)

        return lines
