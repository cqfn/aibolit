# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class NCSSMetric:
    """
    NCSS metric counts non-commenting source statements.

    It counts:
    - keywords from _keyword_node_types
    - declarations from _declarations_node_types
    - local variable declarations and statement expressions
    """

    def value(self, ast: AST) -> int:
        metric = 0
        for node in ast.get_proxy_nodes(
            *NCSSMetric._keyword_node_types,
            *NCSSMetric._declarations_node_types,
            *NCSSMetric._misc_node_types
        ):
            metric += 1

            if node.node_type == ASTNodeType.IF_STATEMENT and self._has_pure_else_statements(node):
                metric += 1
            elif node.node_type == ASTNodeType.TRY_STATEMENT and self._has_finally_block(node):
                metric += 1

        return metric

    def _has_pure_else_statements(self, if_statement: ASTNode) -> bool:
        '''
        Checks is there else branch.
        If else branch appeared to be "else if" construction (not pure "else"),
        returns False.
        '''
        assert if_statement.node_type == ASTNodeType.IF_STATEMENT
        return if_statement.else_statement is not None and \
            if_statement.else_statement.node_type != ASTNodeType.IF_STATEMENT

    def _has_finally_block(self, try_statement: ASTNode) -> bool:
        assert try_statement.node_type == ASTNodeType.TRY_STATEMENT
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
        ASTNodeType.TRY_STATEMENT,
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
