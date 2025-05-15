# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class CountIfReturn:
    '''
    Finds "if" statements with else branches and return statement in then branch.
    '''

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for if_statement in ast.get_proxy_nodes(ASTNodeType.IF_STATEMENT):
            if if_statement.else_statement is not None and \
               self._is_then_branch_return(if_statement):
                lines.append(if_statement.line)

        return lines

    def _is_then_branch_return(self, if_statement: ASTNode) -> bool:
        if if_statement.then_statement.node_type == ASTNodeType.RETURN_STATEMENT:
            return True

        if if_statement.then_statement.node_type == ASTNodeType.BLOCK_STATEMENT:
            return any(statement.node_type == ASTNodeType.RETURN_STATEMENT
                       for statement in if_statement.then_statement.statements)

        return False
