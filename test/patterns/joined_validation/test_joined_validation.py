
import os
from unittest import TestCase
from aibolit.patterns.joined_validation.joined_validation import JoinedValidation
from pathlib import Path


class TestJoinedValidation(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_simple(self):
        self.assertEqual([9], JoinedValidation(Path(self.dir_path, 'JoinedValidation.java')).value())
