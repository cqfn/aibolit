
import os
from unittest import TestCase
from aibolit.patterns.classic_setter.classic_setter import ClassicSetter
from pathlib import Path


class TestSetter(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    setter_finder = ClassicSetter()

    def test_one_valid_patterns(self):
        lines = self.setter_finder.value(Path(self.dir_path, 'BaseKeyframeAnimation.java'))
        self.assertEqual(lines, [40])

    def test_four_setter_patterns(self):
        lines = self.setter_finder.value(Path(self.dir_path, 'Configuration.java'))
        self.assertEqual(lines, [1236, 1240, 3783, 3819])

    def test_another_setter_patterns(self):
        lines = self.setter_finder.value(Path(self.dir_path, 'SequenceFile.java'))
        self.assertEqual(lines, [2849, 2855, 2861, 3127])
