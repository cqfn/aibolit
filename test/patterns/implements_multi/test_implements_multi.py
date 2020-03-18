
import os
from unittest import TestCase
from aibolit.patterns.implements_multi.implements_multi import ImplementsMultiFinder
from pathlib import Path


class TestImplementsMulti(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    multi_finder = ImplementsMultiFinder()

    def test_one_class_with_types(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'AnimatableSplitDimensionPathValue.java'))
        assert len(lines) == 0
#
    def test_two_classes(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'AnimatableTransform.java'))
        assert len(lines) == 1
#
    def test_implements_in_string(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'AuditEventModelProcessor.java'))
        assert len(lines) == 0
#
    def test_implements_with_parantheses(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'BaseKeyframeAnimation.java'))
        assert len(lines) == 0
#
    def test_implements_with_parantheses(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'Configuration.java'))
        assert len(lines) == 1
#
    def test_implements_multi_classes(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'FillContent.java'))
        assert len(lines) == 1
#
    def test_implements_with_parantheses_multi(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'FJIterateTest.java'))
        assert len(lines) == 1
#
    def test_implements_with_parantheses_before(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'FJListProcedureRunner.java'))
        assert len(lines) == 0
#
    def test_implements_in_comments(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'KeyProviderCryptoExtension.java'))
        assert len(lines) == 0
#
    def test_implements_multi(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'OsSecureRandom.java'))
        assert len(lines) == 1
#
    def test_implements_with_parantheses(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'RectangleContent.java'))
        assert len(lines) == 1
#
    def test_implements_with_parantheses(self):
        lines = self.multi_finder.value(Path(self.dir_path, 'SequenceFile.java'))
        assert len(lines) == 1

