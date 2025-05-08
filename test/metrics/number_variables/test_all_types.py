# SPDX-FileCopyrightText: Copyright (c) 2020 Aibolit
# SPDX-License-Identifier: MIT

from aibolit.metrics.number_variables.numVariables import NumVars
import os
from unittest import TestCase
from pathlib import Path


class TestNum_MethodsandVars(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    get_num = NumVars()

    def test1(self):
        lines = self.get_num.value(Path(self.dir_path, '1.java'))
        self.assertEqual(lines, 6)

    def test2(self):
        lines = self.get_num.value(Path(self.dir_path, '2.java'))
        self.assertEqual(lines, 6)

    def test3(self):
        lines = self.get_num.value(Path(self.dir_path, '3.java'))
        self.assertEqual(lines, 12)

    def test4(self):
        lines = self.get_num.value(Path(self.dir_path, '4.java'))
        self.assertEqual(lines, 12)

    def test5(self):
        lines = self.get_num.value(Path(self.dir_path, '5.java'))
        self.assertEqual(lines, 6)
