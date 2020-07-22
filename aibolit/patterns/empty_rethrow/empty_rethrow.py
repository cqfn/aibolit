# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast
from typing import List
from aibolit.ast_framework.ast_node import ASTNode


class EmptyRethrow:
    '''
    Check if we throw the same exception as it was caught
    '''
    def _process_catch(self, ast: AST, catch_clauses: List[ASTNode]):
        lines: List[int] = []
        for catch_clause in catch_clauses:
            throw_statements = ast.get_subtree(catch_clause).get_proxy_nodes(ASTNodeType.THROW_STATEMENT)
            for throw_stat in throw_statements:
                if throw_stat.expression.node_type == ASTNodeType.MEMBER_REFERENCE \
                   and throw_stat.expression.member == catch_clause.parameter.name:
                    lines.append(throw_stat.line)
        return lines

    def value(self, filename) -> List[int]:
        total_code_lines: List[int] = []
        ast = AST.build_from_javalang(build_ast(filename))
        for try_node in ast.get_proxy_nodes(ASTNodeType.TRY_STATEMENT):
            catch_clauses = try_node.catches
            if catch_clauses:
                total_code_lines.extend(self._process_catch(ast, catch_clauses))

        return sorted(total_code_lines)
