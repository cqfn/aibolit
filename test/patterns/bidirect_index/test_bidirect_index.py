import os.path
from pathlib import Path
from unittest import TestCase

from aibolit.patterns.bidirect_index.bidirect_index import BidirectIndex


class BidirectIndexTestCase(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def _lines_from_file(self, filename):
        with open(filename, encoding='utf-8') as f:
            return f.readlines()

    def test_bidirect_index_increase_decrease(self):
        lines = self._lines_from_file(Path(self.dir_path, 'BidirectIndexIncreaseDecrease.java'))
        self.assertEqual(
            BidirectIndex().value(lines),
            [6],
            'Could not find bidirect index when index increased and then decreased',
        )

    def test_bidirect_index_decrease_increase(self):
        lines = self._lines_from_file(Path(self.dir_path, 'BidirectIndexDecreaseIncrease.java'))
        self.assertEqual(
            BidirectIndex().value(lines),
            [6],
            'Could not find bidirect index when index decreased and then increased',
        )

    def test_bidirect_index_increase_decrease_assignment(self):
        lines = self._lines_from_file(
            Path(self.dir_path, 'BidirectIndexIncreaseDecreaseAssignment.java'))
        self.assertEqual(
            BidirectIndex().value(lines),
            [6],
            'Could not find bidirect index when index increased and then decreased with assignment',
        )

    def test_bidirect_index_increase_assignment_decrease(self):
        lines = self._lines_from_file(
            Path(self.dir_path, 'BidirectIndexIncreaseAssignmentDecrease.java'))
        self.assertEqual(
            BidirectIndex().value(lines),
            [6],
            'Could not find bidirect index when index increased with assignment and then decreased',
        )

    def test_bidirect_index_increase_assignment_decrease_assignment(self):
        lines = self._lines_from_file(
            Path(self.dir_path, 'BidirectIndexIncreaseAssignmentDecreaseAssignment.java'))
        self.assertEqual(
            BidirectIndex().value(lines),
            [6],
            'Could not find bidirect index when index increased with assignment '
            'and then decreased with assignment',
        )

    def test_bidirect_index_hidden_scope_true(self):
        lines = self._lines_from_file(Path(self.dir_path, 'BidirectIndexHiddenScope.java'))
        self.assertEqual(
            BidirectIndex().value(lines),
            [],
            'Could not find bidirec index when scope is hidden',
        )

    def test_bidirect_index_outsider(self):
        lines = self._lines_from_file(Path(self.dir_path, 'BidirectIndexOutsider.java'))
        self.assertEqual(
            BidirectIndex().value(lines),
            [13],
            'Could not find bidirec index when index is ot of loop',
        )
