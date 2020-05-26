# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from hashlib import md5
from pathlib import Path
from unittest import TestCase

from aibolit.config import Config
from lxml import etree

from aibolit.__main__ import list_dir, calculate_patterns_and_metrics, \
    create_xml_tree, create_text, format_converter_for_pattern


class TestRecommendPipeline(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRecommendPipeline, self).__init__(*args, **kwargs)
        self.cur_file_dir = Path(os.path.realpath(__file__)).parent
        self.config = Config.get_patterns_config()

    def __create_mock_input(self):
        patterns = [x['code'] for x in self.config['patterns']]
        item = {
            'filename': '1.java',
            'results': [
                {'pattern_code': 'P23',
                 'pattern_name': 'Some patterns name',
                 'code_lines': [1, 2, 4]
                 }
            ],
            'importances': sum([0.1 + x for x in range(len(patterns))])
        }
        another_item = {
            'filename': 'hdd/home/jardani_jovonovich/John_wick.java',
            'results': [
                {'pattern_code': 'P2',
                 'pattern_name': 'Somebody please get this man a gun',
                 'code_lines': [10, 100, 15000]},
                {'pattern_code': 'P4',
                 'pattern_name': 'New item',
                 'code_lines': [5, 6]}
            ],
            'importances': sum([0.1 + 2 * x for x in range(len(patterns))])
        }
        error_file = {
            'error_string': "Error occured",
            'filename': 'hdd/home/Error.java',
            'results': []
        }
        mock_input = [item, another_item, error_file]
        return mock_input

    def test_calculate_patterns_and_metrics(self):
        file = Path(self.cur_file_dir, 'folder/LottieImageAsset.java')
        calculate_patterns_and_metrics(file)

    def test_list_dir_no_java_files(self):
        found_files = []
        file = Path(self.cur_file_dir, 'no_java_files')
        self.assertEqual(list_dir(file, found_files), found_files)

    def test_list_dir(self):
        file = Path(self.cur_file_dir, 'folder')
        found_files = []
        list_dir(file, found_files)
        resuls = {'KeyframeParser.java', 'Metadata.java', 'LottieImageAsset.java'}
        filenames = set([Path(x).name for x in found_files])
        self.assertEqual(filenames, resuls)

    def test_xml_create_full_report(self):
        patterns = [x['code'] for x in self.config['patterns']]
        item = {
            'filename': '1.java',
            'results': [
                {'pattern_code': 'P23',
                 'pattern_name': 'Some patterns name',
                 'code_lines': [1, 2, 4]
                 }
            ],
            'importances': sum([0.1 + x for x in range(len(patterns))])
        }
        another_item = {
            'filename': 'hdd/home/jardani_jovonovich/John_wick.java',
            'results': [
                {'pattern_code': 'P2',
                 'pattern_name': 'Somebody please get this man a gun',
                 'code_lines': [10, 100, 15000]},
                {'pattern_code': 'P4',
                 'pattern_name': 'New item',
                 'code_lines': [5, 6]}
            ],
            'importances': sum([0.1 + 2 * x for x in range(len(patterns))])
        }
        error_file = {
            'error_string': "Error occured",
            'filename': 'hdd/home/Error.java',
            'results': []
        }
        mock_input = [item, another_item, error_file]
        xml_string = create_xml_tree(mock_input, full_report=True)
        md5_hash = md5(etree.tostring(xml_string))
        self.assertEqual(md5_hash.hexdigest(), '35f56275d4ba073e8d9c89b143c124da')

    def test_xml_empty_resutls(self):
        xml_string = create_xml_tree([], True)
        md5_hash = md5(etree.tostring(xml_string))
        self.assertEqual(md5_hash.hexdigest(), '7d55be99025f9d9bba410bdbd2c42cee')

    def test_text_format(self):
        mock_input = self.__create_mock_input()
        new_mock = format_converter_for_pattern(mock_input)
        text = create_text(new_mock, full_report=True)
        md5_hash = md5('\n'.join(text).encode('utf-8'))
        self.assertEqual(md5_hash.hexdigest(), 'a816108b88fc902296067d748487c529')

    def test_empty_text_format(self):
        new_mock = format_converter_for_pattern([])
        text = create_text(new_mock, full_report=True)
        md5_hash = md5('\n'.join(text).encode('utf-8'))
        self.assertEqual(md5_hash.hexdigest(), 'bc22beda46ca18267a677eb32361a2aa')

    def test_empty_lines_format(self):
        mock_input = self.__create_mock_input()
        new_mock = format_converter_for_pattern(mock_input, 'code_line')
        text = create_text(new_mock, full_report=True)
        md5_hash = md5('\n'.join(text).encode('utf-8'))
        self.assertEqual(md5_hash.hexdigest(), 'a61d719999a79a4ef54ede1f5de9ff75')
