
import os
from unittest import TestCase
from aibolit.patterns.public_static_method.public_static_method import PublicStaticMethod
from pathlib import Path


class TestNonFinalAttribute(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_find_non_final_atributes(self):
        lines = PublicStaticMethod().value(Path(self.dir_path, 'PublicStaticMethod.java'))
        self.assertEqual(1, len(lines))
