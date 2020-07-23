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

from aibolit.metrics.fanout.FanOut import FanOut
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class FanOutTestSuite(TestCase):
    def test_1(self):
        ast = FanOutTestSuite._build_ast('1.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 3)

    def test_2(self):
        ast = FanOutTestSuite._build_ast('2.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 1)

    def test_3(self):
        ast = FanOutTestSuite._build_ast('3.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 2)

    def test_4(self):
        ast = FanOutTestSuite._build_ast('4.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 1)

    def test_5(self):
        ast = FanOutTestSuite._build_ast('5.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 1)

    @staticmethod
    def _build_ast(filename: str) -> AST:
        path = Path(__file__).absolute().parent / filename
        return AST.build_from_javalang(build_ast(str(path)))
