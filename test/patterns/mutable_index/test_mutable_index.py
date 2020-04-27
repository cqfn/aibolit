import os
from unittest import TestCase
import unittest
from pathlib import Path
from aibolit.patterns.mutable_index.mutable_index import MutableIndex


class TestMutableIndex(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    @unittest.skip("Not implemented")
    def test_find_mutable_index_assignement(self):
        self.assertEqual(
            [4],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexAssignment.java')),
            'Should match simple index assignent'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_prefix_increment(self):
        self.assertEqual(
            [4],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexPrefixIncrement.java')),
            'Should match index prefix increment (++i)'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_prefix_decrement(self):
        self.assertEqual(
            [4],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexPrefixDecrement.java')),
            'Should match index prefix decrement (--i)'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_postfix_increment(self):
        self.assertEqual(
            [4],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexPostfixIncrement.java')),
            'Should match index postfix increment (i++)'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_postfix_decrement(self):
        self.assertEqual(
            [4],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexPostfixDecrement.java')),
            'Should match index postfix decrement (i--)'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_addition_assignment(self):
        self.assertEqual(
            [4],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexAdditionAssignment.java')),
            'Should match index addition assignment (+=)'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_subtraction_assignment(self):
        self.assertEqual(
            [4],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexSubtractionAssignment.java')),
            'Should match index subtraction assignment (-=)'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_multiplication_assignment(self):
        self.assertEqual(
            [4],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexMultiplicationAssignment.java')),
            'Should match index multiplication assignment (*=)'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_division_assignment(self):
        self.assertEqual(
            [4],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexDivisionAssignment.java')),
            'Should match index division assignment (/=)'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_mod_assignment(self):
        self.assertEqual(
            [4],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexModAssignment.java')),
            'Should match index mod assignment (%=)'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_nested_for(self):
        self.assertEqual(
            [5],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexNestedFor.java')),
            'Should match mutable index in nested for'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_hidden_nested_for(self):
        self.assertEqual(
            [5],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexHiddenNestedFor.java')),
            'Should match mutable index hidden in nested for'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_no_block_for(self):
        self.assertEqual(
            [3],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexNoBlockFor.java')),
            'Should match mutable index in for with no block'
        )
