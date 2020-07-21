import os
from unittest import TestCase
from aibolit.patterns.null_check.null_check import NullCheck
from pathlib import Path


class TestNullCheck(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    class_to_test = NullCheck()

    def test_null_check(self):
        lines = self.class_to_test.value(Path(self.dir_path, '1.java'))
        self.assertEqual(lines, [4])

    def test_null_check_in_constructor(self):
        lines = self.class_to_test.value(Path(self.dir_path, '2.java'))
        self.assertEqual(lines, [])

    def test_null_check_comparison_result_assignment(self):
        lines = self.class_to_test.value(Path(self.dir_path, '3.java'))
        self.assertEqual(lines, [4])

    def test_null_check_ternary(self):
        lines = self.class_to_test.value(Path(self.dir_path, '4.java'))
        self.assertEqual(lines, [4])

    def test_null_check_not_equal_comparison(self):
        lines = self.class_to_test.value(Path(self.dir_path, '5.java'))
        self.assertEqual(lines, [4])
