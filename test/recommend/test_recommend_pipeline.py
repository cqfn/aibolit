# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
import os
from argparse import Namespace
from hashlib import md5
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import TestCase, skip
from unittest.mock import patch

import javalang
import javalang.tree

from aibolit import __main__ as aibolit_main
from aibolit.config import Config

from aibolit.__main__ import list_dir, calculate_patterns_and_metrics, \
    create_xml_tree, create_text, format_converter_for_pattern, find_start_and_end_lines, \
    find_annotation_by_node_type, add_pattern_if_ignored, _process_components, \
    run_recommend_for_file


class TestRecommendPipeline(TestCase):
    cur_file_dir = Path(os.path.realpath(__file__)).parent
    config = Config.get_patterns_config()

    def __create_mock_input(self):
        ex = Exception('Error occurred')
        item = {
            'filename': '1.java',
            'ncss': 100,
            'results': [[
                {'pattern_code': 'P23',
                 'pattern_name': 'Some patterns name',
                 'code_lines': [1, 2, 4],
                 'importance': 0.10
                 }
            ]]
        }
        another_item = {
            'filename': 'hdd/home/jardani_jovonovich/John_wick.java',
            'ncss': 50,
            'results': [
                [{'pattern_code': 'P2',
                  'pattern_name': 'Somebody please get this man a gun',
                  'code_lines': [10, 100, 15000],
                  'importance': 5.67
                  },
                 {'pattern_code': 'P4',
                  'pattern_name': 'New item',
                  'code_lines': [5, 6],
                  'importance': 5.67
                  }],
                [{'pattern_code': 'P2',
                  'pattern_name': 'Somebody please get this man a gun',
                  'code_lines': [11, 101, 15001],
                  'importance': 4.36
                  },
                 {'pattern_code': 'P4',
                  'pattern_name': 'New item',
                  'code_lines': [5, 6],
                  'importance': 3.24
                  }]
            ]
        }
        error_file = {
            'exception': str(ex),
            'filename': 'hdd/home/Error.java',
            'ncss': 0,
            'results': []
        }
        mock_input = [item, another_item, error_file]
        return mock_input

    def __create_input_for_xml(self):
        ex = Exception('Smth happened')
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
        file = Path(self.cur_file_dir, 'folder/LottieImageAsset.java')
        input_params, code_lines_dict, _ = calculate_patterns_and_metrics(
            file,
            patterns_to_suppress=[],
        )
        val = code_lines_dict['P2']
        self.assertNotEqual(val, 0)
        val = code_lines_dict['P24']
        self.assertNotEqual(val, 0)

    def test_calculate_patterns_and_metrics_with_suppress(self):
        file = Path(self.cur_file_dir, 'folder/LottieImageAsset.java')
        input_params, code_lines_dict, _ = calculate_patterns_and_metrics(
            file,
            patterns_to_suppress=['P2'],
        )
        val = code_lines_dict['P2']
        self.assertEqual(val, 0)
        val = code_lines_dict['P24']
        self.assertNotEqual(val, 0)

    def test_decomposition_keeps_class_level_patterns_on_single_component(self):
        """Class-level patterns should be counted once even after class decomposition."""
        java_code = '''
            package com.test;

            import java.util.HashMap;
            import java.util.Map;

            public class ConfigManager {
                private Map<String, String> data = new HashMap<>();
                private int counter = 0;
                private String name = "default";

                public void setValue(String key, String value) { data.put(key, value); counter++; }
                public String getValue(String key) { return data.get(key); }
                public int getCounter() { return counter; }
                public void incrementCounter() { counter++; }
                public String getName() { return name; }
                public void setName(String newName) { this.name = newName; }
                public void reset() { data.clear(); counter = 0; name = "default"; }
                public boolean hasKey(String key) { return data.containsKey(key); }
                public int size() { return data.size(); }
            }
        '''
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir, 'ConfigManager.java')
            file_path.write_text(java_code, encoding='utf-8')
            components, error = aibolit_main.calculate_patterns_and_metrics_with_decomposition(
                str(file_path),
                SimpleNamespace(suppress=[]),
            )

        self.assertIsNone(error)
        self.assertGreater(len(components), 1)
        self.assertEqual(sum(component['input_params']['P4'] for component in components), 1)
        self.assertEqual(sum(component['input_params']['P24'] for component in components), 1)
        self.assertEqual(len(components[0]['code_lines_dict']['lines_P4']), 1)
        self.assertTrue(
            all(component['code_lines_dict']['lines_P4'] == [] for component in components[1:])
        )
        self.assertTrue(
            all(component['code_lines_dict']['lines_P24'] == [] for component in components[1:])
        )

    def test_list_dir_no_java_files(self):
        found_files = []
        file = Path(self.cur_file_dir, 'no_java_files')
        self.assertEqual(list_dir(file, found_files), found_files)

    def test_list_dir(self):
        file = Path(self.cur_file_dir, 'folder')
        found_files = []
        list_dir(file, found_files)
        results = {'KeyframeParser.java', 'Metadata.java', 'LottieImageAsset.java'}
        filenames = set([Path(x).name for x in found_files])
        self.assertEqual(filenames, results)

    def test_xml_create_full_report(self):
        mock_input = self.__create_input_for_xml()
        mock_cmd = self.__create_mock_cmd()
        create_xml_tree(mock_input, full_report=True, cmd=mock_cmd, exit_code=0)

    def test_xml_empty_results(self):
        mock_cmd = self.__create_mock_cmd()
        create_xml_tree([], full_report=True, cmd=mock_cmd, exit_code=0)

    def test_xml(self):
        mock_input = self.__create_mock_input()
        mock_cmd = self.__create_mock_cmd()
        root = create_xml_tree(mock_input, full_report=True, cmd=mock_cmd, exit_code=2)

        self.assertEqual(root.findtext('./header/patterns'), '5')
        self.assertEqual(len(root.findall('./files/file/patterns/pattern')), 5)

    def test_count_value_keeps_original_exception_context(self):
        value_dict = {
            'code': 'P99',
            'make': lambda: None,
        }

        with patch('aibolit.__main__.build_ast', side_effect=KeyError('missing node')):
            with self.assertRaises(RuntimeError) as err:
                getattr(aibolit_main, '__count_value')(
                    value_dict,
                    {},
                    {},
                    'broken/File.java',
                )

        self.assertEqual(
            str(err.exception),
            "Can't count P99 pattern on broken/File.java: 'missing node'",
        )
        self.assertIsInstance(err.exception.__cause__, KeyError)

    def test_text_format(self):
        mock_input = self.__create_mock_input()
        new_mock = format_converter_for_pattern(mock_input)
        text = create_text(new_mock, full_report=True)
        md5_hash = md5('\n'.join(text).encode('utf-8'))
        self.assertEqual(md5_hash.hexdigest(), '0ec2078c516a42f0f58517f58d7fa950')

    def test_empty_lines_format(self):
        new_mock = format_converter_for_pattern([])
        text = create_text(new_mock, full_report=True)
        md5_hash = md5('\n'.join(text).encode('utf-8'))
        self.assertEqual(md5_hash.hexdigest(), 'bc22beda46ca18267a677eb32361a2aa')

    @skip('It is flaky')
    def test_text_format_sort_by_code_line(self):
        mock_input = self.__create_mock_input()
        new_mock = format_converter_for_pattern(mock_input, 'code_line')
        text = create_text(new_mock, full_report=True)
        md5_hash = md5('\n'.join(text).encode('utf-8'))
        self.assertEqual(md5_hash.hexdigest(), '62c794a9fad74c64eea7eb9a5e42e4c8')

    def test_find_start_end_line_function(self):
        # Check start and end line for MethodDeclaration,
        # find_start_and_end_lines is used for functions only at the moment
        file = Path(self.cur_file_dir, 'start_end/LottieImageAsset.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 35)
            self.assertEqual(end, 62)

    def test_find_start_end_line_empty_function(self):
        # Check start and end line for MethodDeclaration,
        # find_start_and_end_lines is used for functions only at the moment
        file = Path(self.cur_file_dir, 'start_end/EmptyFunction.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 35)
            self.assertEqual(end, 35)

    def test_find_start_end_line_empty_function_with_one_line(self):
        file = Path(self.cur_file_dir, 'start_end/OneLineFunction.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 35)
            self.assertEqual(end, 35)

    def test_find_start_end_line_empty_function_with_lambda(self):
        file = Path(self.cur_file_dir, 'start_end/Lambda.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 35)
            self.assertEqual(end, 46)

    def test_find_start_end_line_empty_function_with_anonymous_class(self):
        file = Path(self.cur_file_dir, 'start_end/AnonymousClass.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 35)
            self.assertEqual(end, 44)

    def test_find_start_end_line_empty_function_in_anonymous_class(self):
        file = Path(self.cur_file_dir, 'start_end/AnonymousClass.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[1][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 40)
            self.assertEqual(end, 41)

    def test_find_start_end_line_return_by_one_line(self):
        file = Path(self.cur_file_dir, 'start_end/FileStorage.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 92)
            self.assertEqual(end, 124)

    def test_find_start_end_line_in_function2(self):
        file = Path(self.cur_file_dir, 'start_end/UpDirective.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.MethodDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 25)
            self.assertEqual(end, 41)

    def test_find_start_end_line_in_class(self):
        file = Path(self.cur_file_dir, 'start_end/LottieImageAsset.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            method = list(tree.filter(javalang.tree.ClassDeclaration))[0][1]
            start, end = find_start_and_end_lines(method)
            self.assertEqual(start, 14)
            self.assertEqual(end, 62)

    def test_find_annotation_by_class_declaration(self):
        file = Path(self.cur_file_dir, 'annotations/ClassAnnotations.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            classes_with_annonations = find_annotation_by_node_type(
                tree, javalang.tree.ClassDeclaration
            )
            pattern_found = list(classes_with_annonations.values())[0][0]
            self.assertEqual(pattern_found, 'P11')

    def test_find_multiple_annotations_by_class_declaration(self):
        file = Path(self.cur_file_dir, 'annotations/MutipleAnnotations.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            classes_with_annonations = find_annotation_by_node_type(
                tree, javalang.tree.ClassDeclaration
            )
            patterns_found = list(classes_with_annonations.values())[0]
            self.assertEqual(patterns_found, ['P23', 'P11'])

    def test_find_annotation_method_declaration(self):
        file = Path(self.cur_file_dir, 'annotations/MutipleAnnotations.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            functions_with_annotations = find_annotation_by_node_type(
                tree, javalang.tree.MethodDeclaration
            )
            patterns_found_with_functions = [
                (x.name, y) for x, y in functions_with_annotations.items()
            ]
            self.assertEqual(
                patterns_found_with_functions,
                [('set', ['P23']), ('getStreamReader', ['P23', 'P22'])]
            )

    def test_find_annotation_by_field_declaration(self):
        file = Path(self.cur_file_dir, 'annotations/MutipleAnnotations.java')
        with open(file, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            fields_with_annotations = find_annotation_by_node_type(
                tree, javalang.tree.FieldDeclaration
            )
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

    def test_process_components_deduplicates_class_level_findings(self):
        # A class-level pattern (e.g. P4 "Prohibited class name") re-fires in
        # every decomposed component, reporting the same line repeatedly with
        # different importance values (issue #1217). Only one finding should
        # survive.
        component_findings = [
            [{'code_lines': [6], 'pattern_code': 'P4',
              'pattern_name': 'Prohibited class name', 'importance': 6.40}],
            [{'code_lines': [6], 'pattern_code': 'P4',
              'pattern_name': 'Prohibited class name', 'importance': 3.20}],
            [{'code_lines': [6], 'pattern_code': 'P4',
              'pattern_name': 'Prohibited class name', 'importance': 6.40}],
        ]
        components = [{'code_lines_dict': {}, 'input_params': {}, 'index': i}
                      for i in range(len(component_findings))]
        with patch('aibolit.__main__.create_results', side_effect=component_findings):
            results = _process_components(components, args=None,
                                          classes_with_patterns_ignored=[],
                                          patterns_ignored={})
        flat = [item for sublist in results for item in sublist]
        self.assertEqual(len(flat), 1)
        self.assertEqual(flat[0]['pattern_code'], 'P4')
        self.assertEqual(flat[0]['code_lines'], [6])
        self.assertEqual(flat[0]['importance'], 6.40)

    def test_recommend_reports_class_level_pattern_once(self):
        # End-to-end check for issue #1217: a class that decomposes into many
        # components must not report the same class-level violation per
        # component. No (pattern_code, code_lines) pair may appear twice.
        file = Path(self.cur_file_dir, 'decomposition/ConfigManager.java')
        args = Namespace(suppress=[], model=None, full=True)
        result = run_recommend_for_file(str(file), args)

        self.assertIsNone(result['exception'])
        findings = [item for sublist in result['results'] for item in sublist]
        keys = [(item['pattern_code'], tuple(item['code_lines'])) for item in findings]
        self.assertEqual(sorted(keys), sorted(set(keys)), f'duplicate findings: {keys}')

    def test_process_components_keeps_distinct_findings(self):
        # The same pattern firing on different lines, or different patterns on
        # the same line, are genuinely distinct and must be preserved.
        component_findings = [
            [{'code_lines': [10], 'pattern_code': 'P2',
              'pattern_name': 'Assert in code', 'importance': 5.67}],
            [{'code_lines': [20], 'pattern_code': 'P2',
              'pattern_name': 'Assert in code', 'importance': 4.36}],
            [{'code_lines': [10], 'pattern_code': 'P5',
              'pattern_name': 'Force type casting', 'importance': 1.23}],
        ]
        components = [{'code_lines_dict': {}, 'input_params': {}, 'index': i}
                      for i in range(len(component_findings))]
        with patch('aibolit.__main__.create_results', side_effect=component_findings):
            results = _process_components(components, args=None,
                                          classes_with_patterns_ignored=[],
                                          patterns_ignored={})
        flat = [item for sublist in results for item in sublist]
        self.assertEqual(len(flat), 3)
        self.assertEqual(
            {(item['pattern_code'], tuple(item['code_lines'])) for item in flat},
            {('P2', (10,)), ('P2', (20,)), ('P5', (10,))},
        )
