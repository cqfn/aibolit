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
    def test_find_mutable_index_increment(self):
        self.assertEqual(
            [4],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexIncrement.java')),
            'Should match index increment (++)'
        )

    @unittest.skip("Not implemented")
    def test_find_mutable_index_decrement(self):
        self.assertEqual(
            [4],
            MutableIndex().value(Path(self.dir_path, 'MutableIndexDecrement.java')),
            'Should match index decrement (--)'
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

