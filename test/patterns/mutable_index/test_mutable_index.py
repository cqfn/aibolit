# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase
from pathlib import Path
from aibolit.patterns.mutable_index.mutable_index import MutableIndex


class MutableIndexTestCase(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_find_mutable_index_assignment(self):
        self.assertEqual(
            [7],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexAssignment.java')),
            'Should match simple index assignment',
        )

    def test_find_mutable_index_prefix_increment(self):
        self.assertEqual(
            [7],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexPrefixIncrement.java')),
            'Should match index prefix increment (++i)',
        )

    def test_find_mutable_index_prefix_decrement(self):
        self.assertEqual(
            [7],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexPrefixDecrement.java')),
            'Should match index prefix decrement (--i)',
        )

    def test_find_mutable_index_postfix_increment(self):
        self.assertEqual(
            [7],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexPostfixIncrement.java')),
            'Should match index postfix increment (i++)',
        )

    def test_find_mutable_index_postfix_decrement(self):
        self.assertEqual(
            [7],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexPostfixDecrement.java')),
            'Should match index postfix decrement (i--)',
        )

    def test_find_mutable_index_addition_assignment(self):
        self.assertEqual(
            [7],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexAdditionAssignment.java')),
            'Should match index addition assignment (+=)',
        )

    def test_find_mutable_index_subtraction_assignment(self):
        self.assertEqual(
            [7],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexSubtractionAssignment.java')),
            'Should match index subtraction assignment (-=)',
        )

    def test_find_mutable_index_multiplication_assignment(self):
        self.assertEqual(
            [7],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexMultiplicationAssignment.java')),
            'Should match index multiplication assignment (*=)',
        )

    def test_find_mutable_index_division_assignment(self):
        self.assertEqual(
            [7],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexDivisionAssignment.java')),
            'Should match index division assignment (/=)',
        )

    def test_find_mutable_index_mod_assignment(self):
        self.assertEqual(
            [7],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexModAssignment.java')),
            'Should match index mod assignment (%=)',
        )

    def test_find_mutable_index_nested_for(self):
        self.assertEqual(
            [8],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexNestedFor.java')),
            'Should match mutable index in nested for',
        )

    def test_find_mutable_index_hidden_nested_for(self):
        self.assertEqual(
            [8],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexHiddenNestedFor.java')),
            'Should match mutable index hidden in nested for',
        )

    def test_find_mutable_index_no_block_for(self):
        self.assertEqual(
            [7],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexNoBlockFor.java')),
            'Should match mutable index in for with no block',
        )
