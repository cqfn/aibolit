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

import os
from unittest import TestCase
from aibolit.patterns.var_middle.var_middle import VarMiddle


class VarMiddleTest(TestCase):
    def test_good_class(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/1.java')
        self.assertEqual(lines, [])

    def test_bad_class(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/2.java')
        self.assertEqual(lines, [9, 16])

    def test_case_with_multiline_method_declaration(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/3.java')
        self.assertEqual(lines, [])

    def test_case_with_empty_lines(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/4.java')
        self.assertEqual(lines, [])

    def test_case_autoclosable(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/5.java')
        self.assertEqual(lines, [])

    def test_case_nested_class(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/6.java')
        self.assertEqual(lines, [30, 33])

    def test_declaration_after_super_class_method_call(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/7.java')
        self.assertEqual(lines, [14])

    def test_for_scope_good(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/8.java')
        self.assertEqual(lines, [])

    def test_for_scope_bad(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/9.java')
        self.assertEqual(lines, [11])

    def test_variable_declared_after_for(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/10.java')
        self.assertEqual(lines, [11])

    def test_11(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/11.java')
        self.assertEqual(lines, [])

    def test_catch_good(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/12.java')
        self.assertEqual(lines, [])

    def test_catch_bad(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/13.java')
        self.assertEqual(lines, [38])

    def test_else_bad(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/14.java')
        self.assertEqual(lines, [88])

    def test_variable_after_curly_braces(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/15.java')
        self.assertEqual(lines, [])

    def test_variable_inside_lambda(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/16.java')
        self.assertEqual(lines, [])

    def test_annotation_with_parameters(self):
        pattern = VarMiddle()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/17.java')
        self.assertEqual(lines, [22])
