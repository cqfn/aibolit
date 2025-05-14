# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from unittest import TestCase
from pathlib import Path
from typing import List

from aibolit.patterns.partially_synchronized_methods.partially_synchronized_methods import (
    PartiallySynchronizedMethods,
)
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class PartiallySynchronizedMethodsTestCase(TestCase):
    def test_no_synchronization(self):
        self._test_helper("NoSynchronization.java", [])

    def test_partial_synchronization(self):
        self._test_helper("PartialSynchronization.java", [8, 16, 26])

    def test_full_synchronization(self):
        self._test_helper("FullSynchronization.java", [])

    def test_several_synchronization_statements(self):
        self._test_helper("SeveralSynchronizationStatements.java", [9, 13, 29, 32])

    def test_synchronization_in_nested_scopes(self):
        self._test_helper("SynchronizationInNestedScopes.java", [12, 21, 30])

    def _test_helper(self, filename: str, lines: List[int]):
        filepath = str(Path(__file__).absolute().parent / filename)
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = PartiallySynchronizedMethods()
        self.assertEqual(pattern.value(ast), lines)
