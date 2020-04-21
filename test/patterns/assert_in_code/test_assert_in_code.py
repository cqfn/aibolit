import os.path
from pathlib import Path
from unittest import TestCase

from aibolit.patterns.assert_in_code.assert_in_code import AssertInCode


class TestAssertInCode(TestCase):
    cur_file_dir = Path(os.path.realpath(__file__)).parent

    def test_assert_in_code(self):
        file = Path(self.cur_file_dir, 'Book.java')
        self.assertEqual(AssertInCode().value(file), [3])
