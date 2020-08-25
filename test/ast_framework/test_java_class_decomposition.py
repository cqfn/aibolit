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
from concurrent.futures.thread import ThreadPoolExecutor
from unittest import TestCase
from pathlib import Path

<<<<<<< HEAD
=======
from aibolit.__main__ import flatten
>>>>>>> master
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.java_class_decomposition import decompose_java_class
from aibolit.utils.ast_builder import build_ast
from aibolit.metrics.ncss.ncss import NCSSMetric


class JavaClassDecompositionTestSuite(TestCase):
    cur_dir = Path(__file__).absolute().parent

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

        def count_css(file):
            ast = AST.build_from_javalang(build_ast(str(file)))
            classes_ast = [
                ast.get_subtree(node)
                for node in ast.get_root().types
                if node.node_type == ASTNodeType.CLASS_DECLARATION
            ]
            ncss_sum = 0
            ncss_metric = NCSSMetric()
            for class_ast in classes_ast:
                for component in decompose_java_class(class_ast, 'strong'):
                    ncss = ncss_metric.value(ast=component)
                    ncss_sum += ncss

            ncss_for_class = ncss_metric.value(ast=ast)
            print(file, ncss_for_class, ncss_sum)
            # self.assertEqual(ncss_sum, ncss_for_class)

        folder = Path(__file__).parent.absolute() / "ncss"

        with ThreadPoolExecutor(max_workers=5) as executor:
            result = executor.map(count_css, folder.glob("*.java"))

    def __decompose_with_setter_functionality(self, ignore_getters=False, ignore_setters=False):
        file = str(Path(self.cur_dir, 'LottieImageAsset.java'))
        ast = AST.build_from_javalang(build_ast(file))
        classes_ast = [
            ast.get_subtree(node)
            for node in ast.get_root().types
            if node.node_type == ASTNodeType.CLASS_DECLARATION
        ]
        components = list(decompose_java_class(
            classes_ast[0],
            "strong",
            ignore_setters=ignore_setters,
            ignore_getters=ignore_getters))
        function_names = flatten([
            [x.name for x in list(c.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION))]
            for c in components])
        return function_names

    def test_ignore_setters(self):
        function_names = self.__decompose_with_setter_functionality(ignore_setters=True)
        self.assertTrue('setSomething' not in function_names)
        self.assertTrue('setBitmap' not in function_names)

    def test_do_not_ignore_setters(self):
        function_names = self.__decompose_with_setter_functionality(ignore_setters=False)
        self.assertTrue('setSomething' in function_names)
        self.assertTrue('setBitmap' in function_names)

    def test_ignore_getters(self):
        function_names = self.__decompose_with_setter_functionality(ignore_getters=True)
        self.assertTrue('getWidth' not in function_names)

    def test_do_not_ignore_getters(self):
        function_names = self.__decompose_with_setter_functionality(ignore_getters=False)
        self.assertTrue('getWidth' in function_names)
