
import os
from unittest import TestCase
from aibolit.patterns.implements_multi.implements_multi import ImplementsMultiFinder
from pathlib import Path


class TestImplementsMulti(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    multi_finder = ImplementsMultiFinder()

    def test_one_class_with_types(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'AnimatableSplitDimensionPathValue.java'))
        self.assertEqual(lines, [])

    def test_two_classes(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'AnimatableTransform.java'))
        self.assertEqual(lines, [12])

    def test_implements_in_string(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'AuditEventModelProcessor.java'))
        self.assertEqual(lines, [])

    def test_implements_with_parantheses(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'BaseKeyframeAnimation.java'))
        self.assertEqual(lines, [])

    def test_implements_with_nested_parantheses(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'Configuration.java'))
        self.assertEqual(lines, [225])

    def test_implements_multi_classes(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'FillContent.java'))
        self.assertEqual(lines, [29])

    def test_implements_with_parantheses_multi(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'FJIterateTest.java'))
        self.assertEqual(lines, [601])

    def test_implements_with_parantheses_before(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'FJListProcedureRunner.java'))
        self.assertEqual(lines, [])

    def test_implements_in_comments(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'KeyProviderCryptoExtension.java'))
        self.assertEqual(lines, [])

    def test_implements_multi(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'OsSecureRandom.java'))
        self.assertEqual(lines, [42])

    def test_implements_three(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'RectangleContent.java'))
        self.assertEqual(lines, [22])

    def test_implements_many(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'SequenceFile.java'))
        self.assertEqual(lines, [837])
