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

from aibolit.ast_framework import AST, ASTNode, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class NCSSMetric():
    '''
    NCSS metric counts non-commenting source statements.
    It counts keywords, declarations and statement expressions.
    Following description was used as a reference:
    https://pmd.github.io/latest/pmd_java_metrics_index.html#non-commenting-source-statements-ncss
    '''

    def value(self, filename: str) -> int:
        metric = 0
        ast = AST.build_from_javalang(build_ast(filename))
        for node in ast.get_proxy_nodes(*NCSSMetric._keyword_node_types,
                                        *NCSSMetric._declarations_node_types,
                                        *NCSSMetric._misc_node_types):
            metric += 1
            if node.node_type == ASTNodeType.IF_STATEMENT:
                metric += self._count_else_statements(node)

        for try_statement in ast.get_proxy_nodes(ASTNodeType.TRY_STATEMENT):
            if self._has_finally_block(try_statement):
                metric += 1

        return metric

    def _count_else_statements(self, if_statement: ASTNode) -> int:
        assert(if_statement.node_type == ASTNodeType.IF_STATEMENT)
        else_statements_qty = 0
        # elif_statement might be:
        # - None, if there is no "else" branch
        # - BLOCK_STATEMENT, if there is "else" branch
        # - IF_STATEMENT, if there is "elif" branch
        elif_statement = if_statement.else_statement

        # iterating over sequence of "elif" branches
        while elif_statement is not None and elif_statement.node_type == ASTNodeType.IF_STATEMENT:
            else_statements_qty += 1
            elif_statement = elif_statement.else_statement

        # check for the possible "else" branch in the end of "elif" sequence
        if elif_statement is not None:
            else_statements_qty += 1

        return else_statements_qty

    def _has_finally_block(self, try_statement: ASTNode) -> bool:
        assert(try_statement.node_type == ASTNodeType.TRY_STATEMENT)
        return try_statement.finally_block is not None

    # Two keywords "else" and "finally" are not represented by any nodes
    # and have to be extracted manually from fields
    # of IF_STATEMENT and TRY_STATEMENT respectively
    _keyword_node_types = {
        ASTNodeType.ASSERT_STATEMENT,
        ASTNodeType.BREAK_STATEMENT,
        ASTNodeType.CATCH_CLAUSE,
        ASTNodeType.CONTINUE_STATEMENT,
        ASTNodeType.DO_STATEMENT,
        ASTNodeType.FOR_STATEMENT,
        ASTNodeType.IF_STATEMENT,
        ASTNodeType.RETURN_STATEMENT,
        ASTNodeType.SWITCH_STATEMENT_CASE,
        ASTNodeType.SWITCH_STATEMENT,
        ASTNodeType.SYNCHRONIZED_STATEMENT,
        ASTNodeType.THROW_STATEMENT,
        ASTNodeType.WHILE_STATEMENT,
    }

    # There are two type of declarations: type declarations (annotation, class etc.)
    # and class parts declarations (fields, methods etc.)
    # Package declarations are out of our interest, because it makes harder to compare
    # nested and outer classes.
    _declarations_node_types = {
        ASTNodeType.ANNOTATION_DECLARATION,
        ASTNodeType.CLASS_DECLARATION,
        ASTNodeType.CONSTANT_DECLARATION,
        ASTNodeType.CONSTRUCTOR_DECLARATION,
        ASTNodeType.ENUM_CONSTANT_DECLARATION,
        ASTNodeType.ENUM_DECLARATION,
        ASTNodeType.FIELD_DECLARATION,
        ASTNodeType.INTERFACE_DECLARATION,
        ASTNodeType.METHOD_DECLARATION,
        ASTNodeType.TYPE_DECLARATION,
    }

    _misc_node_types = {
        # Represent declaration of all local variables
        # *excluding* declarations inside "for" loop control.
        # Those declarations are represented by "VARIABLE_DECLARATION" nodes.
        ASTNodeType.LOCAL_VARIABLE_DECLARATION,
        # Statement expressions also includes assignments
        ASTNodeType.STATEMENT_EXPRESSION,
    }
