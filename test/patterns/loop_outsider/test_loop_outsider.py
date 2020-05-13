# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import unittest
from pathlib import Path
from unittest import TestCase
from aibolit.patterns.loop_outsider.loop_outsider import LoopOutsider


@unittest.skip('Not implemented')
class TestLoopOutsider(TestCase):
    """
    @todo #138:30min Continue to implement loop_outsider
     Implement loop_outsider tests regarding for and do-while loops. Then implement
     loop_outsider pattern itself.
    """
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_find_loop_outsider_assignment_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderAssignmentInWhile.java')),
            [5],
            'Could not find loop outsider assignment in while loop'
        )

    def test_find_loop_outsider_prefix_increment_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderPrefixIncrementInWhile.java')),
            [5],
            'Could not find loop outsider with prefix increment in while loop'
        )

    def test_find_loop_outsider_postfix_increment_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderPostfixIncrementInWhile.java')),
            [5],
            'Could not find loop outsider with postfix increment in while loop'
        )

    def test_find_loop_outsider_prefix_decrement_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderPrefixDecrementInWhile.java')),
            [5],
            'Could not find loop outsider with prefix decrement in while loop'
        )

    def test_find_loop_outsider_postfix_decrement_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderPostfixDecrementInWhile.java')),
            [5],
            'Could not find loop outsider with postfix decrement in while loop'
        )

    def test_find_loop_outsider_add_and_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderAddAndInWhile.java')),
            [5],
            'Could not find loop outsider with add AND in while loop'
        )

    def test_find_loop_outsider_subtract_and_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderSubtractAndInWhile.java')),
            [5],
            'Could not find loop outsider with subtract AND in while loop'
        )

    def test_find_loop_outsider_multiply_and_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderMultiplyAndInWhile.java')),
            [5],
            'Could not find loop outsider with multiply AND in while loop'
        )

    def test_find_loop_outsider_divide_and_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderDivideAndInWhile.java')),
            [5],
            'Could not find loop outsider with divide AND in while loop'
        )

    def test_find_loop_outsider_modulus_and_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderModulusAndInWhile.java')),
            [5],
            'Could not find loop outsider with modulus AND in while loop'
        )

    def test_find_loop_outsider_left_shift_and_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderLeftShiftAndInWhile.java')),
            [5],
            'Could not find loop outsider with left shift AND in while loop'
        )

    def test_find_loop_outsider_right_shift_and_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderRightShiftAndInWhile.java')),
            [5],
            'Could not find loop outsider with right shift AND in while loop'
        )

    def test_find_loop_outsider_bitwise_and_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderBitwiseAndInWhile.java')),
            [5],
            'Could not find loop outsider with bitwise AND in while loop'
        )

    def test_find_loop_outsider_bitwise_inclusive_or_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderBitwiseInclusiveOrInWhile.java')),
            [5],
            'Could not find loop outsider with bitwise inclusive OR in while loop'
        )

    def test_find_loop_outsider_bitwise_exclusive_or_in_while(self):
        self.assertEqual(
            LoopOutsider().value(Path(self.dir_path, 'LoopOutsiderBitwiseExclusiveOrInWhile.java')),
            [5],
            'Could not find loop outsider with bitwise exclusive OR in while loop'
        )
