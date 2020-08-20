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
from typing import List
from unittest import TestCase
from pathlib import Path

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.java_class_decomposition import decompose_java_class
from aibolit.utils.ast_builder import build_ast
from aibolit.metrics.ncss.ncss import NCSSMetric

class JavaClassDecompositionTestSuite(TestCase):
    def test_strong_decomposition(self):
        class_ast = self._get_class_ast(
            "MethodUseOtherMethodExample.java", "MethodUseOtherMethod"
        )
        class_components = decompose_java_class(class_ast, "strong")
        self.assertEqual(len(class_components), 7)

    def test_weak_decomposition(self):
        class_ast = self._get_class_ast(
            "MethodUseOtherMethodExample.java", "MethodUseOtherMethod"
        )
        class_components = decompose_java_class(class_ast, "weak")
        self.assertEqual(len(class_components), 5)

    def _get_class_ast(self, filename: str, class_name: str) -> AST:
        package_ast = AST.build_from_javalang(
            build_ast(Path(__file__).parent.absolute() / filename)
        )
        package_declaration = package_ast.get_root()
        try:
            class_declaration = next(
                class_declaration
                for class_declaration in package_declaration.types
                if class_declaration.name == class_name
            )
            return package_ast.get_subtree(class_declaration)

        except StopIteration:
            raise ValueError(
                f"File '{filename}' does not have top level class '{class_name}'."
            )

    def test_ncss(self):
        filename = Path(__file__).parent.absolute() / 'Configuration.java'
        ast = AST.build_from_javalang(build_ast(filename))
        classes_ast = [
            ast.get_subtree(node)
            for node in ast.get_root().types
            if node.node_type == ASTNodeType.CLASS_DECLARATION
        ]
        print(len(classes_ast))
        ncss_sum = 0
        ncss_metric = NCSSMetric()
        for class_ast in classes_ast:
            for component in decompose_java_class(class_ast, 'strong'):
                ncss = ncss_metric.value(ast=component)
                ncss_sum += ncss

        ncss_for_class = ncss_metric.value(ast=ast)
        self.assertEqual(ncss_sum, ncss_for_class)

