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

import json
import os
import pickle
from hashlib import md5
from pathlib import Path
from unittest import TestCase

from lxml import etree

from aibolit.__main__ import list_dir, calculate_patterns_and_metrics, create_xml_tree
from aibolit.model.model import TwoFoldRankingModel, Dataset # type: ignore

class TestNestedBlocks(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestNestedBlocks, self).__init__(*args, **kwargs)
        self.cur_file_dir = Path(os.path.realpath(__file__)).parent

    def test_calculate_patterns_and_metrics(self):
        file = Path(self.cur_file_dir, 'folder/LottieImageAsset.java')
        calculate_patterns_and_metrics(file)
        # run_recommend_for_file(str(file))

    def test_list_dir_empty(self):
        file = Path(self.cur_file_dir, 'empty_dir')
        found_files = []
        self.assertEqual(list_dir(file, found_files), found_files)

    def test_list_dir_no_java_files(self):
        found_files = []
        file = Path(self.cur_file_dir, 'no_java_files')
        self.assertEqual(list_dir(file, found_files), found_files)

    def test_list_dir(self):
        file = Path(self.cur_file_dir, 'folder')
        found_files = []
        list_dir(file, found_files)
        resuls = [
            'KeyframeParser.java',
            'Metadata.java',
            'LottieImageAsset.java'
        ]
        filenames = [Path(x).name for x in found_files]
        self.assertEqual(filenames, resuls)

    def test_xml_create(self):
        file = Path(self.cur_file_dir, 'folder/LottieImageAsset.java')
        results = run_recommend_for_file(str(file))
        xml_string = create_xml_tree([results])
        md5_hash = md5(etree.tostring(xml_string))
        self.assertEqual(md5_hash.hexdigest(), '86e0756b9627280f605d5c6b4cf17f9f')

    def test_xml_empty_resutls(self):
        xml_string = create_xml_tree([])
        md5_hash = md5(etree.tostring(xml_string))
        self.assertEqual(md5_hash, md5_hash.hexdigest())

    def test_recommend_with_error(self):
        file = Path(self.cur_file_dir, r'errors\AbsoluteLayoutSupport.java')
        results = run_recommend_for_file(str(file))
        xml_string = create_xml_tree([results])
        md5_hash = md5(etree.tostring(xml_string))
        self.assertEqual(md5_hash.hexdigest(), '1abcc7fceedf7fce6f8d141c305a7da1')
