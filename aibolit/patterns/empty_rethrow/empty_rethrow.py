# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class EmptyRethrow:
    '''
    Check if we throw the same exception as it was caught
    '''
    def _process_catch(self, ast: AST, catch_clauses: List[ASTNode]):
        lines: List[int] = []
        for catch_clause in catch_clauses:
            throw_statements = ast.get_subtree(catch_clause).get_proxy_nodes(
                ASTNodeType.THROW_STATEMENT)
            for throw_stat in throw_statements:
                if throw_stat.expression.node_type == ASTNodeType.MEMBER_REFERENCE \
                   and throw_stat.expression.member == catch_clause.parameter.name:
                    lines.append(throw_stat.line)
        return lines

    def value(self, ast: AST) -> List[int]:
        total_code_lines: List[int] = []
        for try_node in ast.get_proxy_nodes(ASTNodeType.TRY_STATEMENT):
            catch_clauses = try_node.catches
            if catch_clauses:
                total_code_lines.extend(self._process_catch(ast, catch_clauses))

        return sorted(total_code_lines)
