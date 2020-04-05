
import os
from unittest import TestCase
from aibolit.patterns.private_static_method.private_static_method import PrivateStaticMethod
from pathlib import Path


class TestPrivateStaticMethod(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_find_private_static_methods(self):
        lines = PrivateStaticMethod().value(Path(self.dir_path, 'PrivateStaticMethod.java'))
        self.assertEqual(2, lines[0].position.line)
