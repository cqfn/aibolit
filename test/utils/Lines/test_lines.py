import os
from unittest import TestCase
from pathlib import Path
from aibolit.utils.lines import Lines


class TestLines(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_canReadLines(self):
        self.assertEqual(
            'class SimpleLinesTest {\n',
            (Lines(Path(self.dir_path, 'SimpleLinesTest.java')).value()[1])[0],
            'Did not match first line'
        )
        self.assertEqual(
            '    public void methodOne() {\n',
            (Lines(Path(self.dir_path, 'SimpleLinesTest.java')).value()[1])[1],
            'Did not match second line'
        )
        self.assertEqual(
            '        //do anything\n',
            (Lines(Path(self.dir_path, 'SimpleLinesTest.java')).value()[1])[2],
            'Did not match third line'
        )
        self.assertEqual(
            '    }\n',
            (Lines(Path(self.dir_path, 'SimpleLinesTest.java')).value()[1])[3],
            'Did not match fourth line'
        )
        self.assertEqual(
            '}',
            (Lines(Path(self.dir_path, 'SimpleLinesTest.java')).value()[1])[4],
            'Did not match last line'
        )
