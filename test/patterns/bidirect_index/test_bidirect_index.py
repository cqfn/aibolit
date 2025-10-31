# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os.path
from pathlib import Path
from unittest import TestCase
from aibolit.patterns.bidirect_index.bidirect_index import BidirectIndex


class BidirectIndexTestCase(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_bidirect_index_increase_decrease(self):
        self.assertEqual(
            BidirectIndex().value(Path(self.dir_path, 'BidirectIndexIncreaseDecrease.java')),
            [6],
            'Could not find bidirect index when index increased and then decreased',
        )

    def test_bidirect_index_decrease_increase(self):
        self.assertEqual(
            BidirectIndex().value(Path(self.dir_path, 'BidirectIndexDecreaseIncrease.java')),
            [6],
            'Could not find bidirect index when index decreased and then increased',
        )

    def test_bidirect_index_increase_decrease_assignment(self):
        self.assertEqual(
            BidirectIndex().value(
                Path(self.dir_path, 'BidirectIndexIncreaseDecreaseAssignment.java')
            ),
            [6],
            'Could not find bidirect index when index increased and then decreased with assignment',
        )

    def test_bidirect_index_increase_assignment_decrease(self):
        self.assertEqual(
            BidirectIndex().value(
                Path(self.dir_path, 'BidirectIndexIncreaseAssignmentDecrease.java')
            ),
            [6],
            'Could not find bidirect index when index increased with assignment and then decreased',
        )

    def test_bidirect_index_increase_assignment_decrease_assignment(self):
        self.assertEqual(
            BidirectIndex().value(
                Path(self.dir_path, 'BidirectIndexIncreaseAssignmentDecreaseAssignment.java')
            ),
            [6],
            'Could not find bidirect index when index increased with assignment '
            'and then decreased with assignment',
        )

    def test_bidirect_index_hidden_scope_true(self):
        self.assertEqual(
            BidirectIndex().value(Path(self.dir_path, 'BidirectIndexHiddenScope.java')),
            [],
            'Could not find bidirec index when scope is hidden',
        )

    def test_bidirect_index_outsider(self):
        self.assertEqual(
            BidirectIndex().value(Path(self.dir_path, 'BidirectIndexOutsider.java')),
            [13],
            'Could not find bidirec index when index is ot of loop',
        )
