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
from typing import Any, List

from aibolit.ast_framework import AST, ASTNodeType, ASTNode
from aibolit.utils.ast_builder import build_ast


class HybridConstructor:

    def is_statement_ctor_inv(self, node: ASTNode) -> bool:
        """Is statement explicit constructor invocation."""

        if node.expression.node_type == ASTNodeType.EXPLICIT_CONSTRUCTOR_INVOCATION:
            return True
        else:
            return False

    def traverse_in_if(
            self,
            val: ASTNode,
            exp_ctrs_decls: List[ASTNode],
            other_statements: List[ASTNode]) -> None:
        """Traverse over if condition recursively to find
        explicit constructor invocation."""
        if hasattr(val, 'statements'):
            children = list(val.statements)
            for i in children:
                self.traverse(i, exp_ctrs_decls, other_statements)

        if hasattr(val, 'then_statement'):
            self.traverse_in_if(val.then_statement, exp_ctrs_decls, other_statements)
            other_statements.append(val.then_statement)
        if hasattr(val, 'else_statement'):
            self.traverse_in_if(val.else_statement, exp_ctrs_decls, other_statements)
            other_statements.append(val.else_statement)

    def traverse(
            self,
            statement: ASTNode,
            exp_ctrs_decls: List[ASTNode],
            other_statements: List[ASTNode]) -> None:
        """Traverse over AST recursively to find all explicit
        constructor invocations and other statements."""

        if statement.node_type == ASTNodeType.STATEMENT_EXPRESSION:
            is_ctor_inv = self.is_statement_ctor_inv(statement)
            if is_ctor_inv:
                exp_ctrs_decls.append(statement)
            else:
                other_statements.append(statement)
        elif statement.node_type == ASTNodeType.TRY_STATEMENT:
            self.traverse_in_try(exp_ctrs_decls, other_statements, statement)
        elif statement.node_type in (
                ASTNodeType.DO_STATEMENT,
                ASTNodeType.WHILE_STATEMENT):
            for i in statement.body.children:
                self.traverse(i, exp_ctrs_decls, other_statements)
        elif statement.node_type == ASTNodeType.FOR_STATEMENT:
            for i in statement.body.children:
                other_statements.append(statement)
                self.traverse(i, exp_ctrs_decls, other_statements)
        elif statement.node_type == ASTNodeType.IF_STATEMENT:
            other_statements.append(statement)
            self.traverse_in_if(statement.then_statement, exp_ctrs_decls, other_statements)
            self.traverse_in_if(statement.else_statement, exp_ctrs_decls, other_statements)
        else:
            other_statements.append(statement)

    def traverse_in_try(
            self,
            exp_ctrs_decls: List[ASTNode],
            other_statements: List[ASTNode],
            statement: ASTNode) -> None:
        """Check try statements and find different statements."""
        if (statement.resources is not None) or \
                (statement.catches is not None and statement.catches[0].block != []) or \
                (statement.finally_block is not None):
            other_statements.append(statement)
        for try_stat in statement.block:
            self.traverse(try_stat, exp_ctrs_decls, other_statements)

    def value(self, filename: str) -> List[int]:
        tree = AST.build_from_javalang(build_ast(filename))
        lines = []
        for node in tree.get_proxy_nodes(ASTNodeType.CONSTRUCTOR_DECLARATION):
            exp_ctrs_decls: List[Any] = []
            other_statements: List[Any] = []
            for statement in node.body:
                self.traverse(statement, exp_ctrs_decls, other_statements)

            if len(exp_ctrs_decls) > 0:
                if len(other_statements) > 0:
                    lines.append(node.line)

        return lines
