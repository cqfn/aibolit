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
from aibolit.patterns.partial_synchronized.partial_synchronized import PartialSync


class VarMiddleTest(TestCase):

    def test_simple(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/Simple.java')
        self.assertEqual(lines, [22])

    def test_sync_with_array(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/ArrayIndex.java')
        self.assertEqual(lines, [89])

    def test_sync_with_method_chaining(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/Chain.java')
        self.assertEqual(lines, [183])

    def test_sync_with_class_field(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/FieldClass.java')
        self.assertEqual(lines, [154])

    def test_sync_with_func_call(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/FuncCall.java')
        self.assertEqual(lines, [45])

    def test_sync_with_large_file(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/Large.java')
        self.assertEqual(lines, [1359, 1546, 1584, 1606, 1628, 3347])

    def test_nested_sync(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/NestedSync.java')
        self.assertEqual(lines, [22, 24])

    def test_sync_with_class_this(self):
        """ Handles the case
        # synchronized(AsyncCallHandler.this)
        # {
        #     AsyncCallHandler.this.wait(waitTime);
        # }
        """
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/Object.This.java')
        self.assertEqual(lines, [161])

    def test_sync_sequential(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/SeveralCases.java')
        self.assertEqual(lines, [85, 91, 98])

    def test_sync_in_different_functions(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/SeveralFunctions.java')
        self.assertEqual(lines, [22, 38, 40])

    def test_sync_with_statements_after_it(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/SimpleThisAfter.java')
        self.assertEqual(lines, [22, 24])

    def test_sync_with_statements_before_it(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/SimpleThisBefore.java')
        self.assertEqual(lines, [23, 25])

    def test_sync_with_empty_lines_after_it(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/SimpleThisEmptyLineAfter.java')
        self.assertEqual(lines, [])

    def test_sync_with_empty_lines_before_it(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/SimpleThisEmptyLineBefore.java')
        self.assertEqual(lines, [])

    def test_sync_with_static_class(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/SyncStaticClass.java')
        self.assertEqual(lines, [52])

    def test_sync_with_nested_if_and_for(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/WIthIf.java')
        self.assertEqual(lines, [85])

    def test_sync_with_func_ref(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/SyncWithFunc.java')
        self.assertEqual(lines, [228])

    def test_ctor(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/Constructor.java')
        self.assertEqual(lines, [412])

    def test_lambda(self):
        pattern = PartialSync()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/Lambda.java')
        self.assertEqual(lines, [28])
