# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class EmptyFinally:
    """
    Finds all try-catch-finally statements where the 'finally' block is empty.
    """

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for try_statement in ast.proxy_nodes(ASTNodeType.TRY_STATEMENT):
            # Check if the 'finally' block exists for this try statement
            if hasattr(try_statement, 'finally_block') and try_statement.finally_block is not None:
                block = try_statement.finally_block

                # Aibolit's AST wrapper unwraps BlockStatements into lists of statements.
                # An empty finally block is represented as an empty list [].
                is_empty = (isinstance(block, list) and len(block) == 0) or \
                           (hasattr(block, 'statements') and len(block.statements) == 0)

                if is_empty:
                    # Since the empty block loses its specific line number in the wrapper,
                    # we report the line of the 'try' keyword itself.
                    lines.append(try_statement.line)

        return lines
