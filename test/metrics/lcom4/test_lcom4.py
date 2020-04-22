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
import unittest
from unittest import TestCase
from pathlib import Path
from aibolit.metrics.lcom4.lcom4 import LCOM4


class TestLCOM4(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    pattern = LCOM4()

    def test_class_with_empty_method(self):
        lcom4_val = self.pattern.value(Path(self.dir_path, 'EmptyMethod.java'))
        self.assertEqual(lcom4_val, 2)

    def test_overloaded(self):
        lcom4_val = self.pattern.value(Path(self.dir_path, 'Overloaded.java'))
        lcom4_val2 = self.pattern.value(Path(self.dir_path, 'OverloadedDiffComp.java'))
        self.assertEqual(lcom4_val, 1)
        self.assertTrue(lcom4_val2, 2)

    def test_constructor(self):
        lcom4_val = self.pattern.value(Path(self.dir_path, 'Constructor.java'))
        self.assertEqual(lcom4_val, 1)

    def test_simple(self):
        lcom4_val = self.pattern.value(Path(self.dir_path, 'Simple.java'))
        # If not possible, change to 1
        self.assertTrue(lcom4_val, 2)

    @unittest.skip("Not implemented")
    def test_getter_setter(self):
        lcom4_val = self.pattern.value(Path(self.dir_path, 'GetterSetter.java'))
        # We should ignore all setters and getters
        self.assertEqual(lcom4_val, 1)

    @unittest.skip("Not implemented")
    def test_scope(self):
        lcom4_val = self.pattern.value(Path(self.dir_path, 'Scope.java'))
        self.assertEqual(lcom4_val, 2)

    @unittest.skip("Not implemented")
    def test_class_with_chain(self):
        lcom4_val = self.pattern.value(Path(self.dir_path, 'MethodChain.java'))
        self.assertEqual(lcom4_val, 3)

    @unittest.skip("Not implemented")
    def test_scope_with_anonymous(self):
        lcom4_val = self.pattern.value(Path(self.dir_path, 'ScopeAnonymous.java'))
        self.assertEqual(lcom4_val, 2)
