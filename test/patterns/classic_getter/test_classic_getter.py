
import os
from unittest import TestCase
from aibolit.patterns.classic_getter.classic_getter import ClassicGetter
from pathlib import Path


class TestGetter(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    getter_finder = ClassicGetter()

    def test_manager_in_middle(self):
        lines = self.getter_finder.value(Path(self.dir_path, 'AnimatableSplitDimensionPathValue.java'))
        self.assertEqual(lines, [12])

    def test_controller_in_end(self):
        lines = self.getter_finder.value(Path(self.dir_path, 'AnimatableTransform.java'))
        self.assertEqual(lines, [12])

    def test_one_normal_class(self):
        lines = self.getter_finder.value(Path(self.dir_path, 'AuditEventModelProcessor.java'))
        self.assertEqual(lines, [])

    def test_two_classes_with_pattern(self):
        lines = self.getter_finder.value(Path(self.dir_path, 'BaseKeyframeAnimation.java'))
        self.assertEqual(lines, [18, 186])

    def test_class_parser(self):
        lines = self.getter_finder.value(Path(self.dir_path, 'Configuration.java'))
        self.assertEqual(lines, [3106])

    def test_another_normal_class(self):
        lines = self.getter_finder.value(Path(self.dir_path, 'FillContent.java'))
        self.assertEqual(lines, [76])

    def test_four_normal_classes(self):
        lines = self.getter_finder.value(Path(self.dir_path, 'FJIterateTest.java'))
        self.assertEqual(lines, [])

    def test_two_distant_normal_classes(self):
        lines = self.getter_finder.value(Path(self.dir_path, 'FJListProcedureRunner.java'))
        self.assertEqual(lines, [])

    def test_classes_in_comments(self):
        lines = self.getter_finder.value(Path(self.dir_path, 'KeyProviderCryptoExtension.java'))
        self.assertEqual(lines, [1201, 128, 137, 144])

    def test_classes_in_methods(self):
        lines = self.getter_finder.value(Path(self.dir_path, 'OsSecureRandom.java'))
        self.assertEqual(lines, [])

    def test_normal_class(self):
        lines = self.getter_finder.value(Path(self.dir_path, 'RectangleContent.java'))
        self.assertEqual(lines, [55])

    def test_three_writers_one_reader(self):
        lines = self.getter_finder.value(Path(self.dir_path, 'SequenceFile.java'))
        self.assertEqual(lines, [837, 1478, 1538, 1684])
