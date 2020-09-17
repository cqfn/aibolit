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

from itertools import zip_longest
from pathlib import Path
from unittest import TestCase

from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast
from aibolit.extract_method_baseline.extract_semantic import (
    extract_method_statements_semantic,
    StatementSemantic,
)


def variables_semantic(*variables_names: str) -> StatementSemantic:
    return StatementSemantic(used_variables=set(variables_names))


class ExtractStatementSemanticTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_semantic_extraction(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / "SimpleMethods.java"))
        class_declaration = ast.get_root().types[0]
        assert class_declaration.name == "SimpleMethods", "Wrong java test class"

        for method_declaration in class_declaration.methods:
            with self.subTest(f"Test {method_declaration.name} method."):
                method_semantic = extract_method_statements_semantic(ast.get_subtree(method_declaration))
                items_for_comparison = enumerate(
                    zip_longest(
                        method_semantic.keys(),
                        method_semantic.values(),
                        self.expected_semantic[method_declaration.name],
                    )
                )
                for (
                    comparison_index,
                    (statement, actual_statement_semantic, expected_statement_semantic),
                ) in items_for_comparison:
                    with self.subTest(
                        f"Comparing {comparison_index}th statement {repr(statement)} "
                        f"on line {statement.line} of method {method_declaration.name}."
                    ):
                        self.assertEqual(actual_statement_semantic, expected_statement_semantic)

    expected_semantic = {
        "block": [variables_semantic("x")],
        "forCycle": [variables_semantic("x", "i"), variables_semantic("x", "i", "result")],
        "whileCycle": [variables_semantic("x"), variables_semantic("x")],
        "doWhileCycle": [variables_semantic("x"), variables_semantic("x")],
        "ifBranching": [
            variables_semantic("x"),
            variables_semantic("x"),
            variables_semantic("x"),
            variables_semantic("x"),
            variables_semantic("x"),
        ],
        "synchronizedBlock": [variables_semantic("x"), variables_semantic("x")],
        "switchBranching": [
            variables_semantic("x"),
            variables_semantic("x"),
            variables_semantic("x"),
            variables_semantic("x"),
        ],
        "tryBlock": [
            variables_semantic("x"),
            variables_semantic("x"),
            variables_semantic("x"),
            variables_semantic("x"),
        ],
        "assertStatement": [variables_semantic("x")],
        "returnStatement": [variables_semantic("x")],
        "expression": [variables_semantic("x")],
        "throwStatement": [variables_semantic("x")],
        "localVariableDeclaration": [variables_semantic("x")],
        "breakStatement": [StatementSemantic()],
        "continueStatement": [StatementSemantic()],
        "localMethodCall": [StatementSemantic(used_methods={"localMethod"})],
        "objectMethodCall": [StatementSemantic(used_objects={"o"}, used_methods={"method"})],
        "nestedObject": [StatementSemantic(used_objects={"o"}, used_variables={"x"})],
        "nestedObjectMethodCall": [
            StatementSemantic(used_objects={"o.nestedObject"}, used_methods={"method"})
        ],
        "severalStatements": [
            variables_semantic("x"),
            variables_semantic("x"),
            StatementSemantic(used_objects={"System.out"}, used_methods={"println"}, used_variables={"x"}),
            variables_semantic("x"),
        ],
        "deepNesting": [
            variables_semantic("i"),
            variables_semantic("i"),
            StatementSemantic(used_objects={"System.out"}, used_methods={"println"}, used_variables={"i"}),
            StatementSemantic(used_objects={"System.out"}, used_methods={"println"}),
        ],
        "complexExpressions": [
            variables_semantic("x", "y"),
            variables_semantic("o1", "o2"),
            StatementSemantic(
                used_objects={"o1"}, used_methods={"method", "secondMethod"}, used_variables={"x", "y", "z"}
            ),
            StatementSemantic(
                used_objects={"o1", "o2"},
                used_methods={"method", "thirdMethod", "fourthMethod", "temporalMethod"},
                used_variables={"z"},
            ),
        ],
        "multilineStatement": [variables_semantic("x", "y", "o")],
        "multipleStatementsPerLine": [
            StatementSemantic(used_methods={"localMethod"}, used_variables={"x"}),
            StatementSemantic(used_methods={"localMethod"}, used_variables={"y"}),
        ],
    }
