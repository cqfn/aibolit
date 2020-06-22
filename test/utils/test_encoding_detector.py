import os
from unittest import TestCase
from pathlib import Path

from aibolit.utils.encoding_detector import detect_encoding_of_file


class TestEncodingDetector(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    files_with_encoding = [('ConditionalExpressionCheck.java', 'UTF-8'),
                           ('ExceptionDemo.java', 'GB18030')]

    def test_encoding_detector(self):
        for filename, excepted_encoding in TestEncodingDetector.files_with_encoding:
            with self.subTest():
                actual_encoding = detect_encoding_of_file(Path(self.dir_path, filename))
                self.assertEqual(actual_encoding, excepted_encoding)
