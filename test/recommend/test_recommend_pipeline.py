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

import javalang

from aibolit.config import Config

from aibolit.__main__ import list_dir, calculate_patterns_and_metrics, \
    create_xml_tree, create_text, format_converter_for_pattern, find_start_and_end_lines, \
    find_annotation_by_node_type, add_pattern_if_ignored


class TestRecommendPipeline(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRecommendPipeline, self).__init__(*args, **kwargs)
        self.cur_file_dir = Path(os.path.realpath(__file__)).parent
        self.config = Config.get_patterns_config()

    def __create_mock_input(self):
        ex = Exception("Error occurred")
        item = {
            'filename': '1.java',
            'ncss': 100,
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
            'ncss': 50,
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
            'exception': str(ex),
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
        ex = Exception("Smth happened")
        return [
            {'filename': 'D:\\target\\0001\\fast\\Configuration.java',
             'ncss': 100,
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
             'ncss': 0,
             'exception': str(ex)
             },
            {'filename': 'D:\\target\\0001\\fast\\Another.java',
             'ncss': 50,
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
        input_params, code_lines_dict, _ = calculate_patterns_and_metrics(file, args)
        val = code_lines_dict['P2']
        self.assertNotEqual(val, 0)
        val = code_lines_dict['P24']
        self.assertNotEqual(val, 0)

    def test_calculate_patterns_and_metrics_wih_suppress(self):
        args = self.__suppress_argparse_mock()
        args.suppress = 'P2'
        file = Path(self.cur_file_dir, 'folder/LottieImageAsset.java')
        input_params, code_lines_dict, _ = calculate_patterns_and_metrics(file, args)
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

    def test_xml_empty_results(self):
        mock_cmd = self.__create_mock_cmd()
        create_xml_tree([], full_report=True, cmd=mock_cmd, exit_code=0)

    def test_text_format(self):
        mock_input = self.__create_mock_input()
        new_mock = format_converter_for_pattern(mock_input)
        text = create_text(new_mock, full_report=True)
        md5_hash = md5('\n'.join(text).encode('utf-8'))
        self.assertEqual(md5_hash.hexdigest(), '2a67e22091ba2cfd76847d292ed90142')

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
        self.assertEqual(md5_hash.hexdigest(), '8c6b91b8600848b66a9e91f2047d2d6d')

    def test_find_start_end_line_function(self):
        # Check start and end line for MethodDeclaration,
        # find_start_and_end_lines is used for functions only at the moment
        file = Path(self.cur_file_dir, 'start_end/LottieImageAsset.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 32)
            self.assertEqual(end, 59)

    def test_find_start_end_line_empty_function(self):
        # Check start and end line for MethodDeclaration,
        # find_start_and_end_lines is used for functions only at the moment
        file = Path(self.cur_file_dir, 'start_end/EmptyFunction.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 32)
            self.assertEqual(end, 32)

    def test_find_start_end_line_empty_function_with_one_line(self):
        file = Path(self.cur_file_dir, 'start_end/OneLineFunction.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 32)
            self.assertEqual(end, 32)

    def test_find_start_end_line_empty_function_with_lambda(self):
        file = Path(self.cur_file_dir, 'start_end/Lambda.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 32)
            self.assertEqual(end, 43)

    def test_find_start_end_line_empty_function_with_anonymous_class(self):
        file = Path(self.cur_file_dir, 'start_end/AnonymousClass.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 32)
            self.assertEqual(end, 41)

    def test_find_start_end_line_empty_function_in_anonymous_class(self):
        file = Path(self.cur_file_dir, 'start_end/AnonymousClass.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[1][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 37)
            self.assertEqual(end, 38)

    def test_find_start_end_line_return_by_one_line(self):
        file = Path(self.cur_file_dir, 'start_end/FileStorage.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 108)
            self.assertEqual(end, 140)

    def test_find_start_end_line_in_function2(self):
        file = Path(self.cur_file_dir, 'start_end/UpDirective.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 49)
            self.assertEqual(end, 65)

    def test_find_start_end_line_in_class(self):
        file = Path(self.cur_file_dir, 'start_end/LottieImageAsset.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.ClassDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 11)
            self.assertEqual(end, 59)

    def test_find_annotation_by_class_declaration(self):
        file = Path(self.cur_file_dir, 'annotations/ClassAnnotations.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            classes_with_annonations = find_annotation_by_node_type(tree, javalang.tree.ClassDeclaration)
            pattern_found = list(classes_with_annonations.values())[0][0]
            self.assertEqual(pattern_found, 'P11')

    def test_find_mutiple_annotations_by_class_declaration(self):
        file = Path(self.cur_file_dir, 'annotations/MutipleAnnotations.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            classes_with_annonations = find_annotation_by_node_type(tree, javalang.tree.ClassDeclaration)
            patterns_found = list(classes_with_annonations.values())[0]
            self.assertEqual(patterns_found, ['P23', 'P11'])

    def test_find_annotation_method_declaration(self):
        file = Path(self.cur_file_dir, 'annotations/MutipleAnnotations.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            functions_with_annotations = find_annotation_by_node_type(tree, javalang.tree.MethodDeclaration)
            patterns_found_with_functions = [(x.name, y) for x, y in functions_with_annotations.items()]
            self.assertEqual(patterns_found_with_functions, [('set', ['P23']), ('getStreamReader', ['P23', 'P22'])])

    def test_find_annotation_by_field_declaration(self):
        file = Path(self.cur_file_dir, 'annotations/MutipleAnnotations.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            fields_with_annotations = find_annotation_by_node_type(tree, javalang.tree.FieldDeclaration)
            patterns_found_with_fields = list(fields_with_annotations.values())
            self.assertEqual(patterns_found_with_fields, [['P23'], ['P23', 'P22']])

    def test_pattern_ignore(self):
        pattern_item = {'code_lines': [20],
                        'pattern_code': 'P13',
                        'pattern_name': 'Null check',
                        'importance': 30.95612931128819}
        results = []
        pattern_ignored = {'P13': [[10, 20]]}
        add_pattern_if_ignored(pattern_ignored, pattern_item, results)
        self.assertEqual(results, [])

    def test_pattern_not_ignore(self):
        pattern_item = {'code_lines': [20, 30],
                        'pattern_code': 'P14',
                        'pattern_name': 'Null check',
                        'importance': 30.95612931128819}
        results = []
        pattern_ignored = {'P14': [[60, 100]]}
        add_pattern_if_ignored(pattern_ignored, pattern_item, results)
        self.assertEqual(results[0]['code_lines'], pattern_item['code_lines'])
