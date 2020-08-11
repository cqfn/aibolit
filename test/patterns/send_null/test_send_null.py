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

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.send_null.send_null import SendNull
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class SendNullTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_one_send(self):
        filepath = self.current_directory / "BaseKeyframeAnimation.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [146])

    def test_multi_level_invocation(self):
        filepath = self.current_directory / "Configuration.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(
            lines, [379, 442, 549, 638, 656, 830, 866, 1362, 2393, 2874, 2988, 3080, 3492, 3758, 3855]
        )

    def test_no_null_methods(self):
        filepath = self.current_directory / "FillContent.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple_invocation(self):
        filepath = self.current_directory / "FJIterateTest.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [493])

    def test_more_method_invocations(self):
        filepath = self.current_directory / "SequenceFile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [1097, 1186, 1201, 1217, 3285, 3298, 3367, 3537, 3550])

    def test_constructor_send_null(self):
        filepath = self.current_directory / "Constructor.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5, 14, 15, 16, 17, 18])

    def test_super_in_constructor_with_ternary_operator(self):
        filepath = self.current_directory / "AclPermissionParam.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [46, 50])

    def test_this_with_ternary_operator(self):
        filepath = self.current_directory / "AddOp.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [44, 48])

    def test_super_in_constructor_with_method_inv(self):
        filepath = self.current_directory / "ByteArrayMultipartFileEditor.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [49])
