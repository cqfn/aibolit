import os
from unittest import TestCase
from pathlib import Path
from aibolit.patterns.array_as_argument.array_as_argument import ArrayAsArgument


class TestArrayAsArgument(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_array_as_argument(self):
        self.assertEqual([6, 10], ArrayAsArgument(Path(self.dir_path, 'ArrayAsArgument.java')).value())
