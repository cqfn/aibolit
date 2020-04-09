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
from aibolit.patterns.empty_rethrow.empty_rethrow import EmptyRethrow
from pathlib import Path


class TestEmptyRethrow(TestCase):
    cur_file_dir = Path(os.path.realpath(__file__)).parent
    testClass = EmptyRethrow()

    def test_empty(self):
        file = str(Path(self.cur_file_dir, 'Empty.java'))
        self.assertEqual(self.testClass.value(file), [])

    def test_anonymous(self):
        file = str(Path(self.cur_file_dir, 'Anonymous.java'))
        self.assertEqual(self.testClass.value(file), [19, 25])

    def test_both_catches(self):
        file = str(Path(self.cur_file_dir, 'BothCatches.java'))
        self.assertEqual(self.testClass.value(file), [6, 8])

    def test_instance_different_methods(self):
        file = str(Path(self.cur_file_dir, 'MultipleCatch.java'))
        self.assertEqual(self.testClass.value(file), [6])

    def test_sequential_catch(self):
        file = str(Path(self.cur_file_dir, 'SequentialCatch.java'))
        self.assertEqual(self.testClass.value(file), [6, 8])

    def test_sequential_catch_try(self):
        file = str(Path(self.cur_file_dir, 'SequentialCatchTry.java'))
        self.assertEqual(self.testClass.value(file), [6, 8, 13, 15])

    def test_simple(self):
        file = str(Path(self.cur_file_dir, 'Simple.java'))
        self.assertEqual(self.testClass.value(file), [6])

    def test_tricky_fake(self):
        file = str(Path(self.cur_file_dir, 'TrickyFake.java'))
        self.assertEqual(self.testClass.value(file), [])

    def test_try_inside_catch(self):
        file = str(Path(self.cur_file_dir, 'TryInsideCatch.java'))
        self.assertEqual(self.testClass.value(file), [10])

    def test_try_inside_finally(self):
        file = str(Path(self.cur_file_dir, 'TryInsideFinally.java'))
        self.assertEqual(self.testClass.value(file), [6, 12])

    def test_try_inside_try(self):
        file = str(Path(self.cur_file_dir, 'TryInsideTry.java'))
        self.assertEqual(self.testClass.value(file), [10, 17])

    def test_catch_with_functions(self):
        file = str(Path(self.cur_file_dir, 'CatchWithFunctions.java'))
        self.assertEqual(self.testClass.value(file), [13])

    def test_catch_with_if(self):
        file = str(Path(self.cur_file_dir, 'CatchWithIf.java'))
        self.assertEqual(self.testClass.value(file), [14])

    def test_chained_exceptions(self):
        file = str(Path(self.cur_file_dir, 'DataBaseNavigator.java'))
        file2 = str(Path(self.cur_file_dir, 'ConfigImportWizardPageDbvis.java'))
        file3 = str(Path(self.cur_file_dir, 'DatabaseNavigatorSourceContainer.java'))
        self.assertEqual(self.testClass.value(file), [])
        self.assertEqual(self.testClass.value(file2), [])
        self.assertEqual(self.testClass.value(file3), [])

    def test_try_without_catch(self):
        file = str(Path(self.cur_file_dir, 'ConcurrentDiskUtil.java'))
        self.assertEqual(self.testClass.value(file), [])

    def test_throw_with_cast(self):
        file = str(Path(self.cur_file_dir, 'CommonRdbmsReader.java'))
        self.assertEqual(self.testClass.value(file), [])
