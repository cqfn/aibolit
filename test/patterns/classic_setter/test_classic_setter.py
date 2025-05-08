# SPDX-FileCopyrightText: Copyright (c) 2020 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.classic_setter.classic_setter import ClassicSetter
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class SetterTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_one_valid_patterns(self):
        filepath = self.current_directory / "BaseKeyframeAnimation.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicSetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [40])

    def test_four_setter_patterns(self):
        filepath = self.current_directory / "Configuration.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicSetter()
        lines = pattern.value(ast)
        self.assertEqual(lines,
                         [902, 906, 1236, 1240, 1361, 1539, 1612, 1641, 1670,
                          1703, 1712, 1723, 1801, 1970, 2020, 2336,
                          2507, 3783, 3819])

    def test_another_setter_patterns(self):
        filepath = self.current_directory / "SequenceFile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicSetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [259, 744, 2849, 2855, 2861, 3127])
