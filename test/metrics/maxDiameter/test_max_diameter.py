# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from aibolit.metrics.max_diameter.max_diameter import MaxDiameter
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class MaxDiameterTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test1(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / '1.java'))
        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 20)

    def test2(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / '2.java'))
        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 14)

    def test3(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / '3.java'))
        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 7)

    def test4(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / '4.java'))
        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 10)

    def test5(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / '5.java'))
        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 11)

    def test6(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / '6.java'))
        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 8)

    def test_non_utf8_file(self):
        with TemporaryDirectory() as tmpdir:
            filename = Path(tmpdir, 'NonUtf8.java')
            filename.write_bytes(
                b'class NonUtf8 {\n'
                b'    // Byte 0xb6 reproduces the non-UTF8 inputs from issue #280.\n'
                b'    void method() {}\n'
                b'}\n'
            )

            ast = AST.build_from_javalang(build_ast(filename))

        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 3)
