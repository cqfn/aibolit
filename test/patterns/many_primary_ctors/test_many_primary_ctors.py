import os
from pathlib import Path
from unittest import TestCase

from aibolit.patterns.many_primary_ctors.many_primary_ctors import ManyPrimaryCtors


class TestManyPrimaryCtors(TestCase):
    cur_file_dir = Path(os.path.realpath(__file__)).parent

    def test_many_primary_ctors(self):
        file = Path(self.cur_file_dir, 'Book.java')

        self.assertEqual(ManyPrimaryCtors().value(file), [4, 8])
