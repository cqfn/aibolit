# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path

from unittest import TestCase

from aibolit.metrics.fanout.FanOut import FanOut
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class FanOutTestSuite(TestCase):
    def test_count_types_in_fields(self):
        ast = FanOutTestSuite._build_ast('CountTypesInFields.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 3)

    def test_type_used_several_times(self):
        ast = FanOutTestSuite._build_ast('TypeUsedSeveralTimes.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 1)

    def test_self_usage(self):
        ast = FanOutTestSuite._build_ast('SelfUsage.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 0)

    def test_class_referenced_from_package(self):
        ast = FanOutTestSuite._build_ast('ClassReferencedFromPackage.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 2)

    def test_extending_type(self):
        ast = FanOutTestSuite._build_ast('ExtendingType.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 1)

    def test_generic_type(self):
        ast = FanOutTestSuite._build_ast('GenericType.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 1)

    def test_generic_and_packaged_types(self):
        ast = FanOutTestSuite._build_ast('GenericAndPackagedTypes.java')
        fan_out = FanOut()
        self.assertEqual(fan_out.value(ast), 2)

    @staticmethod
    def _build_ast(filename: str) -> AST:
        path = Path(__file__).absolute().parent / filename
        return AST.build_from_javalang(build_ast(str(path)))
