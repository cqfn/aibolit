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

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.utils.ast_builder import build_ast
from aibolit.extract_method_baseline.extract_semantic import (
    extract_method_statements_semantic,
    StatementSemantic,
)


def variables_semantic(*variables_names: str) -> StatementSemantic:
    return StatementSemantic(used_variables=set(variables_names))


class PaperExampleTestCase(TestCase):
    def test_semantic_extraction(self):
        semantic = extract_method_statements_semantic(self.method_ast)
        for comparison_index, (statement, actual_semantic, expected_semantic) in enumerate(
            zip_longest(semantic.keys(), semantic.values(), self.method_semantic)
        ):
            self.assertEqual(
                actual_semantic,
                expected_semantic,
                f"Failed on {statement.node_type} statement on line {statement.line}. "
                f"Comparison index is {comparison_index}.",
            )

    @classmethod
    def setUpClass(cls):
        current_directory = Path(__file__).absolute().parent
        filepath = current_directory / "ExampleFromPaper.java"

        ast = AST.build_from_javalang(build_ast(filepath))
        try:
            class_declaration = next(
                node
                for node in ast.get_root().types
                if node.node_type == ASTNodeType.CLASS_DECLARATION and node.name == "ExampleFromPaper"
            )

            method_declaration = next(
                node for node in class_declaration.methods if node.name == "grabManifests"
            )
        except StopIteration as e:
            raise RuntimeError(
                f"Failed to find method grabManifests in class ExampleFromPaper in file {filepath}."
            ) from e

        cls.method_ast = ast.get_subtree(method_declaration)

    method_semantic = [
        StatementSemantic(used_variables={"manifests", "length"}, used_objects={"rcs"}),
        StatementSemantic(used_variables={"i", "length"}, used_objects={"rcs"}),
        variables_semantic("rec"),
        variables_semantic("i", "rcs"),
        StatementSemantic(used_variables={"rec", "rcs", "i"}, used_methods={"grabRes"}),
        StatementSemantic(used_variables={"rec", "rcs", "i"}, used_methods={"grabNonFileSetRes"}),
        variables_semantic("rec", "j", "length"),
        StatementSemantic(used_variables={"name", "rec", "j"}, used_methods={"getName", "replace"}),
        variables_semantic("rcs", "i"),
        variables_semantic("afs", "rcs", "i"),
        StatementSemantic(used_objects={"afs"}, used_methods={"equals", "getFullpath", "getProj"}),
        StatementSemantic(used_objects={"name.afs"}, used_methods={"getFullpath", "getProj"}),
        StatementSemantic(used_objects={"afs"}, used_methods={"equals", "getPref", "getProj"}),
        StatementSemantic(used_variables={"pr"}, used_objects={"afs"}, used_methods={"getPref", "getProj"}),
        StatementSemantic(used_objects={"pr"}, used_methods={"endsWith"}),
        variables_semantic("pr"),
        variables_semantic("pr", "name"),
        StatementSemantic(
            used_variables={"MANIFEST_NAME"}, used_objects={"name"}, used_methods={"equalsIgnoreCase"}
        ),
        variables_semantic("manifests", "i", "rec", "j"),
        variables_semantic("manifests", "i"),
        variables_semantic("manifests", "i"),
        variables_semantic("manifests"),
    ]
