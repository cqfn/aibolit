# SPDX-FileCopyrightText: Copyright (c) 2020 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase
from aibolit.patterns.assign_null_finder.assign_null_finder import NullAssignment


class NullAssignmentTestCase(TestCase):
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    def test_several(self):
        lines = NullAssignment().value(self.cur_dir + "/several.java")
        self.assertEqual(lines, [5, 6, 11, 15, 21, 22])

    def test_one(self):
        lines = NullAssignment().value(self.cur_dir + "/one.java")
        self.assertEqual(lines, [8])

    def test_not_null(self):
        lines = NullAssignment().value(self.cur_dir + "/not_null.java")
        self.assertEqual(lines, [])
