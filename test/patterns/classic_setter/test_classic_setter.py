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

from aibolit.patterns.classic_setter.classic_setter import ClassicSetter
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class SetterTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_one_valid_patterns(self):
        filepath = self.current_directory / "BaseKeyframeAnimation.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicSetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [40])

    def test_four_setter_patterns(self):
        filepath = self.current_directory / "Configuration.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicSetter()
        lines = pattern.value(ast)
        self.assertEqual(lines,
                         [902, 906, 1236, 1240, 1361, 1539, 1612, 1641, 1670,
                          1703, 1712, 1723, 1801, 1970, 2020, 2336,
                          2507, 3783, 3819])

    def test_another_setter_patterns(self):
        filepath = self.current_directory / "SequenceFile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicSetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [259, 744, 2849, 2855, 2861, 3127])
