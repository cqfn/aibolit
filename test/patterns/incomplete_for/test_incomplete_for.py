# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase
from pathlib import Path
from aibolit.ast_framework.ast import AST
from aibolit.patterns.incomplete_for.incomplete_for import IncompleteFor
from aibolit.utils.ast_builder import build_ast


class IncompleteForTestCase(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_incomplete_for_no_init_part(self):
        filepath = self.dir_path / 'NoInitPart.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        self.assertEqual(
            [7],
            IncompleteFor().value(ast),
            'Should match incomplete for first part',
        )

    def test_incomplete_for_no_condition_part(self):
        filepath = self.dir_path / 'NoConditionPart.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        self.assertEqual(
            [6],
            IncompleteFor().value(ast),
            'Should match incomplete for condition part',
        )

    def test_incomplete_for_no_update_part(self):
        filepath = self.dir_path / 'NoUpdatePart.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        self.assertEqual(
            [6],
            IncompleteFor().value(ast),
            'Should match incomplete for update part',
        )

    def test_incomplete_for_empty_for(self):
        filepath = self.dir_path / 'EmptyFor.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        self.assertEqual(
            [6],
            IncompleteFor().value(ast),
            'Should match empty for',
        )

    def test_incomplete_for_nested_for(self):
        filepath = self.dir_path / 'NestedFor.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        self.assertEqual(
            [6, 7],
            IncompleteFor().value(ast),
            'Should match nested for loops',
        )

    def test_incomplete_for_complete_for(self):
        filepath = self.dir_path / 'CompleteFor.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        self.assertEqual(
            [],
            IncompleteFor().value(ast),
            'Should not match complete for loop',
        )
