# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from unittest import TestCase
from pathlib import Path
from typing import List, Iterator

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.scope import Scope
from aibolit.utils.ast_builder import build_ast

StatementsTypes = List[ASTNodeType]


class ScopeTestCase(TestCase):
    def test_plain_method(self) -> None:
        self._test_method("plain_method")

    def test_lambda_in_assert(self) -> None:
        self._test_method("lambda_in_assert")

    def test_nested_blocks(self) -> None:
        self._test_method("nested_blocks")

    def test_while_cycle(self) -> None:
        self._test_method("while_cycle")

    def test_for_cycle(self) -> None:
        self._test_method("for_cycle")

    def test_if_branching(self) -> None:
        self._test_method("if_branching")

    def test_local_variables(self) -> None:
        self._test_method("local_variables")

    def test_statements_with_expressions(self) -> None:
        self._test_method("statements_with_expressions")

    def test_switch_branching(self) -> None:
        self._test_method("switch_branching")

    def test_synchronized_block(self) -> None:
        self._test_method("synchronized_block")

    def test_try_statement(self) -> None:
        self._test_method("try_statement")

    def test_multiline_lambda(self) -> None:
        self._test_method("multiline_lambda")

    def test_deep_nesting(self) -> None:
        self._test_method("deep_nesting")

    def test_lambda_parameters(self) -> None:
        scope = Scope.build_from_method_ast(self._get_method_ast("multiline_lambda"))
        lambda_scope = next(scope.nested_scopes)

        self.assertEqual(lambda_scope.parent_node.node_type, ASTNodeType.LAMBDA_EXPRESSION)
        self.assertEqual([parameter.name for parameter in lambda_scope.parameters], ["x", "y"])

    def _test_method(self, method_name: str) -> None:
        scope = Scope.build_from_method_ast(self._get_method_ast(method_name))
        self.assertScope(scope, self._scope_statements_in_preorder_by_method[method_name])

    def assertScope(
        self, scope: Scope, statements_by_scope_in_preorder: List[StatementsTypes]
    ) -> None:
        scope_preorder_index = 0
        self.assertStatements(scope, statements_by_scope_in_preorder[scope_preorder_index])

        scope_stack: List[Iterator[Scope]] = [scope.nested_scopes]
        while len(scope_stack) > 0:
            try:
                scope = next(scope_stack[-1])
                scope_preorder_index += 1
                self.assertStatements(scope, statements_by_scope_in_preorder[scope_preorder_index])
                scope_stack.append(scope.nested_scopes)
            except StopIteration:
                scope_stack.pop()

        self.assertEqual(scope_preorder_index + 1, len(statements_by_scope_in_preorder))

    def assertStatements(self, scope: Scope, statements: StatementsTypes) -> None:
        self.assertEqual([statement.node_type for statement in scope.statements], statements)

    def _get_method_ast(self, method_name) -> AST:
        path = str(Path(__file__).absolute().parent / "ScopeTest.java")
        ast = AST.build_from_javalang(build_ast(path))
        package_declaration = ast.get_root()

        assert len(package_declaration.types) == 1 and \
            package_declaration.types[0].node_type == ASTNodeType.CLASS_DECLARATION

        class_declaration = package_declaration.types[0]

        try:
            return next(
                ast.get_subtree(method_declaration)
                for method_declaration in class_declaration.methods
                if method_declaration.name == method_name
            )
        except StopIteration:
            raise ValueError(f"There is no method {method_name} in class {class_declaration.name}")

    _scope_statements_in_preorder_by_method = {
        "plain_method": [
            [ASTNodeType.LOCAL_VARIABLE_DECLARATION, ASTNodeType.LOCAL_VARIABLE_DECLARATION]
        ],
        "lambda_in_assert": [
            [ASTNodeType.LOCAL_VARIABLE_DECLARATION, ASTNodeType.ASSERT_STATEMENT],
            [ASTNodeType.BINARY_OPERATION],
        ],
        "nested_blocks": [
            [ASTNodeType.LOCAL_VARIABLE_DECLARATION, ASTNodeType.BLOCK_STATEMENT],
            [ASTNodeType.LOCAL_VARIABLE_DECLARATION],
        ],
        "while_cycle": [
            [
                ASTNodeType.LOCAL_VARIABLE_DECLARATION,
                ASTNodeType.DO_STATEMENT,
                ASTNodeType.WHILE_STATEMENT,
                ASTNodeType.WHILE_STATEMENT,
                ASTNodeType.WHILE_STATEMENT,
            ],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.BINARY_OPERATION],
            [ASTNodeType.STATEMENT_EXPRESSION],
        ],
        "for_cycle": [
            [
                ASTNodeType.LOCAL_VARIABLE_DECLARATION,
                ASTNodeType.FOR_STATEMENT,
                ASTNodeType.FOR_STATEMENT,
                ASTNodeType.LOCAL_VARIABLE_DECLARATION,
                ASTNodeType.FOR_STATEMENT,
                ASTNodeType.FOR_STATEMENT,
                ASTNodeType.FOR_STATEMENT,
            ],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.BINARY_OPERATION],
            [ASTNodeType.STATEMENT_EXPRESSION],
        ],
        "if_branching": [
            [
                ASTNodeType.LOCAL_VARIABLE_DECLARATION,
                ASTNodeType.IF_STATEMENT,
                ASTNodeType.IF_STATEMENT,
                ASTNodeType.IF_STATEMENT,
                ASTNodeType.IF_STATEMENT,
                ASTNodeType.IF_STATEMENT,
                ASTNodeType.IF_STATEMENT,
            ],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.BINARY_OPERATION],
            [ASTNodeType.STATEMENT_EXPRESSION],
        ],
        "local_variables": [
            [
                ASTNodeType.LOCAL_VARIABLE_DECLARATION,
                ASTNodeType.LOCAL_VARIABLE_DECLARATION,
                ASTNodeType.LOCAL_VARIABLE_DECLARATION,
            ],
            [ASTNodeType.BINARY_OPERATION],
            [ASTNodeType.BINARY_OPERATION],
        ],
        "statements_with_expressions": [
            [
                ASTNodeType.LOCAL_VARIABLE_DECLARATION,
                ASTNodeType.STATEMENT_EXPRESSION,
                ASTNodeType.THROW_STATEMENT,
                ASTNodeType.RETURN_STATEMENT,
            ],
            [ASTNodeType.BINARY_OPERATION],
            [ASTNodeType.MEMBER_REFERENCE],
            [ASTNodeType.BINARY_OPERATION],
        ],
        "switch_branching": [
            [
                ASTNodeType.LOCAL_VARIABLE_DECLARATION,
                ASTNodeType.SWITCH_STATEMENT,
                ASTNodeType.SWITCH_STATEMENT,
            ],
            [
                ASTNodeType.STATEMENT_EXPRESSION,
                ASTNodeType.STATEMENT_EXPRESSION,
                ASTNodeType.STATEMENT_EXPRESSION,
            ],
            [ASTNodeType.BINARY_OPERATION],
            [ASTNodeType.STATEMENT_EXPRESSION],
        ],
        "synchronized_block": [
            [
                ASTNodeType.LOCAL_VARIABLE_DECLARATION,
                ASTNodeType.SYNCHRONIZED_STATEMENT,
                ASTNodeType.SYNCHRONIZED_STATEMENT,
            ],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.CLASS_CREATOR],
            [ASTNodeType.STATEMENT_EXPRESSION],
        ],
        "try_statement": [
            [ASTNodeType.TRY_STATEMENT],
            [ASTNodeType.MEMBER_REFERENCE],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION],
        ],
        "multiline_lambda": [
            [ASTNodeType.LOCAL_VARIABLE_DECLARATION, ASTNodeType.STATEMENT_EXPRESSION],
            [ASTNodeType.STATEMENT_EXPRESSION, ASTNodeType.RETURN_STATEMENT],
        ],
        "deep_nesting": [
            [ASTNodeType.FOR_STATEMENT],
            [ASTNodeType.IF_STATEMENT],
            [ASTNodeType.ASSERT_STATEMENT],
            [ASTNodeType.BINARY_OPERATION],
        ],
    }
