# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from pathlib import Path
from unittest import TestCase

from aibolit.metrics.spaces.SpaceCounter import IndentationCounter


class TestSpaces(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    max_right = IndentationCounter(max_right=True)
    max_left = IndentationCounter(max_left=True)
    left_var = IndentationCounter(left_var=True)
    right_var = IndentationCounter(right_var=True)

    def test_class_with_best_ident(self):
        val = self.max_left.value(Path(self.dir_path, 'BestIdent.java'))
        self.assertEqual(val, 44)
        val = self.max_right.value(Path(self.dir_path, 'BestIdent.java'))
        self.assertEqual(val, 113)

    def test_class_without_left_spaces(self):
        val = self.max_left.value(Path(self.dir_path, 'NoLeftSpaces.java'))
        self.assertEqual(val, 0)
        val = self.max_right.value(Path(self.dir_path, 'NoLeftSpaces.java'))
        self.assertEqual(val, 55)

    def test_class_without_right_spaces(self):
        val = self.max_left.value(Path(self.dir_path, 'NoRightSpaces.java'))
        self.assertEqual(val, 57)
        val = self.max_right.value(Path(self.dir_path, 'NoRightSpaces.java'))
        self.assertEqual(val, 0)

    def test_class_with_equal_spaces_number(self):
        val = self.max_left.value(Path(self.dir_path, 'SameMean.java'))
        self.assertEqual(val, 4)
        val = self.max_right.value(Path(self.dir_path, 'SameMean.java'))
        self.assertEqual(val, 55)

    def test_class_with_tabs_and_spaces(self):
        val = self.max_left.value(Path(self.dir_path, 'SpacesAndTabs.java'))
        self.assertEqual(val, 8)
        val = self.max_right.value(Path(self.dir_path, 'SpacesAndTabs.java'))
        self.assertEqual(val, 59)

    def test_class_with_worst_ident(self):
        val = self.max_left.value(Path(self.dir_path, 'WorstIdentation.java'))
        self.assertEqual(val, 20)
        val = self.max_right.value(Path(self.dir_path, 'WorstIdentation.java'))
        self.assertEqual(val, 163)

    def test_empty_examples(self):
        val = self.max_left.value(Path(self.dir_path, 'ClusterDataSourceConfiguration.java'))
        self.assertEqual(val, 0)
        val = self.max_right.value(Path(self.dir_path, 'ClusterDataSourceConfiguration.java'))
        self.assertEqual(val, 0)
        val = self.left_var.value(Path(self.dir_path, 'ClusterDataSourceConfiguration.java'))
        self.assertEqual(val, 0)
        val = self.right_var.value(Path(self.dir_path, 'ClusterDataSourceConfiguration.java'))
        self.assertEqual(val, 0)

    def test_one_point_in_series(self):
        val = self.max_left.value(Path(self.dir_path, 'package-info.java'))
        self.assertEqual(val, 0)
        val = self.max_right.value(Path(self.dir_path, 'package-info.java'))
        self.assertEqual(val, 0)
        val = self.left_var.value(Path(self.dir_path, 'package-info.java'))
        self.assertEqual(val, 0)
        val = self.right_var.value(Path(self.dir_path, 'package-info.java'))
        self.assertEqual(val, 0)
