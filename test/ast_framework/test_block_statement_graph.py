from typing import List, Union
from pathlib import Path
from unittest import TestCase

from veniq.ast_framework.block_statement_graph import build_block_statement_graph, Block, Statement
from veniq.ast_framework.block_statement_graph.constants import BlockReason
from veniq.ast_framework import AST, ASTNodeType
from veniq.utils.ast_builder import build_ast


class BlockStatementTestCase(TestCase):
    def test_single_assert_statement(self):
        block_statement_graph = self._get_block_statement_graph("singleAssertStatement")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [ASTNodeType.METHOD_DECLARATION, BlockReason.SINGLE_BLOCK, ASTNodeType.ASSERT_STATEMENT],
        )

    def test_single_return_statement(self):
        block_statement_graph = self._get_block_statement_graph("singleReturnStatement")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [ASTNodeType.METHOD_DECLARATION, BlockReason.SINGLE_BLOCK, ASTNodeType.RETURN_STATEMENT],
        )

    def test_single_statement_expression(self):
        block_statement_graph = self._get_block_statement_graph("singleStatementExpression")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [ASTNodeType.METHOD_DECLARATION, BlockReason.SINGLE_BLOCK, ASTNodeType.STATEMENT_EXPRESSION],
        )

    def test_single_throw_statement(self):
        block_statement_graph = self._get_block_statement_graph("singleThrowStatement")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [ASTNodeType.METHOD_DECLARATION, BlockReason.SINGLE_BLOCK, ASTNodeType.THROW_STATEMENT],
        )

    def test_single_local_variable_declaration(self):
        block_statement_graph = self._get_block_statement_graph("singleVariableDeclarationStatement")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.LOCAL_VARIABLE_DECLARATION,
            ],
        )

    def test_single_block_statement(self):
        block_statement_graph = self._get_block_statement_graph("singleBlockStatement")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.BLOCK_STATEMENT,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.RETURN_STATEMENT,
            ],
        )

    def test_single_do_statement(self):
        block_statement_graph = self._get_block_statement_graph("singleDoStatement")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.DO_STATEMENT,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
            ],
        )

    def test_single_for_statement(self):
        block_statement_graph = self._get_block_statement_graph("singleForStatement")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.FOR_STATEMENT,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
            ],
        )

    def test_single_synchronize_statement(self):
        block_statement_graph = self._get_block_statement_graph("singleSynchronizeStatement")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.SYNCHRONIZED_STATEMENT,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
            ],
        )

    def test_single_while_statement(self):
        block_statement_graph = self._get_block_statement_graph("singleWhileStatement")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.WHILE_STATEMENT,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
            ],
        )

    def test_cycle_with_break(self):
        block_statement_graph = self._get_block_statement_graph("cycleWithBreak")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.WHILE_STATEMENT,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.BREAK_STATEMENT,
            ],
        )

    def test_cycle_with_continue(self):
        block_statement_graph = self._get_block_statement_graph("cycleWithContinue")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.WHILE_STATEMENT,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.CONTINUE_STATEMENT,
            ],
        )

    def test_single_if_then_branch(self):
        block_statement_graph = self._get_block_statement_graph("singleIfThenBranch")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.IF_STATEMENT,
                BlockReason.THEN_BRANCH,
                ASTNodeType.STATEMENT_EXPRESSION,
            ],
        )

    def test_single_if_then_else_branches(self):
        block_statement_graph = self._get_block_statement_graph("singleIfThenElseBranches")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.IF_STATEMENT,
                BlockReason.THEN_BRANCH,
                ASTNodeType.STATEMENT_EXPRESSION,
                BlockReason.ELSE_BRANCH,
                ASTNodeType.STATEMENT_EXPRESSION,
            ],
        )

    def test_several_else_if_branches(self):
        block_statement_graph = self._get_block_statement_graph("severalElseIfBranches")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.IF_STATEMENT,
                BlockReason.THEN_BRANCH,
                ASTNodeType.STATEMENT_EXPRESSION,
                BlockReason.THEN_BRANCH,
                ASTNodeType.STATEMENT_EXPRESSION,
                BlockReason.ELSE_BRANCH,
                ASTNodeType.STATEMENT_EXPRESSION,
            ],
        )

    def test_if_branches_without_curly_braces(self):
        block_statement_graph = self._get_block_statement_graph("ifBranchingWithoutCurlyBraces")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.IF_STATEMENT,
                BlockReason.THEN_BRANCH,
                ASTNodeType.RETURN_STATEMENT,
                BlockReason.ELSE_BRANCH,
                ASTNodeType.RETURN_STATEMENT,
            ],
        )

    def test_switch_branches(self):
        block_statement_graph = self._get_block_statement_graph("switchBranches")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.SWITCH_STATEMENT,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
                ASTNodeType.STATEMENT_EXPRESSION,
                ASTNodeType.BLOCK_STATEMENT,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
                ASTNodeType.STATEMENT_EXPRESSION,
                ASTNodeType.STATEMENT_EXPRESSION,
            ],
        )

    def test_single_try_block(self):
        block_statement_graph = self._get_block_statement_graph("singleTryBlock")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.TRY_STATEMENT,
                BlockReason.TRY_BLOCK,
                ASTNodeType.THROW_STATEMENT,
                BlockReason.CATCH_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
            ],
        )

    def test_full_try_block(self):
        block_statement_graph = self._get_block_statement_graph("fullTryBlock")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.TRY_STATEMENT,
                BlockReason.TRY_RESOURCES,
                ASTNodeType.TRY_RESOURCE,
                BlockReason.TRY_BLOCK,
                ASTNodeType.THROW_STATEMENT,
                BlockReason.CATCH_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
                BlockReason.CATCH_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
                BlockReason.FINALLY_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
            ],
        )

    def test_try_without_catch(self):
        block_statement_graph = self._get_block_statement_graph("tryWithoutCatch")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.TRY_STATEMENT,
                BlockReason.TRY_BLOCK,
                ASTNodeType.THROW_STATEMENT,
                BlockReason.FINALLY_BLOCK,
            ],
        )

    def test_complex_example1(self):
        block_statement_graph = self._get_block_statement_graph("complexExample1")
        self.assertEqual(
            self._flatten_block_statement_graph(block_statement_graph),
            [
                ASTNodeType.METHOD_DECLARATION,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
                ASTNodeType.FOR_STATEMENT,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
                ASTNodeType.WHILE_STATEMENT,
                BlockReason.SINGLE_BLOCK,
                ASTNodeType.STATEMENT_EXPRESSION,
                ASTNodeType.RETURN_STATEMENT,
            ],
        )

    def _get_block_statement_graph(self, method_name: str) -> Block:
        current_directory = Path(__file__).absolute().parent
        filename = "BlockStatementGraphExamples.java"
        ast = AST.build_from_javalang(build_ast(str(current_directory / filename)))

        try:
            class_name = "BlockStatementGraphExamples"
            class_declaration = next(
                node
                for node in ast.get_root().types
                if node.node_type == ASTNodeType.CLASS_DECLARATION and node.name == class_name
            )
        except StopIteration:
            raise RuntimeError(f"Can't find class {class_name} in file {filename}")

        try:
            method_declaration = next(node for node in class_declaration.methods if node.name == method_name)
        except StopIteration:
            raise ValueError(f"Can't find method {method_name} in class {class_name} in file {filename}")

        return build_block_statement_graph(ast.get_subtree(method_declaration))

    @staticmethod
    def _flatten_block_statement_graph(
        root: Union[Block, Statement]
    ) -> List[Union[ASTNodeType, BlockReason]]:
        flattened_graph: List[Union[ASTNodeType, BlockReason]] = []

        def on_node_entering(node: Union[Block, Statement]) -> None:
            if isinstance(node, Block):
                flattened_graph.append(node.reason)
            elif isinstance(node, Statement):
                flattened_graph.append(node.node.node_type)
            else:
                raise ValueError(f"Unknown node {node}")

        root.traverse(on_node_entering)
        return flattened_graph
