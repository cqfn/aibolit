# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from aibolit.utils.encoding_detector import (
    detect_encoding_of_file,
    read_text_with_autodetected_encoding,
)


class TestEncodingDetector(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    files_with_encoding = [('ConditionalExpressionCheck.java', 'UTF-8'),
                           ('ExceptionDemo.java', 'UTF-8')]

    def test_encoding_detector(self):
        for filename, excepted_encoding in TestEncodingDetector.files_with_encoding:
            with self.subTest():
                actual_encoding = detect_encoding_of_file(Path(self.dir_path, filename))
                # Case insensitive comparison for UTF-8
                if excepted_encoding.upper() == 'UTF-8':
                    self.assertEqual(actual_encoding.upper(), excepted_encoding.upper())
                # For other encodings, use exact match
                else:
                    self.assertEqual(actual_encoding, excepted_encoding)

    def test_read_text_falls_back_when_detected_encoding_fails(self):
        with TemporaryDirectory() as tmpdir:
            filename = Path(tmpdir, 'NonUtf8.java')
            filename.write_bytes(b'class NonUtf8 { // \xb6\n}\n')

            with patch(
                'aibolit.utils.encoding_detector.detect_encoding_of_data',
                return_value='utf-8',
            ):
                content = read_text_with_autodetected_encoding(filename)

        self.assertIn('class NonUtf8', content)
