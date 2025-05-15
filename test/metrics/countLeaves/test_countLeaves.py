# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from pathlib import Path
from unittest import TestCase

from aibolit.metrics.countLeaves.numberofleaves import CountNumberOfLeaves


class TestCountLeaves(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    count_leaves = CountNumberOfLeaves()

    def test_simple(self):
        lines = self.count_leaves.value(Path(self.dir_path, 'simple.java'))
        self.assertEqual(lines, 1)

    def test_simple1(self):
        lines = self.count_leaves.value(Path(self.dir_path, '5.java'))
        self.assertEqual(lines, 4)

    def test1(self):
        lines = self.count_leaves.value(Path(self.dir_path, '1.java'))
        self.assertEqual(lines, 106)

    def test2(self):
        lines = self.count_leaves.value(Path(self.dir_path, '2.java'))
        self.assertEqual(lines, 30)

    def test3(self):
        lines = self.count_leaves.value(Path(self.dir_path, '3.java'))
        self.assertEqual(lines, 12)

    def test4(self):
        lines = self.count_leaves.value(Path(self.dir_path, '4.java'))
        self.assertEqual(lines, 12)

    def test5(self):
        lines = self.count_leaves.value(Path(self.dir_path, 'nested_method.java'))
        self.assertEqual(lines, 21)
