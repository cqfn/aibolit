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

    def test_find_protected_method_inner(self):
        self.assertEqual([2, 11], ProtectedMethod().value(Path(self.dir_path, 'InnerClassProtectedMethod.java')),
                         'Should match pattern protected method in inner class')

    def test_find_protected_method_anonymous(self):
        self.assertEqual([5], ProtectedMethod().value(Path(self.dir_path, 'AnonymousClassProtectedMethod.java')),
                         'Should match pattern protected method in anonymous class')
