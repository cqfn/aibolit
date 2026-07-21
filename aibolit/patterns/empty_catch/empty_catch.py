# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class EmptyCatch:
    """
    Finds all try-catch statements where the 'catch' block is empty.
    """

    def value(self, ast: AST) -> List[int]:
        """
        Calculate line numbers of empty catch blocks in the given AST.

        Args:
            ast: The AST of the Java file to analyze.

        Returns:
            A list of line numbers where empty catch blocks are found.
            Since the AST wrapper unwraps empty blocks, the line of the
            parent 'try' statement is returned.
        """
        lines: List[int] = []
        for try_statement in ast.proxy_nodes(ASTNodeType.TRY_STATEMENT):
            # Check if the 'catches' list exists and is not empty
            if hasattr(try_statement, 'catches') and try_statement.catches:
                for catch_clause in try_statement.catches:
                    # In javalang, the body of a catch clause is stored in the 'block' attribute
                    block = getattr(catch_clause, 'block', None)

                    # An empty catch block is represented as an empty list []
                    if block is not None and isinstance(block, list) and len(block) == 0:
                        # Report the line of the 'try' statement
                        lines.append(try_statement.line)

        return lines
