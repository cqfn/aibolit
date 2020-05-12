import os.path
from pathlib import Path
from unittest import TestCase
import unittest
from aibolit.patterns.bidirect_index.bidirect_index import BidirectIndex


@unittest.skip('Not implemented')
class TestBidirectIndex(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_bidirect_index_increase_decrease(self):
        self.assertEqual(
            BidirectIndex().value(Path(self.dir_path, 'BidirectIndexIncreaseDecrease.java')),
            [3],
            'Could not find bidirect index when index increased and then decreased'
        )

    def test_bidirect_index_decrease_increase(self):
        self.assertEqual(
            BidirectIndex().value(Path(self.dir_path, 'BidirectIndexDecreaseIncrease.java')),
            [3],
            'Could not find bidirect index when index decreased and then increased'
        )

    def test_bidirect_index_increase_decrease_assignment(self):
        self.assertEqual(
            BidirectIndex().value(Path(self.dir_path, 'BidirectIndexIncreaseDecreaseAssignment.java')),
            [3],
            'Could not find bidirect index when index increased and then decreased with assignment'
        )

    def test_bidirect_index_increase_assignment_decrease(self):
        self.assertEqual(
            BidirectIndex().value(Path(self.dir_path, 'BidirectIndexIncreaseAssignmentDecrease.java')),
            [3],
            'Could not find bidirect index when index increased with assignment and then decreased'
        )

    def test_bidirect_index_increase_assignment_decrease_assignment(self):
        self.assertEqual(
            BidirectIndex().value(Path(self.dir_path, 'BidirectIndexIncreaseAssignmentDecreaseAssignment.java')),
            [3],
            'Could not find bidirect index when index increased with assignment and then decreased with assignment'
        )

    def test_bidirect_index_hidden_scope_true(self):
        self.assertEqual(
            BidirectIndex().value(Path(self.dir_path, 'BidirectIndexHiddenScope.java')),
            [0],
            'Could not find bidirec index when scope is hidden'
        )

    def test_bidirect_index_outsider(self):
        self.assertEqual(
            BidirectIndex().value(Path(self.dir_path, 'BidirectIndexOutsider.java')),
            [10],
            'Could not find bidirec index when index is ot of loop'
        )
