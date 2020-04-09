
import os
from unittest import TestCase
from aibolit.patterns.non_final_class.non_final_class import NonFinalClass


class TestNonFinalClass(TestCase):

    def test_find_final_class(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/1.java'
        lines = NonFinalClass().value(path)
        self.assertEqual(lines, [2])

    def test_find_non_final_class(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/2.java'
        lines = NonFinalClass().value(path)
        self.assertEqual(lines, [])
