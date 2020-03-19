import os
from pathlib import Path
from unittest import TestCase

from aibolit.patterns.null_check.null_check import NullCheck


class TestNullCheck(TestCase):
    cur_file_dir = Path(os.path.realpath(__file__)).parent
    testClass = NullCheck()

    def test_null_check(self):
        file = Path(self.cur_file_dir, 'NullCheck.java')

        self.assertEqual(len(self.testClass.value(file)), 1)

    def test_null_check_in_constructor(self):
        file = Path(self.cur_file_dir, 'NullCheckInConstructor.java')

        self.assertEqual(len(self.testClass.value(file)), 0)
