
import os
from unittest import TestCase
from aibolit.patterns.er_class.er_class import ErClass
from pathlib import Path


class TestErClass(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    er_class_finder = ErClass()

    def test_manager_in_middle(self):
        lines = self.er_class_finder.value(Path(self.dir_path, 'AnimatableSplitDimensionPathValue.java'))
        self.assertEqual(lines, [12])

    def test_controller_in_end(self):
        lines = self.er_class_finder.value(Path(self.dir_path, 'AnimatableTransform.java'))
        self.assertEqual(lines, [12])

    def test_one_normal_class(self):
        lines = self.er_class_finder.value(Path(self.dir_path, 'AuditEventModelProcessor.java'))
        self.assertEqual(lines, [])

    def test_two_classes_with_pattern(self):
        lines = self.er_class_finder.value(Path(self.dir_path, 'BaseKeyframeAnimation.java'))
        self.assertEqual(lines, [18, 186])

    def test_class_parser(self):
        lines = self.er_class_finder.value(Path(self.dir_path, 'Configuration.java'))
        self.assertEqual(lines, [3106])

    def test_another_normal_class(self):
        lines = self.er_class_finder.value(Path(self.dir_path, 'FillContent.java'))
        self.assertEqual(lines, [])

    def test_four_normal_classes(self):
        lines = self.er_class_finder.value(Path(self.dir_path, 'FJIterateTest.java'))
        self.assertEqual(lines, [])

    def test_two_distant_normal_classes(self):
        lines = self.er_class_finder.value(Path(self.dir_path, 'FJListProcedureRunner.java'))
        self.assertEqual(lines, [])

    def test_classes_in_comments(self):
        lines = self.er_class_finder.value(Path(self.dir_path, 'KeyProviderCryptoExtension.java'))
        self.assertEqual(lines, [])

    def test_classes_in_methods(self):
        lines = self.er_class_finder.value(Path(self.dir_path, 'OsSecureRandom.java'))
        self.assertEqual(lines, [])

    def test_normal_class(self):
        lines = self.er_class_finder.value(Path(self.dir_path, 'RectangleContent.java'))
        self.assertEqual(lines, [])

    def test_three_writers_one_reader(self):
        lines = self.er_class_finder.value(Path(self.dir_path, 'SequenceFile.java'))
        self.assertEqual(lines, [837, 1478, 1538, 1684])
