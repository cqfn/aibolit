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
from aibolit.patterns.redundant_catch.redundant_catch import RedundantCatch


class RedundantCatchTest(TestCase):

    def test_simple(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/Simple.java')
        self.assertEqual(lines, [3])

    def test_both_catches(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/BothCatches.java')
        self.assertEqual(lines, [3])

    def test_fake(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/TrickyFake.java')
        self.assertEqual(lines, [])

    def test_try_inside_anonymous(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/TryInsideAnonymous.java')
        self.assertEqual(lines, [6, 14])

    def test_multiple_catch(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/MultipleCatch.java')
        self.assertEqual(lines, [3])

    def test_sequential_catch(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/SequentialCatch.java')
        self.assertEqual(lines, [3])

    def test_sequential_catch_try(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/SequentialCatchTry.java')
        self.assertEqual(lines, [3, 10])

    def test_try_inside_catch(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/TryInsideCatch.java')
        self.assertEqual(lines, [7])

    def test_try_inside_finally(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/TryInsideFinally.java')
        self.assertEqual(lines, [8])

    def test_try_inside_try(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/TryInsideTry.java')
        self.assertEqual(lines, [5])

    def test_catch_with_functions(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/CatchWithFunctions.java')
        self.assertEqual(lines, [6])

    def test_catch_with_similar_name(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/NotThrow.java')
        self.assertEqual(lines, [256])

    def test_try_without_throws(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/ExcelReader.java')
        self.assertEqual(lines, [])

    def test_try_in_constructor(self):
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/ExcelAnalyserImpl.java')
        self.assertEqual(lines, [43])

    def test_fake_try_in_lambda(self):
        """
        If function has throws, the pattern shouldn't be recognized
        if the same exception is caught in anonymous lambda
        """
        pattern = RedundantCatch()
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + '/Cache.java')
        self.assertEqual(lines, [])
