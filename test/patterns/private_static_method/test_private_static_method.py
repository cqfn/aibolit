
import os
from unittest import TestCase
from aibolit.patterns.private_static_method.private_static_method import PrivateStaticMethod
from pathlib import Path


class TestPrivateStaticMethod(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_find_non_final_atributes(self):
        lines = PrivateStaticMethod().value(Path(self.dir_path, 'PrivateStaticMethod.java'))
        self.assertEqual(1, len(lines))
