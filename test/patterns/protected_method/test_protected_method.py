import os
from unittest import TestCase
from pathlib import Path
from aibolit.patterns.protected_method.protected_method import ProtectedMethod


class TestProtectedMethod(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_not_find_protected_method(self):
        self.assertEqual([], ProtectedMethod().value(Path(self.dir_path, 'NoProtectedMethod.java')),
                         'Should not match pattern protected method')

    def test_find_protected_method(self):
        self.assertEqual([2, 6], ProtectedMethod().value(Path(self.dir_path, 'ProtectedMethod.java')),
                         'Should match pattern protected method')