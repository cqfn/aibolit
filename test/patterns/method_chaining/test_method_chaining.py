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
from aibolit.patterns.method_chaining.method_chaining import MethodChainFind
from pathlib import Path


class TestMethodChain(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    method_chain_finder = MethodChainFind()

    def test_method_chain(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChain.java'))
        self.assertEqual(lines, [21])

    def test_empty_method_chain(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'EmptyMethodChain.java'))
        self.assertEqual(lines, [21])

    def test_chain_with_new_object(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChainNewObjectMethods.java'))
        self.assertEqual(lines, [23, 34])

    def test_method_chain_in_different_methods(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChainInDifferentMethods.java'))
        self.assertEqual(lines, [22, 34])

    def test_chain_in_nested_class(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChainNestedClass.java'))
        self.assertEqual(lines, [19])

    def test_chain_in_anonymous_class(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChainAnonymousClass.java'))
        self.assertEqual(lines, [29])

    def test_chain_in_anonymous_class_empty(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChainAnonymousClassEmpty.java'))
        self.assertEqual(lines, [])

    def test_several_chains(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChainSeveral.java'))
        self.assertEqual(lines, [13, 34, 48])

    def test_chain_without_object_creating(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'WithoutObjectCreating.java'))
        self.assertEqual(lines, [14])

    def test_nested_chain_with_this(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'NestedChainWIthThis.java'))
        self.assertEqual(lines, [14, 15])

    def test_nested_chain_with_simple_method_invocation(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'NestedChainWithSimpleMethodInvocation.java'))
        self.assertEqual(lines, [15, 16])

    def test_nested_chain_complicated_structure(self):
        """
        Several nested structures are checked: nested method chaining
        with nested anonymous classes
        """
        lines = self.method_chain_finder.value(Path(self.dir_path, 'HolyMolyNestedChain.java'))
        self.assertEqual(lines, [60, 67, 77])

    def test_smallest_chain(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'SmallestChain.java'))
        self.assertEqual(lines, [31, 83, 84])

    def test_fake_chain(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'FakeChain.java'))
        self.assertEqual(lines, [])

    def test_many_chains(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MachineLearningGetResultsIT.java'))
        self.assertGreater(len(lines), 300)
