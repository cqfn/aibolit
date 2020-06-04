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
import argparse
import os
from hashlib import md5
from pathlib import Path
from unittest import TestCase

from aibolit.config import Config

from aibolit.__main__ import list_dir, calculate_patterns_and_metrics, \
    create_xml_tree, create_text, format_converter_for_pattern


class TestRecommendPipeline(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRecommendPipeline, self).__init__(*args, **kwargs)
        self.cur_file_dir = Path(os.path.realpath(__file__)).parent
        self.config = Config.get_patterns_config()

    def __create_mock_input(self):
        item = {
            'filename': '1.java',
            'results': [
                {'pattern_code': 'P23',
                 'pattern_name': 'Some patterns name',
                 'code_lines': [1, 2, 4],
                 'importance': 0.10
                 }
            ]
        }
        another_item = {
            'filename': 'hdd/home/jardani_jovonovich/John_wick.java',
            'results': [
                {'pattern_code': 'P2',
                 'pattern_name': 'Somebody please get this man a gun',
                 'code_lines': [10, 100, 15000],
                 'importance': 5.67
                 },
                {'pattern_code': 'P4',
                 'pattern_name': 'New item',
                 'code_lines': [5, 6],
                 'importance': 5.67
                 }
            ]
        }
        error_file = {
            'error_string': "Error occured",
            'filename': 'hdd/home/Error.java',
            'results': []
        }
        mock_input = [item, another_item, error_file]
        return mock_input

    def __suppress_argparse_mock(self):
        argparse_mock = argparse.ArgumentParser()
        argparse_mock.add_argument(
            '--suppress',
            default=[],
            nargs="*",
        )
        argparse_mock.suppress = []
        return argparse_mock

    def __create_input_for_xml(self):
        return [
            {'filename': 'D:\\target\\0001\\fast\\Configuration.java',
             'results': [
                 {'code_lines': [294, 391],
                  'pattern_code': 'P13',
                  'pattern_name': 'Null check',
                  'importance': 30.95612931128819},
                 {'code_lines': [235, 240],
                  'pattern_code': 'P12',
                  'pattern_name': 'Non final attribute',
                  'importance': 17.89671525822768}
             ]},
            {'filename': 'D:\\target\\0001\\fast\\Error.java',
             'results': [],
             'error_string': "Smth happened"
             },
            {'filename': 'D:\\target\\0001\\fast\\Another.java',
             'results': [
                 {'code_lines': [23, 2],
                  'pattern_code': 'P13',
                  'pattern_name': 'Null check',
                  'importance': 10.95},
                 {'code_lines': [235, 240],
                  'pattern_code': 'P12',
                  'pattern_name': 'Non final attribute',
                  'importance': 0.23}
             ]}
        ]

    def __create_mock_cmd(self):
        return [
            '/mnt/d/git/aibolit/aibolit/__main__.py',
            'recommend',
            '--folder=/mnt/d/target/0001/fast',
            '--format=compact',
            '--full'
        ]

    def test_calculate_patterns_and_metrics(self):
        args = self.__suppress_argparse_mock()
        file = Path(self.cur_file_dir, 'folder/LottieImageAsset.java')
        input_params, code_lines_dict, error_string = calculate_patterns_and_metrics(file, args)
        val = code_lines_dict['P2']
        self.assertNotEqual(val, 0)
        val = code_lines_dict['P24']
        self.assertNotEqual(val, 0)

    def test_calculate_patterns_and_metrics_wih_suppress(self):
        args = self.__suppress_argparse_mock()
        args.suppress = 'P2'
        file = Path(self.cur_file_dir, 'folder/LottieImageAsset.java')
        input_params, code_lines_dict, error_string = calculate_patterns_and_metrics(file, args)
        val = code_lines_dict['P2']
        self.assertEqual(val, 0)
        val = code_lines_dict['P24']
        self.assertNotEqual(val, 0)

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
        mock_input = self.__create_input_for_xml()
        mock_cmd = self.__create_mock_cmd()
        create_xml_tree(mock_input, full_report=True, cmd=mock_cmd, exit_code=0)

    def test_xml_empty_resutls(self):
        mock_cmd = self.__create_mock_cmd()
        create_xml_tree([], full_report=True, cmd=mock_cmd, exit_code=0)

    def test_text_format(self):
        mock_input = self.__create_mock_input()
        new_mock = format_converter_for_pattern(mock_input)
        text = create_text(new_mock, full_report=True)
        md5_hash = md5('\n'.join(text).encode('utf-8'))
        self.assertEqual(md5_hash.hexdigest(), '4ac43ebd666b8edf061e7203cd691564')

    def test_empty_lines_format(self):
        new_mock = format_converter_for_pattern([])
        text = create_text(new_mock, full_report=True)
        md5_hash = md5('\n'.join(text).encode('utf-8'))
        self.assertEqual(md5_hash.hexdigest(), 'bc22beda46ca18267a677eb32361a2aa')

    def test_text_format_sort_by_code_line(self):
        mock_input = self.__create_mock_input()
        new_mock = format_converter_for_pattern(mock_input, 'code_line')
        text = create_text(new_mock, full_report=True)
        md5_hash = md5('\n'.join(text).encode('utf-8'))
        self.assertEqual(md5_hash.hexdigest(), 'f026fb25ba62d835cb189978d6f049c4')
