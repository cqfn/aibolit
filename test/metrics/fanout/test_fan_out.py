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
    def test_count_types_in_fields(self):
        ast = FanOutTestSuite._build_ast('CountTypesInFields.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 3)

    def test_type_used_several_times(self):
        ast = FanOutTestSuite._build_ast('TypeUsedSeveralTimes.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 1)

    def test_self_usage(self):
        ast = FanOutTestSuite._build_ast('SelfUsage.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 0)

    def test_class_referenced_from_package(self):
        ast = FanOutTestSuite._build_ast('ClassReferencedFromPackage.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 2)

    def test_extending_type(self):
        ast = FanOutTestSuite._build_ast('ExtendingType.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 1)

    def test_generic_type(self):
        ast = FanOutTestSuite._build_ast('GenericType.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 1)

    def test_generic_and_packaged_types(self):
        ast = FanOutTestSuite._build_ast('GenericAndPackagedTypes.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 2)

    @staticmethod
    def _build_ast(filename: str) -> AST:
        path = Path(__file__).absolute().parent / filename
        return AST.build_from_javalang(build_ast(str(path)))
