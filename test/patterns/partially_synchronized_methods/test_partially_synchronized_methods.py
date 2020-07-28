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

from unittest import TestCase
from pathlib import Path
from typing import List

from aibolit.patterns.partially_synchronized_methods.partially_synchronized_methods import (
    PartiallySynchronizedMethods,
)


class PartiallySynchronizedMethodsTestSuite(TestCase):
    def test_no_synchonization(self):
        self._test_helper("NoSynchronization.java", [])

    def test_partial_synchonization(self):
        self._test_helper("PartialSynchronization.java", [5, 13, 23])

    def test_full_synchonization(self):
        self._test_helper("FullSynchronization.java", [])

    def test_several_synchronization_statements(self):
        self._test_helper("SeveralSynchronizationStatements.java", [6, 10, 26, 29])

    def test_synchronization_in_nested_scopes(self):
        self._test_helper("SynchronizationInNestedScopes.java", [9, 18, 27])

    def _test_helper(self, filename: str, lines: List[int]):
        filepath = str(Path(__file__).absolute().parent / filename)
        pattern = PartiallySynchronizedMethods()
        self.assertEqual(pattern.value(filepath), lines)
