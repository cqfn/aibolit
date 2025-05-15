# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
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
        self.assertEqual(lines, [43])

    def test_four_setter_patterns(self):
        filepath = self.current_directory / "Configuration.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicSetter()
        lines = pattern.value(ast)
        self.assertEqual(lines,
                         [905, 909, 1239, 1243, 1364, 1542, 1615, 1644, 1673,
                          1706, 1715, 1726, 1804, 1973, 2023, 2339,
                          2510, 3786, 3822])

    def test_another_setter_patterns(self):
        filepath = self.current_directory / "SequenceFile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicSetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [262, 747, 2852, 2858, 2864, 3130])
