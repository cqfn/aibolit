
import os
import unittest
from unittest import TestCase
from aibolit.patterns.non_final_argument.non_final_argument import NonFinalArgument
from pathlib import Path


@unittest.skip('Not implemented')
class TestNonFinalArgument(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_find_non_final_argument_in_ctor(self):
        self.assertEqual(
            NonFinalArgument().value(Path(self.dir_path, 'NonFinalArgumentCtor.java')),
            [7]
        )

    def test_find_non_final_argument_in_method(self):
        self.assertEqual(
            NonFinalArgument().value(Path(self.dir_path, 'NonFinalArgumentMethod.java')),
            [11]
        )
